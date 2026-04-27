from models.direction import Direction
from models.request import FloorRequest
from services.elevator_controller import ElevatorController


def main() -> None:
    controller = ElevatorController(current_floor=4, direction=Direction.IDLE)
    for floor in (8, 2, 6, 1):
        controller.add_request(FloorRequest(floor=floor))

    print(controller.run_until_idle())
    print(controller.snapshot())


if __name__ == "__main__":
    main()