import pytest
from src.equivalence import loss_rate, verdict

def test_verdict_supported():
    assert verdict(-0.05, 0.07) == "supported"

def test_verdict_rejected():
    assert verdict(0.11, 0.54) == "rejected"

def test_verdict_inconclusive_straddles():
    assert verdict(0.08, 0.54) == "inconclusive"

def test_verdict_inconclusive_at_bound():
    assert verdict(0.08, 0.1) == "inconclusive"

def test_verdict_nan():
    assert verdict(float('NaN'), 0.1) == "inconclusive"

def test_loss_rate_example():
    loss, low, high = loss_rate([0, 1, 2, 3, 4], [5.0, 4.8, 4.7, 4.4, 4.3], 0.90)
    assert loss == pytest.approx(0.18)
    assert low == pytest.approx(0.1416, abs=1e-3)
    assert high == pytest.approx(0.2184, abs=1e-3)

def test_loss_rate_known_slope():
    weeks = [0, 1, 2, 3, 4, 5]
    logs = [6.0 - 0.3 * t for t in weeks]      # falls exactly 0.3 per week
    loss, low, high = loss_rate(weeks, logs, 0.90)
    assert loss == pytest.approx(0.3)

def test_loss_rate_too_few_points():
    with pytest.raises(ValueError):
        loss_rate([0,1], [4.0,3.8], 0.9)

def test_loss_rate_mismatched_lengths():
    with pytest.raises(ValueError):
        loss_rate([0,1,2], [4.0,3.8,3.4,3.1], 0.9)
