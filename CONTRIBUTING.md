# Contributing

Thanks for improving **eonedge agent-skills**. This repo ships instructional
content (skills, commands, agents) for AI coding agents plus small glue. It runs
on three runtimes from **one source** — edit once, all three pick it up.

## Golden rule: one source, no duplication

- **Skills** live in `.claude/skills/<name>/SKILL.md`. Claude Code and OpenCode
  read them natively; the Gemini CLI plugin symlinks to them.
- **Commands** (`.claude/commands/`) and **agents** (`.claude/agents/`) are the
  single source; `.opencode/*` and `plugins/gemini/.agents/*` are **symlinks**
  into them. Never copy content — edit the file under `.claude/`.

## Adding or editing a skill

Each skill is a folder with a `SKILL.md`. The frontmatter is strict:

```yaml
---
name: my-skill            # must equal the directory name; ^[a-z0-9]+(-[a-z0-9]+)*$
description: One-to-few sentences. This is what an agent reads to decide whether
  to load the skill, so make it specific and trigger-rich.
---
```

Rules the validator enforces:

- `name` **must match the directory name**; `description` is required.
- `SKILL.md` stays **under 500 lines** — link to `references/*.md` for depth.
- No leftover brand tokens from the upstream fork.

Skills defer the engineering bar to `fullstack-standard`
(`references/definition-of-done.md`, `frontend-standards.md`,
`backend-standards.md`) rather than restating it. If you add a skill, make sure
`using-agent-skills` (the router) can route to it.

## Before you open a PR — run the gate locally

```bash
python3 scripts/validate.py                             # structure + frontmatter + manifests
python3 -m unittest discover -s scripts -p 'test_*.py'  # validator's own tests
bun build .opencode/plugins/eonedge-skills.ts --target=node > /dev/null  # plugin build-check
```

All three run in CI on every PR and must pass.

## Git & PR flow

- Branch off `main`: `feat/…`, `fix/…`, `docs/…`, `chore/…`, `test/…`, `refactor/…`.
- **Conventional Commits**: `type(scope): description`.
- Never commit to `main` directly — open a PR; CI must be green; squash and merge.
- Keep PRs focused. Update `README.md` when you change counts or add a runtime.

## Security

Never file a vulnerability in a public issue — see [`SECURITY.md`](SECURITY.md).

By contributing you agree your work is licensed under the [MIT License](LICENSE).
