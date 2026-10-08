# 02 - Methodology and Scoring Rubric

**Status: DRAFT proposed thresholds. Review, change and justify each one before scoring any risk.**

## Process

1. Identify assets (`data/assets.csv`).
2. Model threats per component using STRIDE (`docs/04-threat-model.md`).
3. Record risks (`data/risk_register.csv`) with inherent and residual scores.
4. Map controls and gaps to NIST CSF 2.0 (`data/csf_gap_analysis.csv`).
5. Validate scoring consistency (`docs/09-validation.md`).

## Likelihood (1 to 5)

| Score | Label | Meaning |
|---|---|---|
| 1 | Rare | Less than once in 5 years |
| 2 | Unlikely | Once in 2 to 5 years |
| 3 | Possible | About once a year |
| 4 | Likely | Several times a year |
| 5 | Almost certain | Monthly or more often |

## Impact (1 to 5)

Judge the worst credible outcome across money, regulation, customers and downtime.

| Score | Financial | Regulatory | Customer harm | Downtime |
|---|---|---|---|---|
| 1 | Under EUR 5k | None | None | Under 1 hour |
| 2 | EUR 5k to 50k | Informal query | Few customers inconvenienced | 1 to 4 hours |
| 3 | EUR 50k to 250k | Formal inquiry | Hundreds affected | 4 to 24 hours |
| 4 | EUR 250k to 1m | Fine likely or bank partner escalation | Thousands affected or sensitive data exposed | 1 to 3 days |
| 5 | Over EUR 1m | Licence or bank partnership at risk | Mass exposure of financial or identity data | Over 3 days |

## Score and bands

**Risk score = Likelihood x Impact**

| Score | Band |
|---|---|
| 1 to 5 | Low |
| 6 to 12 | Medium |
| 13 to 19 | High |
| 20 to 25 | Critical |

## Inherent vs residual

- **Inherent:** the risk before any existing control.
- **Residual:** the risk after the controls that actually exist today. List the controls you assumed in the `existing_controls` column. Residual cannot exceed inherent.

## Treatment

Every risk gets one of: **Mitigate, Accept, Transfer, Avoid**, with a one-line reason and, for mitigation, a named action and owner.

## Questions to settle before scoring

- Do the euro thresholds suit a company of this size? Why or why not?
- Is "sensitive data exposed" really a 4, or should it be a 5 for a payments company?
- Who is allowed to accept a High risk?

Record your answers as short decision records in `docs/decisions/`.
