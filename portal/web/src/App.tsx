import { useState, useEffect } from "react";

interface SkillNode {
  id: string;
  title: string;
  prerequisites: string[];
  state: "locked" | "available" | "started" | "acquired" | "mastered";
  mastery_score: number;
  lab_rl_enabled: boolean;
}

interface Activity {
  id: string;
  prompt: string;
  type: "numeric" | "choice";
  options?: string[];
  explanation: string;
}

interface Workspace {
  id: string;
  title: string;
  theory: string;
  worked_example: string;
  activities: Activity[];
  lab_rl_enabled: boolean;
  user_progress: {
    state: string;
    completed_activities: string[];
  };
}

interface QDiagnostic {
  state: [number, number];
  action: number;
  reward: number;
  next_state: [number, number];
  done: boolean;
  old_q: number;
  max_next_q: number;
  target: number;
  td_error: number;
  new_q: number;
  alpha: number;
  gamma: number;
}

const API_BASE = "http://localhost:8000/api";

export function App() {
  const [nodes, setNodes] = useState<SkillNode[]>([]);
  const [activeSkillId, setActiveSkillId] = useState<string>("rl-vocab");
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState<Record<string, { is_correct: boolean; message: string }>>({});

  // LabRL state
  const [labState, setLabState] = useState<[number, number]>([0, 0]);
  const [qTable, setQTable] = useState<Record<string, number[]>>({});
  const [diagnostic, setDiagnostic] = useState<QDiagnostic | null>(null);
  const [labDone, setLabDone] = useState<boolean>(false);

  const fetchGraph = async () => {
    try {
      const res = await fetch(`${API_BASE}/graph`);
      const data = await res.json();
      setNodes(data.nodes);
    } catch (err) {
      console.error("Failed to fetch graph:", err);
    }
  };

  const fetchWorkspace = async (skillId: string) => {
    try {
      const res = await fetch(`${API_BASE}/workspace/${skillId}`);
      const data = await res.json();
      setWorkspace(data);
    } catch (err) {
      console.error("Failed to fetch workspace:", err);
    }
  };

  const resetLab = async () => {
    try {
      const res = await fetch(`${API_BASE}/lab/reset`, { method: "POST" });
      const data = await res.json();
      setLabState(data.state);
      setQTable(data.q_table);
      setDiagnostic(null);
      setLabDone(data.done);
    } catch (err) {
      console.error("Failed to reset lab:", err);
    }
  };

  const stepLab = async (action: number) => {
    try {
      const res = await fetch(`${API_BASE}/lab/step`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      });
      const data = await res.json();
      setLabState(data.step_record.transition.next_state);
      setQTable(data.q_table);
      setDiagnostic(data.diagnostic);
      setLabDone(data.done);
    } catch (err) {
      console.error("Failed to step lab:", err);
    }
  };

  const submitActivity = async (activityId: string) => {
    const given = answers[activityId];
    if (given === undefined || given === "") return;

    try {
      const res = await fetch(`${API_BASE}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          skill_id: activeSkillId,
          activity_id: activityId,
          given_answer: given,
        }),
      });
      const data = await res.json();
      setFeedback((prev) => ({
        ...prev,
        [activityId]: { is_correct: data.is_correct, message: data.feedback },
      }));
      setNodes(data.unlocked_next);
      fetchWorkspace(activeSkillId);
    } catch (err) {
      console.error("Failed to submit activity:", err);
    }
  };

  useEffect(() => {
    fetchGraph();
    fetchWorkspace(activeSkillId);
  }, [activeSkillId]);

  useEffect(() => {
    if (workspace?.lab_rl_enabled) {
      resetLab();
    }
  }, [workspace?.lab_rl_enabled]);

  return (
    <div className="app-container">
      <header className="top-header">
        <div className="brand">ML Starter Learning Portal — Autonomous RL Path</div>
        <button
          className="btn btn-secondary"
          onClick={async () => {
            await fetch(`${API_BASE}/reset-progress`, { method: "POST" });
            fetchGraph();
            fetchWorkspace(activeSkillId);
          }}
        >
          Reset Learner State
        </button>
      </header>

      <div className="main-content">
        <aside className="sidebar">
          <h2>Skill Graph</h2>
          <div className="graph-container">
            {nodes.map((node) => {
              const isActive = node.id === activeSkillId;
              const isLocked = node.state === "locked";
              return (
                <div
                  key={node.id}
                  className={`node-card ${isActive ? "active" : ""} ${isLocked ? "locked" : ""}`}
                  onClick={() => {
                    if (!isLocked) setActiveSkillId(node.id);
                  }}
                >
                  <div>
                    <strong>{node.title}</strong>
                    {node.prerequisites.length > 0 && (
                      <div style={{ fontSize: "0.75rem", color: "#9ca3af" }}>
                        Req: {node.prerequisites.join(", ")}
                      </div>
                    )}
                  </div>
                  <span className={`badge ${node.state}`}>{node.state}</span>
                </div>
              );
            })}
          </div>
        </aside>

        <main className="workspace-area">
          {workspace && (
            <div>
              <h1>{workspace.title}</h1>

              <section className="theory-box">
                <h2>1. Theory & Intuition</h2>
                <p style={{ whiteSpace: "pre-line" }}>{workspace.theory}</p>
              </section>

              <section className="worked-example-box">
                <h2>2. Worked Example</h2>
                <p style={{ whiteSpace: "pre-line" }}>{workspace.worked_example}</p>
              </section>

              <section className="activity-box">
                <h2>3. Evaluated Activity</h2>
                {workspace.activities.map((act) => (
                  <div key={act.id}>
                    <p><strong>Question:</strong> {act.prompt}</p>
                    {act.type === "choice" && act.options ? (
                      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
                        {act.options.map((opt) => (
                          <label key={opt} style={{ cursor: "pointer" }}>
                            <input
                              type="radio"
                              name={act.id}
                              value={opt}
                              checked={answers[act.id] === opt}
                              onChange={(e) =>
                                setAnswers({ ...answers, [act.id]: e.target.value })
                              }
                            />{" "}
                            {opt}
                          </label>
                        ))}
                      </div>
                    ) : (
                      <input
                        type="number"
                        step="0.01"
                        className="input-field"
                        placeholder="Enter calculated number"
                        value={answers[act.id] || ""}
                        onChange={(e) =>
                          setAnswers({ ...answers, [act.id]: e.target.value })
                        }
                      />
                    )}
                    <div>
                      <button className="btn" onClick={() => submitActivity(act.id)}>
                        Submit Answer
                      </button>
                    </div>

                    {feedback[act.id] && (
                      <div
                        style={{
                          marginTop: "0.75rem",
                          color: feedback[act.id].is_correct ? "#34d399" : "#f87171",
                          fontWeight: "bold",
                        }}
                      >
                        {feedback[act.id].message}
                      </div>
                    )}
                  </div>
                ))}
              </section>

              {workspace.lab_rl_enabled && (
                <section className="theory-box" style={{ borderColor: "#3b82f6" }}>
                  <h2>4. Interactive LabRL Practice</h2>
                  <p>Step through the 3x3 GridWorld environment and trace actual TD Q-Learning updates in real time.</p>

                  <div style={{ display: "flex", gap: "2rem", alignItems: "flex-start" }}>
                    <div>
                      <h3>GridWorld MDP (3x3)</h3>
                      <div className="lab-grid">
                        {[0, 1, 2].map((r) =>
                          [0, 1, 2].map((c) => {
                            const isAgent = labState[0] === r && labState[1] === c;
                            const isGoal = r === 2 && c === 2;
                            const isPit = r === 1 && c === 1;
                            let cellClass = "grid-cell";
                            if (isGoal) cellClass += " goal";
                            if (isPit) cellClass += " pit";
                            if (isAgent) cellClass += " agent";

                            return (
                              <div key={`${r},${c}`} className={cellClass}>
                                <span style={{ fontSize: "0.7rem", color: "#9ca3af" }}>({r},{c})</span>
                                {isAgent && <span>🤖</span>}
                                {isGoal && <span>🏁</span>}
                                {isPit && <span>🔥</span>}
                              </div>
                            );
                          })
                        )}
                      </div>

                      <div style={{ marginTop: "1rem" }}>
                        <strong>Actions: </strong>
                        <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
                          <button className="btn" disabled={labDone} onClick={() => stepLab(0)}>UP</button>
                          <button className="btn" disabled={labDone} onClick={() => stepLab(1)}>RIGHT</button>
                          <button className="btn" disabled={labDone} onClick={() => stepLab(2)}>DOWN</button>
                          <button className="btn" disabled={labDone} onClick={() => stepLab(3)}>LEFT</button>
                          <button className="btn btn-secondary" onClick={resetLab}>Reset Lab</button>
                        </div>
                      </div>
                    </div>

                    <div style={{ flex: 1 }}>
                      <h3>Step Diagnostic Trace</h3>
                      {diagnostic ? (
                        <div className="diagnostic-panel">
                          <div><strong>Transition:</strong> s=({diagnostic.state.join(",")}) -&gt; a={["UP","RIGHT","DOWN","LEFT"][diagnostic.action]} -&gt; r={diagnostic.reward} -&gt; s'=({diagnostic.next_state.join(",")})</div>
                          <hr style={{ borderColor: "#334155", margin: "0.5rem 0" }} />
                          <div>Old Q(s,a): {diagnostic.old_q}</div>
                          <div>Max Next Q(s',a'): {diagnostic.max_next_q}</div>
                          <div>Target = r + &gamma; * max_a' Q(s',a'): {diagnostic.reward} + {diagnostic.gamma} * {diagnostic.max_next_q} = {diagnostic.target}</div>
                          <div>TD Error = Target - Old Q: {diagnostic.target} - {diagnostic.old_q} = {diagnostic.td_error}</div>
                          <div style={{ color: "#38bdf8", fontWeight: "bold" }}>New Q(s,a) = Old Q + &alpha; * TD Error = {diagnostic.old_q} + {diagnostic.alpha} * {diagnostic.td_error} = {diagnostic.new_q}</div>
                        </div>
                      ) : (
                        <p style={{ color: "#9ca3af" }}>Take an action to view step-by-step Q-update diagnostics.</p>
                      )}
                    </div>
                  </div>

                  <div className="q-table-container">
                    <h3>Current Q-Table Matrix</h3>
                    <table>
                      <thead>
                        <tr>
                          <th>State (r,c)</th>
                          <th>0: UP</th>
                          <th>1: RIGHT</th>
                          <th>2: DOWN</th>
                          <th>3: LEFT</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(qTable).map(([stateKey, vals]) => (
                          <tr key={stateKey}>
                            <td>({stateKey})</td>
                            {vals.map((v, idx) => (
                              <td key={idx} style={{ color: v > 0 ? "#34d399" : v < 0 ? "#f87171" : "inherit" }}>
                                {v.toFixed(4)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </section>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
