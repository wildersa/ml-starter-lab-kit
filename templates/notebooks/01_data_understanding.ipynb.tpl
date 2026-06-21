{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 01 - Entendimento de Dados\n",
    "\n",
    "Neste notebook, vamos focar em carregar os dados e fazer uma primeira inspeção técnica. O objetivo é garantir que os dados estão acessíveis e entender sua estrutura básica.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como carregar arquivos CSV em Python.\n",
    "- Como verificar o tamanho e as colunas do dataset.\n",
    "- Como identificar o tipo de dado em cada coluna.\n",
    "{% else %}\n",
    "# 01 - Data Understanding\n",
    "\n",
    "In this notebook, we will focus on loading the data and performing a first technical inspection. The goal is to ensure the data is accessible and to understand its basic structure.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to load CSV files in Python.\n",
    "- How to check the size and columns of the dataset.\n",
    "- How to identify the data type in each column.\n",
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
    "from pathlib import Path\n",
    "\n",
    "# Ensure we can import from src\n",
    "if os.getcwd().endswith('notebooks'):\n",
    "    sys.path.append('..')\n",
    "\n",
    "from src.{{PACKAGE_NAME}}.config import load_config, project_root\n",
    "from src.{{PACKAGE_NAME}}.data import load_raw_data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 1. Carregar Configuração e Dados\n",
    "\n",
    "Vamos usar as funções reutilizáveis definidas no pacote `src/{{PACKAGE_NAME}}`.\n",
    "{% else %}\n",
    "## 1. Load Configuration and Data\n",
    "\n",
    "We will use the reusable functions defined in the `src/{{PACKAGE_NAME}}` package.\n",
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
    "print(f\"Project: {config['project']['name']}\")\n",
    "\n",
    "try:\n",
    "    df = load_raw_data()\n",
    "    print(f\"Rows: {len(df)}\")\n",
    "    print(f\"Columns: {len(df.columns)}\")\n",
    "except Exception as e:\n",
    "    print(f\"Error loading data: {e}\")\n",
    "    print(\"Make sure your dataset is at the path defined in configs/config.json\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 2. Inspeção de Colunas\n",
    "\n",
    "Quais são os nomes das colunas e que tipos de valores elas contêm?\n",
    "{% else %}\n",
    "## 2. Column Inspection\n",
    "\n",
    "What are the column names and what types of values do they contain?\n",
    "{% endif %}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if 'df' in locals():\n",
    "    print(df.info())\n",
    "    display(df.head())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## Interpretação\n",
    "- As colunas carregadas correspondem ao que você esperava?\n",
    "- Existem colunas que parecem ser IDs ou datas?\n",
    "\n",
    "## Próximo Passo:\n",
    "No próximo notebook, faremos uma Análise Exploratória de Dados (EDA) mais profunda.\n",
    "{% else %}\n",
    "## Interpretation\n",
    "- Do the loaded columns match what you expected?\n",
    "- Are there columns that appear to be IDs or dates?\n",
    "\n",
    "## Next Step:\n",
    "In the next notebook, we will perform a deeper Exploratory Data Analysis (EDA).\n",
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
