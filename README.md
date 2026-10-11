# SpinDoctor Qwerty for Augment Auggie

**spindoctor-qwerty-augment-auggie** is an [Auggie](https://docs.augmentcode.com/cli/plugins) (Augment Code CLI) **plugin marketplace**
with one plugin, `spindoctor-qwerty`. The plugin bundles the SpinDoctor Qwerty quantum-circuit **simulator** as an MCP server, a skill,
four slash commands, a helper subagent and an honesty rule. Auggie can then build and run circuits with SpinDoctor's `q.*` commands,
run any of the 241 presets, process a folder of command files with `q.folder`, test a theory you give it, and write TXT, PDF, JSON and
CSV reports.

- Version **1.1.0**, engine at **SpinDoctor 3.1.2 parity** (update 3.1.2-298-20261010).
- Layout: `.augment-plugin/marketplace.json` (marketplace `spindoctor-qwerty-marketplace`) and `plugins/spindoctor-qwerty/` with
  `.augment-plugin/plugin.json`, `.mcp.json`, `commands/`, `agents/`, `rules/` and `skills/spindoctor-qwerty/` (skill + bundled engine).
  There are no hooks. The plugin is also valid as a Claude Code plugin layout, which Auggie accepts.
- Self-contained: the engine (pure Python, standard library only, NumPy optional) lives in the skill folder. No network access, no installs.

> **Honest limits.** SpinDoctor runs classical FP64 arithmetic on your computer. It is **not** a quantum computer, never contacts
> quantum hardware, and gives no quantum speed-up or quantum advantage. Registers hold 1-298 logical qubits, but any group of
> entangled qubits (one "factor") is limited to 59 qubits, and dense factors are limited much further by memory
> (2^n x 16 bytes; about 22 qubits with the standard library, more with NumPy). Registers wider than 29 qubits sample in basis Z only.
> Python 3.8 or newer is required (`python3` on PATH).

## Install

1. Install **Python 3.8+** (`python3` on PATH) and Auggie (`npm install -g @augmentcode/auggie`, Node 20+).
2. Choose one:
   - **From GitHub (marketplace):**
     ```sh
     auggie plugin marketplace add LKVexa/spindoctor-qwerty-augment-auggie
     auggie plugin install spindoctor-qwerty@spindoctor-qwerty-marketplace
     ```
     Add `--project` or `--local` to the install command to enable the plugin for a single project only. Plugin marketplaces must be
     enabled for your Augment account; if Auggie says the feature is not enabled, use the local option.
   - **Local folder:** clone this repository and start Auggie with `auggie --plugin-dir ./spindoctor-qwerty-augment-auggie`.
3. Check: `auggie command list --plugin-dir ./spindoctor-qwerty-augment-auggie` lists the commands and the skill. In a session, `/plugins`
   shows the plugin. Then ask *"show the SpinDoctor functions"* or run `/spindoctor-qwerty:qwerty-functions`.

`.mcp.json` starts `python3 ${AUGMENT_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_mcp.py`. Auggie replaces
`${AUGMENT_PLUGIN_ROOT}` with the plugin folder. On Windows, if `python3` is not available, change `"command"` to `"python"`. Set
`SPINDOCTOR_WORKSPACE` to choose where reports go (default `~/spindoctor-workspace`).

## Slash commands

| Command | What it does |
|---|---|
| `/spindoctor-qwerty:qwerty-run <q.* commands>` | Runs q.* commands and summarises probabilities, counts and report paths |
| `/spindoctor-qwerty:qwerty-preset <qc-NNN> [name=value ...]` | Runs one of the 241 presets |
| `/spindoctor-qwerty:qwerty-functions [section] [filter]` | Shows the function table |
| `/spindoctor-qwerty:qwerty-theory <file \| text \| "we discussed">` | Tests a theory and writes a theory test report |

(The exact command names Auggie shows depend on how the plugin was installed; `auggie command list` shows them.)

## What you can ask for

## SpinDoctor Qwerty - plugin tools

| Function | What it does | Command to type |
|---|---|---|
| Function table (spindoctor_functions) | Show this table in chat | Ask: "show the SpinDoctor functions" (CLI: `spindoctor_cli.py functions`) |
| Run a script (spindoctor_run_script) | Run any q.* lines above; returns results + TXT/JSON/CSV/PDF report paths | Ask: "run q.circuit new bell 2 / q.circuit add h 0 / ..." |
| Run a preset (spindoctor_run_preset) | Run qc-001..qc-241 with overrides | Ask: "run preset qc-067 with shots=64" |
| List presets (spindoctor_list_presets) | Search the 241 presets | Ask: "list presets about Grover" |
| Read a report (spindoctor_report) | List/read TXT reports (PDF/JSON paths alongside) | Ask: "show the newest SpinDoctor report" |
| Test a theory from a file (spindoctor_test_theory source=file) | Read a .txt/.md/.pdf/.py/.json/.csv/.q attachment, then hypothesis -> prediction -> q.* script -> run -> verdict + TXT/PDF theory report | Ask: "test the theory in C:/notes/theory.md" (the host must pass the file path/content) |
| Test a theory from text (spindoctor_test_theory source=text) | Same pipeline for pasted text | Ask: "test this theory: a Hadamard on \|0> gives 50/50" |
| Test the theory we discussed (spindoctor_test_theory source=chat) | The AI summarises the theory from the conversation (claims, assumptions, variables, prediction), you confirm, then it is tested; quoted excerpts go in the report under 'Source: chat history'. An exported chat transcript (.txt/.md/.json/.html) also works | Ask: "test the theory we discussed" or "test the theory in my exported chat C:/chats/conversation.json" |

Every command family is listed with a runnable example in **[FUNCTIONS.md](FUNCTIONS.md)** (the exact table the tool shows):
circuits (`q.circuit`, including 298-qubit wide registers and the `mcx7` gate), queries (`q.query`), the tranche register
(`q.tranche`), the procedural grid, presets and sequences, resource planning, math calculators, physics models, lessons, noise, error
correction, compilation, algorithms, inputs/folders/history (`q.input`, `q.folder`, `q.history`) and the cartridge commands.

## Theory testing

`spindoctor_test_theory` turns a claim into a test: hypothesis -> measurable prediction -> `q.*` script -> run -> compare -> a TXT +
JSON + PDF **theory test report** with the hypothesis, script, raw results, verdict (*supported*, *not supported* or *inconclusive*)
and limits.

- **From a file:** .txt, .md, .pdf, .py, .json, .csv or .q. In Auggie, give the file's path in the workspace.
- **From pasted text.**
- **From the chat history:** say *"test the theory we discussed"*. Auggie writes a short summary (claims, assumptions, variables,
  measurable prediction), shows it to you to confirm or correct, then passes it with optional quoted excerpts; the report records them
  under *Source: chat history*. Exported chat transcripts (.txt/.md/.json/.html from ChatGPT, Claude and others) also work.
- The plugin cannot read your conversation or attachments by itself: only the agent sees them, and very long conversations may already
  be truncated by the context window.

Sample theory files and chat transcripts are in `plugins/spindoctor-qwerty/skills/spindoctor-qwerty/examples/theory/`. The two sample
PDFs are stored as text; run `python3 plugins/spindoctor-qwerty/skills/spindoctor-qwerty/examples/theory/make_sample_pdfs.py` to
recreate them.

## Folder ingestion (`q.folder`)

`q.folder run path="<folder>"` runs every supported file at the top level of a folder (.txt, .csv, .json, .qasm, .qasm2, .circuit,
.pdf) in ordinal name order: 1-128 supported files, at most 4 MiB per file, 1-128 commands per file and 4096 characters per command,
strict UTF-8. Other files (for example .md) are skipped and listed. The first failing file stops the job.

## Testing

| Test | Command | Result for 1.1.0 |
|---|---|---|
| Host check + end-to-end (real Auggie used when `AUGGIE` or `auggie` is available) | `python3 tests/auggie_host_check.py` | 9/9 host checks, end-to-end 12/12 |
| Real Auggie CLI 0.36.0 loads the marketplace | `auggie command list --plugin-dir .` | 4 commands + skill listed |

**host-simulated (MCP tools):** the real Auggie CLI was installed for free from npm and used without signing in. It loads this marketplace
with `--plugin-dir` and lists the plugin's commands and skill. Listing or calling MCP tools needs a signed-in agent session, which was not
used. The MCP server was driven by `tests/auggie_host_check.py`, which resolves `.mcp.json` the way Auggie's own code does (plugin-root
variables in command, args and env) and starts the server. `auggie plugin marketplace add` also needs the marketplace feature enabled on an
Augment account. Details in [E2E_RESULTS.md](E2E_RESULTS.md).

## Author and license

Author: **RUSSELL PHILIP SMITHSON** <russellsmithson77@outlook.com>

Copyright (C) 2026 RUSSELL PHILIP SMITHSON. Licensed under the GNU General Public License v3.0 or later (`GPL-3.0-or-later`): see
[LICENSE](LICENSE), [NOTICE](NOTICE) and [COPYRIGHT](COPYRIGHT). `plugin.json` carries `"license": "GPL-3.0-or-later"` and the author;
`marketplace.json` names the owner.
