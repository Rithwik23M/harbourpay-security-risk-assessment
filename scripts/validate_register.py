"""Validate the asset inventory and risk register for HarbourPay.

Checks required columns, score ranges, score arithmetic, residual <= inherent,
allowed treatment values, and that every risk references a real asset.
Exits with a non-zero status if any problem is found.
"""
import csv
import sys
from pathlib import Path

ASSET_COLUMNS = [
    "asset_id", "name", "asset_type", "description",
    "owner", "data_classification", "criticality", "hosting",
]
RISK_COLUMNS = [
    "risk_id", "title", "asset_id", "threat_stride", "vulnerability",
    "inherent_likelihood", "inherent_impact", "inherent_score",
    "existing_controls", "residual_likelihood", "residual_impact",
    "residual_score", "treatment", "treatment_action", "owner",
    "csf_function", "target_date", "status",
]
TREATMENTS = {"Mitigate", "Accept", "Transfer", "Avoid"}
STRIDE = {
    "Spoofing", "Tampering", "Repudiation",
    "Information Disclosure", "Denial of Service", "Elevation of Privilege",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def parse_score(value, label, errors, row_id):
    try:
        number = int(value)
    except (TypeError, ValueError):
        errors.append(f"{row_id}: {label} must be an integer, got {value!r}")
        return None
    if not 1 <= number <= 5:
        errors.append(f"{row_id}: {label} must be between 1 and 5, got {number}")
        return None
    return number


def validate(data_dir):
    errors = []
    data_dir = Path(data_dir)

    asset_cols, assets = read_csv(data_dir / "assets.csv")
    if asset_cols != ASSET_COLUMNS:
        errors.append(f"assets.csv columns do not match expected: {ASSET_COLUMNS}")
    asset_ids = [row.get("asset_id", "") for row in assets]
    if len(asset_ids) != len(set(asset_ids)):
        errors.append("assets.csv contains duplicate asset_id values")

    risk_cols, risks = read_csv(data_dir / "risk_register.csv")
    if risk_cols != RISK_COLUMNS:
        errors.append(f"risk_register.csv columns do not match expected: {RISK_COLUMNS}")
        return errors

    seen = set()
    for row in risks:
        rid = row["risk_id"] or "<missing id>"
        if rid in seen:
            errors.append(f"{rid}: duplicate risk_id")
        seen.add(rid)
        if row["asset_id"] not in asset_ids:
            errors.append(f"{rid}: asset_id {row['asset_id']!r} not found in assets.csv")
        if row["threat_stride"] not in STRIDE:
            errors.append(f"{rid}: threat_stride must be one of {sorted(STRIDE)}")
        if row["treatment"] not in TREATMENTS:
            errors.append(f"{rid}: treatment must be one of {sorted(TREATMENTS)}")
        for field in ("owner", "existing_controls", "treatment_action"):
            if not row[field].strip():
                errors.append(f"{rid}: {field} is required")

        il = parse_score(row["inherent_likelihood"], "inherent_likelihood", errors, rid)
        ii = parse_score(row["inherent_impact"], "inherent_impact", errors, rid)
        rl = parse_score(row["residual_likelihood"], "residual_likelihood", errors, rid)
        ri = parse_score(row["residual_impact"], "residual_impact", errors, rid)
        if None in (il, ii, rl, ri):
            continue
        if str(il * ii) != row["inherent_score"].strip():
            errors.append(f"{rid}: inherent_score should be {il * ii}")
        if str(rl * ri) != row["residual_score"].strip():
            errors.append(f"{rid}: residual_score should be {rl * ri}")
        if rl * ri > il * ii:
            errors.append(f"{rid}: residual score cannot exceed inherent score")
    return errors


def main():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    problems = validate(data_dir)
    if problems:
        print("Validation failed:")
        for problem in problems:
            print(f" - {problem}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
