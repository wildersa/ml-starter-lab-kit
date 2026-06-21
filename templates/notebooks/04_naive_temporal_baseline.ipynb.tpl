{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 04 - Baseline Temporal Ingênuo\n",
    "\n",
    "Em séries temporais, um baseline muito forte é o \"Modelo Ingênuo\" (Naive Model), que prevê que o valor de amanhã será igual ao de hoje.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como criar um modelo de persistência (lagged model).\n",
    "- Como medir o erro de previsão em janelas temporais.\n",
    "- Por que é difícil bater um modelo ingênuo em séries financeiras ou climáticas.\n",
    "{% else %}\n",
    "# 04 - Naive Temporal Baseline\n",
    "\n",
    "In time series, a very strong baseline is the \"Naive Model,\" which predicts that tomorrow's value will be the same as today's.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to create a persistence model (lagged model).\n",
    "- How to measure forecast error over time windows.\n",
    "- Why it is difficult to beat a naive model in financial or weather series.\n",
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
    "from sklearn.metrics import mean_absolute_error\n",
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
    "## 1. Modelo de Persistência (Lag 1)\n",
    "{% else %}\n",
    "## 1. Persistence Model (Lag 1)\n",
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
    "# Assumindo que a primeira coluna numérica é o alvo\n",
    "target_col = df.select_dtypes(include='number').columns[0]\n",
    "\n",
    "df['naive_pred'] = df[target_col].shift(1)\n",
    "\n",
    "valid_df = df.dropna()\n",
    "mae = mean_absolute_error(valid_df[target_col], valid_df['naive_pred'])\n",
    "\n",
    "print(f\"Naive MAE: {mae:.4f}\")\n",
    "\n",
    "plt.figure(figsize=(12, 6))\n",
    "plt.plot(valid_df[target_col].tail(100), label='Actual')\n",
    "plt.plot(valid_df['naive_pred'].tail(100), label='Naive Prediction', linestyle='--')\n",
    "plt.legend()\n",
    "plt.title(\"Actual vs Naive Prediction (Last 100 points)\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Tente usar a média móvel (Moving Average) como um baseline mais suave.\n",
    "- Adicione features de sazonalidade (ex: dia da semana, mês) para melhorar o modelo.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Try using a Moving Average as a smoother baseline.\n",
    "- Add seasonality features (e.g., day of the week, month) to improve the model.\n",
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
