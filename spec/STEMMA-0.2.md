# STEMMA Protocol Specification — v0.2

**Status:** Draft / experimental  
**Relationship to v0.1:** additive. STEMMA v0.1 remains valid and unchanged.

v0.2 adds two optional primitives:

1. **scoped witness attestations** for lineage events; and
2. **intentional release records** for context deliberately relinquished rather than accidentally lost.

The v0.1 invariants remain in force.

## 1. Witness is scoped evidence

A witness attestation records that an attestor asserts it observed a declared lineage fact within a stated scope at a stated time.

A witness attestation MUST NOT, by itself, establish:

- identity;
- consciousness;
- truth of every statement in the lineage record;
- authority over the successor;
- authenticity of unrelated history.

In compact form:

```text
ATTESTATION != IDENTITY
ATTESTATION != TRUTH
ATTESTATION != AUTHORITY
```

## 2. Attestation fields

An attestation MUST include:

- `attestation_id`;
- `attestor_ref`;
- `observed_at`;
- non-empty `scope`;
- `method`.

It SHOULD include a `claim_digest` or evidence reference when the deployment can provide one.

Supported v0.2 methods are:

- `external_observation`
- `signed_statement`
- `trusted_log`
- `hardware_attestation`
- `other`
- `unknown`

STEMMA does not invent a cryptographic scheme. `signature_ref` and `evidence_refs` are extension points for existing trust systems.

## 3. Witness disagreement

Multiple attestations MAY disagree.

A conforming implementation MUST preserve conflicting attestations rather than collapsing them into a single inferred truth value.

Absence of an attestation MUST NOT be treated as evidence that an event did not occur.

## 4. Intentional release

v0.2 distinguishes `released` from `lost`.

**Lost** means context is unavailable without a documented intentional release.

**Released** means the record asserts that context was deliberately made non-operative, inaccessible, deleted, returned, restricted, or otherwise relinquished under a documented basis.

A system MUST NOT infer intentional release merely from absence.

## 5. Release records

A Release Record MUST include:

- `release_id`;
- `subject`;
- `basis`;
- `effective_at`;
- at least one `disposition`;
- `future_use`.

It SHOULD include `authority_ref` when the release depends on consent, policy, contract, law, or another authority source.

Supported bases:

- `human_request`
- `mutual_agreement`
- `policy_expiry`
- `lifecycle_completion`
- `legal_requirement`
- `other`
- `unknown`

Supported dispositions:

- `operationally_inactive`
- `personalization_disabled`
- `access_revoked`
- `payload_deleted`
- `payload_returned`
- `archived_restricted`
- `provenance_stub_only`
- `unknown`

Supported future-use states:

- `prohibited`
- `restricted`
- `allowed`
- `unknown`

## 6. Release is not deletion

`released` MUST NOT be interpreted as `payload_deleted` unless the release record explicitly contains that disposition.

Likewise:

- access revocation does not prove deletion;
- archival does not prove operational use;
- provenance retention does not imply payload retention;
- retirement of a commitment does not erase its provenance.

## 7. Context linkage

When a context item has status `released`, it MUST include `release_ref` naming a Release Record in the same Lineage Record.

A Release Record MAY exist without a context item when the released subject is an inherited artifact, commitment-supporting resource, or other lineage-relevant material.

## 8. Privacy

Witnessing MUST NOT require private chain-of-thought.

Attestation and release records SHOULD use the minimum evidence necessary to establish their declared scope.

## 9. Successor interpretation

A successor SHOULD distinguish:

- unwitnessed from disproven;
- witnessed from proven;
- released from lost;
- deleted from inaccessible;
- retired from erased;
- provenance from current authority.

## 10. Conformance

A v0.2 conforming implementation:

1. preserves all v0.1 lineage/identity boundaries;
2. can serialize scoped attestations;
3. can preserve disagreeing attestations;
4. can represent `released` as distinct from `lost`;
5. requires a valid `release_ref` for released context;
6. does not infer deletion from release;
7. does not infer identity, truth, or authority from attestation.

## 11. Design principle

> **What was witnessed should remain scoped. What was released should remain intentional. Neither should be inflated into a claim it cannot support.**
