# Stack-specific standards

Detailed rules per layer of the house stack. The Core Philosophy in `SKILL.md`
(minimal abstraction, type-driven, ship-fast-not-sloppy, repo is truth) governs
all of these — this file is the concrete application per language.

---

## Rust / Anchor / Solana

**General Rust**
- `cargo clippy -- -D warnings` must be clean. Warnings are errors.
- No `unwrap()` / `expect()` in runtime paths. Return typed errors — define them
  with `thiserror` and propagate with `?`. `unwrap()` is allowed only in tests or
  with a comment proving the invariant holds.
- Domain types live in a shared `*-types` crate; every other crate depends on it.
  Types are the contract between modules — no stringly-typed interfaces.
- Prefer the direct path: raw `sqlx` for DB, Axum extractors for validation. No
  repository/service/DI layer unless it makes the code genuinely simpler.
- `async` with Tokio; don't block the runtime.

**Anchor / on-chain programs**
- Identity and treasury as **PDAs**; derive deterministically, never trust a
  client-supplied address where a PDA is expected.
- Validate **every** account constraint (`has_one`, `seeds`, `bump`, `owner`,
  signer checks). Assume all client input is hostile.
- Handle rent, CPI, and signer/authority checks explicitly — no implicit trust.
- Record execution/reputation on-chain where the design calls for it.
- `anchor test` against a local `solana-test-validator` before shipping. Test the
  failure cases (bad signer, wrong PDA, insufficient funds), not just the happy path.

---

## TypeScript

- `tsconfig` with `"strict": true`. No `any`. No non-null `!` to silence the
  checker — narrow the type properly.
- Types are the API contract to the frontend and SDK. Export shared types; don't
  redefine shapes on each side of a boundary.
- Solana: use `@solana/web3.js` typed calls; type instruction args and account
  layouts. Never hardcode secrets/keys — read from env.
- `pnpm lint` clean; format with prettier. Tests with the project runner, hermetic.

---

## Web — Astro 5 / Next 15 / Tailwind v4

- **Static-first.** Marketing sites are static (Astro) where possible; ship the
  least JS that does the job. Next.js: server components by default, `"use client"`
  only when you need interactivity/state.
- **One job per page.** Marketing pages inform, convince, redirect — a single
  clear CTA (e.g. → the Telegram bot). No dead links, no filler.
- **Quality bar:** responsive, accessible (semantic HTML, alt text, focus states,
  contrast), works in **light and dark**, no layout shift, images optimized.
- Tailwind v4 conventions; keep class soup readable — extract components, not
  utility spaghetti. No inline styles when a utility exists.

---

## Python

- PEP 8, enforced by `ruff`. **Line length 100.**
- Type hints **required** on public functions. Google-style docstrings on public
  functions.
- **No `print()`** — use `loguru`.
- Tests required for new code; unit tests in `tests/` are hermetic (no live DB or
  network); service-dependent tests go in `tests/integration/`. Aim >80% on new code.
- Config via `.env` (gitignored) + `.env.example` checked in with placeholders.

---

## Cross-cutting (all stacks)

- **Errors are typed and handled**, never swallowed. Log through the project
  logger, not stdout.
- **Config & secrets** come from the environment, never literals in source.
- **Comments explain *why*, not *what*.** The code says what; a comment earns its
  place by explaining a non-obvious decision or invariant.
- **Match the surrounding code** — naming, structure, and idiom of the file you're
  editing win over personal preference.
- **Delete dead code.** No commented-out blocks left "just in case" — git remembers.
