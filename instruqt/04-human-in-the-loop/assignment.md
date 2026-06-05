---
slug: human-in-the-loop
id: omyvoydii2je
type: challenge
title: 'Demo 4: Human-in-the-Loop'
teaser: The agent pauses mid-execution to ask you a question. A Temporal signal resumes
  it.
notes:
- type: text
  contents: |-
    # What if the agent needs to ask you something before it can continue?

    The workflow is running. The agent realizes it doesn't have enough
    information to proceed. It needs your input right now, mid-execution.

    In a plain Python script, you'd have to restart. In Temporal, the
    workflow suspends with no worker resources consumed - and resumes the
    instant you answer.
- type: text
  contents: |-
    # Three Temporal primitives working together

    ask_user sets workflow state and awaits wait_condition. The workflow
    is suspended - durably - holding no threads, no memory.

    provide_user_input is a signal. It delivers your answer and unblocks
    the wait_condition.

    Two queries let the starter poll: is_input_needed and
    get_pending_question. The starter asks the question on the terminal
    and sends your answer as a signal.
tabs:
- id: hrubvxth7ui9
  title: Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo4-hitl
- id: wimstsxxbuud
  title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo4-hitl
- id: cbjsucaomvrg
  title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- id: e1sim7ca2cyi
  title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
- id: mxwobjyx8ugr
  title: Editor
  type: code
  hostname: workshop
  path: /root/workshop/demo4-hitl
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

# Demo 4: Human-in-the-Loop

> [!NOTE]
> **Tabs:** [button label="Worker" background="#444CE7"](tab-0) [button label="Starter" background="#444CE7"](tab-1) [button label="Temporal UI" background="#444CE7"](tab-2) [button label="Network Control Panel" background="#444CE7"](tab-3) [button label="Editor" background="#444CE7"](tab-4)

## What Changed

Click the [button label="Editor" background="#444CE7"](tab-4) tab and open `demo4-hitl`:

- `tools_workflow.py` - an `ask_user` `@function_tool` is defined inside `run()` as a closure. It sets `self._input_needed = True` and blocks on `await workflow.wait_condition(...)`. The signal handler flips the flag to unblock it.
- `start_workflow.py` - polls queries every 2 seconds. When `is_input_needed` is True, it prints the question, reads your response, and sends it as a signal.

## Start the Worker

Click the [button label="Worker" background="#444CE7"](tab-0) terminal.

```bash,run
uv run python -m worker
```

## Run It

Click the [button label="Starter" background="#444CE7"](tab-1) terminal. The agent can't answer without knowing your destination - it will pause and ask you.

```bash,run
uv run python -m start_workflow "What's the weather like where I'm traveling to this weekend?"
```

Type your destination when prompted and press Enter.

## Watch the Suspension

Click the [button label="Temporal UI" background="#444CE7"](tab-2) tab while the workflow waits. The status shows **Running** but there are no pending activity tasks. The workflow is suspended on `wait_condition` - no worker threads consumed.

When you respond, a new event appears in the history: the signal arrives, `wait_condition` unblocks, and the agent continues.

## Reconnect to a Waiting Workflow

If you close the [button label="Starter" background="#444CE7"](tab-1) terminal while the agent is waiting, the workflow keeps running on the server. Find the workflow ID in the [button label="Temporal UI" background="#444CE7"](tab-2), then reconnect:

```bash,nocopy
uv run python -m start_workflow --workflow-id <workflow-id-from-ui>
```

Click **Check** when you've completed a full interaction with the agent.
