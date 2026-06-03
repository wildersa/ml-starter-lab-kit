
from src.sample_ml_project.features import add_ratio_feature


def test_add_ratio_feature():
    rows = [
        {"a": "10", "b": "2"},
        {"a": "10", "b": "0"},
    ]

    result = add_ratio_feature(rows, name="a_por_b", numerator="a", denominator="b")

    assert result[0]["a_por_b"] == 5
    assert result[1]["a_por_b"] is None
