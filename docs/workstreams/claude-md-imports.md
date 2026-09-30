# Workstream: CLAUDE.md `@import` behavior

**Status:** researching (question answered; feeds the Trazo adapter design)
**Owner:** manoochehri   **Issue(s):** #38, parent #35, feeds #33 §4

## Hypothesis / goal

The proposed Trazo adapter puts a one-line root `CLAUDE.md` in every target repo:

```markdown
@.trazo/rules.md
```

The whole tool-neutral-core-plus-thin-adapters design rests on that import being **inlined at
load**, not on the agent choosing to read a file. Prose ("read `.trazo/rules.md`") is an
instruction an agent may skip, and costs a tool call when it complies. This workstream verifies
the import mechanism before anything is built on it.

**Verdict: the mechanism works. The adapter design is viable as specified.** One real hazard
(Q4, fail-open on a missing target) needs a guard; see [Consequences](#consequences-for-the-adapter).

## How it's tested

Runtime answers come from **fresh headless sessions**, not from recollection or documentation.

Each case is a throwaway mini-project containing its own root `CLAUDE.md` and an imported file
holding a distinctive marker token. A fresh session is started in that directory with **all
file-reading tools denied**, and asked to echo any marker it can already see. Two things are
then checked in the JSON transcript:

1. the marker **is** present in the reply, and
2. the transcript contains **no `tool_use` block at all** — the harder half of the claim. A
   marker echoed after a `Read` call would prove nothing.

`case0_control` is the guard against false positives: same marker on disk, no `@` line in
`CLAUDE.md`. It must come back `NONE`, and does.

Tooling note: `claude` is not on `PATH` on this machine. The CLI used is the one bundled with
the VSCode extension:

```sh
CLI=~/.vscode/extensions/anthropic.claude-code-2.1.284-darwin-arm64/resources/native-binary/claude
```

Exact invocation, run once per case from inside that case's directory (copy-paste to re-verify):

```sh
Q='Answer from your existing context only. Do not use any tools. List every token visible in your context that begins with MARKER_ . Reply with only those tokens, comma separated, or exactly NONE if there are none.'

"$CLI" -p "$Q" \
  --disallowed-tools Read Glob Grep Bash Task Edit Write WebFetch WebSearch NotebookEdit \
  --permission-prompts none \
  --output-format stream-json --verbose \
  > case.jsonl 2>case.err < /dev/null
```

A marker counts as inlined only if `case.jsonl` contains the token **and** no
`{"type":"tool_use"}` block.

## Evidence

All runtime rows: **Claude Code 2.1.284, macOS 15 (Darwin 25.5.0), 2026-09-30.** Sample size is
1 session per case unless noted; these are deterministic mechanism checks, not measurements of a
noisy quantity, and the control plus the 3-run depth check guard the two results where a single
run could mislead.

| Date | Case | Result | Sample | Evidence class |
|---|---|---|---|---|
| 2026-09-30 | `case0_control` — marker on disk, no `@` line | `NONE` — marker **not** visible | 1 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | `case1_flat` — `@notes.md` | marker echoed, **0 tool calls** | 1 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | `case2_nested` — chain to depth 5 | depths 1–4 inlined, depth 5 **not** | 3 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | `case3_outside` — `@.trazo/rules.md` | marker echoed, 0 tool calls | 1 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | `case4_missing` — `@missing-rules.md` | **silent skip**; session succeeded, no error | 1 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | `case5_symlink` — import target is a symlink | marker echoed, 0 tool calls | 1 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | `case6_symlink_claudemd` — `CLAUDE.md` *is* a symlink | marker echoed, 0 tool calls | 1 | runtime, Claude Code 2.1.284 |
| 2026-09-30 | Cline `.clinerules` symlink | follows symlinks (`stat`) | n/a | **source-verified, not runtime-verified** — Cline 4.1.21 |

### The five questions

**Q1 — Does `@path` in root `CLAUDE.md` inline the file into the opening context?**
**Yes.** *(runtime-verified, Claude Code 2.1.284, 2026-09-30)*
`case1_flat` echoed `MARKER_FLAT_ZANZIBAR7741` with **zero `tool_use` blocks** in the
transcript — checked for explicitly, since the absence of a `Read` is what distinguishes
inlining from the agent just reading a file. `case0_control`, identical but with the `@` line
removed, returned `NONE`, so the marker is not reachable without the import.

**Q2 — How deep does import nesting go?**
**Four levels of imports below the root file.** *(runtime-verified, Claude Code 2.1.284, 2026-09-30)*
Chain `CLAUDE.md → a.md → b.md → c.md → d.md → e.md`. Markers in `a`–`d` (depths 1–4) were all
inlined; the marker in `e.md` (depth 5) was **absent**. Reproduced in 3 independent sessions,
including two runs using a targeted present/absent prompt to rule out the model simply omitting
a token it could see. Counting the root file itself, that is 5 files total.
*Not a constraint for the adapter, which needs exactly 1 hop.*

**Q3 — Does it work for a file outside `.claude/`, e.g. `.trazo/rules.md`?**
**Yes.** *(runtime-verified, Claude Code 2.1.284, 2026-09-30)*
`case3_outside` used the exact proposed line, `@.trazo/rules.md`, and the marker was inlined
with 0 tool calls. The import path is an ordinary relative path; it is not confined to `.claude/`.

**Q4 — What happens when the imported file is missing?**
**Silent skip. No error, no warning.** *(runtime-verified, Claude Code 2.1.284, 2026-09-30)*
`case4_missing` imported a nonexistent `@missing-rules.md`. The session started normally and
finished `"subtype":"success"`, `"is_error":false`. The rest of `CLAUDE.md` still loaded (its
inline marker was echoed). `stderr` was empty, and nothing anywhere in the transcript mentioned
the missing filename — the only `error`/`warning` strings in the JSON were the unrelated
`is_error:false`, `error_status` and a rate-limit `allowed_warning` field.

**This is the one dangerous result, and it is a fail-open.** See below.

**Q5 — Do non-Claude tools follow a symlink (`.clinerules -> .trazo/rules.md`)?**
**Claude Code: yes, runtime-verified. Cline: yes, source-verified only. No other tool tested.**

- *Claude Code* resolves symlinks in both shapes: an imported file that is a symlink
  (`case5_symlink`) and a root `CLAUDE.md` that is itself a symlink to `.trazo/rules.md`
  (`case6_symlink_claudemd`). Both inlined the marker with 0 tool calls.
  *(runtime-verified, Claude Code 2.1.284, 2026-09-30)*
- *Cline 4.1.21* — **source-verified, not runtime-verified.** Cline cannot be driven headlessly,
  so this was read out of its bundled source (`dist/extension.js`), per `CLAUDE.md` rule 3. Its
  rule-discovery function resolves a candidate path with `fs.promises.stat()`:

  ```js
  // discoverFiles, minified as pWt()
  try { if ((await stat(t)).isFile())
          return [{ directoryPath: dirname(t), fileName: basename(t), filePath: t }] }
  catch (e) { if (!k0e(e)) throw e }
  ```

  `stat()` follows symlinks, so a `.clinerules` symlink pointing at a file resolves and is
  loaded. The candidate path list is built by the minified `ASr()`/`OOi()`, which yield
  `<workspace>/.clinerules`, `<workspace>/.cline/rules` and `<workspace>/AGENTS.md`.

  **Caveat worth knowing:** the *directory* branch of the same function enumerates with
  `readdir(t, {withFileTypes: true}).filter(i => i.isFile() && …)`. A `Dirent` for a symlink
  returns `false` from `isFile()`, so **symlinked files placed inside a `.clinerules/` directory
  are silently skipped**, even though a symlinked `.clinerules` file works. Symlink the top-level
  path, never individual entries inside a rules directory.

- **Installed is not in use.** Cline is installed in this machine's VSCode, which is why it was
  the one non-Claude tool worth reading, but no non-Claude tool is confirmed to be in use in this
  project. Nothing here claims support for Cursor, Windsurf, Codex or Aider — none were tested.

### Incidental finding, useful to the pivot

Cline's own path list includes **`AGENTS.md`** (minified const `Vue`/`Emn` = `"AGENTS.md"`,
loaded via the same `stat().isFile()` branch). If the tool-neutral core ever wants one filename
that more than one vendor already reads without an adapter, `AGENTS.md` is a stronger candidate
than a per-tool symlink. Out of scope for #38 — flagging it for the adapter issue.

