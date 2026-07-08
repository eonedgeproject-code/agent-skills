# Project July

[![CI](https://github.com/eonedgeproject-code/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/eonedgeproject-code/agent-skills/actions/workflows/ci.yml)

Development workspace + **eonedge agent-skills** — a full software-development
lifecycle framework for AI coding agents, tuned to the house stack.

Ported and adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
(MIT) to the eonedge stack: **Rust / Anchor / Solana · TypeScript · Astro 5 /
Next 15 / Tailwind v4 · Python**.

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
  /spec           /plan          /build         /test          /review         /ship
```

## What's here

| Layer | Path | Count |
|---|---|---|
| **Core standard** | `.claude/skills/fullstack-standard/` | the always-on engineering bar (+ frontend/backend/DoD refs) |
| **Lifecycle skills** | `.claude/skills/` | 24 workflow skills, spec → ship |
| **Slash commands** | `.claude/commands/` | 8 (`/spec /plan /build /test /review /ship /webperf /code-simplify`) |
| **Specialist personas** | `.claude/agents/` | 4 (code-reviewer, security-auditor, test-engineer, web-performance-auditor) |
| **Session hook** | `.claude/hooks/session-start.sh` | injects the skill-discovery router each session |
| **Claude Code plugin** | `.claude-plugin/`, `hooks/` | installable as a Claude Code plugin (`eonedge-skills@eonedge`) |
| **Gemini CLI plugin** | `plugins/gemini/` | same content for Gemini CLI — `.agents/` symlinked to `.claude/*`, no duplication |
| **OpenCode plugin** | `.opencode/`, `opencode.json` | same content for OpenCode — skills read natively from `.claude/skills`, commands/agents symlinked, no duplication |

`fullstack-standard` is the always-on core — every other skill is measured against
its Definition of Done gate. `using-agent-skills` is the meta-skill router that maps
an intent (feature / bug / review / deploy) onto the right skill sequence.

## Commands

| Doing | Command | Skill |
|---|---|---|
| Define what to build | `/spec` | spec-driven-development |
| Plan how to build it | `/plan` | planning-and-task-breakdown |
| Build incrementally | `/build` (`/build auto`) | incremental-implementation + test-driven-development |
| Prove it works | `/test` | test-driven-development |
| Review before merge | `/review` | code-review-and-quality (five-axis) |
| Simplify the code | `/code-simplify` | code-simplification |
| Audit web perf | `/webperf` | web-performance-auditor persona |
| Ship to production | `/ship` | parallel fan-out → go/no-go |

## Skills by phase

- **Define** — interview-me, idea-refine, spec-driven-development
- **Plan** — planning-and-task-breakdown
- **Build** — incremental-implementation, test-driven-development, context-engineering, source-driven-development, doubt-driven-development, frontend-ui-engineering, api-and-interface-design
- **Verify** — browser-testing-with-devtools, debugging-and-error-recovery
- **Review** — code-review-and-quality, code-simplification, security-and-hardening, performance-optimization
- **Ship** — git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration, documentation-and-adrs, observability-and-instrumentation, shipping-and-launch
- **Meta** — using-agent-skills

## Tool support

One source of content, three agent runtimes:

| Runtime | Root | Discovery |
|---|---|---|
| **Claude Code** | `.claude/` | native (`.claude/skills`, `.claude/commands`, `.claude/agents`) |
| **Gemini CLI** | `plugins/gemini/` | self-contained plugin (`GEMINI_PLUGIN_ROOT=plugins/gemini`); its `.agents/` symlinks skills/commands/agents into `.claude/*`, so both tools always run the same skills — edit once. |
| **OpenCode** | `.opencode/` + `opencode.json` | skills read **natively** from `.claude/skills` (OpenCode's documented fallback); `.opencode/commands` & `.opencode/agents` symlink into `.claude/*`; `opencode.json` `instructions` makes `fullstack-standard` always-on. See [`.opencode/README.md`](.opencode/README.md). |

## Setup

Skills, commands, and agents are auto-discovered from `.claude/` (Claude Code),
`plugins/gemini/` (Gemini CLI, `GEMINI_PLUGIN_ROOT=plugins/gemini`), or `.opencode/`
+ `opencode.json` (OpenCode) — restart the session in this workspace to load them.

The session-start hook needs `jq` for full meta-skill injection:

```bash
sudo apt-get install -y jq   # without it, skills still work individually
```

Install as a plugin elsewhere:

```
/plugin marketplace add eonedgeproject-code/agent-skills
/plugin install eonedge-skills@eonedge
```
