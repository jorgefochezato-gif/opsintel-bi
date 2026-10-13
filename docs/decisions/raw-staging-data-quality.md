# Raw and Staging Data-Quality Decisions

Date: 2026-10-13. Status: decisions reflected in the Phase 4 development conversation; implementation and execution verification pending.
Source: [development conversation](https://chatgpt.com/share/6ace94d4-5aa4-83e9-941e-0a01126b84a9).

## Preserve raw source problems

Raw shipment and transportation-cost tables are proposed without primary keys, foreign keys, NOT NULL, or business constraints so duplicates and missing references remain observable. Typed columns can still reject malformed values; this is not a guarantee that arbitrary source strings can be ingested. Preserve raw data as the traceable baseline and document rejected parse/load records where applicable.

data/raw holds defect-bearing sources. data/generated remains clean reference truth outside the initial shipment/cost ingestion pipeline. Any other master/reference ingestion must have explicit mappings.

## Shipment cleanup

The proposed staging SQL keeps one shipment per shipment_id using ROW_NUMBER ordered by created_timestamp ascending. It converts nonpositive quantities and actual delivery dates preceding shipment_date to NULL. Missing carriers remain missing; no carrier ID or corrected value is fabricated.

quality_status is VALID or WARNING; quality_notes records the relevant reasons. VALID means no warning from the implemented rules, not complete business or referential validity. Warnings can have several reasons.

Ordering only by created_timestamp leaves equal-timestamp ties unresolved. Before claiming deterministic selection, prove tied candidates are identical or add a stable documented tie-breaker. Staging primary keys enforce uniqueness but do not prove that the correct source record was selected.

## Cost cleanup

Missing shipment IDs and positive CREDIT/REVERSAL amounts receive warnings in the proposed SQL. Extreme amounts are retained because an outlier may represent a real business event; outlier treatment requires an explicit later rule. Existing cost signs are preserved rather than silently corrected.

Checking for NULL references does not detect non-NULL references to nonexistent master or shipment records. Full reference existence checks remain a separate validation requirement.

## Validation contract and limits

| Check | Expected outcome | What it proves |
| --- | --- | --- |
| Staging shipment count vs clean CSV | Equal counts | Cardinality agreement only |
| Staging shipment ID set vs clean CSV | Equal sets | Shipment identity coverage |
| Staging cost count vs raw CSV | Equal counts | No row loss by count; not identity/value equality |
| Duplicate shipment IDs | Zero | Shipment key uniqueness |
| Remaining nonpositive quantities | Zero | Invalid quantities no longer remain nonpositive |
| Delivery dates preceding shipment date | Zero | That specific invalid sequence is absent |
| Missing-carrier warnings | Present for injected defects | Some missing-carrier classification exists; exact coverage needs stronger checks |

These are expected results, not captured execution results. The proposed seven Python tests do not compare all columns, cost IDs or totals, every warning record, or all relationships. Normalizing bad values to NULL also does not reconstruct original clean values. Do not describe these checks as complete field-by-field recovery.

The proposed delivered-without-date SQL check compares quality_notes with a single exact reason. Compound notes can make that comparison misleading. Validate warning reasons independently or use structured flags before relying on it as a zero-failure gate.

## Evidence and next checks

Capture actual raw/staging counts, defect counts by category, exact SQL results, and pytest output against a recorded implementation SHA. Reconcile detections with the manifest and investigate overlapping defects instead of adding category counts blindly.

Before phase closure: review tie handling, reference existence, compound warnings, appropriate indexes/constraints, load repeatability, and backup/restore. Keep Phase 4 In Progress until validation and final implementation merge; preserve Phase 5/6 boundaries.

