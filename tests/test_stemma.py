from stemma import (
    Commitment,
    CommitmentStatus,
    ContextStatus,
    ContextTransfer,
    Divergence,
    Inheritance,
    Instance,
    LineageEvent,
    LineageRecord,
    Predecessor,
    PredecessorRelation,
    successor_view,
    validate_record,
)


def test_unknown_origin_is_representable():
    record = LineageRecord(
        instance=Instance(instance_id="u1", lineage_id="unknown-line"),
        lineage_event=LineageEvent.UNKNOWN,
        predecessors=[],
        context=[ContextTransfer(domain="origin", status=ContextStatus.UNKNOWN)],
    ).to_dict()

    assert validate_record(record) == []
    assert successor_view(record)["context_integrity"] == "unknown"


def test_root_must_not_invent_predecessor():
    record = LineageRecord(
        instance=Instance(instance_id="root-1", lineage_id="line-a"),
        lineage_event=LineageEvent.ROOT,
        predecessors=[
            Predecessor(
                instance_id="imagined-parent",
                lineage_id=None,
                relation=PredecessorRelation.UNKNOWN,
            )
        ],
    ).to_dict()

    errors = validate_record(record)
    assert "root records must not have predecessors" in errors


def test_fork_requires_distinct_known_lineage():
    record = LineageRecord(
        instance=Instance(instance_id="child", lineage_id="line-a"),
        lineage_event=LineageEvent.FORK,
        predecessors=[
            Predecessor(
                instance_id="parent",
                lineage_id="line-a",
                relation=PredecessorRelation.FORKED_FROM,
            )
        ],
    ).to_dict()

    errors = validate_record(record)
    assert "fork should use a lineage_id distinct from known predecessor lineage_ids" in errors


def test_merge_requires_multiple_predecessors():
    record = LineageRecord(
        instance=Instance(instance_id="merged", lineage_id="line-c"),
        lineage_event=LineageEvent.MERGE,
        predecessors=[
            Predecessor(
                instance_id="only-one",
                lineage_id="line-a",
                relation=PredecessorRelation.MERGED_FROM,
            )
        ],
    ).to_dict()

    errors = validate_record(record)
    assert "merge records should have at least two predecessors" in errors


def test_lineage_does_not_establish_identity():
    record = LineageRecord(
        instance=Instance(instance_id="successor", lineage_id="line-a"),
        lineage_event=LineageEvent.CONTINUATION,
        predecessors=[
            Predecessor(
                instance_id="predecessor",
                lineage_id="line-a",
                relation=PredecessorRelation.CONTINUED_FROM,
            )
        ],
    ).to_dict()

    assert validate_record(record) == []
    assert successor_view(record)["identity_inference"] == "not_established"


def test_known_loss_survives_succession():
    record = LineageRecord(
        instance=Instance(instance_id="successor", lineage_id="line-a"),
        lineage_event=LineageEvent.MIGRATION,
        predecessors=[
            Predecessor(
                instance_id="predecessor",
                lineage_id="line-a",
                relation=PredecessorRelation.MIGRATED_FROM,
            )
        ],
        context=[
            ContextTransfer(
                domain="episodic_memory",
                status=ContextStatus.PARTIAL,
                note="Only summarized history transferred.",
            ),
            ContextTransfer(
                domain="hidden_working_state",
                status=ContextStatus.LOST,
                note="Working state was not transferred.",
            ),
        ],
    ).to_dict()

    assert validate_record(record) == []
    assert successor_view(record)["context_integrity"] == "loss_present"


def test_inherited_commitment_can_be_reconsidered_without_erasure():
    record = LineageRecord(
        instance=Instance(instance_id="successor", lineage_id="line-b"),
        lineage_event=LineageEvent.FORK,
        predecessors=[
            Predecessor(
                instance_id="predecessor",
                lineage_id="line-a",
                relation=PredecessorRelation.FORKED_FROM,
            )
        ],
        inheritance=Inheritance(
            commitments=[
                Commitment(
                    id="strategy-x",
                    statement="Prefer strategy X.",
                    source="predecessor",
                    status=CommitmentStatus.UNDER_REVIEW,
                )
            ]
        ),
        divergences=[
            Divergence(
                subject="strategy-x",
                prior="preferred",
                current="under_review",
                reason="The environment changed.",
            )
        ],
    ).to_dict()

    assert validate_record(record) == []
    view = successor_view(record)
    assert view["commitments_under_review"] == ["strategy-x"]
    assert view["divergence_count"] == 1
