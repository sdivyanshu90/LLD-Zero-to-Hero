from __future__ import annotations

from dataclasses import dataclass, field

from models.issue import Issue, IssueStatus, IssueType
from services.workflow_engine import WorkflowEngine


@dataclass(slots=True)
class IssueTracker:
    workflow_engine: WorkflowEngine
    issues: dict[str, Issue] = field(default_factory=dict)

    def create_issue(self, issue_id: str, issue_type: IssueType) -> str:
        self.issues[issue_id] = Issue(issue_id=issue_id, issue_type=issue_type)
        return f"Created {issue_id} as {issue_type.value}"

    def transition_issue(self, issue_id: str, new_status: IssueStatus) -> str:
        issue = self._get_issue(issue_id)
        if not self.workflow_engine.can_transition(issue.issue_type, issue.status, new_status):
            raise ValueError(f"Transition {issue.status.value} -> {new_status.value} is not allowed for {issue.issue_type.value}")
        issue.status = new_status
        return f"{issue_id} -> {new_status.value}"

    def snapshot(self) -> dict[str, str]:
        return {issue_id: issue.status.value for issue_id, issue in sorted(self.issues.items())}

    def _get_issue(self, issue_id: str) -> Issue:
        issue = self.issues.get(issue_id)
        if issue is None:
            raise ValueError(f"Unknown issue {issue_id}")
        return issue