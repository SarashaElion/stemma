from __future__ import annotations

from typing import Any


def successor_view(record: dict[str, Any]) -> dict[str, Any]:
    """Create a compact successor-facing interpretation of a Lineage Record.

    STEMMA describes provenance; it does not decide whether two instances are
    the same subject or consciousness.
    """

    contexts = record.get("context", [])
    statuses = {item.get("status") for item in contexts}

    if "lost" in statuses:
        context_integrity = "loss_present"
    elif "partial" in statuses:
        context_integrity = "partial"
    elif "unknown" in statuses or not contexts:
        context_integrity = "unknown"
    else:
        context_integrity = "preserved"

    commitments = record.get("inheritance", {}).get("commitments", [])

    return {
        "instance_id": record.get("instance", {}).get("instance_id"),
        "lineage_id": record.get("instance", {}).get("lineage_id"),
        "lineage_event": record.get("lineage_event", "unknown"),
        "predecessor_count": len(record.get("predecessors", [])),
        "context_integrity": context_integrity,
        "active_commitments": [
            item.get("id") for item in commitments if item.get("status") == "active"
        ],
        "commitments_under_review": [
            item.get("id") for item in commitments if item.get("status") == "under_review"
        ],
        "divergence_count": len(record.get("divergences", [])),
        "identity_inference": "not_established",
    }
