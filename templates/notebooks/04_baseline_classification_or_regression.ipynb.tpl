{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 04 - Baseline de Classificação ou Regressão\n",
    "\n",
    "Um baseline é um modelo simples que serve como ponto de partida. Ele nos diz o desempenho mínimo que devemos superar com modelos mais complexos.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como criar um modelo simples (ex: Regressão Logística ou Linear).\n",
    "- Como treinar e prever usando a biblioteca Scikit-Learn.\n",
    "- A importância de ter uma métrica de referência.\n",
    "{% else %}\n",
    "# 04 - Baseline Classification or Regression\n",
    "\n",
    "A baseline is a simple model that serves as a starting point. It tells us the minimum performance we should beat with more complex models.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to create a simple model (e.g., Logistic or Linear Regression).\n",
    "- How to train and predict using the Scikit-Learn library.\n",
    "- The importance of having a reference metric.\n",
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
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.dummy import DummyClassifier, DummyRegressor\n",
    "from sklearn.linear_model import LogisticRegression, Ridge\n",
    "\n",
    "if os.getcwd().endswith('notebooks'):\n",
    "    sys.path.append('..')\n",
    "\n",
    "from src.{{PACKAGE_NAME}}.config import load_config\n",
    "from src.{{PACKAGE_NAME}}.data import load_raw_data\n",
    "from src.{{PACKAGE_NAME}}.features import preprocess_features"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 1. Preparar Dados\n",
    "{% else %}\n",
    "## 1. Prepare Data\n",
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
    "X, y = preprocess_features(df)\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 2. Treinar Dummy Baseline\n",
    "\n",
    "O `Dummy` sempre prevê a classe mais frequente ou a média. Se o seu modelo real não for melhor que isso, algo está errado!\n",
    "{% else %}\n",
    "## 2. Train Dummy Baseline\n",
    "\n",
    "The `Dummy` always predicts the most frequent class or the mean. If your real model is not better than this, something is wrong!\n",
    "{% endif %}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "config = load_config()\n",
    "is_classification = config['project']['task'] == 'supervised' # Simplificação\n",
    "\n",
    "if is_classification:\n",
    "    dummy = DummyClassifier(strategy=\"most_frequent\")\n",
    "    model = LogisticRegression()\n",
    "else:\n",
    "    dummy = DummyRegressor(strategy=\"mean\")\n",
    "    model = Ridge()\n",
    "\n",
    "dummy.fit(X_train, y_train)\n",
    "model.fit(X_train, y_train)\n",
    "\n",
    "print(f\"Dummy score: {dummy.score(X_test, y_test):.4f}\")\n",
    "print(f\"Model score: {model.score(X_test, y_test):.4f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Tente usar um modelo de árvore de decisão (`DecisionTreeClassifier` ou `Regressor`).\n",
    "- Verifique se a diferença de performance entre treino e teste indica overfitting.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Try using a decision tree model (`DecisionTreeClassifier` or `Regressor`).\n",
    "- Check if the performance difference between training and testing indicates overfitting.\n",
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
