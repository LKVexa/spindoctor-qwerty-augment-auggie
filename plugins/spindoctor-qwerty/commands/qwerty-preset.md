---
description: Run a SpinDoctor preset (qc-001..qc-241)
argument-hint: <preset-id> [name=value ...]
---

Run SpinDoctor preset $ARGUMENTS with the `spindoctor_run_preset` tool (preset id plus optional name=value overrides; use
`spindoctor_list_presets` to find one). Summarise each step and give the TXT/PDF report paths. Classical simulation only.

If those tools are not available, follow the spindoctor-qwerty skill: its CLI is `scripts/spindoctor_cli.py` inside that skill's folder (Auggie only expands `${AUGMENT_PLUGIN_ROOT}` in `.mcp.json` and hooks, not in commands).
