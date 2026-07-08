#!/usr/bin/env python3
"""Validate the skills plugin repo: frontmatter, name/dir match, JSON, line caps,
and a brand-leak guard. Dependency-free (stdlib only). Exit 1 on any failure."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
DESC = re.compile(r"^description:\s*(.+)$", re.MULTILINE)
SKILL_MAX_LINES = 500
# Built from parts so this file itself doesn't trip the brand-leak guard.
BANNED = re.compile("or" + "vix", re.IGNORECASE)

errors: list[str] = []
checks = 0


def ok(_msg: str) -> None:
    global checks
    checks += 1


def fail(msg: str) -> None:
    errors.append(msg)


def frontmatter(path: Path) -> str | None:
    m = FM.match(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def check_frontmatter(path: Path, *, need_name: bool, expected_name: str | None) -> None:
    rel = path.relative_to(ROOT)
    fm = frontmatter(path)
    if fm is None:
        fail(f"{rel}: missing or malformed YAML frontmatter (must open with `---`)")
        return
    if not DESC.search(fm):
        fail(f"{rel}: frontmatter missing `description:`")
    if need_name:
        nm = NAME.search(fm)
        if not nm:
            fail(f"{rel}: frontmatter missing `name:`")
        elif expected_name is not None and nm.group(1) != expected_name:
            fail(f"{rel}: name `{nm.group(1)}` != expected `{expected_name}`")
    if DESC.search(fm):
        ok(str(rel))


def main() -> int:
    # 1. Skills
    skills_dir = ROOT / ".claude" / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        fail(".claude/skills: no SKILL.md files found")
    for f in skill_files:
        check_frontmatter(f, need_name=True, expected_name=f.parent.name)
        n = len(f.read_text(encoding="utf-8").splitlines())
        if n > SKILL_MAX_LINES:
            fail(f"{f.relative_to(ROOT)}: {n} lines exceeds cap of {SKILL_MAX_LINES}")

    # 2. Commands (frontmatter needs description; name is derived from filename)
    for f in sorted((ROOT / ".claude" / "commands").glob("*.md")):
        check_frontmatter(f, need_name=False, expected_name=None)

    # 3. Agents (name must match filename stem)
    for f in sorted((ROOT / ".claude" / "agents").glob("*.md")):
        check_frontmatter(f, need_name=True, expected_name=f.stem)

    # 4. JSON manifests valid + plugin paths exist
    json_files = [
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / "plugin.json",
        ROOT / "hooks" / "hooks.json",
        ROOT / "plugins" / "gemini" / "hooks.json",  # Gemini CLI plugin manifest
    ]
    plugin_manifest = None
    for j in json_files:
        if not j.exists():
            fail(f"{j.relative_to(ROOT)}: missing")
            continue
        try:
            data = json.loads(j.read_text(encoding="utf-8"))
            ok(str(j.relative_to(ROOT)))
            if j.name == "plugin.json" and j.parent.name == ".claude-plugin":
                plugin_manifest = data
        except json.JSONDecodeError as e:
            fail(f"{j.relative_to(ROOT)}: invalid JSON — {e}")

    # 4b. plugin.json referenced paths must exist
    if plugin_manifest:
        refs: list[str] = []
        for key in ("commands", "skills"):
            v = plugin_manifest.get(key)
            refs += v if isinstance(v, list) else [v] if v else []
        refs += plugin_manifest.get("agents", []) if isinstance(plugin_manifest.get("agents"), list) else []
        for r in refs:
            if not (ROOT / r).exists():
                fail(f".claude-plugin/plugin.json: referenced path does not exist -> {r}")
            else:
                ok(f"path:{r}")

    # 5. Brand-leak guard across shipped content (skip scripts/ and .github/)
    scan_globs = [
        ".claude/skills/*/SKILL.md",
        ".claude/commands/*.md",
        ".claude/agents/*.md",
        ".claude/hooks/*.sh",
        ".claude-plugin/*.json",
        "hooks/*.json",
        "plugin.json",
        "README.md",
        "plugins/gemini/.agents/hooks/*.sh",   # Gemini CLI plugin hook
        "plugins/gemini/hooks.json",           # Gemini CLI plugin manifest
    ]
    for pattern in scan_globs:
        for f in sorted(ROOT.glob(pattern)):
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if BANNED.search(line):
                    fail(f"{f.relative_to(ROOT)}:{i}: brand leak — banned token present")

    # Report
    print(f"ran {checks} checks across skills / commands / agents / manifests")
    if errors:
        print(f"\n✗ {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("✓ all validations passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
