#!/usr/bin/env python3
"""Tests for validate.py — the repo's sole quality gate. Dependency-free
(stdlib unittest only), mirroring validate.py itself. Run:

    python3 -m unittest discover -s scripts -p 'test_*.py'
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

# Load validate.py by path (it's a script, not an installed module).
_MOD_PATH = Path(__file__).resolve().parent / "validate.py"
_spec = importlib.util.spec_from_file_location("validate_mod", _MOD_PATH)
assert _spec and _spec.loader
validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate)

ORIG_ROOT = validate.ROOT
# Built from parts so this test file doesn't itself carry the banned token.
BANNED_TOKEN = "or" + "vix"


class RegexTests(unittest.TestCase):
    def test_frontmatter_block_extracted(self) -> None:
        text = "---\nname: foo\ndescription: bar\n---\n\n# Body\n"
        m = validate.FM.match(text)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertIn("name: foo", m.group(1))

    def test_no_frontmatter_returns_none(self) -> None:
        self.assertIsNone(validate.FM.match("# Just a heading\n"))

    def test_name_and_description_captured(self) -> None:
        fm = "name: foo\ndescription: bar baz"
        self.assertEqual(validate.NAME.search(fm).group(1), "foo")  # type: ignore[union-attr]
        self.assertEqual(validate.DESC.search(fm).group(1), "bar baz")  # type: ignore[union-attr]

    def test_brand_leak_guard(self) -> None:
        self.assertTrue(validate.BANNED.search(f"line mentions {BANNED_TOKEN} here"))
        self.assertTrue(validate.BANNED.search(BANNED_TOKEN.upper()))  # case-insensitive
        self.assertIsNone(validate.BANNED.search("a perfectly clean line"))


class FrontmatterFileTests(unittest.TestCase):
    """check_frontmatter appends to validate.errors and uses ROOT for display,
    so point ROOT at a temp dir and inspect the error list."""

    def setUp(self) -> None:
        validate.errors.clear()
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        validate.ROOT = self.tmp

    def tearDown(self) -> None:
        validate.ROOT = ORIG_ROOT
        self._tmp.cleanup()

    def _skill(self, dir_name: str, body: str) -> Path:
        d = self.tmp / dir_name
        d.mkdir(parents=True, exist_ok=True)
        f = d / "SKILL.md"
        f.write_text(body, encoding="utf-8")
        return f

    def test_valid_skill_produces_no_error(self) -> None:
        f = self._skill("good-skill", "---\nname: good-skill\ndescription: does a thing\n---\n\n# Good\n")
        validate.check_frontmatter(f, need_name=True, expected_name="good-skill")
        self.assertEqual(validate.errors, [])

    def test_missing_description_is_caught(self) -> None:
        f = self._skill("no-desc", "---\nname: no-desc\n---\n\n# X\n")
        validate.check_frontmatter(f, need_name=True, expected_name="no-desc")
        self.assertTrue(any("description" in e for e in validate.errors))

    def test_name_directory_mismatch_is_caught(self) -> None:
        f = self._skill("dir-name", "---\nname: other-name\ndescription: d\n---\n\n# X\n")
        validate.check_frontmatter(f, need_name=True, expected_name="dir-name")
        self.assertTrue(any("!= expected" in e for e in validate.errors))

    def test_missing_frontmatter_is_caught(self) -> None:
        f = self._skill("no-fm", "# Heading only, no frontmatter\n")
        validate.check_frontmatter(f, need_name=True, expected_name="no-fm")
        self.assertTrue(any("frontmatter" in e for e in validate.errors))


class ReferenceAndLinkTests(unittest.TestCase):
    def setUp(self) -> None:
        validate.errors.clear()
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        validate.ROOT = self.tmp

    def tearDown(self) -> None:
        validate.ROOT = ORIG_ROOT
        self._tmp.cleanup()

    def _skill(self, name: str, body: str) -> Path:
        d = self.tmp / name
        d.mkdir(parents=True, exist_ok=True)
        f = d / "SKILL.md"
        f.write_text(body, encoding="utf-8")
        return f

    def test_reference_resolved_via_canonical_dir(self) -> None:
        ref_dir = self.tmp / "fullstack-standard" / "references"
        ref_dir.mkdir(parents=True)
        (ref_dir / "backend-standards.md").write_text("x", encoding="utf-8")
        f = self._skill("a", "defer to `references/backend-standards.md` for detail")
        validate.check_skill_references([f], ref_dir)
        self.assertEqual(validate.errors, [])

    def test_missing_reference_is_caught(self) -> None:
        ref_dir = self.tmp / "fullstack-standard" / "references"
        ref_dir.mkdir(parents=True)
        f = self._skill("b", "see `references/does-not-exist.md`")
        validate.check_skill_references([f], ref_dir)
        self.assertTrue(any("does-not-exist.md" in e for e in validate.errors))

    def test_local_reference_dir_resolves(self) -> None:
        f = self._skill("c", "see `references/local.md`")
        (f.parent / "references").mkdir()
        (f.parent / "references" / "local.md").write_text("x", encoding="utf-8")
        validate.check_skill_references([f], self.tmp / "nonexistent")
        self.assertEqual(validate.errors, [])

    def test_resolving_local_link_ok(self) -> None:
        (self.tmp / "LICENSE").write_text("MIT", encoding="utf-8")
        doc = self.tmp / "README.md"
        doc.write_text("see [the license](LICENSE) and [web](https://example.com)", encoding="utf-8")
        validate.check_local_links(doc)
        self.assertEqual(validate.errors, [])

    def test_broken_local_link_is_caught(self) -> None:
        doc = self.tmp / "README.md"
        doc.write_text("see [gone](MISSING.md)", encoding="utf-8")
        validate.check_local_links(doc)
        self.assertTrue(any("MISSING.md" in e for e in validate.errors))


class IntegrationTest(unittest.TestCase):
    def test_main_passes_on_the_real_repo(self) -> None:
        validate.errors.clear()
        validate.ROOT = ORIG_ROOT
        rc = validate.main()
        self.assertEqual(rc, 0, f"validator reported problems: {validate.errors}")


if __name__ == "__main__":
    unittest.main()
