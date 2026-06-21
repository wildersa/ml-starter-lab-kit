{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 05 - Interpretação de Clusters\n",
    "\n",
    "Após criar os grupos (clusters), precisamos entender o que cada grupo representa em termos de negócio ou domínio.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como comparar as médias das variáveis entre os clusters.\n",
    "- Como visualizar os grupos (ex: usando PCA 2D).\n",
    "- Como dar um \"nome\" ou perfil para cada cluster.\n",
    "{% else %}\n",
    "# 05 - Cluster Interpretation\n",
    "\n",
    "After creating the groups (clusters), we need to understand what each group represents in terms of business or domain.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to compare variable means across clusters.\n",
    "- How to visualize groups (e.g., using 2D PCA).\n",
    "- How to give a \"name\" or profile to each cluster.\n",
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
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "\n",
    "if os.getcwd().endswith('notebooks'):\n",
    "    sys.path.append('..')\n",
    "\n",
    "from src.{{PACKAGE_NAME}}.data import load_raw_data\n",
    "from src.{{PACKAGE_NAME}}.features import preprocess_features"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## 1. Perfil dos Clusters\n",
    "{% else %}\n",
    "## 1. Cluster Profiling\n",
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
    "X, _ = preprocess_features(df)\n",
    "scaler = StandardScaler()\n",
    "X_scaled = scaler.fit_transform(X)\n",
    "\n",
    "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
    "df['cluster'] = kmeans.fit_predict(X_scaled)\n",
    "\n",
    "cluster_summary = df.groupby('cluster').mean(numeric_only=True)\n",
    "display(cluster_summary)\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "sns.heatmap(cluster_summary.T, cmap='YlGnBu', annot=True)\n",
    "plt.title(\"Feature Means per Cluster (Standardized)\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Tente usar gráficos de radar (spider charts) para comparar os clusters.\n",
    "- Verifique se os clusters são estáveis mudando a semente (random_state) do K-Means.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Try using radar charts (spider charts) to compare clusters.\n",
    "- Check if the clusters are stable by changing the seed (random_state) of K-Means.\n",
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
