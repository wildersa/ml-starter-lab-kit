-r requirements.txt
pandas
numpy
scikit-learn
matplotlib
seaborn
{% if LEARNING_ENABLED == "true" or GENERATE_BANDIT == "true" %}
streamlit
{% endif %}
