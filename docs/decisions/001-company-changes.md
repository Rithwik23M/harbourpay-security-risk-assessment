# Decision 001: Company profile changes

Date: 2026-10-08
Status: Accepted

## Context

The starter profile for HarbourPay assumed AWS for hosting and Okta for staff identity. I changed these so the scenario reflects choices I can reason about and defend.

## Change 1: Cloud provider moved from AWS to Azure

- **Options considered:** AWS, Azure.
- **Chosen:** Microsoft Azure.
- **Why:** Azure is widely used by Irish enterprises and financial firms, and it fits the Microsoft tooling a regulated company is likely to use for identity, logging and compliance reporting.
- **Trade-offs:** The team would need Azure skills, and the assessment must use Azure terms in places (for example Azure API Management and Microsoft Defender for Cloud).
- **Consequence:** All hosting entries in `data/assets.csv` now say Azure. The AWS admin accounts asset became "Azure admin accounts".

## Change 2: Staff identity moved from Okta to Microsoft Entra ID

- **Options considered:** Keep Okta, switch to Microsoft Entra ID.
- **Chosen:** Microsoft Entra ID.
- **Why:** With Azure as the cloud, Entra ID is the native identity service. It removes a separate vendor, and it keeps staff sign-in and cloud administration under one identity system.
- **Trade-offs:** Fewer vendors and simpler administration, but a single point of failure. If Entra ID is compromised, an attacker may reach most systems. This makes asset A-004 a high-impact target for the threat model.
- **Consequence:** Asset A-004 is now Microsoft Entra ID. Assumption A-02 in the company profile refers to Entra ID MFA.

## Change 3: [write your third change here]

- **Options considered:**
- **Chosen:**
- **Why:**
- **Trade-offs:**
- **Consequence:**
