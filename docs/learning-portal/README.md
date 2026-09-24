# Learning Portal & Lab Runtime MVP

The Learning Portal is a local-first interactive learning environment for Machine Learning and Reinforcement Learning paths.

## Quick Start

### 1. Start the Control Plane (Portal API)

```bash
# Run from repository root
uvicorn portal.api.main:app --reload --port 8000
```

The Control Plane API will be available at `http://localhost:8000`.

### 2. Start the Execution Plane (Lab Runtime)

```bash
# Run from repository root in a separate process
uvicorn portal.runtime.main:app --reload --port 8001
```

The Lab Runtime service will be available at `http://localhost:8001`.
*(Note: If the Lab Runtime is offline, the Portal API remains fully functional for theory, Skill Graph navigation, and evaluated activities, gracefully returning a 503 status for simulation actions.)*

### 3. Start the Learner Web Application (React + TypeScript)

```bash
cd portal/web
npm install
npm run dev
```

Open your browser at `http://localhost:5173` to explore the Learning Portal.

## Architecture

- **Control Plane (`portal/api/`)**: FastAPI + SQLite (`portal.db`) managing skill graph prerequisite unlocking, activity evaluation, and evidence persistence. Completely decoupled from execution internals.
- **Execution Plane (`portal/runtime/`)**: Standalone FastAPI service managing runtime sessions, capability requests, deterministic RL simulation execution (`portal/lab_rl/`), and step diagnostics (`old_q`, `target`, `td_error`, `new_q`).
- **Learner UI (`portal/web/`)**: React + TypeScript + Vite providing Skill Graph navigation, Skill Workspace, and interactive LabRL canvas.

## Boundary Invariant

```text
Portal / Control Plane != Lab Runtime / Execution Plane
```

- Portal API process executes zero arbitrary learner Python code and contains no imports from `portal.lab_rl`.
- Lab Runtime executes simulations in isolated sessions and contains no database mutation or mastery/progression logic.

## Curriculum Path Delivered

1. `RL vocabulary`
2. `Reward vs Return`
3. `Discounting`
4. `MDP`
5. `V and Q`
6. `Bellman backup`
7. `TD / Q-Learning` (unlocks interactive LabRL GridWorld)
