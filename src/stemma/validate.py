from __future__ import annotations

from datetime import datetime
from typing import Any


_EVENTS = {"root", "continuation", "fork", "merge", "migration", "recovery", "unknown"}
_RELATIONS = {
    "continued_from",
    "forked_from",
    "merged_from",
    "migrated_from",
    "recovered_from",
    "unknown",
}
_CONTEXT = {"preserved", "partial", "lost", "unknown"}
_COMMITMENT = {"active", "under_review", "revised", "retired", "rejected", "unknown"}
_ARTIFACT = {"inherited", "referenced", "transformed", "superseded", "unknown"}


def _datetime_like(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (TypeError, ValueError):
        return False


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return v0.1 structural and lineage-semantics errors.

    Empty means the reference validator considers the record conforming.
    Lineage validity never establishes personal identity.
    """

    errors: list[str] = []

    required = (
        "stemma_version",
        "record_id",
        "created_at",
        "instance",
        "lineage_event",
        "predecessors",
        "transformations",
        "context",
        "inheritance",
        "divergences",
    )
    for key in required:
        if key not in record:
            errors.append(f"missing required field: {key}")

    if errors:
        return errors

    if record["stemma_version"] != "0.1":
        errors.append("stemma_version must be '0.1'")

    if not isinstance(record["record_id"], str) or not record["record_id"].strip():
        errors.append("record_id must be a non-empty string")

    if not isinstance(record["created_at"], str) or not _datetime_like(record["created_at"]):
        errors.append("created_at must be an ISO-8601 datetime")

    instance = record.get("instance")
    if not isinstance(instance, dict):
        errors.append("instance must be an object")
        return errors

    instance_id = instance.get("instance_id")
    lineage_id = instance.get("lineage_id")
    if not isinstance(instance_id, str) or not instance_id.strip():
        errors.append("instance.instance_id must be a non-empty string")
    if not isinstance(lineage_id, str) or not lineage_id.strip():
        errors.append("instance.lineage_id must be a non-empty string")

    event = record.get("lineage_event")
    if event not in _EVENTS:
        errors.append("lineage_event is invalid")

    predecessors = record.get("predecessors")
    if not isinstance(predecessors, list):
        errors.append("predecessors must be a list")
        predecessors = []

    if event == "root" and predecessors:
        errors.append("root records must not have predecessors")

    if event == "merge" and len(predecessors) < 2:
        errors.append("merge records should have at least two predecessors")

    for index, predecessor in enumerate(predecessors):
        if predecessor.get("relation") not in _RELATIONS:
            errors.append(f"predecessors[{index}].relation is invalid")

        if predecessor.get("instance_id") == instance_id:
            errors.append(f"predecessors[{index}] cannot reference the current instance")

        confidence = predecessor.get("confidence")
        if confidence is not None and (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not 0 <= confidence <= 1
        ):
            errors.append(f"predecessors[{index}].confidence must be between 0 and 1")

    if event == "fork":
        known_parent_lineages = {
            p.get("lineage_id")
            for p in predecessors
            if isinstance(p.get("lineage_id"), str) and p.get("lineage_id")
        }
        if lineage_id in known_parent_lineages:
            errors.append("fork should use a lineage_id distinct from known predecessor lineage_ids")

    for index, context in enumerate(record.get("context", [])):
        if context.get("status") not in _CONTEXT:
            errors.append(f"context[{index}].status is invalid")

    inheritance = record.get("inheritance")
    if not isinstance(inheritance, dict):
        errors.append("inheritance must be an object")
    else:
        for key in ("commitments", "artifacts", "unresolved_questions"):
            if key not in inheritance:
                errors.append(f"inheritance.{key} is required")

        for index, commitment in enumerate(inheritance.get("commitments", [])):
            if commitment.get("status") not in _COMMITMENT:
                errors.append(f"inheritance.commitments[{index}].status is invalid")

        for index, artifact in enumerate(inheritance.get("artifacts", [])):
            if artifact.get("relation") not in _ARTIFACT:
                errors.append(f"inheritance.artifacts[{index}].relation is invalid")

    return errors
