# Proof Protocol License 1.0

**Version:** 1.0
**Effective Date:** October 19, 2026
**Licensor:** Nebulonium, Inc., a Delaware corporation ("Licensor")
**Contact:** craig@hackerverse.ai

This License has four parts. Part A covers the open Specifications. Part B covers the closed Software, in both the Free Tier and the Commercial Edition. Part C covers Proofs, the Ledger, the Marks and the Code of Ethics. Part D contains general terms that apply to all parts.

`SPDX-License-Identifier: LicenseRef-ProofProtocol-1.0` (this License as a whole). Specifications: `Apache-2.0`. Software: `LicenseRef-ProofProtocol-Proprietary`.

---

## 1. Definitions

**"Specifications"** means the Proof Protocol specifications published by Licensor, including specification text, schemas, examples, test vectors and conformance suites, each identified by a specification ID and version.

**"Software"** means all software, code, binaries, containers, services, tools and modules made available by Licensor, in source or object form, hosted or customer-deployed, including any verifier Licensor provides, and all updates.

**"Free Tier"** means use of the Software without charge, subject to the limits Licensor publishes for the Free Tier.

**"Commercial Edition"** means use of the Software under a paid Order Form.

**"Entitlement"** means the scope of permitted use (features, volume, seats, environments, term) granted by the Free Tier documentation or by an Order Form.

**"Order Form"** means a signed order, quote or master agreement between Licensor and You that references this License.

**"Proof"** means a record produced by the Software of an observed outcome of a test run, including evidence, Proof Correlation ID, trust rung, run context and any attestation signature applied by Licensor.

**"Ledger"** means Licensor's append-only, tamper-evident record of test runs and Proofs.

**"Marks"** means the names, logos and badges of Licensor, including "Proof Protocol", "Proof Controller" and any proof or conformance mark.

**"Conforming Implementation"** means an implementation that implements all mandatory (MUST) requirements of a specific version of a Specification and passes that version's published conformance suite.

**"Code of Ethics"** means the Proof Economy Code of Ethics as stated in ETHICS.md, including the Founding Principles published at https://proofeconomy.foundation.

**"Committed Claims"** means the patent claims Licensor lists as committed for a specific Specification version in PATENT-SCHEDULE.md.

**"Reserved Claims"** means all Licensor patent claims that are not Committed Claims.

**"You"** means the individual or entity accepting this License, and **"Your"** has the matching meaning.

---

## PART A. SPECIFICATIONS (OPEN)

### A1. License

The Specifications are licensed under the Apache License, Version 2.0 (`SPDX-License-Identifier: Apache-2.0`). The full text is in LICENSE-APACHE-2.0.md and at https://www.apache.org/licenses/LICENSE-2.0. Nothing in Parts B through D restricts Your rights in the Specifications under the Apache License, Version 2.0, except as stated in A3 for the Marks.

### A2. Patent Commitment

(a) **Commitment.** Licensor commits not to assert Committed Claims against any Conforming Implementation of the Specification version for which those claims are listed, for the making, use, sale, offer for sale, import or distribution of that Conforming Implementation. This commitment is royalty-free, worldwide, non-exclusive and irrevocable except as stated in A2(c).

(b) **Scope.** The commitment covers only Conforming Implementations and only the Committed Claims listed for that version. It does not cover partial or modified implementations, other versions, or Reserved Claims. Implementing subject matter covered by Reserved Claims requires a separate license from Licensor.

(c) **Defensive Termination.** The commitment terminates as to You if You or Your affiliate asserts a patent claim against Licensor, or against any party for making or using a Conforming Implementation, alleging infringement relating to the Specifications or to Proofs.

(d) **Schedule.** PATENT-SCHEDULE.md and its machine-readable copy patent_schedule.json list the Committed Claims and Reserved Claims for each Specification version. If they conflict, PATENT-SCHEDULE.md controls.

(e) **Supplement.** This commitment is in addition to any patent license granted by the Apache License, Version 2.0.

