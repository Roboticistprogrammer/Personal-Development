# Agent team

I will use GitHub Copilot CLI in a Codespace to orchestrate the custom agents that build Mona's Project Pulse dashboard.

| Agent | Model | Responsibility | Definition |
| --- | --- | --- | --- |
| Orchestrator | Claude Opus 4.7 (copilot) | Coordinates the Planner, Designer, and Coder; manages phases, dependencies, and integration. | `.github/agents/orchestrator.agent.md` |
| Planner | Claude Opus 4.7 (copilot) | Researches the repo and produces a phased implementation plan with file ownership and risks. | `.github/agents/planner.agent.md` |
| Designer | Gemini 3.1 Pro (copilot) | Defines UX, layout, accessibility, and visual styling for the dashboard. | `.github/agents/designer.agent.md` |
| Coder | GPT-5.5 (copilot) | Implements the static dashboard and required support files within assigned scope. | `.github/agents/coder.agent.md` |

The Orchestrator will request a plan from the Planner, route design direction from the Designer, and then assign the Coder the concrete implementation tasks. Work will proceed in ordered phases to avoid overlapping file edits while keeping the dashboard cohesive.
