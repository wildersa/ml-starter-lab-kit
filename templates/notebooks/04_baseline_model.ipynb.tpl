{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 04 - Modelo Baseline\n",
    "\n",
    "Um baseline é um modelo simples que serve como ponto de partida. Ele nos diz o desempenho mínimo que devemos superar com modelos mais complexos.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como criar um modelo simples.\n",
    "- Como treinar e prever.\n",
    "- A importância de ter uma métrica de referência.\n",
    "{% else %}\n",
    "# 04 - Baseline Model\n",
    "\n",
    "A baseline is a simple model that serves as a starting point. It tells us the minimum performance we should beat with more complex models.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to create a simple model.\n",
    "- How to train and predict.\n",
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
    "\n",
    "print(\"Ready for modeling\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Implemente o treinamento de um modelo simples (ex: Scikit-Learn).\n",
    "- Meça o tempo de treinamento e de inferência.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Implement training for a simple model (e.g., Scikit-Learn).\n",
    "- Measure training and inference time.\n",
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
