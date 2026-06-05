---
slug: multi-agent
id: bgvlffymxc8u
type: challenge
title: 'Demo 5: Multi-Agent Orchestration'
teaser: Three agents, three workflows. A personal assistant delegates to specialists
  via child workflow and Nexus.
notes:
- type: text
  contents: |-
    # What if each specialist were its own workflow?

    Demo 4 was one workflow, one agent. Demo 5 introduces agent-as-workflow:
    each specialist is a real Temporal workflow execution, not an inline function.

    Two different invocation patterns. Two different visibility profiles in
    the Temporal UI. One orchestrator that doesn't care which pattern each
    specialist uses.
- type: text
  contents: |-
    # Child workflows vs. Nexus

    The weather agent is a child workflow. Parent-child semantics, trace
    context propagates, shows as StartChildWorkflowExecution in the parent.

    The F1 expert is a Nexus operation. Designed for cross-namespace
    boundaries, clean typed interface, shows as NexusOperationScheduled
    in the parent.

    Same result from the orchestrator's point of view. Different shapes
    in the event history.
tabs:
- id: mxfyeq9hrvp7
  title: Worker PA
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo5-multi-agent
- id: l2rtjamym8q6
  title: Worker F1
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo5-multi-agent
- id: wyykjfu4i6yv
  title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo5-multi-agent
- id: zv27fekpruih
  title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- id: jgmuec1bmeuc
  title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
- id: eufjafkekbwj
  title: Editor
  type: code
  hostname: workshop
  path: /root/workshop/demo5-multi-agent
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Demo 5: Multi-Agent Orchestration

> [!NOTE]
> **Tabs:** [button label="Worker PA" background="#444CE7"](tab-0) [button label="Worker F1" background="#444CE7"](tab-1) [button label="Starter" background="#444CE7"](tab-2) [button label="Temporal UI" background="#444CE7"](tab-3) [button label="Network Control Panel" background="#444CE7"](tab-4) [button label="Editor" background="#444CE7"](tab-5)

## What Changed

Click the [button label="Editor" background="#444CE7"](tab-5) tab. Key files in `demo5-multi-agent`:

- `personal_assistant.py` - the orchestrator. Uses `child_workflow_as_tool` for weather and `nexus_operation_as_tool` for F1.
- `weather_agent.py` - runs as its own workflow on `weather-agent-tq`.
- `f1_expert_agent.py` - runs as its own workflow on `f1-expert-agent-tq`. Also defines the Nexus service interface and handler.
- `worker_pa.py` - orchestrator + weather agent (two task queues, one process).
- `worker_f1.py` - F1 expert + Nexus handler (separate process, separate plugin config).

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
uv run python -m start_workflow "When is the next F1 race and what's the weather there right now?"
```

## The Key Moment

Click the [button label="Temporal UI" background="#444CE7"](tab-3) tab. Look for **three separate workflow executions**:

- The **orchestrator** on `orchestrator-tq`. Its history shows `StartChildWorkflowExecution` for weather and `NexusOperationScheduled` for F1.
- A separate **WeatherAgentWorkflow** on `weather-agent-tq`.
- A separate **F1ExpertAgentWorkflow** on `f1-expert-agent-tq`.

Each specialist is independently observable, independently retryable, and could run on a different team's infrastructure.

## Try More Prompts

Click the [button label="Starter" background="#444CE7"](tab-2) terminal.

```bash,run
uv run python -m start_workflow "What's the current weather at the locations of the next two F1 races?"
```

```bash,run
uv run python -m start_workflow "When is the next F1 race?"
```

Click **Check** when you've run at least one workflow successfully.
