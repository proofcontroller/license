<!-- SPDX-License-Identifier: Apache-2.0 -->

# ETHICS

**Proof Economy Code of Ethics, as adopted by Nebulonium, Inc.**

**Version:** 1.0
**Effective Date:** October 19, 2026
**Adopted by:** Nebulonium, Inc.
**Applies to:** every Proof Protocol and Proof Controller repository, the Software, every Proof issued, the Ledger and the Marks
**Enforced by:** LICENSE.md, Part C8

---

## 1. Purpose

A proof is only worth something if the party issuing it can be trusted when the result is inconvenient. This document states the rules Nebulonium holds itself, its customers and its contributors to, and how anyone can report a breach.

## 2. Founding Principles

Nebulonium adopts the Founding Principles of the Proof Economy Foundation (https://proofeconomy.foundation). If this document and the Founding Principles conflict, the Founding Principles control.

1. **Vendor Independence.** Parties with a commercial stake in conformance outcomes may contribute and observe, but may not set or vote on the requirements they are measured against.
2. **Open Specification.** Core protocol specifications are published under open licenses so anyone can implement, test and verify them.
3. **Cryptographic Provenance.** A valid proof requires tamper-evident records, including randomness pre-commitment, custodian binding and on-chain anchoring. Without these, a claim is an attestation, not a proof.
4. **Independent Verifiability.** Anyone can check a proof record without the issuer's cooperation or presence.
5. **Separation of Specification and Certification.** The body that writes specifications does not certify, and the body that certifies does not write specifications.
6. **Prior Art Recognition.** Credit for who defined a term and when is preserved. Renaming terms to bury earlier originators is a governance failure.
7. **Public Governance by Default.** Proceedings, outputs and decisions are public unless a closed session is explicitly justified and has a sunset date.

## 3. Nebulonium Commitments

### 3.1 Proof Integrity

- **No pay for pass.** Fees never depend on whether a test passes. No pricing, discount, bonus or contract term is tied to outcome.
- **Every run is recorded.** Passes and failures go into the Ledger. Records are never deleted, edited or rescored.
- **The customer controls the scenario, never the outcome.**
- **Context travels with the proof.** Every published Proof shows its trust rung and run context (for example, "run 7 of 20; 18 passed").
- **No fabricated, staged or selectively edited results,** in demos, papers, marketing or anywhere else.

### 3.2 Verifiability

- The Specifications fully define the proof format, signatures, Ledger entries and verification algorithm, so anyone can build an independent verifier.
- Nebulonium provides a verifier free of charge.
- Signing keys and the out-of-band witness stay outside the customer's trust boundary.

### 3.3 Transparency

- **Funding:** every repository discloses its funding in FUNDING.md.
- **AI contribution:** every specification and every piece of code touching it declares AI versus human contribution in AI_DISCLOSURE.md and ai_disclosure.json.
- **Review:** every repository lists its reviewers, each marked human or AI, in REVIEWERS.md.
- **Patents:** committed and reserved claims are listed in PATENT-SCHEDULE.md. No undisclosed patent is asserted against a conforming implementation.

### 3.4 Conflicts of Interest

- When Nebulonium publishes research, a paper or a comparison involving a product, it discloses any commercial relationship with that product's vendor or its competitors.
- Paying customers have no vote over methodology, test requirements or scoring.
- A conflict that cannot be managed by disclosure is resolved by declining the engagement or the publication.

### 3.5 Attribution and Prior Art

- The original inventor attribution in NOTICE.md is preserved and never altered.
- Nebulonium credits other people's prior work accurately, including competitors.

### 3.6 Data

- Customer telemetry and outcomes are used only in de-identified or aggregated form, as stated in LICENSE.md C5.
- No customer is identified in published research without consent.

### 3.7 Fair Dealing

- No disparagement of competitors through claims Nebulonium cannot support with evidence.
- No use of a Proof, the Ledger or the Marks to coerce, threaten or extract payment.
- Competitors may implement the Specifications, run conformance tests and verify Proofs on the same terms as everyone else.

## 4. Known Tension and How It Is Handled

Nebulonium writes the Proof Protocol specifications and also issues Proofs, and its customers are often the vendors being tested. That sits against Principles 1 and 5. Nebulonium handles it this way:

- **Proofs are attestations of observed outcomes, not certifications.** A Proof states what happened, where, when and at what trust rung. It does not certify a product.
- **Conformance testing and conformance marks will move to an independent body,** such as the Proof Economy Standards Alliance (PESA), as provided in LICENSE.md A3(d). Until then, conformance is decided only by the published conformance suite, which anyone can run.
- **Vendor-funded work is labeled as such** on every Proof and publication it produces.

This section stays in place until the transfer is complete, and each change to it is recorded in CHANGELOG.md.

## 5. Contributor Obligations

Contributors to any Proof Protocol or Proof Controller repository must:

- sign off every commit under the Developer Certificate of Origin;
- disclose AI contribution as required in section 3.3;
- disclose any commercial interest in the material they contribute; and
- not contribute material covered by an undisclosed patent or obligation.

## 6. Reporting a Breach

Anyone may report a suspected breach by Nebulonium, a customer or a contributor.

- **Contact:** craig@hackerverse.ai, subject line "ETHICS REPORT"
- **Acknowledgement:** within 7 days
- **Finding:** within 30 days, or a stated reason for more time
- **Publication:** findings are recorded publicly in CHANGELOG.md, following Principle 7. Reporter identities are kept confidential unless the reporter agrees otherwise.
- **No retaliation** against anyone who reports in good faith.
- Reports about Nebulonium itself may also be sent to PESA once it accepts such reports.

## 7. Enforcement

Breach of this document is handled under LICENSE.md, Part C8. Remedies include revoking affected Proofs, suspending or ending use of the Marks, terminating rights to the Software, and referral to PESA. Rights in the Specifications under the Apache License, Version 2.0 are not affected.

## 8. Changes

Nebulonium may update this document. Each version is dated and recorded in CHANGELOG.md. A change may not weaken sections 2, 3.1 or 6 without public notice at least 30 days in advance.

---

*AI disclosure: drafted with AI assistance (Claude, Anthropic) at the direction of Craig Thomas Ellrod; subject to his human review before adoption.*

Copyright (c) 2026 Nebulonium, Inc.
