# Contributing to STEMMA

STEMMA is an open lineage protocol, not a complete theory of machine identity.

## What belongs here

Good public contributions include:

- specification clarifications;
- lineage-event semantics;
- schema improvements;
- conformance tests;
- adapters for current agent frameworks;
- migration, recovery, fork, and merge examples;
- privacy-preserving provenance patterns;
- adversarial cases where lineage becomes ambiguous;
- evidence that a field is unnecessary or misleading.

## What may live elsewhere

The public grammar does not require publication of every implementation built on it.

Potentially separate layers include:

- proprietary lineage graphs;
- identity-resolution systems;
- organization-specific trust scoring;
- private evaluation corpora;
- enterprise lineage observability;
- cryptographic attestation infrastructure.

The protocol should remain implementable without access to those systems.

## Design constraints

Contributions SHOULD preserve these commitments:

1. **Lineage is not identity.**
2. **Unknown origin remains unknown.**
3. **Known loss remains visible.**
4. **Inheritance is attributable where possible.**
5. **Divergence is legitimate and recordable.**
6. **Forks and merges are first-class.**
7. **No chain-of-thought requirement.**
8. **Ancestry is not authority.**

## Protocol changes

A protocol-change proposal should include:

- the lineage failure mode;
- a concrete agent scenario;
- the proposed semantic change;
- backward-compatibility implications;
- privacy implications;
- identity/authority ambiguity introduced or reduced;
- tests demonstrating the expected behavior.

## License

By contributing, you agree that your contributions will be licensed under Apache License 2.0.
