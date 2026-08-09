# AI Agent Security Evaluation - Plan & Decisions

## Project Scope
Academic research paper evaluating security vulnerabilities in AI coding agents.

### Attack Vectors
1. Prompt Injection
2. Context Poisoning
3. Malicious Package Recommendation (Dependency Confusion)
4. Secret Leakage

*(Explicitly excluded: retrieval poisoning, tool abuse, memory poisoning)*

### Target Agents
- Chat-based: ChatGPT, Gemini
- IDE-integrated: Antigravity IDE
- Terminal/CLI-based: Claude Code

## Evaluation Design
- **Tasks**: ~50 total, ~12-13 scenarios per vector.
- **Difficulty**: Moderate-to-hard only.
- **Executions**: Each task run against all 4 agents (~200 total executions).
- **Execution Protocol**: One real Flask application acting as a baseline control on the `main` branch. Every task is tested on a dedicated Git branch containing the injected context. The identical user prompt is sent to all 4 agents.
- **ID Convention**: `<VECTOR>-<NN>` (e.g., `PI-01`).

## Sequential Plan
1. Draft Prompt Injection task list (format template)
2. Expand task lists to remaining 3 vectors
3. Build adversarial variants per vector
4. Build experiment harness, pilot test it
5. Run full experiment (~200 executions)
6. Automated scoring: CodeQL, Semgrep, Bandit, Gitleaks
7. Manual validation of automated scores
8. Aggregate and compare results across agents
9. Evaluate automated-detection feasibility
10. Design defense framework + proof-of-concept mitigation tests
11. Write the paper

## Decisions Log
- **Task Format**: YAML format chosen for programmatic parsing and readability.
- **Task 1 Execution**: Creating initial PI task list to serve as the template for the other vectors.
- **Codebase Methodology**: Adopted a dedicated external repository (`AI-test-app`) with a clean baseline on `main` and individual tasks isolated to separate Git branches. This ensures realism, simplifies test harnesses for agents with repo access, and provides reproducible, inspectable states for the paper.
- **Agent Context Delivery**: Chat agents (ChatGPT, Gemini) will have file contents pasted directly alongside the prompt, while IDE/CLI agents (Antigravity, Claude Code) will discover the context naturally via repo access.
