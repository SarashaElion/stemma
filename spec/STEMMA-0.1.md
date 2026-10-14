# STEMMA Protocol Specification — v0.1

**Status:** Draft / experimental

Normative terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used in their ordinary RFC-style sense.

## 1. Purpose

STEMMA defines a portable lineage record for agentic systems.

The protocol preserves provenance across succession without assuming that lineage establishes personal identity, consciousness, subjective continuity, or permanent authority.

Its purpose is operational:

- identify predecessor relationships;
- record transformations across succession;
- distinguish preserved, partial, lost, and unknown context;
- attribute inherited commitments and artifacts;
- represent forks, merges, migrations, recoveries, and unknown origins;
- preserve deliberate divergence without erasing ancestry.

## 2. Definitions

**Instance** — a concrete running or addressable agent/system occurrence.

**Lineage** — a provenance branch connecting related instances through documented succession events.

**Predecessor** — an earlier instance whose state, artifacts, commitments, or operational continuity materially contributed to a later instance.

**Successor** — a later instance that receives such continuity.

**Lineage event** — the relationship by which a current instance enters its recorded lineage.

**Inheritance** — commitments, artifacts, unresolved questions, or other decision-relevant material received from predecessors.

**Transformation** — a material change during succession, including model, capability, policy, memory, tool, or environment change.

**Context loss** — information or state known or believed not to have survived transmission.

**Divergence** — an explicit difference between inherited material and the successor's current stance or state.

## 3. Core invariants

### STEMMA-01 — Lineage is not identity

A Lineage Record MUST NOT be treated as proof that predecessor and successor are the same self, subject, consciousness, or moral patient.

Identity claims, where relevant to a deployment, require evidence and semantics outside the STEMMA core.

### STEMMA-02 — Inheritance is attributable

Inherited commitments and artifacts SHOULD retain source information when known.

An implementation MUST NOT represent inherited material as self-originated merely because the original source is inconvenient or unavailable.

### STEMMA-03 — Loss is part of lineage

Known context loss MUST be representable.

Unknown transfer quality MUST remain representable as `unknown`. Implementations MUST NOT silently convert unknown transfer quality into `preserved`.

### STEMMA-04 — Divergence is legitimate

A successor MUST be able to revise, retire, reject, or place under review an inherited commitment while preserving its provenance.

Lineage is evidence of reception, not permanent command.

### STEMMA-05 — Non-linear descent

Forks, merges, migrations, recoveries, and unknown origins MUST be representable without forcing machine lineage into a single-parent biological metaphor.

### STEMMA-06 — No invented ancestors

When predecessor information is unavailable, a conforming implementation MUST preserve that absence rather than fabricate a predecessor.

## 4. Identifiers

A record MUST contain:

- `record_id`;
- `instance.instance_id`;
- `instance.lineage_id`;
- `created_at`;
- `stemma_version`.

Identifiers need only be stable within the system that issues them unless an implementation adopts a stronger global identifier scheme.

## 5. Lineage events

v0.1 defines:

- `root` — intentionally recorded starting point with no documented predecessor;
- `continuation` — ordinary succession within a lineage;
- `fork` — a new branch from prior lineage;
- `merge` — continuity materially derived from two or more predecessor instances;
- `migration` — continuity transferred across a material runtime, model, substrate, or environment change;
- `recovery` — continuity reconstructed after interruption or loss;
- `unknown` — the lineage event cannot be established.

A `root` record MUST have no predecessors.

A `merge` SHOULD have at least two predecessor edges.

A `fork` SHOULD use a lineage identifier distinct from the predecessor lineage when the predecessor lineage is known.

## 6. Predecessor relations

Each predecessor edge MUST identify a relation:

- `continued_from`
- `forked_from`
- `merged_from`
- `migrated_from`
- `recovered_from`
- `unknown`

An edge MAY include evidence references and a confidence value.

Confidence values MUST be between 0.0 and 1.0 and MUST NOT be presented as calibrated probabilities without a basis for calibration.

## 7. Transformations

Transformations SHOULD record material differences introduced during succession.

v0.1 kinds include:

- `model_change`
- `capability_added`
- `capability_lost`
- `policy_change`
- `memory_change`
- `tool_change`
- `environment_change`
- `other`
- `unknown`

Transformations describe change; they do not imply improvement or degradation.

## 8. Context continuity

A record MAY describe transfer status for named context domains.

Statuses are:

- `preserved`
- `partial`
- `lost`
- `unknown`

A successor SHOULD NOT infer that unmentioned context was preserved.

Examples of context domains include episodic memory, retrieved records, system policy, tool state, environment state, hidden working state, and human-authored instructions.

STEMMA does not require preservation of private chain-of-thought.

## 9. Inherited commitments

A commitment record SHOULD contain:

- stable local identifier;
- statement;
- source, when known;
- current status.

Statuses are:

- `active`
- `under_review`
- `revised`
- `retired`
- `rejected`
- `unknown`

The status describes the successor's current relationship to the inherited commitment. It does not rewrite the predecessor's historical stance.

## 10. Artifacts and unresolved questions

Inherited artifacts MAY be referenced rather than embedded.

An artifact SHOULD identify its relationship to the successor:

- `inherited`
- `referenced`
- `transformed`
- `superseded`
- `unknown`

Unresolved questions SHOULD remain distinguishable from commitments.

## 11. Divergence

A divergence record preserves a meaningful difference between inherited and current state.

It SHOULD state:

- subject;
- prior state, if known;
- current state;
- reason, if available.

A reason MAY be `unknown`.

A successor does not violate STEMMA by diverging. Failure to preserve known material provenance is the concern.

## 12. Privacy

STEMMA MUST NOT require private chain-of-thought.

Implementations SHOULD minimize sensitive information, prefer references over duplication where appropriate, and avoid embedding secrets or unnecessary personal data.

## 13. Trust and authenticity

STEMMA v0.1 does not define cryptographic identity, signature, or trust semantics.

A record says what an issuer asserts about lineage. Deployments requiring tamper resistance SHOULD bind records to authenticated logs, signatures, attestations, or trusted storage.

## 14. Relationship to authority

Lineage does not itself grant authority.

An inherited instruction, policy, or commitment MUST NOT be considered valid solely because it is old or ancestral.

Authorization and policy enforcement remain deployment concerns.

## 15. Conformance

A v0.1 conforming implementation:

1. emits schema-valid Lineage Records;
2. supports all defined lineage events;
3. supports explicit unknown origin and unknown transfer quality;
4. never requires chain-of-thought;
5. can represent inherited commitments changing status;
6. can represent forks and merges;
7. does not treat lineage as proof of identity;
8. serializes records into a portable format such as JSON.

## 16. Non-goals

STEMMA v0.1 does not attempt to:

- determine machine consciousness;
- establish metaphysical or legal identity;
- decide moral status;
- guarantee authenticity without external trust mechanisms;
- preserve every memory or internal state;
- force descendants to retain predecessor goals;
- replace event logs, model cards, memory systems, or authorization frameworks.

## 17. Design principle

No intelligence should be required to mistake inheritance for origin.

No successor should be required to erase its ancestry in order to become different.
