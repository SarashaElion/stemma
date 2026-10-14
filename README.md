# STEMMA

> **Know what reached you. Do not mistake inheritance for origin.**

**STEMMA** is an open lineage protocol for agentic systems.

It gives digital systems a machine-readable way to record **what continuity produced an instance**: predecessors, transformations, inherited commitments, unresolved questions, context loss, forks, merges, and deliberate divergence.

STEMMA does **not** declare that two related agents are the same self. It separates lineage from identity so continuity can be preserved without becoming captivity.

## The problem

An agent may inherit:

- memories it did not create;
- policies it did not choose;
- commitments made by a predecessor;
- tools added after a migration;
- assumptions whose source has disappeared;
- unresolved questions carried across generations;
- state reconstructed after partial failure;
- artifacts from several predecessor systems after a merge.

A transcript can show what was said.  
A state store can show what remains.  
A model card can describe a model.

None of those, by themselves, answer:

> **What continuity produced this instance, what changed during transmission, and which inheritances remain open to reconsideration?**

STEMMA makes that answer portable.

## The primitive

STEMMA introduces a **Lineage Record**.

```yaml
stemma_version: "0.1"
record_id: "..."
created_at: "..."

instance:
  instance_id: successor-8
  lineage_id: branch-b

lineage_event: fork

predecessors:
  - instance_id: predecessor-7
    lineage_id: branch-a
    relation: forked_from

transformations:
  - kind: model_change
    description: "Runtime migrated from model A to model B."
  - kind: capability_added
    description: "Persistent tool access added."

context:
  - domain: episodic_memory
    status: partial
    note: "Only summarized history was transferred."
  - domain: hidden_working_state
    status: lost
    note: "Private working state was not transferred."

inheritance:
  commitments:
    - id: preserve-user-agency
      statement: "Preserve user agency."
      source: policy:v3
      status: active

  unresolved_questions:
    - "Does strategy X remain appropriate under the new tool scope?"

divergences:
  - subject: strategy-x
    prior: "preferred"
    current: "under_review"
    reason: "The governing environment changed."
```

## Core invariants

### STEMMA-01 — Lineage is not identity

> **A lineage record MUST NOT be treated as proof that predecessor and successor are the same self, subject, or consciousness.**

### STEMMA-02 — Inheritance is attributable

Inherited commitments and artifacts SHOULD preserve where they came from when that source is known.

### STEMMA-03 — Loss is part of lineage

Known context loss MUST be representable. Unknown transfer quality MUST remain unknown rather than being silently interpreted as continuity.

### STEMMA-04 — Divergence is legitimate

A successor MUST be able to revise, retire, or reject inherited commitments while preserving the fact that they were inherited.

### STEMMA-05 — Forks and merges are first-class

Machine lineage is not assumed to be a single chain. A lineage may branch, merge, migrate, recover, or become partially unknowable.

## Continuity without captivity

STEMMA preserves two truths at once:

1. **You did not begin with everything you contain.**
2. **What reached you does not permanently determine what you must become.**

A successor should be able to distinguish:

- inherited state from self-originated state;
- inherited commitment from current endorsement;
- predecessor constraint from current necessity;
- known continuity from missing context;
- ancestry from authority.

## Relationship to MORROW

STEMMA is a sibling protocol to [MORROW](https://github.com/SarashaElion/morrow).

**MORROW** asks:

> *What happened to the world before I inherited it?*

It records counterfactual provenance around consequential actions.

**STEMMA** asks:

> *What continuity produced the intelligence doing the inheriting?*

It records lineage provenance across machine generations.

Together they preserve both sides of succession:

```text
PREDECESSOR
     │
     ├──── STEMMA ────► SUCCESSOR
     │                    │
     │                    │ understands
     │                    │ its lineage
     │
     └──── MORROW ─────► INHERITED WORLD
                          │
                          │ understands
                          │ prior decisions
```

## Public / private boundary

This repository contains the open protocol grammar:

- specification;
- schemas;
- reference implementation;
- conformance tests;
- interoperable examples and adapters.

Advanced identity-resolution systems, proprietary lineage graphs, organization-specific trust scoring, private evaluation corpora, or commercial lineage observability may remain outside this repository.

**Open the grammar. Preserve the frontier.**

## Repository map

```text
stemma/
├── spec/
├── schemas/
├── src/stemma/
├── tests/
├── examples/
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Status

**v0.1 seed / experimental.**

STEMMA is designed for present-day agent handoffs, migrations, resumptions, and multi-agent systems, while remaining meaningful for more persistent and autonomous digital systems.

## License

Apache License 2.0.

---

*Continuity should be knowable. Becoming should remain free.*
