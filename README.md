# DataDoctor

**DataDoctor** is a Python application for analyzing data quality and cleaning CSV and Excel files.

The application helps identify common data issues, remove duplicate rows, trim unnecessary spaces, and export cleaned data and quality reports.

## Features

- **CSV and Excel support** — upload `.csv` and `.xlsx` files.
- **Data quality analysis** — inspect data types, missing values, extra spaces, and unique values.
- **Duplicate detection** — identify duplicate rows.
- **Data cleaning** — remove duplicates and trim leading or trailing spaces.
- **Before-and-after comparison** — compare dataset statistics before and after cleaning.
- **Export cleaned data** — download the result as CSV or Excel.
- **Quality reports** — export an Excel report containing column-level quality information and overall statistics.
- **Automated tests** — verify core data processing functionality.

## Tech Stack

- Python
- Pandas
- Streamlit
- OpenPyXL
- Pytest

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MistaLire/DataDoctor.git
cd DataDoctor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

Start the application:

```bash
python -m streamlit run app.py
```

Streamlit will open the application in your browser.

1. Upload a CSV or Excel file.
2. Review the data preview and quality report.
3. Select the cleaning options you need.
4. Review the cleaned data and compare statistics.
5. Download the cleaned dataset or Excel quality report.

## Running Tests

Run the automated tests with:

```bash
python -m pytest -v
```

## Project Structure

```text
DataDoctor/
├── app.py
├── data_processing.py
├── test_data_processing.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Purpose

DataDoctor was created as a practical Python project to explore data quality analysis, data cleaning, automated testing, and interactive web application development.

## License

No license has been specified yet.