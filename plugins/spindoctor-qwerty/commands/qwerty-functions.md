---
description: Show every SpinDoctor function as a table (Function | What it does | Command to type)
argument-hint: "[commands|gates|tools|presets|all] [filter]"
---

Call the `spindoctor_functions` tool (section and filter from: $ARGUMENTS; default section commands) and show the returned
Markdown table to the user verbatim.

If those tools are not available, follow the spindoctor-qwerty skill: its CLI is `scripts/spindoctor_cli.py` inside that skill's folder (Auggie only expands `${AUGMENT_PLUGIN_ROOT}` in `.mcp.json` and hooks, not in commands).
