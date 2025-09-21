import pytest

from traffic_sim.models.traffic_light import TrafficLight


def test_set_state_and_queries():
    light = TrafficLight()
    light.set_state("NS", "GREEN")
    assert light.is_green_for("NS")
    assert not light.is_green_for("EW")
    assert not light.is_yellow_for("NS")

    light.set_state("EW", "YELLOW")
    assert light.is_yellow_for("EW")
    assert not light.is_green_for("EW")


def test_set_state_rejects_bad_values():
    light = TrafficLight()
    with pytest.raises(AssertionError):
        light.set_state("BAD", "GREEN")
    with pytest.raises(AssertionError):
        light.set_state("NS", "BLUE")
