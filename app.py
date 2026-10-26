from io import BytesIO

import pandas as pd
import streamlit as st

from data_processing import build_quality_report, clean_data


# -------------------- НАСТРОЙКИ --------------------

st.set_page_config(
    page_title="DataDoctor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------- ДИЗАЙН --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #172554 0%, transparent 40%),
        #708090;
    color: #708090;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: #f8fafc !important;
    font-family: 'Inter', sans-serif !important;
}

p, label {
    color: #aab6ca;
}

.hero {
    padding: 30px 34px;
    border: 1px solid #263653;
    border-radius: 24px;
    background: linear-gradient(120deg, #131e35, #10182a 65%, #102b36);
    margin-bottom: 28px;
}

.brand {
    font-size: 14px;
    color: #5eead4;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.hero-title {
    font-size: clamp(30px, 4vw, 45px);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #f8fafc;
    margin-bottom: 14px;
}

.hero-title span {
    color: #5eead4;
}

.hero-description {
    font-size: 15px;
    line-height: 1.8;
    max-width: 680px;
    color: #aab6ca;
}

.section-heading {
    font-size: 21px;
    font-weight: 700;
    color: #f1f5f9;
    margin-top: 30px;
    margin-bottom: 6px;
}

.section-description {
    font-size: 13px;
    color: #000000;
    margin-bottom: 18px;
}

div[data-testid="stFileUploader"] {
    border: 1px dashed #000000;
    background: #101a2b;
    padding: 18px;
    border-radius: 18px;
}

div[data-testid="stFileUploader"] section {
    background: transparent;
}

div[data-testid="stFileUploader"] button {
    background: #ffffff;
    color: #000000;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

div[data-testid="stFileUploader"] button:hover {
    background: #7CFC00;
    color: #6B8E23;
}

.metric-card {
    background: linear-gradient(145deg, #151f33, #101827);
    border: 1px solid #28364d;
    border-radius: 17px;
    padding: 20px;
    min-height: 125px;
    margin-bottom: 12px;
}

.metric-label {
    color: #91a1b8;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 13px;
}

.metric-value {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1px;
}

.metric-note {
    color: #5eead4;
    font-size: 11px;
    margin-top: 8px;
}

.panel {
    background: #111a2a;
    border: 1px solid #28364d;
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #29384f;
    border-radius: 14px;
    overflow: hidden;
}

.stDownloadButton button {
    width: 100%;
    min-height: 46px;
    border-radius: 12px;
    border: 1px solid #37536b;
    background: #15273a;
    color: #e2e8f0;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stDownloadButton button:hover {
    border-color: #5eead4;
    background: #1b3947;
    color: #99f6e4;
}

.stButton button {
    border-radius: 10px;
}

div[data-testid="stCheckbox"] label {
    color: #dbe4f0;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

.footer {
    border-top: 1px solid #26344a;
    margin-top: 45px;
    padding-top: 20px;
    color: #708099;
    font-size: 12px;
    text-align: center;
}

div[data-testid="stCaptionContainer"] {
    color: #8493aa;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 22px;
    }

    .metric-value {
        font-size: 25px;
    }
}

</style>
""", unsafe_allow_html=True)


# -------------------- ШАПКА --------------------

st.markdown("""
<div class="hero">
    <div class="brand">DATADOCTOR / DATA QUALITY TOOL</div>
    <div class="hero-title">
        Приведи свои данные<br>
        в <span>идеальный порядок.</span>
    </div>
    <div class="hero-description">
        Проверяй CSV и Excel, находи ошибки, удаляй дубликаты
        и лишние пробелы. Получай чистые данные и подробный
        отчёт о качестве в несколько кликов.
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- ЗАГРУЗКА --------------------

st.markdown(
    '<div class="section-heading">01 / Загрузка данных</div>'
    '<div class="section-description">'
    'Выбери файл, который хочешь проверить и очистить.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Перетащи файл сюда или нажми кнопку выбора",
    type=["csv", "xlsx"],
    help="Поддерживаются CSV и Excel (.xlsx)."
)


if uploaded_file is not None:
    try:
        # Чтение файла
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            try:
                df = pd.read_csv(
                    uploaded_file,
                    sep=None,
                    engine="python",
                    encoding="utf-8-sig"
                )
            except UnicodeDecodeError:
                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    sep=None,
                    engine="python",
                    encoding="cp1251"
                )

        # Проверка наличия данных
        if df.empty or df.dropna(how="all").empty:
            st.warning(
                "Файл пустой или не содержит данных для обработки."
            )
            st.stop()

        # -------------------- ИСХОДНЫЕ ДАННЫЕ --------------------

        st.markdown(
            '<div class="section-heading">02 / Обзор файла</div>'
            '<div class="section-description">'
            'Предварительный просмотр исходных данных.'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(f"Загружен файл: {uploaded_file.name}")

        st.dataframe(
            df.head(100),
            use_container_width=True,
            hide_index=True
        )

        # -------------------- СТАТИСТИКА --------------------

        st.markdown(
            '<div class="section-heading">03 / Качество данных</div>'
            '<div class="section-description">'
            'Основные показатели исходного файла.'
            '</div>',
            unsafe_allow_html=True
        )

        duplicates = int(df.duplicated().sum())
        missing = int(df.isna().sum().sum())

        metrics = [
            ("СТРОК", f"{len(df):,}", "Количество записей"),
            ("СТОЛБЦОВ", f"{len(df.columns):,}", "Полей в таблице"),
            ("ДУБЛИКАТОВ", f"{duplicates:,}", "Повторяющихся строк"),
            ("ПУСТЫХ ЯЧЕЕК", f"{missing:,}", "Не заполнено")
        ]

        metric_columns = st.columns(4)

        for column, metric in zip(metric_columns, metrics):
            label, value, note = metric

            with column:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                        <div class="metric-note">{note}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -------------------- ОТЧЁТ --------------------

        st.markdown(
            '<div class="section-heading">04 / Отчёт по столбцам</div>'
            '<div class="section-description">'
            'Найди проблемные поля до начала очистки.'
            '</div>',
            unsafe_allow_html=True
        )

        report_df = build_quality_report(df)

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True
        )

        # Общая статистика для экспорта
        summary_df = pd.DataFrame({
            "Показатель": [
                "Количество строк",
                "Количество столбцов",
                "Дубликатов строк",
                "Пустых ячеек"
            ],
            "Значение": [
                len(df),
                len(df.columns),
                duplicates,
                missing
            ]
        })

        report_buffer = BytesIO()

        with pd.ExcelWriter(
            report_buffer,
            engine="openpyxl"
        ) as writer:
            report_df.to_excel(
                writer,
                index=False,
                sheet_name="Качество данных"
            )

            summary_df.to_excel(
                writer,
                index=False,
                sheet_name="Общая статистика"
            )

        # -------------------- ОЧИСТКА --------------------

        st.markdown(
            '<div class="section-heading">05 / Очистка</div>'
            '<div class="section-description">'
            'Выбери, какие проблемы необходимо исправить.'
            '</div>',
            unsafe_allow_html=True
        )

        option_column, info_column = st.columns([1, 1])

        with option_column:
            st.markdown('<div class="panel">', unsafe_allow_html=True)

            remove_duplicates = st.checkbox(
                "Удалить повторяющиеся строки",
                value=True
            )

            trim_spaces = st.checkbox(
                "Убрать лишние пробелы",
                value=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with info_column:
            st.markdown("""
            <div class="panel">
                <div style="color:#5eead4;font-weight:700;
                            margin-bottom:12px;">
                    КАК ЭТО РАБОТАЕТ
                </div>
                <div style="color:#aab6ca;font-size:13px;
                            line-height:1.9;">
                    • Исходный файл остаётся без изменений.<br>
                    • Очистка выполняется по выбранным правилам.<br>
                    • Результат можно скачать в CSV или Excel.
                </div>
            </div>
            """, unsafe_allow_html=True)

        cleaned_df = clean_data(
            df,
            remove_duplicates=remove_duplicates,
            trim_spaces=trim_spaces
        )

        # -------------------- РЕЗУЛЬТАТ --------------------

        st.markdown(
            '<div class="section-heading">06 / Результат</div>'
            '<div class="section-description">'
            'Сравни количество записей до и после очистки.'
            '</div>',
            unsafe_allow_html=True
        )

        result_col1, result_col2, result_col3 = st.columns(3)

        result_col1.metric(
            "До очистки",
            len(df)
        )

        result_col2.metric(
            "После очистки",
            len(cleaned_df)
        )

        result_col3.metric(
            "Удалено строк",
            len(df) - len(cleaned_df)
        )

        st.dataframe(
            cleaned_df,
            use_container_width=True,
            hide_index=True
        )

        # -------------------- СКАЧИВАНИЕ --------------------

        st.markdown(
            '<div class="section-heading">07 / Экспорт</div>'
            '<div class="section-description">'
            'Скачай очищенные данные или отдельный отчёт.'
            '</div>',
            unsafe_allow_html=True
        )

        csv_data = cleaned_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:
            cleaned_df.to_excel(
                writer,
                index=False,
                sheet_name="Очищенные данные"
            )

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            st.download_button(
                label="Скачать очищенные данные · Excel",
                data=excel_buffer.getvalue(),
                file_name="cleaned_data.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        with download_col2:
            st.download_button(
                label="Скачать отчёт о качестве · Excel",
                data=report_buffer.getvalue(),
                file_name="data_quality_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        st.download_button(
            label="Скачать очищенные данные · CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as error:
        st.error(
            f"Не удалось обработать файл: {error}"
        )


# -------------------- ПОДВАЛ --------------------

st.markdown("""
<div class="footer">
    DATADOCTOR · DATA QUALITY MADE SIMPLE
</div>
""", unsafe_allow_html=True)