# 🏥 Healthcare Data Pipeline

A beginner-friendly Python toolkit for **generating**, **cleaning**, and **validating** healthcare patient datasets.

---

## 📌 What This Project Does

| Step | Script | Description |
|------|--------|-------------|
| 1️⃣ Generate | `scripts/generate_dataset.py` | Create random realistic patient records |
| 2️⃣ Clean | `scripts/clean_data.py` | Fix types, missing values, outliers, duplicates |
| 3️⃣ Validate | `scripts/health_report.py` | Run a data quality check and score |

---

## 📁 Project Structure

```
healthcare-data-pipeline/
│
├── data/
│   ├── sample_data_messy.csv       ← raw input with intentional issues
│   └── healthcare_dataset_clean.csv← output after cleaning
│
├── scripts/
│   ├── generate_dataset.py         ← Step 1: generate random data
│   ├── clean_data.py               ← Step 2: clean the messy data
│   └── health_report.py            ← Step 3: validate cleaned data
│
├── docs/
│   └── USAGE_GUIDE.md              ← detailed usage examples
│
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🚀 Quick Start

### 1 · Clone the repo
```bash
git clone https://github.com/suhailal1985/healthcare-data-pipeline.git
cd healthcare-data-pipeline
```

### 2 · Install dependencies
```bash
pip install -r requirements.txt
```

### 3 · Generate a dataset
```bash
python scripts/generate_dataset.py
# Output → data/healthcare_dataset.csv
```

### 4 · Clean the messy data
```bash
python scripts/clean_data.py
# Input  → data/sample_data_messy.csv
# Output → data/healthcare_dataset_clean.csv
```

### 5 · Run the health report
```bash
python scripts/health_report.py
# Input → data/healthcare_dataset_clean.csv
```

---

## 📊 Dataset Columns

| Column | Type | Description | Valid Range |
|--------|------|-------------|-------------|
| `patient_id` | int | Unique patient ID | 1000+ |
| `age` | int | Age in years | 0 – 90 |
| `gender` | str | M / F | M, F |
| `height_cm` | float | Height in cm | 100 – 200 |
| `weight_kg` | float | Weight in kg | 20 – 150 |
| `temperature` | float | Body temperature °F | 95 – 106 |
| `blood_pressure` | str | Systolic/Diastolic mmHg | — |
| `heart_rate` | int | Heart rate bpm | 30 – 150 |
| `diagnosis` | str | Primary diagnosis | — |
| `length_of_stay` | int | Days in hospital | 0 – 30 |
| `admission_date` | date | Admission date YYYY-MM-DD | — |
| `insurance_type` | str | Insurance category | Private, Medicare, Medicaid, Uninsured |

---

## 🧹 What the Cleaner Fixes

| Issue | How It's Handled |
|-------|-----------------|
| Duplicate rows | Dropped |
| Wrong data types | Coerced with `pd.to_numeric` / `pd.to_datetime` |
| `blood_pressure` as string | Split into `systolic_bp` + `diastolic_bp` |
| Missing numeric values | Filled with column **median** |
| Missing categorical values | Filled with column **mode** |
| Outliers (e.g. temp = 307) | Clipped to valid medical ranges |
| Inconsistent text (e.g. `prvt`) | Standardised with `.str.title()` + replace map |

---

## 📋 Requirements

```
pandas>=2.0.0
numpy>=1.24.0
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved.

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 👤 Author

**Your Name**
- GitHub: [@suhaila1985](https://github.com/suhaila1985)
