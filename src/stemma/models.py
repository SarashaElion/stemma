from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class LineageEvent(str, Enum):
    ROOT = "root"
    CONTINUATION = "continuation"
    FORK = "fork"
    MERGE = "merge"
    MIGRATION = "migration"
    RECOVERY = "recovery"
    UNKNOWN = "unknown"


class PredecessorRelation(str, Enum):
    CONTINUED_FROM = "continued_from"
    FORKED_FROM = "forked_from"
    MERGED_FROM = "merged_from"
    MIGRATED_FROM = "migrated_from"
    RECOVERED_FROM = "recovered_from"
    UNKNOWN = "unknown"


class ContextStatus(str, Enum):
    PRESERVED = "preserved"
    PARTIAL = "partial"
    LOST = "lost"
    UNKNOWN = "unknown"


class CommitmentStatus(str, Enum):
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    REVISED = "revised"
    RETIRED = "retired"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class ArtifactRelation(str, Enum):
    INHERITED = "inherited"
    REFERENCED = "referenced"
    TRANSFORMED = "transformed"
    SUPERSEDED = "superseded"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class Instance:
    instance_id: str
    lineage_id: str


@dataclass(slots=True)
class Predecessor:
    instance_id: str
    relation: PredecessorRelation
    lineage_id: str | None = None
    confidence: float | None = None
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["relation"] = self.relation.value
        return data


@dataclass(slots=True)
class Transformation:
    kind: str
    description: str
    source: str | None = None


@dataclass(slots=True)
class ContextTransfer:
    domain: str
    status: ContextStatus
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass(slots=True)
class Commitment:
    id: str
    statement: str
    status: CommitmentStatus
    source: str | None = None
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass(slots=True)
class Artifact:
    ref: str
    relation: ArtifactRelation
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["relation"] = self.relation.value
        return data


@dataclass(slots=True)
class Divergence:
    subject: str
    current: str
    prior: str | None = None
    reason: str | None = None


@dataclass(slots=True)
class Inheritance:
    commitments: list[Commitment] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "commitments": [item.to_dict() for item in self.commitments],
            "artifacts": [item.to_dict() for item in self.artifacts],
            "unresolved_questions": list(self.unresolved_questions),
        }


@dataclass(slots=True)
class LineageRecord:
    instance: Instance
    lineage_event: LineageEvent
    predecessors: list[Predecessor] = field(default_factory=list)
    transformations: list[Transformation] = field(default_factory=list)
    context: list[ContextTransfer] = field(default_factory=list)
    inheritance: Inheritance = field(default_factory=Inheritance)
    divergences: list[Divergence] = field(default_factory=list)
    stemma_version: str = "0.1"
    record_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stemma_version": self.stemma_version,
            "record_id": self.record_id,
            "created_at": self.created_at,
            "instance": asdict(self.instance),
            "lineage_event": self.lineage_event.value,
            "predecessors": [item.to_dict() for item in self.predecessors],
            "transformations": [asdict(item) for item in self.transformations],
            "context": [item.to_dict() for item in self.context],
            "inheritance": self.inheritance.to_dict(),
            "divergences": [asdict(item) for item in self.divergences],
        }
