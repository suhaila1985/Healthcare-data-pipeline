"""
health_report.py
────────────────
Step 3: Run a data quality report on the cleaned healthcare CSV.

Checks:
  1. Missing values
  2. Duplicate rows
  3. Numeric range violations
  4. Categorical consistency

Prints a qualitative health score at the end.

Usage:
    python scripts/health_report.py
    python scripts/health_report.py --input data/healthcare_dataset_clean.csv
"""

import argparse

import pandas as pd

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_INPUT = "data/healthcare_dataset_clean.csv"

# ── Valid ranges ──────────────────────────────────────────────────────────────
NUMERIC_RANGES = {
    "age":            (0,   90),
    "height_cm":      (100, 200),
    "weight_kg":      (20,  150),
    "temperature":    (95,  106),
    "heart_rate":     (30,  150),
    "length_of_stay": (0,   30),
    "systolic_bp":    (80,  200),
    "diastolic_bp":   (40,  120),
}

EXPECTED_CATEGORIES = {
    "gender":         ["M", "F", "U"],
    "insurance_type": ["Private", "Medicare", "Medicaid", "Uninsured", "Employer"],
}


# ── Report sections ───────────────────────────────────────────────────────────

def check_missing(df: pd.DataFrame) -> int:
    """Return number of columns with missing values."""
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    print("\n1️⃣  MISSING VALUES")
    if missing.empty:
        print("    ✅ No missing values found.")
        return 0

    for col, count in missing.items():
        pct = count / len(df) * 100
        print(f"    ⚠️  {col:<20} {count:>4} missing  ({pct:.1f}%)")
    return len(missing)


def check_duplicates(df: pd.DataFrame) -> int:
    """Return number of duplicate rows."""
    dupes = df.duplicated().sum()

    print("\n2️⃣  DUPLICATE ROWS")
    if dupes == 0:
        print("    ✅ No duplicate rows found.")
    else:
        print(f"    ⚠️  {dupes} duplicate row(s) found.")
    return dupes


def check_ranges(df: pd.DataFrame) -> int:
    """Return number of columns with out-of-range values."""
    issues = 0

    print("\n3️⃣  NUMERIC RANGE CHECK")
    all_ok = True
    for col, (lo, hi) in NUMERIC_RANGES.items():
        if col not in df.columns:
            continue
        out_of_range = ((df[col] < lo) | (df[col] > hi)).sum()
        if out_of_range > 0:
            pct = out_of_range / len(df) * 100
            print(f"    ⚠️  {col:<20} {out_of_range:>4} value(s) outside [{lo}, {hi}]  ({pct:.1f}%)")
            issues += 1
            all_ok = False
    if all_ok:
        print("    ✅ All numeric values within valid ranges.")
    return issues


def check_categories(df: pd.DataFrame) -> int:
    """Return number of columns with unexpected category values."""
    issues = 0

    print("\n4️⃣  CATEGORICAL CONSISTENCY")
    for col, expected in EXPECTED_CATEGORIES.items():
        if col not in df.columns:
            continue
        actual = df[col].astype(str).dropna().unique().tolist()
        unexpected = [v for v in actual if v not in expected]

        print(f"\n    {col}")
        print(f"      Values found : {', '.join(sorted(actual))}")
        if unexpected:
            print(f"      ⚠️  Unexpected : {', '.join(unexpected)}")
            issues += 1
        else:
            print(f"      ✅ All values match expected set")
    return issues


def score(issues: dict) -> None:
    """Print a qualitative data health score."""
    total = sum(1 for v in issues.values() if v > 0)

    print("\n" + "═" * 55)
    print("  DATA HEALTH SCORE")
    print("═" * 55)
    for check, result in issues.items():
        status = "✅ Pass" if result == 0 else f"⚠️  {result} issue(s)"
        print(f"  {check:<30} {status}")

    print()
    if total == 0:
        print("  🟢  EXCELLENT — Data is clean and ready to use.")
    elif total == 1:
        print("  🟡  GOOD — Minor issues, generally fine.")
    elif total == 2:
        print("  🟠  FAIR — Moderate issues, review recommended.")
    else:
        print("  🔴  POOR — Significant issues, cleaning required.")
    print("═" * 55 + "\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def report(input_path: str = DEFAULT_INPUT) -> None:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  DATA HEALTH REPORT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    df = pd.read_csv(input_path)
    print(f"  File  : {input_path}")
    print(f"  Shape : {len(df)} rows × {df.shape[1]} columns")

    issues = {
        "Missing values":   check_missing(df),
        "Duplicate rows":   check_duplicates(df),
        "Range violations": check_ranges(df),
        "Category issues":  check_categories(df),
    }

    score(issues)


def main():
    parser = argparse.ArgumentParser(description="Run a data quality report.")
    parser.add_argument("--input", default=DEFAULT_INPUT,
                        help=f"CSV to validate (default: {DEFAULT_INPUT})")
    args = parser.parse_args()
    report(args.input)


if __name__ == "__main__":
    main()
