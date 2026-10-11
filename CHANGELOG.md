# Changelog

## 1.1.0 (2026-10-10)

- Engine rebased on **SpinDoctor 3.1.2** (update 3.1.2-298-20261010): 1-298 logical qubits with 59-qubit entangled factors,
  prepared-factor Born-Z sampling above 29 qubits, the `mcx7` gate, wide basis indices, `q.folder` with 3.1.2 semantics,
  CSV report copies and measurement-CSV fitting equations. 241 presets replayed against the updated 3.1.2 reference.
- New tools: `spindoctor_functions` (in-chat function table) and `spindoctor_test_theory` (file, pasted text, chat history,
  exported chat transcripts).
- Repository is now an Auggie **marketplace** (`.augment-plugin/marketplace.json` + `plugins/spindoctor-qwerty/`), so
  `auggie plugin marketplace add LKVexa/spindoctor-qwerty-augment-auggie` and `auggie --plugin-dir <clone>` both work.
- Fix: the slash commands and the subagent told Auggie to run `python3 "${AUGMENT_PLUGIN_ROOT}/..."`. Auggie only expands
  plugin-root variables in `.mcp.json` and hooks (checked in Auggie 0.36.0), so that fallback pointed at a non-existent path.
  The commands now use the MCP tools and fall back to the skill's own CLI.
- Commands, agent, skill and rule updated from 3.0.3 / "1..29 qubits" to the 3.1.2 limits; new `rules/spindoctor-honesty.md`.
- Empty `hooks/hooks.json` removed (no hooks). `.mcp.json` gets `PYTHONUTF8` and `PYTHONDONTWRITEBYTECODE`.
- plugin.json: license MIT -> GPL-3.0-or-later; author RUSSELL PHILIP SMITHSON with email; homepage and repository.
- Optional reproducibility: `SPINDOCTOR_MEASUREMENT_SEED` / `SPINDOCTOR_FIELD_SEED` (64 hex characters) seed a new workspace.

## 1.0.0

- First release (SpinDoctor 3.0.3 semantics).
