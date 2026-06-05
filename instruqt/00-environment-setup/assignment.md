---
slug: environment-setup
id: ""
type: challenge
title: Environment Setup
teaser: Verify the sandbox is healthy before the first demo.
notes:
- type: text
  contents: |-
    # Welcome

    A Temporal dev server is running in your sandbox. Seven progressive
    demos take a plain Python agentic loop to a multi-language, multi-framework
    agent system.

    Each demo adds one thing. You see before and after in the Temporal Web UI.

    The blue buttons in these instructions are clickable. Click any to jump
    to that tab.
tabs:
- title: Terminal
  type: terminal
  hostname: workshop
  workdir: /root/workshop
- title: Temporal UI
  type: service
  hostname: workshop
  port: 8233
- title: Network Control Panel
  type: service
  hostname: workshop
  port: 5000
difficulty: basic
timelimit: 600
---

# Environment Setup

> [!NOTE]
> **Sandbox tabs:**
> - [button label="Terminal" background="#444CE7"](tab-0) - your working terminal
> - [button label="Temporal UI" background="#444CE7"](tab-1) - Temporal Web UI
> - [button label="Network Control Panel" background="#444CE7"](tab-2) - proxy toggles for fault-tolerance demos

## Check the Temporal server

Click the [button label="Terminal" background="#444CE7"](tab-0) tab.

```bash,run
temporal operator cluster health
```

You should see:

```bash,nocopy
SERVING
```

Click the [button label="Temporal UI" background="#444CE7"](tab-1) tab. An empty workflow list means the server is healthy and no workflows have run yet.

## Verify your tools

```bash,run
python --version && uv --version && temporal --version && node --version && java -version
```

## Set your API key

You need your own OpenAI API key for this workshop. Add it to your shell so it persists across all terminal tabs:

```bash,run
echo 'export OPENAI_API_KEY=sk-your-key-here' >> ~/.bashrc && source ~/.bashrc
```

Replace `sk-your-key-here` with your actual key. Verify it took:

```bash,run
echo $OPENAI_API_KEY
```

You should see your key starting with `sk-`.

## Check the Network Control Panel

Click the [button label="Network Control Panel" background="#444CE7"](tab-2) tab. All four services should show green. Your facilitator uses this panel to toggle external services on and off during demos to show Temporal's retry behavior.

## Explore the workshop

```bash,run
ls /root/workshop
```

Seven demo directories. Each is self-contained with its own dependencies and task queue.

Click **Check** when you're ready to continue.
