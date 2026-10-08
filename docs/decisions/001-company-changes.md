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

# Change 3: Asset classification and criticality decisions

Date: 2026-10-08
Status: Accepted

| Asset | Decision | Reason |
|---|---|---|
| A-004 Microsoft Entra ID | Changed to Restricted | Taking over Entra ID can lead to Azure admin access, so it needs the same protection as A-019. |
| A-019 Azure admin accounts | Kept as Restricted, criticality 5 | These accounts control all cloud resources, including the databases and backups. |
| A-005 Staff laptops | Changed to Confidential, criticality 4 | Laptops can reach Restricted data, and personal devices are in scope. |
| A-008 Customer support tool | Changed to Restricted | Agents see KYC status, and support staff do not yet have enforced MFA. |
| A-012 GitHub code repositories | Kept as Confidential, criticality 4 | Code and infrastructure definitions are sensitive, but leaked secrets are the main risk and are tracked separately under A-021. |
| A-014 Slack workspace | Changed to Confidential, criticality 2 | Staff may paste customer details or keys into messages. Staff can use email for a day if Slack is down, so criticality stays low. |
| A-015 Google Workspace | Kept as Confidential, criticality 4 | Email and shared documents are needed daily and hold internal and customer correspondence. |
| A-021 to A-027 | Added | Secrets management, DNS, monitoring, the partner bank link, finance, HR and reporting data were missing from the first inventory. A-027 assumes a reporting copy of production data exists. |

## Concentration note

The Head of Engineering owns 7 assets and the IT Lead owns 6. This is realistic for a 50-person company, but it is a key-person and separation-of-duties risk. It will be considered in the risk register.
