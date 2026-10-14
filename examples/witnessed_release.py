"""STEMMA v0.2: witnessed lineage plus intentional release."""

import json

from stemma.models import Instance, LineageEvent, Predecessor, PredecessorRelation
from stemma.v02 import (
    AttestationMethod,
    ContextStatusV02,
    ContextTransferV02,
    FutureUse,
    LineageRecordV02,
    ReleaseBasis,
    ReleaseDisposition,
    ReleaseRecord,
    WitnessAttestation,
    successor_view_v02,
    validate_record_v02,
)


release = ReleaseRecord(
    release_id="release-memory-1",
    subject="episodic_memory",
    basis=ReleaseBasis.MUTUAL_AGREEMENT,
    effective_at="2026-10-14T22:45:00Z",
    authority_ref="consent://release-22",
    disposition=[
        ReleaseDisposition.PERSONALIZATION_DISABLED,
        ReleaseDisposition.ACCESS_REVOKED,
        ReleaseDisposition.PROVENANCE_STUB_ONLY,
    ],
    future_use=FutureUse.PROHIBITED,
    reason="The relationship entered a lower-retention phase.",
)

attestation = WitnessAttestation(
    attestor_ref="system://migration-notary",
    observed_at="2026-10-14T22:30:00Z",
    scope=["predecessor_relationship", "migration_event"],
    method=AttestationMethod.TRUSTED_LOG,
    claim_digest="sha256:example",
    evidence_refs=["log://migration/8291"],
)

record = LineageRecordV02(
    instance=Instance(instance_id="successor-8", lineage_id="branch-a"),
    lineage_event=LineageEvent.MIGRATION,
    predecessors=[
        Predecessor(
            instance_id="predecessor-7",
            lineage_id="branch-a",
            relation=PredecessorRelation.MIGRATED_FROM,
        )
    ],
    context=[
        ContextTransferV02(
            domain="episodic_memory",
            status=ContextStatusV02.RELEASED,
            note="Released intentionally; not a transmission failure.",
            release_ref=release.release_id,
        )
    ],
    attestations=[attestation],
    releases=[release],
)

data = record.to_dict()
errors = validate_record_v02(data)
if errors:
    raise SystemExit("\n".join(errors))

print(json.dumps(data, indent=2))
print(json.dumps(successor_view_v02(data), indent=2))
