# End-to-end results - spindoctor-qwerty-augment-auggie 1.1.0

Date: 2026-10-10 (PT). Engine: SpinDoctor Qwerty 1.1.0, SpinDoctor 3.1.2 parity (update 3.1.2-298-20261010).

## Publishing decision (recorded as required)

RUSSELL PHILIP SMITHSON approved publishing ("GO") on the basis that the **updated SpinDoctor 3.1.2** builds and passes its own test
suite **18/18**, with the three test checks that still assumed the old 29-qubit limit adapted to the new 298-qubit limit
(`engine_regressions` dense comparison restricted to gates with at most 3 operands now that `mcx7` has 8; `direct_preset_regressions`
and `csv_gate_regressions` now expect 299 qubits, not 30, to be refused). Unmodified, the update passes 15/18 because of exactly
those three stale checks.

## Reference used

All parity comparisons use reference outputs regenerated from the **updated** SpinDoctor 3.1.2 C# build (241 presets in one
session, the folder-ingest chug series, and direct wide-register commands).

## Shared engine (Phase A, run once for all repos)

| Suite | Result |
|---|---|
| 241 presets replayed against the updated 3.1.2 reference | 236 identical; 5 with documented differences (qc-006, qc-008, qc-009, qc-016, qc-019: OpenCL GPU fields absent in a CPU-only engine, tranche checkpoint wording, session-state file name). qc-198 fails preflight in both C# and the engine (`q.compile synthesize` is not implemented in SpinDoctor 3.1.2 either). Work-accounting counters are compared separately and documented. |
| Folder-ingest chug series (41 folders) | 40 pass; `08_cancel` not applicable (the engine runs `q.folder` synchronously, so there is nothing to cancel; the job completes correctly) |
| Wide-register parity (direct 298-qubit commands) | 0 differences |
| 11-file 298-qubit example folder | identical (73 distinct outcomes, histogram preview and counts match) |
| Engine validation suite | 22/22 |
| Theory-testing suite (files, text, chat summary, 5 transcript formats) | 43/43 |
| Function-table examples (every "Command to type") | 168/168 run OK |

## This repository: clean-room test

The staged repository was copied into a fresh, empty folder with an empty HOME and a minimal environment (`env -i`). It had no access to
engine development folders or tools. The README's local install option was followed (`auggie --plugin-dir <clone>`), and the host check
was run against the copy.

| Check | Result |
|---|---|
| marketplace.json + plugin.json (name, version 1.1.0 in both, GPL-3.0-or-later, author) | PASS |
| commands (4, with descriptions), agents, rules, skill name/description rules, no hooks | PASS |
| `.mcp.json` resolved as Auggie resolves it (plugin-root variables replaced) -> script inside the plugin folder | PASS |
| **Real Auggie CLI 0.36.0**: `auggie command list --plugin-dir <clone>` lists the 4 commands and the skill | PASS |
| MCP initialize + tools/list (6 tools), function table, one script per command family, 298-qubit `mcx7` circuit | PASS |
| Presets qc-001..qc-025 vs the updated-3.1.2 reference (seeded) | PASS (20 identical, 5 documented differences) |
| `q.folder` on a small mixed folder (.txt/.csv/.json/.qasm, .md skipped and listed) | PASS |
| Theory test from a file, from a chat summary + excerpts, and from an exported transcript | PASS |
| TXT + PDF reports generated; PDFs validated (header, xref, trailer, EOF) | PASS |
| Summary | host checks 9/9, end-to-end 12/12 |

## Host app

| Item | Result |
|---|---|
| Auggie CLI | Real `@augmentcode/auggie` 0.36.0 from npm, installed in an isolated folder and HOME. **No sign-in, no API key.** |
| Local marketplace load | `auggie command list --plugin-dir <repo>` lists `qwerty-run`, `qwerty-preset`, `qwerty-functions`, `qwerty-theory` and the skill `spindoctor-qwerty:spindoctor-qwerty` |
| `auggie plugin marketplace add` | Not testable here: it says "Plugin marketplace feature is not enabled for your account" without a signed-in account with the feature |
| Plugin-root variables | Checked in Auggie's own code: `${AUGMENT_PLUGIN_ROOT}`/`${AUGGIE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_ROOT}` are replaced in `.mcp.json` command/args/env and in hooks only, not in command or agent text. That is why 1.1.0 removed those variables from the commands. |
| MCP tool listing | **host-simulated**: listing or calling MCP tools needs a signed-in agent session, which was not used. `tests/auggie_host_check.py` resolves `.mcp.json` the same way and starts the server. |

## Post-push verification

Recorded in the final commit of this file after the repository was cloned back from GitHub.
