from __future__ import annotations

from dataclasses import dataclass

from models.issue import IssueStatus, IssueType


@dataclass(frozen=True, slots=True)
class WorkflowEngine:
    transition_map: dict[IssueType, dict[IssueStatus, set[IssueStatus]]]

    def can_transition(self, issue_type: IssueType, current: IssueStatus, new: IssueStatus) -> bool:
        return new in self.transition_map.get(issue_type, {}).get(current, set())

    @classmethod
    def default_engine(cls) -> "WorkflowEngine":
        return cls(
            transition_map={
                IssueType.BUG: {
                    IssueStatus.OPEN: {IssueStatus.IN_PROGRESS},
                    IssueStatus.IN_PROGRESS: {IssueStatus.DONE},
                },
                IssueType.TASK: {
                    IssueStatus.OPEN: {IssueStatus.IN_PROGRESS},
                    IssueStatus.IN_PROGRESS: {IssueStatus.IN_REVIEW, IssueStatus.DONE},
                    IssueStatus.IN_REVIEW: {IssueStatus.DONE},
                },
                IssueType.STORY: {
                    IssueStatus.OPEN: {IssueStatus.IN_PROGRESS},
                    IssueStatus.IN_PROGRESS: {IssueStatus.IN_REVIEW},
                    IssueStatus.IN_REVIEW: {IssueStatus.DONE},
                },
            }
        )