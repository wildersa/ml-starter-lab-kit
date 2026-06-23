# Local Agent Guidance

Welcome! This project is designed for both human learners and AI agents.

## For Agents (LLM CLIs)

If you are an AI agent helping a user in this project:

1. **Inspect before answering**: Always check the current project state (files, configs, and notebooks) before providing advice.
2. **Use the Tutor Skill**: When the user asks for learning help, next steps, notebook review, dataset understanding, metric explanation, or ML challenges, please read and follow the instructions in:
   `.agents/skills/ml-lab-tutor/SKILL.md`
3. **Prefer Guidance**: Aim to explain and guide the learner through the process rather than just completing tasks silently.
4. **Accuracy**: Do not fabricate dataset details if the project files (like `data/raw/`) are missing or empty.

The ML Lab Tutor skill provides specific context about the educational flow and project structure to help you be a better mentor.
