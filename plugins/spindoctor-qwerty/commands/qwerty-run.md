---
description: Run SpinDoctor q.* commands with the bundled classical simulator
argument-hint: <q.* commands separated by newlines>
---

Run these SpinDoctor q.* commands with the `spindoctor_run_script` tool (one command per line), then summarise the results,
the exact probabilities next to the sampled counts, and the TXT/PDF report paths:

$ARGUMENTS

If those tools are not available, follow the spindoctor-qwerty skill: its CLI is `scripts/spindoctor_cli.py` inside that skill's folder (Auggie only expands `${AUGMENT_PLUGIN_ROOT}` in `.mcp.json` and hooks, not in commands).

Remind the user that this is a classical FP64 simulation on their computer, not quantum hardware. Registers wider than
29 qubits (up to 298) sample in basis z only.
