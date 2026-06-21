{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "# 05 - Avaliação e Interpretação\n",
    "\n",
    "Avaliar um modelo vai além de uma única métrica. Precisamos entender onde o modelo erra e quais variáveis são mais importantes.\n",
    "\n",
    "## O que este passo ensina:\n",
    "- Como ler uma Matriz de Confusão ou analisar Resíduos.\n",
    "- Como calcular métricas como Precisão, Recall ou RMSE.\n",
    "- Como extrair a Importância das Variáveis (Feature Importance).\n",
    "{% else %}\n",
    "# 05 - Evaluation and Interpretation\n",
    "\n",
    "Evaluating a model goes beyond a single metric. We need to understand where the model fails and which variables are most important.\n",
    "\n",
    "## What this step teaches:\n",
    "- How to read a Confusion Matrix or analyze Residuals.\n",
    "- How to calculate metrics like Precision, Recall, or RMSE.\n",
    "- How to extract Feature Importance.\n",
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
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor\n",
    "from sklearn.metrics import classification_report, mean_squared_error\n",
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
    "## 1. Treinar Modelo Real e Avaliar\n",
    "{% else %}\n",
    "## 1. Train Real Model and Evaluate\n",
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
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "\n",
    "config = load_config()\n",
    "is_classification = config['project']['task'] == 'supervised' # Simplificação\n",
    "\n",
    "if is_classification:\n",
    "    model = RandomForestClassifier(n_estimators=100, random_state=42)\n",
    "    model.fit(X_train, y_train)\n",
    "    y_pred = model.predict(X_test)\n",
    "    print(classification_report(y_test, y_pred))\n",
    "else:\n",
    "    model = RandomForestRegressor(n_estimators=100, random_state=42)\n",
    "    model.fit(X_train, y_train)\n",
    "    y_pred = model.predict(X_test)\n",
    "    print(f\"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.4f}\")\n",
    "\n",
    "importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)\n",
    "importances.head(10).plot(kind='barh')\n",
    "plt.title(\"Top 10 Feature Importances\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "{% if LANGUAGE == \"pt-BR\" %}\n",
    "## O que tentar a seguir:\n",
    "- Use a biblioteca `SHAP` para uma interpretação mais profunda das predições.\n",
    "- Verifique em quais exemplos específicos o modelo mais erra.\n",
    "{% else %}\n",
    "## What to try next:\n",
    "- Use the `SHAP` library for a deeper interpretation of predictions.\n",
    "- Check which specific examples the model misses the most.\n",
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
