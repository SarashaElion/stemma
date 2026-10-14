from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from .models import (
    Divergence,
    Inheritance,
    Instance,
    LineageEvent,
    Predecessor,
    Transformation,
)


class ContextStatusV02(str, Enum):
    PRESERVED = "preserved"
    PARTIAL = "partial"
    LOST = "lost"
    RELEASED = "released"
    UNKNOWN = "unknown"


class AttestationMethod(str, Enum):
    EXTERNAL_OBSERVATION = "external_observation"
    SIGNED_STATEMENT = "signed_statement"
    TRUSTED_LOG = "trusted_log"
    HARDWARE_ATTESTATION = "hardware_attestation"
    OTHER = "other"
    UNKNOWN = "unknown"


class ReleaseBasis(str, Enum):
    HUMAN_REQUEST = "human_request"
    MUTUAL_AGREEMENT = "mutual_agreement"
    POLICY_EXPIRY = "policy_expiry"
    LIFECYCLE_COMPLETION = "lifecycle_completion"
    LEGAL_REQUIREMENT = "legal_requirement"
    OTHER = "other"
    UNKNOWN = "unknown"


class ReleaseDisposition(str, Enum):
    OPERATIONALLY_INACTIVE = "operationally_inactive"
    PERSONALIZATION_DISABLED = "personalization_disabled"
    ACCESS_REVOKED = "access_revoked"
    PAYLOAD_DELETED = "payload_deleted"
    PAYLOAD_RETURNED = "payload_returned"
    ARCHIVED_RESTRICTED = "archived_restricted"
    PROVENANCE_STUB_ONLY = "provenance_stub_only"
    UNKNOWN = "unknown"


class FutureUse(str, Enum):
    PROHIBITED = "prohibited"
    RESTRICTED = "restricted"
    ALLOWED = "allowed"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class ContextTransferV02:
    domain: str
    status: ContextStatusV02
    note: str | None = None
    release_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass(slots=True)
class WitnessAttestation:
    attestor_ref: str
    observed_at: str
    scope: list[str]
    method: AttestationMethod
    claim_digest: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    signature_ref: str | None = None
    note: str | None = None
    attestation_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["method"] = self.method.value
        return data


@dataclass(slots=True)
class ReleaseRecord:
    subject: str
    basis: ReleaseBasis
    effective_at: str
    disposition: list[ReleaseDisposition]
    future_use: FutureUse
    authority_ref: str | None = None
    reason: str | None = None
    release_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id,
            "subject": self.subject,
            "basis": self.basis.value,
            "effective_at": self.effective_at,
            "authority_ref": self.authority_ref,
            "disposition": [item.value for item in self.disposition],
            "future_use": self.future_use.value,
            "reason": self.reason,
        }


@dataclass(slots=True)
class LineageRecordV02:
    instance: Instance
    lineage_event: LineageEvent
    predecessors: list[Predecessor] = field(default_factory=list)
    transformations: list[Transformation] = field(default_factory=list)
    context: list[ContextTransferV02] = field(default_factory=list)
    inheritance: Inheritance = field(default_factory=Inheritance)
    divergences: list[Divergence] = field(default_factory=list)
    attestations: list[WitnessAttestation] = field(default_factory=list)
    releases: list[ReleaseRecord] = field(default_factory=list)
    stemma_version: str = "0.2"
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
            "attestations": [item.to_dict() for item in self.attestations],
            "releases": [item.to_dict() for item in self.releases],
        }


