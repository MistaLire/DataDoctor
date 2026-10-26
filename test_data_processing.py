import pandas as pd

from data_processing import build_quality_report, clean_data


def test_remove_duplicates():
    df = pd.DataFrame({
        "Имя": ["Анна", "Анна", "Иван"],
        "Возраст": [20, 20, 25]
    })

    result = clean_data(df, remove_duplicates=True)

    assert len(result) == 2


def test_trim_spaces():
    df = pd.DataFrame({
        "Имя": [" Анна ", "Иван "]
    })

    result = clean_data(df, trim_spaces=True)

    assert result["Имя"].tolist() == ["Анна", "Иван"]


def test_keep_duplicates_when_disabled():
    df = pd.DataFrame({
        "Имя": ["Анна", "Анна"]
    })

    result = clean_data(df, remove_duplicates=False)

    assert len(result) == 2


def test_quality_report_counts_empty_cells():
    df = pd.DataFrame({
        "Имя": ["Анна", None, "Иван"],
        "Возраст": [20, 25, None]
    })

    report = build_quality_report(df)

    assert report["Пустых ячеек"].sum() == 2


def test_quality_report_counts_extra_spaces():
    df = pd.DataFrame({
        "Имя": [" Анна ", "Иван", "Пётр "]
    })

    report = build_quality_report(df)

    assert report.loc[0, "Лишних пробелов"] == 2