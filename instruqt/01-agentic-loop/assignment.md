---
slug: agentic-loop
id: jhjmk33je3jb
type: challenge
title: 'Demo 1: The Hand-Written Agentic Loop'
teaser: Build an agentic loop from scratch as a Temporal workflow. Watch it survive
  a failure mid-run.
notes:
- type: text
  contents: |-
    # What happens when the worker dies mid-execution?

    Your agent was halfway through a multi-step tool chain when the process
    crashed. The LLM had already answered. A tool had already run. Where
    is that work now?

    In a plain Python script: gone. Start over.

    In a Temporal workflow: every step is recorded. The next worker picks
    up exactly where the last one left off.
- type: text
  contents: |-
    # The loop most frameworks hide from you

    Call the LLM. Check if it wants a tool. Call the tool. Feed the result
    back. Repeat until the model returns a final answer.

    Demo 1 makes that loop explicit, written by hand as a Temporal workflow.
    The LLM call is one activity. Each tool dispatch is another. Every step
    appears in the event history.
tabs:
- id: lwctpem6uc5b
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo1-agentic-loop
- id: yvpvqjosguer
  title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo1-agentic-loop
- id: zt7hqroq3xgg
  title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- id: k63ba3axuacz
  title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
- id: vplvdkfqzcb3
  title: Editor
  type: code
  hostname: workshop
  path: /root/workshop/demo1-agentic-loop
difficulty: basic
timelimit: 1200
enhanced_loading: null
---

# Demo 1: The Hand-Written Agentic Loop

> [!NOTE]
> **Tabs:** [button label="Worker" background="#444CE7"](tab-0) [button label="Starter" background="#444CE7"](tab-1) [button label="Temporal UI" background="#444CE7"](tab-2) [button label="Network Control Panel" background="#444CE7"](tab-3) [button label="Editor" background="#444CE7"](tab-4)

## The Code

Click the [button label="Editor" background="#444CE7"](tab-4) tab and open `demo1-agentic-loop`. Key files:

- `workflows/agent.py` - the `while True` loop: call LLM, dispatch tool if needed, repeat until done
- `activities/openai_responses.py` - the LLM activity
- `activities/tool_invoker.py` - a single dynamic activity that routes to whichever tool the LLM chose
- `tools/` - four weather tools: `get_ip_address`, `get_location_info`, `get_coordinates`, `get_weather`

## Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-0) terminal.

```bash,run
uv run python -m worker
```

You should see:

```bash,nocopy
Worker started. Listening on task queue: tool-invoking-agent-python-task-queue
```

## Run It

Click the [button label="Starter" background="#444CE7"](tab-1) terminal.

```bash,run
uv run python -m start_workflow "What is the weather in Barcelona?"
```

## Watch the Event History

Click the [button label="Temporal UI" background="#444CE7"](tab-2) tab while the workflow runs. Click into it. Each LLM call and each tool invocation appears as a separate activity in the event history - the full decision trail of the agent.

## The Durability Point

Run a multi-step prompt that chains several tools:

```bash,run
uv run python -m start_workflow "What is the weather where I am right now?"
```

While it runs, click the [button label="Network Control Panel" background="#444CE7"](tab-3) tab and disable **Weather**. Watch the activity fail and retry in the Temporal UI. Re-enable it and watch the workflow resume - no code changes.

Click **Check** when you've run at least one workflow successfully.
