import pandas as pd


def build_quality_report(df):
    """Создаёт отчёт о качестве исходных данных."""

    report = []

    for column in df.columns:
        empty_count = int(df[column].isna().sum())

        if (
            df[column].dtype == "object"
            or isinstance(df[column].dtype, pd.StringDtype)
        ):
            values = df[column].dropna()

            spaces_count = int(
                values.map(
                    lambda value: (
                        isinstance(value, str)
                        and value != value.strip()
                    )
                ).sum()
            )
        else:
            spaces_count = 0

        report.append({
            "Столбец": str(column),
            "Тип данных": str(df[column].dtype),
            "Пустых ячеек": empty_count,
            "Лишних пробелов": spaces_count,
            "Уникальных значений": int(df[column].nunique())
        })

    return pd.DataFrame(report)


def clean_data(
    df,
    remove_duplicates=True,
    trim_spaces=True
):
    """Очищает данные и возвращает результат."""

    cleaned_df = df.copy()

    if trim_spaces:
        text_columns = cleaned_df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in text_columns:
            cleaned_df[column] = cleaned_df[column].map(
                lambda value: (
                    value.strip()
                    if isinstance(value, str)
                    else value
                )
            )

    if remove_duplicates:
        cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df