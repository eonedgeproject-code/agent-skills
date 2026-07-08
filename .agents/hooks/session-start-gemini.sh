#!/bin/bash
# eonedge agent-skills — Gemini/Antigravity session start hook
# Injects the using-agent-skills meta-skill (skill-discovery flowchart) into every
# new session so the agent routes intent to the right skill instead of winging it.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CANDIDATES=(
  "$(dirname "$SCRIPT_DIR")/skills"                      # .agents/hooks -> .agents/skills
  "${GEMINI_PLUGIN_ROOT}/skills"                         # Gemini installed plugin root
  "${GEMINI_PROJECT_DIR}/.agents/skills"                 # Gemini project agent dir
  "${GEMINI_PROJECT_DIR}/skills"                         # Gemini project root dir
)

META_SKILL=""
for dir in "${CANDIDATES[@]}"; do
  [ -f "$dir/using-agent-skills/SKILL.md" ] && META_SKILL="$dir/using-agent-skills/SKILL.md" && break
done

if ! command -v jq >/dev/null 2>&1; then
  echo '{"priority": "INFO", "message": "eonedge-skills: jq not found on PATH — install it (apt-get install jq) to enable meta-skill injection. Skills remain available individually."}'
  exit 0
fi

if [ -n "$META_SKILL" ] && [ -f "$META_SKILL" ]; then
  CONTENT=$(cat "$META_SKILL")
  jq -cn \
    --arg message "eonedge-skills loaded. Use the skill discovery flowchart to pick the right skill; the fullstack-standard skill is the always-on engineering bar.

$CONTENT" \
    '{priority: "IMPORTANT", message: $message}'
else
  echo '{"priority": "INFO", "message": "eonedge-skills: using-agent-skills meta-skill not found. Skills may still be available individually."}'
fi
