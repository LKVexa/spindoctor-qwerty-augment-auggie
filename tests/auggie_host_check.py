#!/usr/bin/env python3
# SpinDoctor Qwerty 1.1.0 - Auggie stand-in host
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Auggie stand-in host check. Standard library only (Python 3.8+); no Augment account needed.

1. Validates .augment-plugin/marketplace.json and the plugin's .augment-plugin/plugin.json, commands, agents, rules and
   skill (skill name rule ^[a-z0-9-]+$, 1-64 chars, no '--'; description 1-1024 chars, as Auggie checks them).
2. Reads plugins/spindoctor-qwerty/.mcp.json exactly as Auggie does: ${AUGMENT_PLUGIN_ROOT}, ${AUGGIE_PLUGIN_ROOT}
   and ${CLAUDE_PLUGIN_ROOT} in command/args/env are replaced with the plugin folder. It then starts that server and
   runs tests/e2e_mcp.py through it.
3. If the real Auggie CLI is available (set AUGGIE=/path/to/auggie or have `auggie` on PATH), it also runs
   `auggie command list --plugin-dir <repo>` and checks that the four commands and the skill are listed. No sign-in.

usage: python3 tests/auggie_host_check.py [REPO_DIR]"""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VARS = ("${CLAUDE_PLUGIN_ROOT}", "${AUGMENT_PLUGIN_ROOT}", "${AUGGIE_PLUGIN_ROOT}")
COMMANDS = ("qwerty-run", "qwerty-preset", "qwerty-functions", "qwerty-theory")


def frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", open(path, encoding="utf-8").read(), re.S)
    return dict(re.findall(r"^([A-Za-z_-]+):\s*(.+)$", m.group(1), re.M)) if m else {}


def sub(s, root):
    for v in VARS: s = s.replace(v, root)
    return s


def main():
    repo = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
    ok = True

    def T(name, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond); print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  -- " + str(detail)))

    mk = json.load(open(os.path.join(repo, ".augment-plugin", "marketplace.json"), encoding="utf-8"))
    entry = next((p for p in mk.get("plugins", []) if p.get("name") == "spindoctor-qwerty"), None)
    T("marketplace.json: name and a spindoctor-qwerty entry with a ./plugins source", mk.get("name") and entry and entry.get("source", "").startswith("./"), mk)
    root = os.path.realpath(os.path.join(repo, entry["source"]))
    pj = json.load(open(os.path.join(root, ".augment-plugin", "plugin.json"), encoding="utf-8"))
    T("plugin.json: name, version 1.1.0 (= marketplace entry), GPL-3.0-or-later, author", pj.get("name") == "spindoctor-qwerty" and pj.get("version") == entry.get("version") == "1.1.0" and pj.get("license") == "GPL-3.0-or-later" and pj.get("author", {}).get("name") == "RUSSELL PHILIP SMITHSON", pj)
    cmds = sorted(f[:-3] for f in os.listdir(os.path.join(root, "commands")) if f.endswith(".md"))
    T("commands/: four commands, each with a description", cmds == sorted(COMMANDS) and all(frontmatter(os.path.join(root, "commands", c + ".md")).get("description") for c in cmds), cmds)
    T("agents/ and rules/ present", any(f.endswith(".md") for f in os.listdir(os.path.join(root, "agents"))) and any(f.endswith(".md") for f in os.listdir(os.path.join(root, "rules"))))
    fm = frontmatter(os.path.join(root, "skills", "spindoctor-qwerty", "SKILL.md"))
    name, desc = fm.get("name", ""), fm.get("description", "")
    T("skill: valid name (^[a-z0-9-]+$, 1-64, no '--') matching its folder; description 1-1024 chars", name == "spindoctor-qwerty" and re.match(r"^[a-z0-9-]+$", name) and "--" not in name and 1 <= len(desc) <= 1024, (name, len(desc)))
    T("no hooks (hooks/hooks.json absent)", not os.path.exists(os.path.join(root, "hooks", "hooks.json")))
    mcp = json.load(open(os.path.join(root, ".mcp.json"), encoding="utf-8"))["mcpServers"]["spindoctor-qwerty"]
    cmd = [sub(mcp["command"], root)] + [sub(a, root) for a in mcp.get("args", [])]
    env = dict(os.environ, **{k: sub(str(v), root) for k, v in mcp.get("env", {}).items()})
    T(".mcp.json: stdio server whose script resolves inside the plugin folder", mcp.get("type", "stdio") == "stdio" and os.path.isfile(cmd[1]) and os.path.realpath(cmd[1]).startswith(root + os.sep), cmd)
    if os.environ.get("SPINDOCTOR_PYTHON"): cmd[0] = os.environ["SPINDOCTOR_PYTHON"]
    auggie = os.environ.get("AUGGIE") or shutil.which("auggie")
    if auggie:
        r = subprocess.run([auggie, "command", "list", "--plugin-dir", repo], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)
        out = r.stdout + r.stderr
        T("real Auggie CLI lists the four commands and the skill (auggie command list --plugin-dir)", all(":" + c in out for c in COMMANDS) and "spindoctor-qwerty:spindoctor-qwerty" in out, out[-800:])
    else:
        print("SKIP real Auggie CLI not found (set AUGGIE=/path/to/auggie)")
    r = subprocess.run([sys.executable, os.path.join(HERE, "e2e_mcp.py"), "--server"] + cmd + ["--examples", os.path.join(root, "skills", "spindoctor-qwerty", "examples", "theory"), "--out", os.path.join(HERE, "e2e_results.json")], env=env)
    T("end-to-end test through the server declared in .mcp.json", r.returncode == 0)
    print("HOST-CHECK", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
