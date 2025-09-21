from traffic_sim.control.fixed_cycle import FixedCyclePolicy


def test_fixed_cycle_decisions():
    policy = FixedCyclePolicy(green_ns=8, yellow_ns=2, green_ew=8, yellow_ew=2)

    assert policy.decide(None, 0.0) == ("NS", "GREEN")
    assert policy.decide(None, 7.0) == ("NS", "GREEN")
    assert policy.decide(None, 9.0) == ("NS", "YELLOW")
    assert policy.decide(None, 10.0) == ("EW", "GREEN")
    assert policy.decide(None, 17.9) == ("EW", "GREEN")
    assert policy.decide(None, 18.0) == ("EW", "YELLOW")
    assert policy.decide(None, 21.5) == ("NS", "GREEN")
