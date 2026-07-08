# eonedge agent-skills — OpenCode integration

Same content as the Claude Code plugin, wired for [OpenCode](https://opencode.ai)
with **zero duplication**. One source of skills, three runtimes.

## How OpenCode picks it up

| Piece | Where OpenCode reads it | Mechanism |
|---|---|---|
| **25 skills** | `.claude/skills/<name>/SKILL.md` | **native** — OpenCode discovers `.claude/skills` directly and exposes them via its built-in `skill` tool. No symlink (avoids double-loading), no porting — the `name`/`description` frontmatter is already exactly what OpenCode recognizes. |
| **8 commands** | `.opencode/commands/` | symlink → `../.claude/commands`. `description` frontmatter + prompt body + `$ARGUMENTS` are all OpenCode-native syntax. |
| **4 agents** | `.opencode/agents/` | symlink → `../.claude/agents`. Filename is the agent id; `description` drives selection. |
| **Always-on bar** | `opencode.json` → `instructions` | injects `fullstack-standard` into every session — the OpenCode-idiomatic equivalent of the Claude/Gemini session-start hook. |
| **Session announce** | `.opencode/plugins/eonedge-skills.ts` | a real `@opencode-ai/plugin` module; logs a load line on `session.created`. |

## Setup

Nothing to install — open this repo in OpenCode and everything auto-discovers.
Skills load on demand through the `skill` tool; `fullstack-standard` is always on.

Edit a skill once under `.claude/skills/` and all three runtimes (Claude Code,
Gemini CLI, OpenCode) run the same content.
