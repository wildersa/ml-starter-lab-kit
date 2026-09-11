import streamlit as st
import pandas as pd
import time
import importlib
import sys
from pathlib import Path

# Setup path for local imports
pkg_dir = Path(__file__).resolve().parent
src_dir = pkg_dir.parent

if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

try:
    module_name = "{{PACKAGE_NAME}}"
    rl_mod = importlib.import_module(f"{module_name}.rl")
    RLRunner = rl_mod.RLRunner
    GridworldToyEnv = rl_mod.GridworldToyEnv
    ToyRLAgent = rl_mod.ToyRLAgent
    StepRecord = rl_mod.StepRecord
except ImportError:
    try:
        from rl import RLRunner, GridworldToyEnv, ToyRLAgent, StepRecord
    except ImportError as e:
        st.error(f"Could not import RL module: {e}")
        st.stop()

# Page config
st.set_page_config(
    page_title="{{PROJECT_NAME}} - Visual RL Workspace",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session State
if "runner" not in st.session_state:
    env = GridworldToyEnv(grid_size=3)
    agent = ToyRLAgent(alpha=0.1, gamma=0.9, epsilon=0.2)
    st.session_state.runner = RLRunner(env, agent)

if "auto_stepping" not in st.session_state:
    st.session_state.auto_stepping = False

if "selected_action" not in st.session_state:
    st.session_state.selected_action = "UP"

runner: RLRunner = st.session_state.runner

st.title("🤖 Reinforcement Learning Workspace & Assisted Training")
st.markdown("""
Interactive visual environment for reinforcement learning.
Inspect state vs. observation, action selection, reward transitions, and agent parameter updates at each step.
""")

# Top Control Bar (Assisted Training Mode)
st.subheader("🕹️ Controls & Assisted Training")
col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([1.5, 1.5, 1.5, 1.5, 2])

with col_ctrl1:
    if st.button("🔄 [ RESET EPISODE ]", use_container_width=True):
        runner.reset_episode()
        st.session_state.auto_stepping = False
        st.rerun()

with col_ctrl2:
    if st.button("➡️ [ STEP ]", use_container_width=True):
        st.session_state.auto_stepping = False
        chosen_act = st.session_state.selected_action
        runner.step(action=chosen_act)
        st.rerun()

with col_ctrl3:
    if st.button("▶️ [ AUTO ]", use_container_width=True):
        st.session_state.auto_stepping = True

with col_ctrl4:
    if st.button("⏸️ [ PAUSE ]", use_container_width=True):
        st.session_state.auto_stepping = False

with col_ctrl5:
    auto_speed = st.slider("Auto Step Delay (s)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

st.divider()

# Main 2-column layout: Left (Environment & Agent), Right (Transition & Theory)
left_col, right_col = st.columns([1, 1])

with left_col:
    # Environment Panel
    st.header("🌍 Environment Panel")

    current_obs = runner.current_obs
    current_state = runner.env.get_state()
    available_actions = runner.env.available_actions(current_obs)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Episode", runner.episode_count)
    m2.metric("Step Number", runner.step_count)
    m3.metric("Cumulative Return", f"{runner.cumulative_return:.2f}")
    status_str = "TERMINATED" if runner.is_terminated else ("TRUNCATED" if runner.is_truncated else "ACTIVE")
    m4.metric("Episode Status", status_str)

    st.markdown("#### Grid World Visualization")
    ascii_grid = runner.env.render_ascii()
    st.code(ascii_grid, language="text")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.info(f"**True State (s)**: `{current_state}`")
    with col_s2:
        st.success(f"**Observation (o)**: `{current_obs}`")

    st.divider()

    # Agent Panel
    st.header("🧠 Agent Panel")

    st.subheader("1. Manual Action Selection")
    st.session_state.selected_action = st.radio(
        "Choose action for next manual step:",
        options=available_actions,
        index=available_actions.index(st.session_state.selected_action) if st.session_state.selected_action in available_actions else 0,
        horizontal=True
    )

    st.subheader("2. Policy Representation P(a|s)")
    policy_dict = runner.agent.get_policy(current_obs, available_actions)
    if policy_dict:
        policy_df = pd.DataFrame([policy_dict], index=[f"State {current_obs}"])
        st.dataframe(policy_df.style.highlight_max(axis=1, color="lightgreen"), use_container_width=True)

    st.subheader("3. Action-Value Table Q(s, a)")
    q_dict = runner.agent.get_q_values(current_obs)
    if q_dict:
        q_df = pd.DataFrame([q_dict], index=[f"State {current_obs}"])
        st.dataframe(q_df, use_container_width=True)

    with st.expander("🛠️ Override Q-Value (Assisted Teaching Mode)"):
        st.caption("Manually adjust Q-values to observe how action selection and policy change immediately.")
        edit_act = st.selectbox("Action to edit", options=available_actions, key="edit_q_act")
        edit_val = st.number_input("New Q-value", value=float(q_dict.get(edit_act, 0.0)), step=0.1, key="edit_q_val")
        if st.button("Apply Q-value Override"):
            runner.agent.set_q_value(current_obs, edit_act, edit_val)
            st.success(f"Updated Q({current_obs}, '{edit_act}') = {edit_val}")
            st.rerun()

with right_col:
    # Transition Panel
    st.header("⚡ Step Transition Panel")

    if runner.history:
        latest_record: StepRecord = runner.history[-1]
        st.markdown(f"**Latest Interaction Step #{latest_record.step} (Episode {latest_record.episode})**")

        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            st.markdown(f"**Before**\n- State: `{latest_record.state_before}`\n- Obs: `{latest_record.observation_before}`")
        with t_col2:
            st.markdown(f"**Action & Reward**\n- Action: `{latest_record.action}`\n- Reward: `{latest_record.reward}`")
        with t_col3:
            st.markdown(f"**After**\n- State: `{latest_record.state_after}`\n- Obs: `{latest_record.observation_after}`")

        st.subheader("Agent Update Diagnostics")
        st.json(latest_record.update_info)
    else:
        st.info("No transitions executed yet in this session. Click **[ STEP ]** to perform the first step.")

    st.divider()

    # Theory & Context Panel
    st.header("💡 Contextual Theory Panel")

    if runner.history:
        rec = runner.history[-1]
        q_old = rec.update_info.get("q_old", 0.0)
        target = rec.update_info.get("target", 0.0)
        td_err = rec.update_info.get("td_error", 0.0)
        q_new = rec.update_info.get("q_new", 0.0)
        st.markdown(
            f"### Step Analysis\n"
            f"- **State vs Observation**: State `{rec.state_before}` was directly observed by agent.\n"
            f"- **Action Selection**: Action **`{rec.action}`** was chosen.\n"
            f"- **Reward Source**: Execution yielded reward **`{rec.reward}`**.\n"
            f"- **Bellman Target & TD Error**:\n"
            f"  - Previous Q-value Q(s, a): `{q_old}`\n"
            f"  - Target r + γ max Q(s', a'): `{target}`\n"
            f"  - TD Error δ: `{td_err}`\n"
            f"  - Updated Q-value Q_new(s, a): `{q_new}`\n"
        )
    else:
        st.markdown(r"""
        ### Reinforcement Learning Basics
        - **State ($s$)**: Full configuration of the environment.
        - **Observation ($o$)**: Information perceived by the agent.
        - **Action ($a$)**: Decision executed by the agent from available choices.
        - **Reward ($r$)**: Scalar feedback returned by the environment.
        - **Return ($G_t$)**: Cumulative discounted sum of future rewards.
        - **Policy ($\pi(a|s)$)**: Agent's decision strategy mapping states to action probabilities.
        """)

st.divider()

# History Panel
st.header("📜 Step History Panel")
if runner.history:
    history_data = [
        {
            "Episode": r.episode,
            "Step": r.step,
            "State Before": str(r.state_before),
            "Obs Before": str(r.observation_before),
            "Action": r.action,
            "Reward": r.reward,
            "State After": str(r.state_after),
            "Obs After": str(r.observation_after),
            "Terminated": r.terminated,
            "Truncated": r.truncated
        }
        for r in runner.history
    ]
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True)

    # Step Inspector
    selected_step_idx = st.selectbox(
        "Inspect specific step from history:",
        options=list(range(len(runner.history))),
        format_func=lambda i: f"Step #{runner.history[i].step} (Episode {runner.history[i].episode}, Action: {runner.history[i].action})"
    )
    st.json(runner.history[selected_step_idx].__dict__)
else:
    st.info("History is currently empty.")

# Auto-stepping loop trigger
if st.session_state.auto_stepping and not runner.is_terminated:
    time.sleep(auto_speed)
    runner.step()
    st.rerun()
