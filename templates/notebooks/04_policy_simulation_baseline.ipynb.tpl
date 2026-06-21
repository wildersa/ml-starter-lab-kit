{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 04 - Baseline de Simulação de Política\n",
    "\n",
    "Em Bandit, avaliamos o desempenho simulando o que teria acontecido se usássemos uma política diferente daquela que coletou os dados (Off-policy Evaluation).\n",
    "\n",
    "## O que este passo ensina:\n",
    "- O conceito de política Aleatória (Random Policy).\n",
    "- Como estimar a recompensa esperada de uma nova política.\n",
    "- Por que não podemos simplesmente usar a acurácia para avaliar um Bandit.\n",
    "{% else %}\n",
    "# 04 - Policy Simulation Baseline\n",
    "\n",
    "In Bandit, we evaluate performance by simulating what would have happened if we used a policy different from the one that collected the data (Off-policy Evaluation).\n",
    "\n",
    "## What this step teaches:\n",
    "- The concept of a Random Policy.\n",
    "- How to estimate the expected reward of a new policy.\n",
    "- Why we cannot simply use accuracy to evaluate a Bandit.\n",
    "{% endif %}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import sys\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "if os.getcwd().endswith('notebooks'):\n",
    "    sys.path.append('..')\n",
    "\n",
    "from src.{{PACKAGE_NAME}}.data import load_raw_data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 1. Estimativa de Recompensa (Random Baseline)\n",
    "{% else %}\n",
    "## 1. Reward Estimation (Random Baseline)\n",
    "{% endif %}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = load_raw_data()\n",
    "reward_col = 'reward' if 'reward' in df.columns else df.select_dtypes(include='number').columns[0]\n",
    "\n",
    "print(f\"Logged policy average reward: {df[reward_col].mean():.4f}\")\n",
    "\n",
    "if 'action' in df.columns:\n",
    "    # Simulação simplificada (Rejection Sampling)\n",
    "    num_arms = df['action'].nunique()\n",
    "    random_reward = []\n",
    "    for _ in range(10):\n",
    "        # Sorteamos uma ação aleatória para cada linha\n",
    "        simulated_actions = np.random.choice(df['action'].unique(), size=len(df))\n",
    "        # Apenas as linhas onde a ação sorteada coincide com a coletada\n",
    "        matched = df[df['action'] == simulated_actions]\n",
    "        random_reward.append(matched[reward_col].mean())\n",
    "    \n",
    "    print(f\"Simulated Random Policy average reward: {np.mean(random_reward):.4f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Implemente uma política \"Epsilon-Greedy\" simples.\n",
    "- Estude o método IPW (Inverse Probability Weighting) para uma avaliação off-policy mais robusta.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Implement a simple \"Epsilon-Greedy\" policy.\n",
    "- Study the IPW (Inverse Probability Weighting) method for more robust off-policy evaluation.\n",
    "{% endif %}"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
