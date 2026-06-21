{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 04 - Baseline de Agrupamento (Clustering)\n",
    "\n",
    "No agrupamento, queremos encontrar grupos naturais nos dados sem usar rótulos pré-definidos.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como normalizar dados para algoritmos baseados em distância.\n",
    "- Como aplicar o algoritmo K-Means.\n",
    "- Como usar o método do \"Cotovelo\" (Elbow Method) para escolher o número de clusters.\n",
    "{% else %}\n",
    "# 04 - Clustering Baseline\n",
    "\n",
    "In clustering, we want to find natural groups in the data without using predefined labels.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to normalize data for distance-based algorithms.\n",
    "- How to apply the K-Means algorithm.\n",
    "- How to use the \"Elbow Method\" to choose the number of clusters.\n",
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
    "from sklearn.cluster import KMeans\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "import matplotlib.pyplot as plt\n",
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
    "## 1. Escalonamento e K-Means\n",
    "{% else %}\n",
    "## 1. Scaling and K-Means\n",
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
    "\n",
    "scaler = StandardScaler()\n",
    "X_scaled = scaler.fit_transform(X)\n",
    "\n",
    "wcss = []\n",
    "for i in range(1, 11):\n",
    "    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10)\n",
    "    kmeans.fit(X_scaled)\n",
    "    wcss.append(kmeans.inertia_)\n",
    "\n",
    "plt.plot(range(1, 11), wcss)\n",
    "plt.title('Elbow Method')\n",
    "plt.xlabel('Number of clusters')\n",
    "plt.ylabel('WCSS')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Experimente o algoritmo PCA para reduzir a dimensionalidade antes do agrupamento.\n",
    "- Tente outros algoritmos como DBSCAN ou Agrupamento Hierárquico.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Experiment with the PCA algorithm to reduce dimensionality before clustering.\n",
    "- Try other algorithms like DBSCAN or Hierarchical Clustering.\n",
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
