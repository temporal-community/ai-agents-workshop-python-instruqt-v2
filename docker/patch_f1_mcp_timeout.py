#!/usr/bin/env python3
"""Set an explicit 60s timeout on every F1 MCP server in the baked workshop.

The Agents SDK defaults MCPServerStdio reads to 5 seconds. FastF1 cold
fetches often take longer than that, so each factory gets
client_session_timeout_seconds=60. The Temporal activities that wrap those
calls also get an explicit 60s start-to-close timeout.
"""
import os
from pathlib import Path

WORKSHOP = Path(os.environ.get("WORKSHOP_ROOT", "/opt/workshop"))

FACTORY_OLD = """        cache_tools_list=True,
    )"""
FACTORY_NEW = """        cache_tools_list=True,
        client_session_timeout_seconds=60,
    )"""
FACTORY_MARKER = "client_session_timeout_seconds=60"

ACTIVITY_OLD = 'stateless_mcp_server(name="f1-data", cache_tools_list=True)'
ACTIVITY_NEW = """stateless_mcp_server(
            name="f1-data",
            cache_tools_list=True,
            config=workflow.ActivityConfig(
                start_to_close_timeout=timedelta(seconds=60)
            ),
        )"""
ACTIVITY_MARKER = 'config=workflow.ActivityConfig(\n                start_to_close_timeout=timedelta(seconds=60)'

FACTORIES = [
    WORKSHOP / "demo3-mcp/worker.py",
    WORKSHOP / "demo5-multi-agent/worker_f1.py",
    WORKSHOP / "demo6a-different-sdks/worker_f1.py",
    WORKSHOP / "demo6b-different-languages/worker_f1.py",
]

ACTIVITIES = [
    WORKSHOP / "demo3-mcp/tools_workflow.py",
    WORKSHOP / "demo5-multi-agent/f1_expert_agent.py",
    WORKSHOP / "demo6a-different-sdks/f1_expert_agent.py",
    WORKSHOP / "demo6b-different-languages/f1_expert_agent.py",
]


def _replace_once(path: Path, old: str, new: str, marker: str) -> None:
    text = path.read_text()
    if old not in text:
        if marker in text:
            print(f"already set: {path}")
            return
        raise SystemExit(f"F1 MCP timeout site not found in {path}")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected 1 match in {path}, found {count}")
    path.write_text(text.replace(old, new, 1))
    print(f"patched: {path}")


def main() -> None:
    for path in FACTORIES:
        _replace_once(path, FACTORY_OLD, FACTORY_NEW, FACTORY_MARKER)
    for path in ACTIVITIES:
        _replace_once(path, ACTIVITY_OLD, ACTIVITY_NEW, ACTIVITY_MARKER)


if __name__ == "__main__":
    main()
