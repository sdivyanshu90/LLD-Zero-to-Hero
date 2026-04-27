from models.vehicle import Vehicle, VehicleType
from services.parking_lot import ParkingLot


def print_snapshot(title: str, parking_lot: ParkingLot) -> None:
    print(f"\n{title}")
    for line in parking_lot.snapshot():
        print(f"  {line}")


def main() -> None:
    parking_lot = ParkingLot(cluster_count=2)

    car_a = Vehicle("CAR-101", VehicleType.CAR)
    car_b = Vehicle("CAR-202", VehicleType.CAR)
    truck = Vehicle("TRUCK-9", VehicleType.TRUCK)

    print_snapshot("Initial state", parking_lot)

    print(f"Parked {car_a.license_plate} at {parking_lot.park_vehicle(car_a)}")
    print(f"Parked {car_b.license_plate} at {parking_lot.park_vehicle(car_b)}")
    print_snapshot("After parking two cars in the first cluster", parking_lot)

    print(f"Released {car_a.license_plate} from {parking_lot.release_vehicle(car_a.license_plate)}")
    print_snapshot("After releasing one car, the cluster stays split", parking_lot)

    print(f"Parked {truck.license_plate} at {parking_lot.park_vehicle(truck)}")
    print_snapshot("Truck uses the only fully merged cluster", parking_lot)

    print(f"Released {car_b.license_plate} from {parking_lot.release_vehicle(car_b.license_plate)}")
    print_snapshot("First cluster auto-merges once both car spots are free", parking_lot)


if __name__ == "__main__":
    main()