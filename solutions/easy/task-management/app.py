from models.simple_task import SimpleTask
from models.task_group import TaskGroup
from services.task_board import TaskBoard


def main() -> None:
    board = TaskBoard()
    backend = TaskGroup("Backend")
    backend.add(SimpleTask("Design API"))
    backend.add(SimpleTask("Implement service"))

    ui = TaskGroup("UI")
    ui.add(SimpleTask("Create mockups", completed=True))
    ui.add(SimpleTask("Build screens"))

    epic = TaskGroup("Release 1")
    epic.add(backend)
    epic.add(ui)
    board.add_root_task(epic)

    print(board.snapshot())
    print(board.overall_completion())
    backend.children[0].mark_complete()
    print(board.overall_completion())


if __name__ == "__main__":
    main()