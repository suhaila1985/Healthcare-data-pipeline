"""
generate_dataset.py
───────────────────
Step 1: Generate a random, clean healthcare dataset.

Usage:
    python scripts/generate_dataset.py              # 200 rows (default)
    python scripts/generate_dataset.py --rows 500   # custom row count
    python scripts/generate_dataset.py --rows 1000 --output data/my_data.csv
"""

import argparse
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_ROWS   = 200
DEFAULT_OUTPUT = "data/simple_healthcare_dataset.csv"
DEFAULT_SEED   = 42

# ── Lookup tables ─────────────────────────────────────────────────────────────
DIAGNOSES = [
    "Hypertension", "Diabetes", "Asthma", "Heart Disease",
    "Injury", "Cancer", "COPD", "Anxiety", "Depression", "Obesity",
]
INSURANCE  = ["Private", "Medicare", "Medicaid", "Uninsured"]
GENDERS    = ["Male", "Female"]
DATE_START = date(2022, 1, 1)
DATE_END   = date(2024, 12, 31)


# ── Helpers ───────────────────────────────────────────────────────────────────

def random_dates(n: int) -> list:
    span = (DATE_END - DATE_START).days
    return [
        (DATE_START + timedelta(days=random.randint(0, span))).strftime("%Y-%m-%d")
        for _ in range(n)
    ]


# ── Main generator ────────────────────────────────────────────────────────────

def generate(n: int = DEFAULT_ROWS, seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """Return a DataFrame of n random patient records."""
    np.random.seed(seed)
    random.seed(seed)

    df = pd.DataFrame({
        "patient_id":     range(1001, 1001 + n),
        "age":            np.random.randint(18, 90, n),
        "gender":         random.choices(GENDERS, k=n),
        "height_cm":      np.round(np.random.normal(168, 9,  n), 1),
        "weight_kg":      np.round(np.random.normal(74,  14, n), 1),
        "temperature":    np.round(np.random.uniform(97.5, 99.5, n), 1),
        "blood_pressure": [
            f"{random.randint(100, 160)}/{random.randint(60, 100)}"
            for _ in range(n)
        ],
        "heart_rate":     np.random.randint(55, 105, n),
        "diagnosis":      random.choices(DIAGNOSES, k=n),
        "length_of_stay": np.random.randint(1, 15, n),
        "admission_date": random_dates(n),
        "insurance_type": random.choices(INSURANCE, k=n),
    })
    return df


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate a random healthcare dataset.")
    parser.add_argument("--rows",   type=int, default=DEFAULT_ROWS,
                        help=f"Number of rows (default: {DEFAULT_ROWS})")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT,
                        help=f"Output CSV path (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--seed",   type=int, default=DEFAULT_SEED,
                        help=f"Random seed (default: {DEFAULT_SEED})")
    args = parser.parse_args()

    df = generate(n=args.rows, seed=args.seed)
    df.to_csv(args.output, index=False)

    print(f"✅ Dataset generated → {args.output}")
    print(f"   Rows: {len(df)}  |  Columns: {len(df.columns)}")
    print(f"   Missing: {df.isnull().sum().sum()}  |  Duplicates: {df.duplicated().sum()}")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