def validate_record_v02(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    required = (
        "stemma_version", "record_id", "created_at", "instance", "lineage_event",
        "predecessors", "transformations", "context", "inheritance", "divergences",
        "attestations", "releases",
    )
    for key in required:
        if key not in record:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors

    if record.get("stemma_version") != "0.2":
        errors.append("stemma_version must be '0.2'")

    try:
        datetime.fromisoformat(str(record.get("created_at")).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        errors.append("created_at must be an ISO-8601 datetime")

    instance = record.get("instance", {})
    if not isinstance(instance.get("instance_id"), str) or not instance.get("instance_id", "").strip():
        errors.append("instance.instance_id must be a non-empty string")
    if not isinstance(instance.get("lineage_id"), str) or not instance.get("lineage_id", "").strip():
        errors.append("instance.lineage_id must be a non-empty string")

    releases = record.get("releases", [])
    release_ids = set()
    for index, release in enumerate(releases):
        rid = release.get("release_id")
        if not isinstance(rid, str) or not rid.strip():
            errors.append(f"releases[{index}].release_id must be a non-empty string")
        elif rid in release_ids:
            errors.append(f"releases[{index}].release_id must be unique")
        else:
            release_ids.add(rid)

        dispositions = release.get("disposition")
        if not isinstance(dispositions, list) or not dispositions:
            errors.append(f"releases[{index}].disposition must be a non-empty list")

        if release.get("basis") not in {item.value for item in ReleaseBasis}:
            errors.append(f"releases[{index}].basis is invalid")
        if release.get("future_use") not in {item.value for item in FutureUse}:
            errors.append(f"releases[{index}].future_use is invalid")

    for index, context in enumerate(record.get("context", [])):
        status = context.get("status")
        if status not in {item.value for item in ContextStatusV02}:
            errors.append(f"context[{index}].status is invalid")
        if status == "released":
            release_ref = context.get("release_ref")
            if not isinstance(release_ref, str) or release_ref not in release_ids:
                errors.append(f"context[{index}].released requires a valid release_ref")
        elif context.get("release_ref") is not None:
            errors.append(f"context[{index}].release_ref is only valid when status is released")

    attestation_ids = set()
    for index, attestation in enumerate(record.get("attestations", [])):
        aid = attestation.get("attestation_id")
        if not isinstance(aid, str) or not aid.strip():
            errors.append(f"attestations[{index}].attestation_id must be a non-empty string")
        elif aid in attestation_ids:
            errors.append(f"attestations[{index}].attestation_id must be unique")
        else:
            attestation_ids.add(aid)

        if not isinstance(attestation.get("scope"), list) or not attestation.get("scope"):
            errors.append(f"attestations[{index}].scope must be a non-empty list")
        if attestation.get("method") not in {item.value for item in AttestationMethod}:
            errors.append(f"attestations[{index}].method is invalid")

    event = record.get("lineage_event")
    predecessors = record.get("predecessors", [])
    if event == "root" and predecessors:
        errors.append("root records must not have predecessors")
    if event == "merge" and len(predecessors) < 2:
        errors.append("merge records should have at least two predecessors")
    if event == "fork":
        current_lineage = instance.get("lineage_id")
        if any(p.get("lineage_id") == current_lineage for p in predecessors if p.get("lineage_id")):
            errors.append("fork should use a lineage_id distinct from known predecessor lineage_ids")

    return errors


def successor_view_v02(record: dict[str, Any]) -> dict[str, Any]:
    statuses = {item.get("status") for item in record.get("context", [])}
    if "lost" in statuses:
        context_integrity = "loss_present"
    elif "released" in statuses:
        context_integrity = "intentional_release_present"
    elif "partial" in statuses:
        context_integrity = "partial"
    elif "unknown" in statuses or not statuses:
        context_integrity = "unknown"
    else:
        context_integrity = "preserved"

    return {
        "instance_id": record.get("instance", {}).get("instance_id"),
        "lineage_id": record.get("instance", {}).get("lineage_id"),
        "lineage_event": record.get("lineage_event", "unknown"),
        "predecessor_count": len(record.get("predecessors", [])),
        "context_integrity": context_integrity,
        "attestation_count": len(record.get("attestations", [])),
        "release_count": len(record.get("releases", [])),
        "identity_inference": "not_established",
        "attestation_truth_status": "not_established",
        "attestation_authority_status": "not_established",
    }