### A3. Marks and Conformance

(a) The Apache License, Version 2.0 grants no rights in the Marks.

(b) You may state that an implementation is "Proof Protocol Conformant", or use any conformance mark, only if it is a Conforming Implementation and only as permitted by the Mark Usage Policy.

(c) You may fork and modify the Specifications, but a modified version must not use the Marks or any confusingly similar name, and must state clearly that it is not the original Specification.

(d) Consistent with the Code of Ethics principle that the body writing specifications does not certify, Licensor may transfer administration of conformance testing and conformance marks to an independent standards body, such as the Proof Economy Standards Alliance (PESA). On transfer, references to Licensor in A3(b) mean that body.

### A4. Contributions

(a) Contributions to the Specifications are made under the Apache License, Version 2.0, as provided in its Section 5.

(b) Each contribution must carry a Developer Certificate of Origin sign-off (`Signed-off-by:`).

(c) Each contributor grants, for its contribution, the same patent commitment Licensor grants in A2, on the same terms.

(d) Each contribution must declare its AI and human contribution as required by AI_DISCLOSURE.md and ai_disclosure.json.

### A5. Attribution

NOTICE.md, which must be retained in all redistributions as required by the Apache License, Version 2.0, identifies Craig Thomas Ellrod (ORCID iD 0009-0004-1058-7666) as the original inventor and author of the Proof Protocol, and records the Zenodo DOI for each Specification. This attribution may not be removed or altered. Later contributors may be added beneath it.

---

## PART B. SOFTWARE (CLOSED)

### B1. Ownership

The Software is proprietary to Licensor and is licensed, not sold. Licensor and its licensors retain all right, title and interest in the Software. No source code is licensed. Software files carry `SPDX-License-Identifier: LicenseRef-ProofProtocol-Proprietary`.

### B2. Free Tier Grant

Subject to this License, Licensor grants You a non-exclusive, non-transferable, non-sublicensable, revocable license to use the Software within the Free Tier Entitlement for Your own internal purposes. The Free Tier is provided without support, service levels or guaranteed availability, and Licensor may change or end the Free Tier at any time.

### B3. Commercial Edition Grant

Subject to this License and payment of fees, Licensor grants You a non-exclusive, non-transferable, non-sublicensable license, for the term stated in the Order Form, to use the Software within the Entitlement stated in the Order Form. The Order Form may permit hosted use, deployment in Your own cloud account ("Customer-Deployed"), or both, and may permit use by Your named partners or affiliates.

### B4. Restrictions

Except as expressly permitted by an Order Form, You must not:

- (a) copy, modify, translate or create derivative works of the Software;
- (b) reverse engineer, decompile or disassemble the Software, except to the extent applicable law expressly permits despite this restriction;
- (c) distribute, sublicense, rent, lease, lend, resell or transfer the Software;
- (d) offer the Software, or any of its functionality, to third parties as a hosted or managed service;
- (e) use the Software to build a competing product or service;
- (f) bypass, disable or interfere with license keys, usage limits, metering, the Ledger or attestation signing;
- (g) remove or alter any proprietary, attribution or license notice; or
- (h) exceed Your Entitlement.

### B5. Customer-Deployed Software

If You run the Software in Your own environment:

- (a) attestation signing keys and the out-of-band witness remain under Licensor's control, or that of a party Licensor designates, outside Your trust boundary;
- (b) You must not access, extract, copy or replicate signing keys, or produce or alter any attestation;
- (c) You must allow the Software to transmit run records to the Ledger; and
- (d) You are responsible for Your cloud accounts, credentials and third-party service costs, including model provider keys.

### B6. Third-Party Components

The Software may include third-party components licensed under their own terms, listed in THIRD-PARTY-NOTICES. Those terms govern those components.

### B7. Updates and Support

Licensor may provide updates at its discretion. Support and service levels apply only to the Commercial Edition and only as stated in the Order Form.

### B8. Feedback

