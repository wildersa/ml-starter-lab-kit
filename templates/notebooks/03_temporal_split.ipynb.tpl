{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 03 - Divisão Temporal\n",
    "\n",
    "Em séries temporais, não podemos usar uma divisão aleatória (random split), pois isso causaria vazamento de dados do futuro para o passado.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Por que a ordem cronológica importa.\n",
    "- Como dividir os dados em treino e teste mantendo a ordem do tempo.\n",
    "- Como visualizar a divisão temporal.\n",
    "{% else %}\n",
    "# 03 - Temporal Split\n",
    "\n",
    "In time series, we cannot use a random split, as that would cause data leakage from the future into the past.\n",
    "\n",
    "## What this step teaches:\n",
    "- Why chronological order matters.\n",
    "- How to split data into training and testing sets while maintaining time order.\n",
    "- How to visualize the temporal split.\n",
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
    "import matplotlib.pyplot as plt\n",
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
    "## 1. Carregar Dados e Ordenar por Tempo\n",
    "{% else %}\n",
    "## 1. Load Data and Sort by Time\n",
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
    "# Assumindo que existe uma coluna de data\n",
    "date_col = load_config().get('eda', {}).get('date_columns', [None])[0]\n",
    "\n",
    "if date_col and date_col in df.columns:\n",
    "    df[date_col] = pd.to_datetime(df[date_col])\n",
    "    df = df.sort_values(date_col)\n",
    "    print(f\"Sorted by {date_col}\")\n",
    "else:\n",
    "    print(\"Date column not found. Using index as proxy for time.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 2. Divisão Treino/Teste\n",
    "{% else %}\n",
    "## 2. Train/Test Split\n",
    "{% endif %}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "split_idx = int(len(df) * 0.8)\n",
    "train = df.iloc[:split_idx]\n",
    "test = df.iloc[split_idx:]\n",
    "\n",
    "print(f\"Training rows: {len(train)}\")\n",
    "print(f\"Test rows: {len(test)}\")\n",
    "\n",
    "plt.figure(figsize=(12, 6))\n",
    "plt.plot(train.index, [1]*len(train), '|', label='Train')\n",
    "plt.plot(test.index, [1]*len(test), '|', label='Test')\n",
    "plt.title(\"Temporal Split Visualization\")\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Experimente diferentes pontos de corte para o teste.\n",
    "- Verifique se existem janelas de tempo sem dados (gaps).\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Experiment with different split points for testing.\n",
    "- Check for time windows without data (gaps).\n",
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
