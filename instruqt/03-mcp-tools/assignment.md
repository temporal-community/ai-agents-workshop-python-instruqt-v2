---
slug: mcp-tools
id: ""
type: challenge
title: 'Demo 3: MCP Tool Servers'
teaser: Add a Formula 1 data server via MCP. Each tool call becomes a durable Temporal
  activity automatically.
notes:
- type: text
  contents: |-
    # What if your agent's tools lived on a separate server?

    Model Context Protocol (MCP) is a standard for connecting AI agents to
    external tool servers. Any team can publish a tool server. Any agent can
    consume it without importing a library.

    Demo 3 adds an F1 race data server alongside the existing weather tools.
    The agent can now chain F1 data with weather data in a single workflow.
- type: text
  contents: |-
    # Every MCP call is a Temporal activity

    StatelessMCPServerProvider routes every MCP operation through Temporal.
    Each listTools and callTool becomes its own activity in the workflow
    history - durable, retryable, observable - without extra code from you.
tabs:
- title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo3-mcp
- title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo3-mcp
- title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
- title: Editor
  type: code
  hostname: workshop
  path: /root/workshop/demo3-mcp
difficulty: basic
timelimit: 1500
---

# Demo 3: MCP Tool Servers

> [!NOTE]
> **Tabs:** [button label="Worker" background="#444CE7"](tab-0) [button label="Starter" background="#444CE7"](tab-1) [button label="Temporal UI" background="#444CE7"](tab-2) [button label="Network Control Panel" background="#444CE7"](tab-3) [button label="Editor" background="#444CE7"](tab-4)

## What Changed

Click the [button label="Editor" background="#444CE7"](tab-4) tab and open `demo3-mcp`:

- `worker.py` - a `StatelessMCPServerProvider` is registered with the plugin. It launches the F1 MCP server process and wraps its operations as Temporal activities automatically.
- `tools_workflow.py` - `stateless_mcp_server("f1-data")` gives the agent a handle to the MCP server. Eight F1 tools appear alongside the four weather tools.

## Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-0) terminal.

```bash,run
uv run python -m worker
```

## Run It

Click the [button label="Starter" background="#444CE7"](tab-1) terminal.

```bash,run
uv run python -m start_workflow "When is the next F1 race and what's the weather there right now?"
```

> [!NOTE]
> The first workflow may take 15-30 seconds on F1 tool calls while FastF1 fetches session data. Subsequent runs are fast from the local cache.

## Watch the Event History

Click the [button label="Temporal UI" background="#444CE7"](tab-2) tab. Three kinds of activity entries in the workflow history:

- `InvokeModelActivity` - LLM reasoning steps
- Weather activities (`get_coordinates`, `get_weather`, etc.)
- `f1-data-list-tools` and `f1-data-call-tool-v2` - MCP operations, each a durable activity

## Break It

Click the [button label="Network Control Panel" background="#444CE7"](tab-3) and disable **Weather** mid-workflow. Watch the weather activities fail and retry. Re-enable and watch them succeed.

## Try More Prompts

```bash,run
uv run python -m start_workflow "What is the 2026 F1 race calendar?"
```

```bash,run
uv run python -m start_workflow "What were the results of the last Monaco Grand Prix?"
```

Click **Check** when you've run at least one workflow successfully.
