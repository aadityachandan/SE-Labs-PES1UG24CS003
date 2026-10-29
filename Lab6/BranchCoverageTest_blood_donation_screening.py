"""Lab 6 - Branch coverage tests for blood_donation_screening.py

Run:
    coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
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


GOOD = {"age": 30, "weight_kg": 70, "hb": 14.0}


# ---------- process_donor_cohort: validation ----------

def test_invalid_cohorts_not_a_list():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


def test_invalid_volume_zero():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_invalid_volume_negative():
    with pytest.raises(ValueError):
        process_donor_cohort([], -10)


# ---------- process_donor_cohort: cohort-level branches ----------

def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([GOOD])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_empty_cohort_list_is_zero_yield():
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_unregistered_cohort_is_skipped():
    result = process_donor_cohort([make_cohort([GOOD], registered=False)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_cohort_missing_registration_key_is_skipped():
    result = process_donor_cohort([{"donors": [GOOD]}], 450)
    assert result["status"] == "ZERO_YIELD"


def test_cohort_with_no_donors_loop_never_enters():
    result = process_donor_cohort([make_cohort([])], 450)
    assert result["status"] == "ZERO_YIELD"


def test_cohort_defaults_when_type_and_donors_missing():
    result = process_donor_cohort([{"clinic_registered": True}], 450)
    assert result["status"] == "ZERO_YIELD"


def test_fast_track_true_adds_bonus():
    result = process_donor_cohort([make_cohort([GOOD], fast_track=True)], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_false_no_bonus():
    result = process_donor_cohort([make_cohort([GOOD], fast_track=False)], 450)
    assert result["collected_ml"] == 450


def test_fast_track_bonus_on_empty_cohort_gives_accepted():
    result = process_donor_cohort([make_cohort([], fast_track=True)], 450)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_multiple_cohorts_accumulate():
    cohorts = [make_cohort([GOOD]), make_cohort([GOOD], fast_track=True)]
    result = process_donor_cohort(cohorts, 450)
    assert result == {"collected_ml": 950, "status": "ACCEPTED"}


# ---------- process_donor_cohort: donor-level branches ----------

def test_underage_deferred():
    result = process_donor_cohort([make_cohort([{"age": 16, "weight_kg": 70, "hb": 14.0}])], 450)
    assert result["status"] == "ZERO_YIELD"


def test_underweight_deferred():
    result = process_donor_cohort([make_cohort([{"age": 30, "weight_kg": 49, "hb": 14.0}])], 450)
    assert result["status"] == "ZERO_YIELD"


def test_boundary_age_17_and_weight_50_accepted():
    result = process_donor_cohort([make_cohort([{"age": 17, "weight_kg": 50, "hb": 12.5}])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_boundary_hb_18_accepted():
    result = process_donor_cohort([make_cohort([{"age": 30, "weight_kg": 70, "hb": 18.0}])], 450)
    assert result["collected_ml"] == 450


def test_missing_donor_fields_use_defaults_and_are_deferred():
    result = process_donor_cohort([make_cohort([{}])], 450)
    assert result["status"] == "ZERO_YIELD"


def test_low_hb_standard_cohort_continues_to_next_donor():
    cohort = make_cohort([{"age": 30, "weight_kg": 70, "hb": 11.0}, GOOD])
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_low_hb_high_altitude_resets_total_and_breaks():
    cohort = make_cohort(
        [GOOD, {"age": 30, "weight_kg": 70, "hb": 10.0}, GOOD],
        ctype="high_altitude",
    )
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_cohort_with_normal_hb_not_reset():
    result = process_donor_cohort([make_cohort([GOOD], ctype="high_altitude")], 450)
    assert result["collected_ml"] == 450


def test_high_hb_deferred_and_continues():
    cohort = make_cohort([{"age": 30, "weight_kg": 70, "hb": 19.0}, GOOD])
    result = process_donor_cohort([cohort], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# ---------- process_donor_cohort: final status branches ----------

def test_high_deferral_when_more_than_four_deferred():
    donors = [{"age": 15, "weight_kg": 70, "hb": 14.0}] * 5
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_exactly_four_deferrals_is_not_high_deferral():
    donors = [{"age": 15, "weight_kg": 70, "hb": 14.0}] * 4 + [GOOD]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_high_deferral_takes_priority_even_with_collection():
    donors = [{"age": 15, "weight_kg": 70, "hb": 14.0}] * 5 + [GOOD]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


# ---------- verify_storage_centrifuge ----------

def test_centrifuge_none_is_no_data():
    assert verify_storage_centrifuge(None) == "NO_DATA"


def test_centrifuge_empty_is_no_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_two_consecutive_drops_abort():
    assert verify_storage_centrifuge([[3500, 2500, 2000]]) == "ABORT_SPIN"


def test_centrifuge_single_drop_is_stable():
    assert verify_storage_centrifuge([[3500, 2500, 3500]]) == "STABLE"


def test_centrifuge_streak_resets_between_drops():
    assert verify_storage_centrifuge([[2000, 3500, 2000, 3500]]) == "STABLE"


def test_centrifuge_all_stable_runs():
    assert verify_storage_centrifuge([[3500, 3600], [3200, 3300]]) == "STABLE"


def test_centrifuge_abort_in_later_run():
    assert verify_storage_centrifuge([[3500, 3600], [2900, 2800]]) == "ABORT_SPIN"


def test_centrifuge_streak_does_not_carry_across_runs():
    assert verify_storage_centrifuge([[3500, 2000], [2000, 3500]]) == "STABLE"


def test_centrifuge_empty_run_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"
