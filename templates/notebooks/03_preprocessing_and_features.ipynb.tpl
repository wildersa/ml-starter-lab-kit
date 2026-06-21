{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 03 - Pré-processamento e Features\n",
    "\n",
    "Nesta etapa, transformamos os dados brutos em um formato adequado para o modelo de Machine Learning.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como lidar com valores ausentes (imputação).\n",
    "- Como codificar variáveis categóricas.\n",
    "- Como criar novas variáveis (Feature Engineering).\n",
    "{% else %}\n",
    "# 03 - Preprocessing and Features\n",
    "\n",
    "In this step, we transform the raw data into a format suitable for the Machine Learning model.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to handle missing values (imputation).\n",
    "- How to encode categorical variables.\n",
    "- How to create new variables (Feature Engineering).\n",
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
    "from src.{{PACKAGE_NAME}}.data import load_raw_data\n",
    "from src.{{PACKAGE_NAME}}.features import preprocess_features"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 1. Aplicar Pré-processamento\n",
    "\n",
    "Vamos usar a função `preprocess_features` definida em `src/{{PACKAGE_NAME}}/features.py`.\n",
    "{% else %}\n",
    "## 1. Apply Preprocessing\n",
    "\n",
    "We will use the `preprocess_features` function defined in `src/{{PACKAGE_NAME}}/features.py`.\n",
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
    "print(f\"Features shape: {X.shape}\")\n",
    "if y is not None:\n",
    "    print(f\"Target shape: {y.shape}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Abra `src/{{PACKAGE_NAME}}/features.py` e adicione uma nova transformação.\n",
    "- Tente criar uma feature de interação (ex: multiplicando duas colunas numéricas).\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Open `src/{{PACKAGE_NAME}}/features.py` and add a new transformation.\n",
    "- Try creating an interaction feature (e.g., multiplying two numeric columns).\n",
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
