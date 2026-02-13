"""
clean_data.py
─────────────
Step 2: Clean a messy healthcare CSV.

Fixes:
  • Duplicate rows
  • Wrong / mixed data types
  • blood_pressure string → systolic_bp + diastolic_bp (float)
  • admission_date → datetime
  • Missing values (numeric → median, categorical → mode)
  • Outliers clipped to valid medical ranges
  • Inconsistent text (whitespace, casing, abbreviations)

Usage:
    python scripts/clean_data.py
    python scripts/clean_data.py --input data/sample_data_messy.csv --output data/clean.csv
"""

import argparse

import numpy as np
import pandas as pd

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_INPUT  = "data/sample_data_messy.csv"
DEFAULT_OUTPUT = "data/healthcare_dataset_clean.csv"

# ── Valid medical ranges for clipping ─────────────────────────────────────────
CLIP_RANGES = {
    "age":            (0,   90),
    "height_cm":      (100, 200),
    "weight_kg":      (20,  150),
    "temperature":    (95,  106),
    "heart_rate":     (30,  150),
    "length_of_stay": (0,   30),
    "systolic_bp":    (80,  200),
    "diastolic_bp":   (40,  120),
}

# ── Text standardisation maps ─────────────────────────────────────────────────
GENDER_MAP = {
    "Male": "M", "Female": "F", "M": "M", "F": "F",
    "male": "M", "female": "F", "MALE": "M", "FEMALE": "F",
    "1": "U", "2": "U", "X": "U", "Unknown": "U",
}
INSURANCE_MAP = {
    "Prvt": "Private", "prvt": "Private",
    "Med":  "Medicare", "med": "Medicare",
    "None": "Uninsured", "NA": "Uninsured", "nan": "Uninsured",
}


# ── Pipeline steps ────────────────────────────────────────────────────────────

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    print(f"  [2] Duplicates removed   : {before - len(df)}")
    return df


def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    # Integer columns
    for col in ["patient_id", "age", "heart_rate", "length_of_stay"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Float columns
    for col in ["height_cm", "weight_kg", "temperature"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # blood_pressure → split into systolic / diastolic
    df["blood_pressure"] = df["blood_pressure"].astype(str)
    bp = df["blood_pressure"].str.extract(r"(\d+\.?\d*)/?(\d+\.?\d*)?")
    df["systolic_bp"]  = pd.to_numeric(bp[0], errors="coerce")
    df["diastolic_bp"] = pd.to_numeric(bp[1], errors="coerce")
    df = df.drop(columns=["blood_pressure"])

    # Dates
    df["admission_date"] = pd.to_datetime(df["admission_date"], errors="coerce")

    # insurance_type: clean string 'nan' → real NaN
    df["insurance_type"] = df["insurance_type"].replace({"nan": np.nan})

    print("  [3] Data types fixed")
    return df


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols     = ["age", "height_cm", "weight_kg", "temperature",
                        "heart_rate", "length_of_stay", "systolic_bp", "diastolic_bp"]
    categorical_cols = ["gender", "diagnosis", "insurance_type", "admission_date"]

    for col in numeric_cols:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        if col in df.columns and df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    remaining = df.isnull().sum().sum()
    print(f"  [4] Missing values filled  (remaining: {remaining})")
    return df


def clip_outliers(df: pd.DataFrame) -> pd.DataFrame:
    for col, (lo, hi) in CLIP_RANGES.items():
        if col in df.columns:
            df[col] = df[col].clip(lo, hi)
    print("  [5] Outliers clipped to valid ranges")
    return df


def standardise_text(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["gender", "insurance_type", "diagnosis"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    df["gender"]         = df["gender"].replace(GENDER_MAP)
    df["insurance_type"] = df["insurance_type"].replace(INSURANCE_MAP)

    print("  [6] Text columns standardised")
    return df


# ── Main ──────────────────────────────────────────────────────────────────────

def clean(input_path: str = DEFAULT_INPUT,
          output_path: str = DEFAULT_OUTPUT) -> pd.DataFrame:
    """Run the full cleaning pipeline and return the cleaned DataFrame."""

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  HEALTHCARE DATA CLEANING PIPELINE")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Step 1 – Load
    df = pd.read_csv(input_path)
    print(f"  [1] Loaded  →  {len(df)} rows × {df.shape[1]} columns")

    # Steps 2-6
    df = remove_duplicates(df)
    df = fix_types(df)
    df = fill_missing(df)
    df = clip_outliers(df)
    df = standardise_text(df)

    # Step 7 – Save
    df.to_csv(output_path, index=False)
    print(f"\n  ✅ Saved  →  {output_path}")
    print(f"     Final shape : {len(df)} rows × {df.shape[1]} columns")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    return df


def main():
    parser = argparse.ArgumentParser(description="Clean a messy healthcare CSV.")
    parser.add_argument("--input",  default=DEFAULT_INPUT,
                        help=f"Input CSV  (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help=f"Output CSV (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()
    clean(args.input, args.output)


if __name__ == "__main__":
    main()