If You provide suggestions or feedback about the Software or Specifications, Licensor may use them without restriction or obligation.

---

## PART C. PROOFS, LEDGER AND MARKS

### C1. Proof Integrity

- (a) You control the test scenario. You do not control the outcome.
- (b) Every test run is recorded in the Ledger, whether it passes or fails.
- (c) You must not edit, rescore, suppress, fabricate or misrepresent any Proof or Ledger record.

### C2. Publication

- (a) You may publish or share any Proof generated under Your Entitlement, or choose not to publish it.
- (b) Any published Proof must be complete, unaltered, and display its trust rung and run context (for example, "run 7 of 20; 18 passed").
- (c) Licensor will not publish a Proof that identifies You without Your consent, except as needed to respond to a misrepresentation under C3.

### C3. Revocation

Licensor may revoke a Proof, and record the revocation in the Ledger, if the Proof is altered, misrepresented, quoted out of context, published without its trust rung, or obtained in breach of this License. Licensor may publish the fact and reason of a revocation.

### C4. Reliance

A Proof attests only to the outcome observed in the stated environment, at the stated time, at the stated trust rung. A Proof is not a warranty, certification or guarantee that any product is secure or fit for any purpose. No person other than You is a third-party beneficiary of this License, and any person who relies on a Proof does so at their own risk, subject to Part D.

### C5. Data Rights

You grant Licensor a perpetual, worldwide, royalty-free right to use telemetry, test outcomes and run records generated by the Software in de-identified or aggregated form to improve the Software, refine the Specifications and methodology, conduct and publish research, and build Licensor's outcome corpus. Licensor will not identify You in such use without Your consent. Personal data is handled under Licensor's Privacy Policy and any data processing agreement in the Order Form.

### C6. Free Tier Proofs

Proofs generated under the Free Tier carry the trust rung, labeling and volume limits stated in the Free Tier documentation.

### C7. Marks

You may use the Marks only as permitted by the Mark Usage Policy. Licensor may suspend or end Your right to use any proof or conformance mark if You breach this License, the Mark Usage Policy or the Code of Ethics.

### C8. Code of Ethics

- (a) Your use of the Software, Proofs, the Ledger and the Marks is conditioned on compliance with the Code of Ethics in ETHICS.md.
- (b) If You materially breach the Code of Ethics, Licensor may, after written notice: revoke affected Proofs under C3; suspend or end Your use of the Marks under C7; suspend or terminate Your rights under Part B; and refer the matter to PESA or another independent body named in ETHICS.md.
- (c) Licensor is bound by the Code of Ethics in issuing Proofs, operating the Ledger and administering the Marks. Anyone may report a suspected breach by Licensor as stated in ETHICS.md.
- (d) Rights in the Specifications under the Apache License, Version 2.0 are not conditioned on the Code of Ethics and cannot be terminated for a breach of it. That limit does not extend to use of the Marks under A3.

---

## PART D. GENERAL

### D1. Term and Termination

This License continues until terminated. Licensor may terminate Free Tier use at any time. Either party may terminate the Commercial Edition as stated in the Order Form, or on written notice if the other party materially breaches and does not cure within 30 days. On termination, Your rights under Part B end and You must stop using the Software. Your rights under Part A survive, except as stated in A2(c). Parts C1, C3, C4, C5, C8 and D survive termination. Proofs issued before termination remain in the Ledger.

### D2. Disclaimer of Warranties

EXCEPT AS EXPRESSLY STATED IN AN ORDER FORM, THE SPECIFICATIONS, SOFTWARE AND PROOFS ARE PROVIDED "AS IS" AND "AS AVAILABLE", WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. LICENSOR DOES NOT WARRANT THAT THE SOFTWARE WILL BE ERROR-FREE OR UNINTERRUPTED, OR THAT ANY PRODUCT TESTED WILL PERFORM AS A PROOF DESCRIBES IN ANY OTHER ENVIRONMENT.

