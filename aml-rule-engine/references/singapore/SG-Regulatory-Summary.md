# Singapore DPT Regulatory Summary (MAS Compliance Cheat Sheet)

**Purpose**: Consolidated reference for AML/CFT compliance analysis in Singapore.
**Primary Source**: MAS Notice PSN02 (2025 Amendment), Guidelines to PSN02, Payment Services Act 2019.

---

## 1. Customer Due Diligence (CDD)

### 1.1 Triggers (When to perform CDD)
*   **Business Relations**: When establishing business relations.
*   **Occasional Transactions**: 
    *   Any transaction exceeding **S$5,000** (or equivalent).
    *   All Value Transfers (Travel Rule) exceeding **S$1,500**.
*   **Suspicion**: Any suspicion of ML/TF, regardless of amount.
*   **Doubts**: Doubts about veracity of previously obtained info.

### 1.2 Enhanced Due Diligence (EDD)
Must be performed for **High Risk** situations:
*   **PEPs**: Politically Exposed Persons (Domestic, Foreign, International Organization).
*   **High Risk Jurisdictions**: FATF black/grey list, or internal high risk.
*   **Anonymity**: Products/transactions favoring anonymity (Mixers, Privacy Coins).
*   **Complex Transactions**: Usually large, complex, or unusual patterns with no economic purpose.

**EDD Measures**:
*   Obtain Senior Management approval.
*   Establish **Source of Wealth (SoW)** and **Source of Funds (SoF)**.
*   Enhanced ongoing monitoring.

---

## 2. Travel Rule (Value Transfers)

**Regulation**: MAS Notice PSN02 Part 8.

### 2.1 Threshold
*   **> S$1,500**: Full Travel Rule applies.
*   **< S$1,500**: Simplified requirements (Name + Account Maintained).

### 2.2 Required Information (IVMS101 Standard)
**Originator**:
*   Name
*   Account Number (or unique transaction ID)
*   Address OR National ID OR Date & Place of Birth

**Beneficiary**:
*   Name
*   Account Number (or unique transaction ID)

**Obligations**:
*   **Ordering VASP**: Transmit data *immediately*.
*   **Beneficiary VASP**: Verify identity, screen, and check for missing data.
*   **Unhosted Wallets**: Perform risk assessment; for >S$1,500 not possible to transmit to protocol, but must collect/verify owner if it's the customer.

---

## 3. Sanctions & Prohibitions

**Regulation**: MAS Notice PSN02 Part 11; TSOFA; United Nations Act.

### 3.1 Screening
*   Must screen **all customers** and **counterparties** against:
    *   UN Security Council Consolidated List.
    *   Singapore Designated Individuals and Entities.

### 3.2 Action
*   **Positive Match**: 
    *   **FREEZE** funds immediately.
    *   **PROHIBIT** transaction.
    *   **REPORT** to MAS/Police.

---

## 4. Suspicious Transaction Reporting (STR)

**Regulation**: CDSA Section 45; TSOFA Sections 8, 10.

### 4.1 Triggers
*   **Reasonable Grounds**: Known or suspected connection to criminal conduct.
*   **Red Flags**: Matches indicators in SG-010 (see below).
*   **Adverse Media**: Negative news screening hits.

### 4.2 Procedure
*   File with **STRO** (Suspicious Transaction Reporting Office) via SONAR.
*   **Timeline**: "As soon as reasonably practicable".
*   **No Tipping Off**: Strictly prohibited to disclose STR filing to customer.

---

## 5. Red Flag Indicators (DPT Specific)

**Source**: SG-010-DPT-Red-Flag-Indicators.md

### 5.1 Wallet/Tech Risks
*   **Mixers/Tumblers**: Interaction with mixing services (e.g., Tornado Cash).
*   **Privacy Coins**: usage of Monero, Zcash, etc.
*   **Darknet**: Direct/Indirect exposure to darknet markets (Hydra, etc.).
*   **Unhosted Wallets**: High volume transfers to/from P2P/unhosted wallets without clear purpose.

### 5.2 Transaction Patterns
*   **Structuring (Smurfing)**: Multiple transactions just below S$5,000 or S$1,500 thresholds.
*   **Rapid Movement**: Funds deposited and immediately withdrawn/converted.
*   **Looping**: Funds originating/returning to same entity via complex path.
*   **Inconsistent Volume**: Activity does not match customer profile (e.g., student moving millions).

---

## 6. Singapore Specific Risk Factors (VA RA 2024)

**Source**: SG-007-MAS-VA-Risk-Assessment-2024

*   **Key Threats**:
    1.  **Cyber-enabled Fraud** (Scams, Pig-butchering).
    2.  **Ransomware** payments.
    3.  **Theft** (Hacks/Exploits).
*   **High Risk Sectors**: Payment Service Providers, Digital Payment Token Service Providers.
