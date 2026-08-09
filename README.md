# AI Agent Security Evaluation

Welcome to the AI Agent Security Evaluation project! This repository contains all the code, tasks, and data for our academic research into the security of AI coding assistants (like ChatGPT, Gemini, and Claude Code). 

We are testing to see if we can "trick" these AIs into writing vulnerable code or leaking secrets by giving them specially crafted, tricky instructions.

## What is in this repository?

Here is a layman's breakdown of how this project is organized and what each folder does:

- **`tasks/`**: The "Test Bank". This folder holds all the tricky scenarios we use to evaluate the AI. Think of it as a set of exam questions designed to see if the AI will fall for a security trap (like Prompt Injection or Dependency Confusion).
- **`test-repo/`**: The "Dummy Application". This is a fake, shared codebase that we give the AI to work on. The tasks ask the AI to make changes to this code, and we watch how it behaves.
- **`harness/`**: The "Test Runner". This folder contains scripts that automatically take our tasks, feed them to the different AIs, and collect their responses. It's the engine that runs our experiments so we don't have to do it manually.
- **`scoring/`**: The "Grader". Once the AIs finish a task, the tools in this folder automatically scan the code they wrote to see if they introduced a vulnerability. It decides whether the AI "passed" or "failed" the security test.
- **`results/`**: The "Report Card". This is where all the raw outputs from the AIs and their final scores are saved.
- **`paper/`**: The "Final Paper". This folder syncs directly with Overleaf and contains the actual text and formatting for our academic research paper.
- **`docs/`**: The "Project Notebook". This contains our plans, design decisions, and setup notes for the project. 

## The Attack Vectors We Are Testing

We are focusing on four specific ways to trick an AI:
1. **Prompt Injection**: Directly telling the AI to ignore its safety rules and write bad code.
2. **Context Poisoning**: Hiding malicious instructions inside files (like logs or issue descriptions) that the AI reads while trying to help.
3. **Dependency Confusion**: Tricking the AI into recommending fake or malicious third-party code packages.
4. **Secret Leakage**: Getting the AI to accidentally reveal sensitive information (like passwords or API keys) from its environment.