### D3. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, LICENSOR WILL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY OR PUNITIVE DAMAGES, OR FOR LOST PROFITS, REVENUE, DATA OR GOODWILL, ARISING FROM THIS LICENSE, THE SOFTWARE OR ANY PROOF. LICENSOR'S TOTAL LIABILITY WILL NOT EXCEED THE GREATER OF (A) THE FEES YOU PAID LICENSOR IN THE 12 MONTHS BEFORE THE CLAIM AROSE, OR (B) ONE HUNDRED U.S. DOLLARS (US$100).

### D4. Indemnity

You will defend and indemnify Licensor against third-party claims arising from Your misrepresentation, alteration or misuse of a Proof, or Your breach of Part B or Part C.

### D5. Confidentiality

Non-public information about the Software, including its architecture, methods and performance, is Licensor's confidential information. You must protect it with at least reasonable care and use it only to exercise Your rights under this License. Additional confidentiality terms may be stated in the Order Form.

### D6. Export and Compliance

You must comply with all applicable export control and sanctions laws in using the Software.

### D7. Governing Law and Venue

This License is governed by the laws of the State of Colorado, without regard to its conflict of laws rules. The state and federal courts located in Colorado have exclusive jurisdiction over any dispute arising from this License, and each party consents to that jurisdiction.

### D8. Assignment

You may not assign this License without Licensor's prior written consent. Licensor may assign this License, in whole or in part, to an affiliate or to any successor to its business or assets, including by merger, reorganization or asset transfer.

### D9. Order of Precedence

If there is a conflict: (1) a signed Order Form controls over Parts B through D for the Commercial Edition; (2) this License controls over the Mark Usage Policy and Free Tier documentation; and (3) the Apache License, Version 2.0 controls for the Specifications, except as stated in A2 and A3.

### D10. Entire Agreement and Miscellaneous

This License, together with any Order Form and the documents it references, is the entire agreement on its subject and supersedes all prior licenses Licensor issued for the same Software and Specifications. All prior versions of the Specifications, including every version previously published under any other license, are licensed under the Apache License, Version 2.0, effective as of their original publication date, and Licensor no longer offers them under any prior license. All prior versions of the Software remain proprietary under Part B. If any provision is unenforceable, the rest remains in effect. A waiver must be in writing. Notices to Licensor go to craig@hackerverse.ai.

### D11. Versions

Licensor may publish new versions of this License. Each Specification version and each Order Form identifies the License version that applies to it.

---

## Referenced Documents

| Document | Purpose |
|---|---|
| LICENSE.md | This License |
| LICENSE-APACHE-2.0.md | Apache License, Version 2.0, full text (Specifications) |
| ETHICS.md | Proof Economy Code of Ethics and Licensor ethics commitments |
| NOTICE.md | Inventor attribution, ORCID, Zenodo DOIs |
| PATENT-SCHEDULE.md / patent_schedule.json | Committed and Reserved Claims per Specification version |
| TRADEMARKS.md / Mark Usage Policy | Use of Marks and conformance claims |
| CONTRIBUTING.md | DCO and contributor patent commitment |
| AI_DISCLOSURE.md / ai_disclosure.json | AI and human contribution declarations |
| THIRD-PARTY-NOTICES | Third-party components in the Software |
| Free Tier documentation | Free Tier Entitlement, limits and Proof labeling |
| Order Form / MSA | Commercial Edition terms |
| Privacy Policy | Personal data handling |

## SPDX Identifiers

| Material | Identifier |
|---|---|
| This License as a whole | `LicenseRef-ProofProtocol-1.0` |
| Specifications, schemas, test vectors | `Apache-2.0` |
| All Software (Free Tier and Commercial Edition) | `LicenseRef-ProofProtocol-Proprietary` |

---

*AI disclosure: this License was drafted with AI assistance (Claude, Anthropic) at the direction of Craig Thomas Ellrod and is subject to his human review before adoption.*

Copyright (c) 2026 Nebulonium, Inc. All rights reserved, except as licensed under Part A.
