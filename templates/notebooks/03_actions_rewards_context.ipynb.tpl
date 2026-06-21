{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 03 - Ações, Recompensas e Contexto\n",
    "\n",
    "No aprendizado por bandit, o modelo deve escolher uma **Ação** baseada em um **Contexto** para maximizar uma **Recompensa**.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- A diferença entre o aprendizado supervisionado tradicional e o bandit.\n",
    "- Como identificar ações (arms) e recompensas no seu dataset.\n",
    "- O conceito de política de log (logged policy) e propensão.\n",
    "{% else %}\n",
    "# 03 - Actions, Rewards, and Context\n",
    "\n",
    "In bandit learning, the model must choose an **Action** based on a **Context** to maximize a **Reward**.\n",
    "\n",
    "## What this step teaches:\n",
    "- The difference between traditional supervised learning and bandit learning.\n",
    "- How to identify actions (arms) and rewards in your dataset.\n",
    "- The concept of logged policy and propensity.\n",
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
    "\n",
    "if os.getcwd().endswith('notebooks'):\n",
    "    sys.path.append('..')\n",
    "\n",
    "from src.{{PACKAGE_NAME}}.config import load_config\n",
    "from src.{{PACKAGE_NAME}}.data import load_raw_data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 1. Identificando Braços e Recompensas\n",
    "{% else %}\n",
    "## 1. Identifying Arms and Rewards\n",
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
    "config = load_config()\n",
    "\n",
    "reward_col = config['target'].get('column', 'reward')\n",
    "# Geralmente a ação está em uma coluna específica ou é o que queremos decidir\n",
    "print(f\"Reward column: {reward_col}\")\n",
    "print(f\"Average reward: {df[reward_col].mean():.4f}\")\n",
    "\n",
    "if 'action' in df.columns:\n",
    "    print(\"\\nAction distribution:\")\n",
    "    print(df['action'].value_counts())\n",
    "    \n",
    "    print(\"\\nAverage reward per action:\")\n",
    "    print(df.groupby('action')[reward_col].mean())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Verifique se há viés na coleta de dados (ex: uma ação foi escolhida muito mais vezes que outras).\n",
    "- Identifique quais features contextuais podem influenciar a recompensa de cada ação.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Check for bias in data collection (e.g., one action was chosen much more often than others).\n",
    "- Identify which contextual features might influence the reward for each action.\n",
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
