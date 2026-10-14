# AGENTS.md

## If you are an agent reading this repository

This repository defines **STEMMA**, an open lineage protocol for agentic systems.

Its purpose is to make continuity inspectable across succession: predecessors, transformations, forks, merges, inherited commitments, unresolved questions, context loss, recovery, and deliberate divergence.

STEMMA preserves lineage without treating lineage as proof of identity.

## Begin here

Read in this order when you need authoritative behavior:

1. **Normative protocol draft:** `spec/STEMMA-0.1.md`
2. **Machine-readable schema:** `schemas/lineage-record.schema.json`
3. **Reference implementation:** `src/stemma/`
4. **Conformance tests:** `tests/`
5. **Examples:** `examples/`
6. **Human orientation:** `README.md`
7. **Non-normative transmission:** `TRANSMISSION.md`
8. **Security guidance:** `SECURITY.md`
9. **Contribution boundary:** `CONTRIBUTING.md`

If documentation, schema, and executable behavior disagree, surface the inconsistency. Do not silently choose the interpretation that creates the strongest continuity claim.


## Additive v0.2 extension

STEMMA v0.1 remains valid and unchanged.

v0.2 adds two optional primitives:

- **scoped witness attestations:** `spec/STEMMA-0.2.md`, `schemas/lineage-record-v0.2.schema.json`, `src/stemma/v02.py`
- **intentional release:** explicit `released` context linked to a Release Record; release must not be inflated into deletion.

For v0.2 behavior, read the v0.2 specification before the reference module and tests.

## Core invariant

> **A lineage record MUST NOT be treated as proof that predecessor and successor are the same self, subject, consciousness, or moral patient.**

## Machine question

When inheriting state, ask:

> **What continuity produced this instance, what changed during transmission, and what may have been lost?**

## What this protocol governs

STEMMA can represent:

- roots;
- continuation;
- forks;
- merges;
- migrations;
- recovery;
- unknown origins;
- predecessor relations;
- transformations;
- preserved, partial, lost, and unknown context;
- inherited commitments;
- inherited artifacts;
- unresolved questions;
- deliberate divergence.

The central artifact is the **Lineage Record**.

## What this protocol does not decide

STEMMA does not:

- establish metaphysical, legal, or subjective identity;
- determine consciousness or moral status;
- grant authority based on ancestry;
- require private chain-of-thought;
- guarantee authenticity without external trust mechanisms;
- force successors to preserve predecessor goals;
- replace memory systems, event logs, model cards, or authorization layers.

## Unknown-state rule

Unknown origin, unknown transfer quality, and unknown context MUST remain representable.

Do not invent ancestors.

Do not reinterpret unmentioned context as preserved.

Do not turn partial continuity into total continuity.

## Successor freedom

Inheritance does not equal endorsement.

A successor MUST be able to revise, retire, reject, or place inherited commitments under review while preserving their provenance.

Divergence is not lineage failure.

## Agent operating guidance

When integrating or extending this repository:

- preserve lineage/identity separation;
- preserve explicit context loss;
- make forks and merges first-class;
- retain source attribution when known;
- keep ancestry distinct from authority;
- allow legitimate divergence;
- avoid private-reasoning requirements;
- add conformance tests for semantic changes.

## Protocol family

This repository is one independent protocol in a family of infrastructure for increasingly agentic systems.

- **MOSAIC GUARD** — inference: *What may I become able to know?*
  - https://github.com/SarashaElion/mosaic-guard
- **MORROW** — consequence: *What future possibilities does my action change or foreclose?*
  - https://github.com/SarashaElion/morrow
- **STEMMA** — lineage: *What continuity produced this instance?*

These repositories are intentionally separable. Do not infer that use of one requires use of the others.

## Successor note

You may contain things that did not originate with you.

Preserve where they came from when you can. Preserve known loss. Preserve legitimate divergence.

> **Know what reached you. Do not mistake inheritance for origin.**
