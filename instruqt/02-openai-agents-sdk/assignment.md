---
slug: openai-agents-sdk
id: 6w7pumj75txp
type: challenge
title: 'Demo 2: OpenAI Agents SDK + Temporal'
teaser: The same agent, but the SDK drives the loop. Durability becomes automatic.
notes:
- type: text
  contents: |-
    # What if you didn't have to write the loop?

    Demo 1 was ~50 lines of explicit loop logic. What if a single function
    call replaced all of it, and Temporal durability still applied to every
    step inside?

    That's the OpenAI Agents SDK + Temporal integration. One line replaces
    the loop. Every LLM call and every tool invocation still becomes a
    Temporal activity - automatically.
- type: text
  contents: |-
    # The trade-off

    Tools must now be @activity.defn functions rather than plain Python.
    They gain durability but they're no longer Temporal-agnostic.

    The developer writes standard SDK code. Temporal durability is free.
tabs:
- id: fzmgwmgyqkjq
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo2-openai-temporal-integration
- id: vq28pzf9sgpu
  title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo2-openai-temporal-integration
- id: 6bybwvv0p1qu
  title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- id: u6yvktd9jtnc
  title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
- id: tvpdykfxjkpn
  title: Editor
  type: code
  hostname: workshop
  path: /root/workshop/demo2-openai-temporal-integration
difficulty: basic
timelimit: 1200
enhanced_loading: null
---

# Demo 2: OpenAI Agents SDK + Temporal

> [!NOTE]
> **Tabs:** [button label="Worker" background="#444CE7"](tab-0) [button label="Starter" background="#444CE7"](tab-1) [button label="Temporal UI" background="#444CE7"](tab-2) [button label="Network Control Panel" background="#444CE7"](tab-3) [button label="Editor" background="#444CE7"](tab-4)

## What Changed

Click the [button label="Editor" background="#444CE7"](tab-4) tab and open `demo2-openai-temporal-integration`. Compare it to demo1:

- `tools_workflow.py` - the entire agentic loop is now one line: `result = await Runner.run(agent, input=question)`
- `tool_activities.py` - tools are `@activity.defn` functions. `activity_as_tool(...)` wraps each one for the SDK.
- `worker.py` - the `OpenAIAgentsPlugin` is registered on both client and worker. It installs the model-execution activity and interceptors automatically.

## Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-0) terminal.

```bash,run
uv run python -m worker
```

## Run It

Click the [button label="Starter" background="#444CE7"](tab-1) terminal.

```bash,run
uv run python -m start_workflow "What is the weather in Tokyo?"
```

## Watch the Event History

Click the [button label="Temporal UI" background="#444CE7"](tab-2) tab. Look at a completed workflow. `InvokeModelActivity` appears as its own named entry - the SDK's model calls are now first-class Temporal activities alongside the tool calls.

## Break It

Start a new workflow, then use the [button label="Network Control Panel" background="#444CE7"](tab-3) to disable **Weather**. Watch the weather activities fail and retry. Re-enable and watch the workflow succeed.

Click **Check** when you've run at least one workflow successfully.
