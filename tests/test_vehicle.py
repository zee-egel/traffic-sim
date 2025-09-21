from traffic_sim.models.intersection import Intersection
from traffic_sim.models.road import Road
from traffic_sim.models.vehicle import Vehicle


def make_setup(color: str):
    intersection = Intersection("X")
    road = Road(name="Test", length_m=100.0, speed_mps=10.0, to_intersection=intersection, approach_dir="NS")
    intersection.register_road(road)
    vehicle = Vehicle(id="car-1", road=road, pos_m=98.0, enter_time_s=0.0)
    intersection.signal.set_state("NS", color)
    return intersection, vehicle


def test_vehicle_stops_on_red():
    intersection, vehicle = make_setup("RED")
    vehicle.update(dt=1.0, intersection=intersection)
    assert vehicle.pos_m == 98.0
    assert not vehicle.finished


def test_vehicle_advances_on_green():
    intersection, vehicle = make_setup("GREEN")
    vehicle.update(dt=1.0, intersection=intersection)
    assert vehicle.pos_m > 98.0
