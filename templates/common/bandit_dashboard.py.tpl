import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys

# Setup path for local imports
# We expect to be in src/{{PACKAGE_NAME}}/bandit_dashboard.py
pkg_dir = Path(__file__).resolve().parent
src_dir = pkg_dir.parent

if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

try:
    from .core.config import project_root
except ImportError:
    try:
        from core.config import project_root
    except ImportError:
        # Fallback if not in package structure
        def project_root():
            return Path(__file__).resolve().parents[2]

# Page config
st.set_page_config(
    page_title="{{PROJECT_NAME}} - Bandit Lab Dashboard",
    page_icon="🎰",
    layout="wide"
)

def main():
    lang = "{{LANGUAGE}}"

    translations = {
        "en": {
            "title": "🎰 {{PROJECT_NAME}} - Bandit Lab Dashboard",
            "summary": "Summary Metrics",
            "history": "Simulation History",
            "cumulative_reward": "Cumulative Reward",
            "cumulative_regret": "Cumulative Regret",
            "arm_selection": "Arm Selection Counts",
            "missing_data": "No Bandit Lab results found.",
            "run_instruction": "Please run the Bandit Lab simulation first:",
            "round": "Round",
            "policy": "Policy",
            "reward": "Reward",
            "regret": "Regret",
            "total_reward": "Total Reward",
            "avg_reward": "Average Reward",
            "best_arm_rate": "Best Arm Rate",
        },
        "pt-BR": {
            "title": "🎰 {{PROJECT_NAME}} - Dashboard do Bandit Lab",
            "summary": "Métricas de Resumo",
            "history": "Histórico da Simulação",
            "cumulative_reward": "Recompensa Acumulada",
            "cumulative_regret": "Regret Acumulado",
            "arm_selection": "Contagem de Escolha dos Arms",
            "missing_data": "Resultados do Bandit Lab não encontrados.",
            "run_instruction": "Por favor, execute a simulação do Bandit Lab primeiro:",
            "round": "Rodada",
            "policy": "Política",
            "reward": "Recompensa",
            "regret": "Regret",
            "total_reward": "Recompensa Total",
            "avg_reward": "Recompensa Média",
            "best_arm_rate": "Taxa de Melhor Arm",
        }
    }

    t = translations.get(lang, translations["en"])

    st.title(t["title"])

    root = project_root()
    results_path = root / "configs/bandit_results.json"
    history_path = root / "reports/bandit-history.csv"

    if not results_path.exists() or not history_path.exists():
        st.warning(t["missing_data"])
        st.info(t["run_instruction"])
        st.code(f"python -m {{PACKAGE_NAME}}.lab bandit")
        return

    # Load results
    try:
        with open(results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        st.error(f"Error loading results: {e}")
        return

    # Summary section
    st.header(t["summary"])

    policies = list(results.keys())
    cols = st.columns(len(policies))

    for i, policy in enumerate(policies):
        with cols[i]:
            st.subheader(policy.replace("_", " ").title())
            metrics = results[policy]
            st.metric(t["total_reward"], metrics["total_reward"])
            st.metric(t["avg_reward"], metrics["average_reward"])
            st.metric(t["regret"], metrics["cumulative_regret"])
            st.metric(t["best_arm_rate"], f"{metrics['best_arm_selection_rate']*100:.1f}%")

    # Visualizations
    st.header(t["history"])

    try:
        df = pd.read_csv(history_path)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(t["cumulative_reward"])
            # Reshape for plotting: index=round, columns=policy, values=cumulative_reward
            reward_df = df.pivot(index="round", columns="policy", values="cumulative_reward")
            st.line_chart(reward_df)

        with col2:
            st.subheader(t["cumulative_regret"])
            regret_df = df.pivot(index="round", columns="policy", values="cumulative_regret")
            st.line_chart(regret_df)

        st.subheader(t["arm_selection"])
        # Group by policy and selected_arm to get counts
        arm_counts = df.groupby(["policy", "selected_arm"]).size().reset_index(name="count")
        # Pivot for bar chart
        arm_pivot = arm_counts.pivot(index="selected_arm", columns="policy", values="count").fillna(0)
        st.bar_chart(arm_pivot)

    except Exception as e:
        st.error(f"Error loading history: {e}")

if __name__ == "__main__":
    main()
