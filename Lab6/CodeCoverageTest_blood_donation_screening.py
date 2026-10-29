"""Lab 6 - Code (line) coverage tests for blood_donation_screening.py

Run:
    coverage run -m pytest CodeCoverageTest_blood_donation_screening.py
    coverage report -m
"""
import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def make_cohort(donors, registered=True, ctype="standard", fast_track=False):
    return {
        "clinic_registered": registered,
        "type": ctype,
        "fast_track": fast_track,
        "donors": donors,
    }


# ---------- process_donor_cohort ----------

def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([{"age": 25, "weight_kg": 65, "hb": 14.0}])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohorts_not_a_list():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


def test_invalid_volume_zero():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_cohort_is_skipped():
    cohort = make_cohort([{"age": 25, "weight_kg": 65, "hb": 14.0}], registered=False)
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_underage_donor_deferred():
    result = process_donor_cohort([make_cohort([{"age": 16, "weight_kg": 65, "hb": 14.0}])], 450)
    assert result["status"] == "ZERO_YIELD"


def test_low_hemoglobin_standard_cohort():
    cohort = make_cohort([
        {"age": 30, "weight_kg": 70, "hb": 11.0},   # deferred, keeps going
        {"age": 30, "weight_kg": 70, "hb": 14.0},   # accepted
    ])
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hemoglobin_high_altitude_resets_total_and_breaks():
    cohort = make_cohort(
        [
            {"age": 30, "weight_kg": 70, "hb": 14.0},   # +450
            {"age": 30, "weight_kg": 70, "hb": 10.0},   # resets to 0, break
            {"age": 30, "weight_kg": 70, "hb": 14.0},   # never reached
        ],
        ctype="high_altitude",
    )
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hemoglobin_deferred():
    result = process_donor_cohort([make_cohort([{"age": 30, "weight_kg": 70, "hb": 19.0}])], 450)
    assert result["status"] == "ZERO_YIELD"


def test_fast_track_bonus_added():
    cohort = make_cohort([{"age": 30, "weight_kg": 70, "hb": 14.0}], fast_track=True)
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_high_deferral_status():
    donors = [{"age": 15, "weight_kg": 65, "hb": 14.0}] * 5  # 5 deferrals (> 4)
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


# ---------- verify_storage_centrifuge ----------

def test_centrifuge_no_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_abort_spin():
    assert verify_storage_centrifuge([[3500, 2500, 2000]]) == "ABORT_SPIN"


def test_centrifuge_stable():
    assert verify_storage_centrifuge([[3500, 3200, 3100]]) == "STABLE"
