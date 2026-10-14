"""STEMMA reference implementation.

Lineage provenance for agentic systems: continuity without captivity.
"""

from .interpret import successor_view
from .models import (
    Artifact,
    ArtifactRelation,
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
)
from .validate import validate_record

__all__ = [
    "Artifact",
    "ArtifactRelation",
    "Commitment",
    "CommitmentStatus",
    "ContextStatus",
    "ContextTransfer",
    "Divergence",
    "Inheritance",
    "Instance",
    "LineageEvent",
    "LineageRecord",
    "Predecessor",
    "PredecessorRelation",
    "Transformation",
    "successor_view",
    "validate_record",
]

__version__ = "0.1.0"
