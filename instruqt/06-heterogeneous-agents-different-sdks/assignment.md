---
slug: heterogeneous-agents-different-sdks
id: ""
type: challenge
title: 'Demo 6a: Heterogeneous Agents - Different SDKs'
teaser: A Strands agent joins the OpenAI specialists. Same orchestrator, different
  framework, visible trade-off in the event history.
notes:
- type: text
  contents: |-
    # What if a specialist was built with a completely different framework?

    Demo 5 had two specialists, both using the OpenAI Agents SDK. Demo 6a
    adds a third: a travel planner built with Strands Agents SDK.

    Zero Temporal imports in the travel planner. The orchestrator doesn't
    care what framework its specialists use.
- type: text
  contents: |-
    # The durability trade-off, made visible

    OpenAI agents: per-step durability. Every LLM call and every tool call
    is its own Temporal activity. If a worker dies mid-loop, only the
    failing step retries.

    Strands agent: coarse-grained durability. The entire agent loop is one
    activity. If the worker dies, the whole loop restarts.

    Same orchestrator. Same Temporal primitives. Fundamentally different
    visibility in the event history.
tabs:
- title: Worker PA
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6a-different-sdks
- title: Worker F1
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6a-different-sdks
- title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6a-different-sdks
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
  path: /root/workshop/demo6a-different-sdks
difficulty: basic
timelimit: 1800
---

# Demo 6a: Heterogeneous Agents - Different SDKs

> [!NOTE]
> **Tabs:** [button label="Worker PA" background="#444CE7"](tab-0) [button label="Worker F1" background="#444CE7"](tab-1) [button label="Starter" background="#444CE7"](tab-2) [button label="Temporal UI" background="#444CE7"](tab-3) [button label="Network Control Panel" background="#444CE7"](tab-4) [button label="Editor" background="#444CE7"](tab-5)

## What Changed

Click the [button label="Editor" background="#444CE7"](tab-5) tab and open `demo6a-different-sdks`:

- `travel_planner.py` - the Strands travel agent. **Zero Temporal imports.** Could be a library vendored from another team's codebase.
- `travel_planner_activity.py` - a single `@activity.defn` wrapper. It lazy-imports `travel_planner` and calls `run()`. About 10 lines.
- `personal_assistant.py` - now wires three tools: weather (child workflow), F1 (Nexus), and travel planner (direct activity).

## Start the Workers

Click the [button label="Worker PA" background="#444CE7"](tab-0) terminal.

```bash,run
uv run python -m worker_pa
```

Click the [button label="Worker F1" background="#444CE7"](tab-1) terminal.

```bash,run
uv run python -m worker_f1
```

## Run It

Click the [button label="Starter" background="#444CE7"](tab-2) terminal.

```bash,run
uv run python -m start_workflow "When is the next F1 race, what's the weather there right now, and what should I know about visiting?"
```

## The Contrast

Open the orchestrator workflow in the [button label="Temporal UI" background="#444CE7"](tab-3) and compare to demo 5:

- Weather: `StartChildWorkflowExecution` (same as demo 5)
- F1: `NexusOperationScheduled` / `NexusOperationCompleted` (same as demo 5)
- Travel planner: **a single `ScheduleActivityTask: ask_travel_planner`** - the entire Strands loop, all its LLM calls and tool calls, inside one opaque event

That contrast is the point.

## Try More Prompts

```bash,run
uv run python -m start_workflow "Tell me about Monaco as a travel destination."
```

```bash,run
uv run python -m start_workflow "What's the current weather at the locations of the next two F1 races?"
```

Click **Check** when you've run at least one workflow that invokes the travel planner.
