# Security Policy

This repository ships **eonedge agent-skills** — instructional content (skills,
commands, agents) and small glue (validation script, session hooks, an OpenCode
plugin). It has no runtime service, but the skills guide how production code on
the house stack (Rust/Anchor/Solana, TypeScript, Astro/Next, Python) gets built,
so guidance that could weaken a consumer's security is in scope.

## Reporting a vulnerability

**Do not open a public issue or pull request for a security problem.** Public
disclosure before a fix puts every downstream user at risk.

Report privately through either channel:

- **GitHub Security Advisories** — the [Security tab][advisories] → *Report a
  vulnerability* (preferred; keeps the report and fix coordinated in one place).
- **Email** — <eonedgeproject@gmail.com> with subject `SECURITY:` and a clear
  description.

Please include:

- What the issue is and where (file/skill/command, or the guidance at fault).
- How to reproduce or a concrete scenario showing the impact.
- Any suggested remediation.

We aim to acknowledge within **3 business days** and to agree on a disclosure
timeline once the report is triaged. Please give us a reasonable window to ship
a fix before any public disclosure.

## In scope

- Skill/command/agent guidance that would lead a following agent to write
  insecure code (e.g. skipping signer/authority checks, leaking secrets,
  unsafe CPI/PDA handling, unvalidated input at a boundary).
- The validation script, session hooks, and the OpenCode plugin.
- Any secret, key, or credential accidentally committed to this repository.

## Out of scope

- Vulnerabilities in your own application code that merely *used* a skill — file
  those against your project.
- Third-party tools (Claude Code, Gemini CLI, OpenCode) themselves — report to
  their respective maintainers.

## Leaked credentials

If you find a key, token, or other credential committed to this repo, treat it
as compromised: report it privately as above and **rotate it immediately** — do
not just delete the commit. This mirrors the `fullstack-standard` skill's
secret-hygiene rule.

[advisories]: https://github.com/eonedgeproject-code/agent-skills/security/advisories
