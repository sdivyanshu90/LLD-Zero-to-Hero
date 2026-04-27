from models.issue import IssueStatus, IssueType
from services.issue_tracker import IssueTracker
from services.workflow_engine import WorkflowEngine


def main() -> None:
    engine = WorkflowEngine.default_engine()
    tracker = IssueTracker(workflow_engine=engine)

    print(tracker.create_issue("I-1", IssueType.BUG))
    print(tracker.transition_issue("I-1", IssueStatus.IN_PROGRESS))
    print(tracker.transition_issue("I-1", IssueStatus.DONE))
    print(tracker.snapshot())


if __name__ == "__main__":
    main()