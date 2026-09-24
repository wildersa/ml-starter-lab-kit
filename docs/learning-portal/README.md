# Learning Portal & LabRL MVP

The Learning Portal is a local-first interactive learning environment for Machine Learning and Reinforcement Learning paths.

## Quick Start

### 1. Start the Portal Backend API & LabRL Engine (FastAPI)

```bash
# Run from repository root
uvicorn portal.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 2. Start the Learner Web Application (React + TypeScript)

```bash
cd portal/web
npm install
npm run dev
```

Open your browser at `http://localhost:5173` to explore the Learning Portal.

## Architecture

- **Control Plane (Portal API)**: FastAPI + SQLite (`portal.db`) managing skill graph prerequisite unlocking, activity evaluation, and evidence persistence.
- **Learner UI**: React + TypeScript + Vite providing the Skill Graph navigation, Skill Workspace, and interactive LabRL canvas.
- **Execution Plane (LabRL)**: Isolated Python module (`portal/lab_rl/`) executing MDP transitions and tabular Q-Learning step diagnostics (`old_q`, `target`, `td_error`, `new_q`).

## Curriculum Path Delivered

1. `RL vocabulary`
2. `Reward vs Return`
3. `Discounting`
4. `MDP`
5. `V and Q`
6. `Bellman backup`
7. `TD / Q-Learning` (unlocks interactive LabRL GridWorld)
