from dataclasses import dataclass
from enum import Enum


class IssueType(Enum):
    BUG = "bug"
    TASK = "task"
    STORY = "story"


class IssueStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


@dataclass(slots=True)
class Issue:
    issue_id: str
    issue_type: IssueType
    status: IssueStatus = IssueStatus.OPEN