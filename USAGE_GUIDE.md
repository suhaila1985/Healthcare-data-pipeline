# Usage Guide

---

## Installation

```bash
git clone https://github.com/suhaila1985/healthcare-data-pipeline.git
cd healthcare-data-pipeline
pip install -r requirements.txt
```

---

## Step 1 — Generate a Dataset

```bash
# Default: 200 rows → data/healthcare_dataset.csv
python scripts/generate_dataset.py

# 500 rows with a custom filename
python scripts/generate_dataset.py --rows 500 --output data/my_patients.csv

# Reproducible with a specific seed
python scripts/generate_dataset.py --rows 1000 --seed 7
```

**Import as a function:**
```python
from scripts.generate_dataset import generate

df = generate(n=300)
print(df.head())
```

---

## Step 2 — Clean the Messy Data

```bash
# Default paths
python scripts/clean_data.py

# Custom paths
python scripts/clean_data.py --input data/sample_data_messy.csv --output data/clean.csv
```

**Import as a function:**
```python
from scripts.clean_data import clean

df = clean(
    input_path="data/sample_data_messy.csv",
    output_path="data/clean.csv"
)
```

**What gets fixed:**

| Problem | Fix |
|---------|-----|
| Duplicate rows | Dropped |
| `age = "forty-two"` | Coerced → NaN → filled with median |
| `blood_pressure = "120/80"` | Split into `systolic_bp=120`, `diastolic_bp=80` |
| `admission_date = "15/01/2023"` | Parsed to datetime |
| `temperature = 307.7` | Clipped to 106 |
| `gender = "male"` | Standardised to `M` |
| `insurance_type = "prvt"` | Standardised to `Private` |

---

## Step 3 — Run the Health Report

```bash
# Default: checks data/healthcare_dataset_clean.csv
python scripts/health_report.py

# Custom file
python scripts/health_report.py --input data/clean.csv
```

**Sample output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DATA HEALTH REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  MISSING VALUES
    ✅ No missing values found.

2️⃣  DUPLICATE ROWS
    ✅ No duplicate rows found.

3️⃣  NUMERIC RANGE CHECK
    ✅ All numeric values within valid ranges.

4️⃣  CATEGORICAL CONSISTENCY
    gender         ✅ All values match expected set
    insurance_type ✅ All values match expected set

═══════════════════════════════════════════════════════
  DATA HEALTH SCORE
═══════════════════════════════════════════════════════
  Missing values                 ✅ Pass
  Duplicate rows                 ✅ Pass
  Range violations               ✅ Pass
  Category issues                ✅ Pass

  🟢  EXCELLENT — Data is clean and ready to use.
═══════════════════════════════════════════════════════
```

---

## Run the Full Pipeline

```bash
python scripts/generate_dataset.py
python scripts/clean_data.py --input data/sample_data_messy.csv
python scripts/health_report.py
```

---

## Valid Medical Ranges Reference

| Column | Min | Max |
|--------|-----|-----|
| `age` | 0 | 90 |
| `height_cm` | 100 cm | 200 cm |
| `weight_kg` | 20 kg | 150 kg |
| `temperature` | 95 °F | 106 °F |
| `heart_rate` | 30 bpm | 150 bpm |
| `length_of_stay` | 0 days | 30 days |
| `systolic_bp` | 80 mmHg | 200 mmHg |
| `diastolic_bp` | 40 mmHg | 120 mmHg |
