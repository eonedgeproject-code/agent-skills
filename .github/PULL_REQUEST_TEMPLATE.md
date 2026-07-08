<!-- Keep PRs focused. Conventional Commit title: type(scope): description -->

## What & why

<!-- What does this change and why? Link any issue. -->

## Checklist

- [ ] Edited the **single source** under `.claude/` (not a symlinked copy).
- [ ] `python3 scripts/validate.py` passes.
- [ ] `python3 -m unittest discover -s scripts -p 'test_*.py'` passes.
- [ ] `bun build .opencode/plugins/eonedge-skills.ts --target=node` passes (if plugin touched).
- [ ] New/changed skill: `name` matches its directory, `SKILL.md` under 500 lines, routable from `using-agent-skills`.
- [ ] `README.md` updated if counts or runtimes changed.
- [ ] Conventional Commit title; branched off `main`.
- [ ] No secrets in the diff.
