# 01 - Company Profile and Assumptions

**Important:** HarbourPay Ltd is fictional. Everything below is an assumption made to give the assessment a realistic scope. Change anything that does not feel right, and record the change in `docs/decisions/`.

## Business

- **Name:** HarbourPay Ltd
- **Location:** Dublin, Ireland
- **Size:** 50 staff, Series A funded
- **Product:** a prepaid payroll card and mobile app for gig workers
- **Trigger event:** a partner bank has asked for evidence of a working security programme within 90 days

## Staff (assumed)

| Team | Headcount | Notes |
|---|---|---|
| Engineering | 20 | Backend, mobile, platform |
| Operations and support | 10 | Handle customer queries, can view KYC documents |
| Compliance and finance | 8 | AML monitoring, reporting |
| Sales and other | 12 | Mostly remote |

Working model: remote-first, staff use a mix of company and personal phones.

## Technology (assumed)

- Cloud: Microsoft Azure, with microservices behind an API gateway
- Database: PostgreSQL
- Identity: Okta SSO for staff, but MFA is not enforced for the support team; customers log in with email, password and SMS code
- Source control and CI: GitHub
- Collaboration: Slack and Google Workspace
- Third parties: a card processor (holds card data and returns tokens), a KYC vendor (verifies identity documents), an email and SMS provider

## Data held (assumed)

- Customer personal data (name, address, date of birth, phone, email)
- KYC documents (passport and ID images)
- Transaction records
- Card tokens (no raw card numbers stored, tokenised by the processor)
- Internal financial and HR records

## Scope of this assessment

**In scope:** the customer wallet application, the API platform, the cloud environment, staff devices and accounts, and the key third parties.

**Out of scope:** physical office security, detailed code review, penetration testing.

## Regulatory context (to verify before citing)

Assumed relevant: GDPR, PCI DSS v4.0 (via the processor), and EU digital operational resilience rules for financial entities. Confirm the current requirements from official sources before quoting specific clauses.

## Assumption log

| ID | Assumption | Why it matters | Confidence |
|---|---|---|---|
| A-01 | No raw card numbers are stored | Reduces PCI scope | Medium |
| A-02 | MFA is not enforced for support staff | Raises account takeover risk | Medium |
| A-03 | Logs are not yet centralised | Affects detection scoring | Low |
| A-04 | Backups exist but restores are untested | Affects recovery scoring | Low |
