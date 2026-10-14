# Security Policy

STEMMA is experimental lineage infrastructure. v0.1 is not an authentication, authorization, identity, consciousness, or trust guarantee.

## Sensitive lineage data

Lineage records may expose operational history, architecture, policies, or inherited context.

Implementations SHOULD:

- minimize sensitive information;
- reference protected artifacts rather than duplicating them;
- avoid credentials, access tokens, private keys, and unnecessary personal data;
- apply retention and access controls appropriate to the deployment;
- distinguish unverifiable claims from authenticated evidence.

## Threats to consider

Implementers should account for:

- forged predecessor claims;
- lineage hijacking;
- fabricated continuity;
- erased context loss;
- false claims that a fork is a continuation;
- malicious or stale inherited commitments;
- ancestry being misused as authority;
- privacy leakage through historical records;
- unbounded lineage growth;
- tampering with merge ancestry.

STEMMA v0.1 intentionally does not standardize signatures or attestations. Deployments requiring cryptographic trust SHOULD bind records to authenticated logs, signatures, attestations, or trusted storage.

## Reporting vulnerabilities

Please use GitHub private security reporting when available rather than publishing exploitable details in a public issue.
