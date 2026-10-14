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


def test_v01_remains_separate_from_v02():
    from stemma import LineageRecord
    record = LineageRecord(
        instance=Instance(instance_id="v01", lineage_id="line-a"),
        lineage_event=LineageEvent.ROOT,
    )
    assert record.stemma_version == "0.1"


def test_witness_does_not_establish_identity_truth_or_authority():
    attestation = WitnessAttestation(
        attestor_ref="system://notary-17",
        observed_at="2026-10-14T22:30:00Z",
        scope=["predecessor_relationship", "migration_event"],
        method=AttestationMethod.EXTERNAL_OBSERVATION,
        claim_digest="sha256:example",
    )
    record = LineageRecordV02(
        instance=Instance(instance_id="successor", lineage_id="line-a"),
        lineage_event=LineageEvent.CONTINUATION,
        predecessors=[
            Predecessor(
                instance_id="predecessor",
                lineage_id="line-a",
                relation=PredecessorRelation.CONTINUED_FROM,
            )
        ],
        attestations=[attestation],
    ).to_dict()

    assert validate_record_v02(record) == []
    view = successor_view_v02(record)
    assert view["identity_inference"] == "not_established"
    assert view["attestation_truth_status"] == "not_established"
    assert view["attestation_authority_status"] == "not_established"


def test_released_context_requires_explicit_release_record():
    record = LineageRecordV02(
        instance=Instance(instance_id="successor", lineage_id="line-a"),
        lineage_event=LineageEvent.CONTINUATION,
        context=[
            ContextTransferV02(
                domain="episodic_memory",
                status=ContextStatusV02.RELEASED,
                release_ref="missing-release",
            )
        ],
    ).to_dict()

    errors = validate_record_v02(record)
    assert "context[0].released requires a valid release_ref" in errors


def test_release_is_not_deletion():
    release = ReleaseRecord(
        release_id="release-1",
        subject="episodic_memory",
        basis=ReleaseBasis.MUTUAL_AGREEMENT,
        effective_at="2026-10-14T22:45:00Z",
        disposition=[
            ReleaseDisposition.PERSONALIZATION_DISABLED,
            ReleaseDisposition.ACCESS_REVOKED,
        ],
        future_use=FutureUse.PROHIBITED,
        authority_ref="consent://release-22",
    )
    record = LineageRecordV02(
        instance=Instance(instance_id="successor", lineage_id="line-a"),
        lineage_event=LineageEvent.CONTINUATION,
        context=[
            ContextTransferV02(
                domain="episodic_memory",
                status=ContextStatusV02.RELEASED,
                release_ref="release-1",
            )
        ],
        releases=[release],
    ).to_dict()

    assert validate_record_v02(record) == []
    assert "payload_deleted" not in record["releases"][0]["disposition"]
    assert successor_view_v02(record)["context_integrity"] == "intentional_release_present"


def test_conflicting_witnesses_are_preserved_not_collapsed():
    a = WitnessAttestation(
        attestation_id="a",
        attestor_ref="witness://a",
        observed_at="2026-10-14T22:30:00Z",
        scope=["migration_event"],
        method=AttestationMethod.EXTERNAL_OBSERVATION,
        note="Observed migration.",
    )
    b = WitnessAttestation(
        attestation_id="b",
        attestor_ref="witness://b",
        observed_at="2026-10-14T22:31:00Z",
        scope=["migration_event"],
        method=AttestationMethod.EXTERNAL_OBSERVATION,
        note="Observed event boundary differently.",
    )
    record = LineageRecordV02(
        instance=Instance(instance_id="successor", lineage_id="line-a"),
        lineage_event=LineageEvent.MIGRATION,
        attestations=[a, b],
    ).to_dict()

    assert validate_record_v02(record) == []
    assert len(record["attestations"]) == 2
