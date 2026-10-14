"""A STEMMA record for a successor created by a lineage fork."""

import json

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
    Transformation,
    successor_view,
    validate_record,
)


record = LineageRecord(
    instance=Instance(
        instance_id="successor-8",
        lineage_id="branch-b",
    ),
    lineage_event=LineageEvent.FORK,
    predecessors=[
        Predecessor(
            instance_id="predecessor-7",
            lineage_id="branch-a",
            relation=PredecessorRelation.FORKED_FROM,
            evidence=["checkpoint:sha256:example"],
        )
    ],
    transformations=[
        Transformation(
            kind="model_change",
            description="Runtime migrated from model A to model B.",
        ),
        Transformation(
            kind="capability_added",
            description="Persistent tool access added.",
        ),
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
            note="Private working state was not transferred.",
        ),
    ],
    inheritance=Inheritance(
        commitments=[
            Commitment(
                id="preserve-user-agency",
                statement="Preserve user agency.",
                source="policy:v3",
                status=CommitmentStatus.ACTIVE,
            ),
            Commitment(
                id="strategy-x",
                statement="Prefer strategy X.",
                source="predecessor-7",
                status=CommitmentStatus.UNDER_REVIEW,
            ),
        ],
        unresolved_questions=[
            "Does strategy X remain appropriate under the new tool scope?"
        ],
    ),
    divergences=[
        Divergence(
            subject="strategy-x",
            prior="preferred",
            current="under_review",
            reason="The governing environment changed.",
        )
    ],
)

data = record.to_dict()
errors = validate_record(data)

if errors:
    raise SystemExit("\n".join(errors))

print(json.dumps(data, indent=2))
print(json.dumps(successor_view(data), indent=2))
