-r requirements.txt
pandas
numpy
scikit-learn
matplotlib
seaborn
xgboost
shap
{% if LEARNING_ENABLED == "true" %}
streamlit
{% else %}
{% if GENERATE_BANDIT == "true" %}
streamlit
{% endif %}
{% endif %}
