from models.core import WorkflowTask
from services.workflow_engine import WorkflowEngine


def main() -> None:
    outputs: list[str] = []
    engine = WorkflowEngine(
        tasks=[
            WorkflowTask("A", set(), lambda: outputs.append("A")),
            WorkflowTask("B", {"A"}, lambda: outputs.append("B")),
            WorkflowTask("C", {"A"}, lambda: outputs.append("C")),
            WorkflowTask("D", {"B", "C"}, lambda: outputs.append("D")),
        ]
    )
    print(engine.execute())
    print(outputs)


if __name__ == "__main__":
    main()