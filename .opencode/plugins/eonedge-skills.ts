// eonedge agent-skills — OpenCode plugin
// Announces the skills bundle at session start, the OpenCode analogue of the
// Claude Code / Gemini CLI session-start hooks. The actual routing is native:
// OpenCode discovers the 25 SKILL.md files under .claude/skills and exposes
// them through its built-in `skill` tool, and opencode.json injects the
// always-on fullstack-standard bar via `instructions`.
//
// Type-only import — erased at runtime, so this plugin needs no dependencies
// and no `bun install`. `@opencode-ai/plugin` is provided by OpenCode itself.
import type { Plugin } from "@opencode-ai/plugin"

export const EonedgeSkills: Plugin = async () => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.created") {
        console.log(
          "[eonedge-skills] loaded — fullstack-standard is the always-on engineering bar. " +
            "Use the `skill` tool to route intent across the lifecycle: " +
            "spec → plan → build → verify → review → ship.",
        )
      }
    },
  }
}
