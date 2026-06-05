---
slug: heterogeneous-agents-different-languages
id: sxfuduetezvx
type: challenge
title: 'Demo 6b: Heterogeneous Agents - Different Languages'
teaser: The travel planner moves to Java and Spring AI. Per-step durability across
  a language boundary, over Nexus.
notes:
- type: text
  contents: |-
    # What if a specialist was written in a completely different language?

    Demo 6a showed different frameworks, same language. Demo 6b shows a
    different language entirely: the travel planner is reimplemented in
    Java with Spring AI.

    The Python orchestrator reaches it over Nexus - the same boundary it
    already uses for the F1 expert. The Java side shares no code with
    Python. They agree only on string names and JSON shapes.
- type: text
  contents: |-
    # The payoff: per-step durability across the language boundary

    In demo 6a the Strands travel planner was one opaque activity. The
    entire loop lived inside one event.

    In demo 6b the Spring AI travel planner gets per-step durability.
    Every LLM call and every tool call is its own Temporal activity -
    exactly like the OpenAI Agents SDK specialists.

    Compare the two histories side by side.
tabs:
- id: wuhmheksfvbj
  title: Java Worker
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6b-different-languages/travel-planner-java
- id: qvbbeyvbqa16
  title: Worker PA
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6b-different-languages
- id: linlzgiwwetj
  title: Worker F1
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6b-different-languages
- id: tff3kjs1m61c
  title: Starter
  type: terminal
  hostname: workshop
  workdir: /root/workshop/demo6b-different-languages
- id: nfbjfjujuaw8
  title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- id: 1ktdnrqxf7n7
  title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
- id: jtydohne7boe
  title: Editor
  type: code
  hostname: workshop
  path: /root/workshop/demo6b-different-languages
difficulty: basic
timelimit: 2400
enhanced_loading: null
---

# Demo 6b: Heterogeneous Agents - Different Languages

> [!NOTE]
> **Tabs:** [button label="Java Worker" background="#444CE7"](tab-0) [button label="Worker PA" background="#444CE7"](tab-1) [button label="Worker F1" background="#444CE7"](tab-2) [button label="Starter" background="#444CE7"](tab-3) [button label="Temporal UI" background="#444CE7"](tab-4) [button label="Network Control Panel" background="#444CE7"](tab-5) [button label="Editor" background="#444CE7"](tab-6)

## What Changed from 6a

| | demo6a | demo6b |
|---|---|---|
| Travel planner language | Python | Java |
| Travel planner framework | Strands Agents SDK | Spring AI |
| Invocation from orchestrator | direct activity | Nexus operation |
| Durability of travel agent | coarse (whole loop = one activity) | per-step (each LLM/tool call = one activity) |

## Start the Java Worker

Click the [button label="Java Worker" background="#444CE7"](tab-0) terminal. Dependencies were pre-fetched in the image so this starts in seconds.

```bash,run
./mvnw spring-boot:run
```

## Start the Python Workers

Click the [button label="Worker PA" background="#444CE7"](tab-1) terminal.

```bash,run
uv run python -m worker_pa
```

Click the [button label="Worker F1" background="#444CE7"](tab-2) terminal.

```bash,run
uv run python -m worker_f1
```

## Run It

Click the [button label="Starter" background="#444CE7"](tab-3) terminal.

```bash,run
uv run python -m start_workflow "What should I know about visiting Monaco?"
```

## The Key Comparison

Open the [button label="Temporal UI" background="#444CE7"](tab-4) tab.

In the **orchestrator** history, the travel planner path now shows `NexusOperationScheduled` / `NexusOperationCompleted` instead of a single opaque activity event.

Then find the **`TravelPlannerAgentWorkflow`** on `travel-planner-agent-tq`. Its history shows per-step activities: a `ChatModelActivity` for each LLM call, individual activities for each tool call. That's Spring AI giving the Java agent the same per-step durability the OpenAI Agents SDK gives the Python agents.

## Try More Prompts

Click the [button label="Starter" background="#444CE7"](tab-3) terminal.

```bash,run
uv run python -m start_workflow "What's the weather at the next F1 race and what should I know about visiting the destination?"
```

```bash,run
uv run python -m start_workflow "When is the next F1 race?"
```

Click **Check** when you've run at least one workflow that invokes the Java travel planner.
