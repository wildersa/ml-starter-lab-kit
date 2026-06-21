{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 02 - Análise Exploratória de Dados (EDA)\n",
    "\n",
    "A EDA é uma etapa crucial onde buscamos entender distribuições, correlações e possíveis problemas de qualidade nos dados (como valores ausentes ou outliers).\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como visualizar a distribuição da variável alvo.\n",
    "- Como identificar valores ausentes.\n",
    "- Como detectar possíveis vazamentos de dados (leakage).\n",
    "{% else %}\n",
    "# 02 - Exploratory Data Analysis (EDA)\n",
    "\n",
    "EDA is a crucial step where we seek to understand distributions, correlations, and potential data quality issues (such as missing values or outliers).\n",
    "\n",
    "## What this step teaches:\n",
    "- How to visualize the target variable distribution.\n",
    "- How to identify missing values.\n",
    "- How to detect potential data leakage.\n",
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
    "import seaborn as sns\n",
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
    "## 1. Distribuição do Alvo\n",
    "{% else %}\n",
    "## 1. Target Distribution\n",
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
    "target = config['target'].get('column')\n",
    "df = load_raw_data()\n",
    "\n",
    "if target and target in df.columns:\n",
    "    plt.figure(figsize=(8, 5))\n",
    "    if df[target].dtype in ['int64', 'float64'] and df[target].nunique() > 10:\n",
    "        sns.histplot(df[target], kde=True)\n",
    "    else:\n",
    "        sns.countplot(data=df, x=target)\n",
    "    plt.title(f\"Distribution of {target}\")\n",
    "    plt.show()\n",
    "else:\n",
    "    print(\"Target column not found or not configured.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 2. Valores Ausentes\n",
    "{% else %}\n",
    "## 2. Missing Values\n",
    "{% endif %}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "missing = df.isnull().sum()\n",
    "missing = missing[missing > 0]\n",
    "if not missing.empty:\n",
    "    print(\"Missing values per column:\")\n",
    "    print(missing)\n",
    "else:\n",
    "    print(\"No missing values detected.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Explore a correlação entre as variáveis usando `df.corr()`.\n",
    "- Crie gráficos de dispersão (scatter plots) para ver a relação entre features e o alvo.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Explore correlations between variables using `df.corr()`.\n",
    "- Create scatter plots to see the relationship between features and the target.\n",
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