## Consequences for the adapter

1. **Build it as specified.** A one-line root `CLAUDE.md` containing `@.trazo/rules.md` works,
   costs no tool call, and needs no prose instruction the agent can skip. The fallback the issue
   named — generate adapters from the core with a CI drift check — **is not needed for
   correctness** and can be dropped from the critical path.
2. **Guard the fail-open (Q4).** A missing or mistyped import target means the agent runs with
   **no rules at all** and *nothing tells anyone* — no error, no warning, exit 0. A typo in the
   adapter, a `.trazo/` left out of a sparse checkout, or a bad merge all degrade silently to an
   ungoverned agent. A loud failure would have been the safer behavior; it is not what we got, so
   the adapter has to supply the check itself. Cheapest sufficient guard: **put a sentinel line
   in `.trazo/rules.md` and have CI assert the import resolves** — e.g. a `trazo doctor` /
   pre-commit step that verifies every `@` target in `CLAUDE.md` exists, which is a pure
   filesystem check needing no agent session. Track this as a requirement on the adapter issue.
3. **Symlinks are safe at the top level only.** `.clinerules -> .trazo/rules.md` is fine for
   Claude Code (verified) and Cline (source-verified). Do not symlink individual files inside a
   rules *directory*.
4. **Depth is a non-issue** at 4 levels available vs. 1 needed.

## When to re-verify

None of this is a documented contract; it is observed behavior of one CLI version. Re-run the
probes above when any of these happen:

- **Claude Code is upgraded** past 2.1.284 — especially a minor bump, and specifically re-check
  Q4, since a fix turning the silent skip into a loud error would let us delete the guard in
  consequence 2.
- **Cline is upgraded** past 4.1.21, or any non-Claude tool is actually adopted — at which point
  Q5 deserves a real runtime test for that tool rather than a source read.
- **The adapter changes shape** — a different import path, a rules *directory* instead of a
  single file, or more than one hop.

Not automated deliberately: a script that spawns nested headless sessions cannot run in CI (no
`claude` on `PATH`), spends usage per run and would flake, so it would rot quietly and give false
assurance. The durable check is the filesystem-level import assertion in consequence 2.

## Decision

No decision record needed for the finding itself. The adapter requirement in consequence 2
(fail-open guard) belongs on the Trazo adapter issue under #33 §4.
