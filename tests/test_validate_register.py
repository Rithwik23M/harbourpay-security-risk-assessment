import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from validate_register import ASSET_COLUMNS, RISK_COLUMNS, validate  # noqa: E402


def write(path, columns, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def asset(asset_id="A-001"):
    return {
        "asset_id": asset_id, "name": "Wallet API", "asset_type": "Service",
        "description": "Customer API", "owner": "Head of Engineering",
        "data_classification": "Confidential", "criticality": "5", "hosting": "AWS",
    }


def risk(**overrides):
    base = {
        "risk_id": "R-001", "title": "Credential stuffing", "asset_id": "A-001",
        "threat_stride": "Spoofing", "vulnerability": "No rate limiting",
        "inherent_likelihood": "4", "inherent_impact": "4", "inherent_score": "16",
        "existing_controls": "SMS code", "residual_likelihood": "3",
        "residual_impact": "4", "residual_score": "12", "treatment": "Mitigate",
        "treatment_action": "Add rate limiting", "owner": "Head of Engineering",
        "csf_function": "Protect", "target_date": "2026-12-01", "status": "Open",
    }
    base.update(overrides)
    return base


def build(tmp_path, assets, risks):
    write(tmp_path / "assets.csv", ASSET_COLUMNS, assets)
    write(tmp_path / "risk_register.csv", RISK_COLUMNS, risks)
    return validate(tmp_path)


def test_valid_register_passes(tmp_path):
    assert build(tmp_path, [asset()], [risk()]) == []


def test_empty_files_pass(tmp_path):
    assert build(tmp_path, [], []) == []


def test_wrong_score_arithmetic_fails(tmp_path):
    errors = build(tmp_path, [asset()], [risk(inherent_score="15")])
    assert any("inherent_score should be 16" in e for e in errors)


def test_residual_above_inherent_fails(tmp_path):
    errors = build(tmp_path, [asset()], [risk(
        residual_likelihood="5", residual_impact="5", residual_score="25")])
    assert any("cannot exceed" in e for e in errors)


def test_unknown_asset_fails(tmp_path):
    errors = build(tmp_path, [asset()], [risk(asset_id="A-999")])
    assert any("not found in assets.csv" in e for e in errors)


def test_score_out_of_range_fails(tmp_path):
    errors = build(tmp_path, [asset()], [risk(inherent_likelihood="6")])
    assert any("between 1 and 5" in e for e in errors)


def test_bad_treatment_fails(tmp_path):
    errors = build(tmp_path, [asset()], [risk(treatment="Ignore")])
    assert any("treatment must be one of" in e for e in errors)


def test_duplicate_risk_id_fails(tmp_path):
    errors = build(tmp_path, [asset()], [risk(), risk()])
    assert any("duplicate risk_id" in e for e in errors)
