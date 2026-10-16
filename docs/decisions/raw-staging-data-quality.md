# Raw and Staging Data-Quality Decisions

Date: 2026-10-16. Status: published in merged Phase 4 PR #22; issue #6 is completed. Decisions below describe the current code and its validation limits.
Evidence: [implementation PR #22](https://github.com/jorgefochezato-gif/opsintel-bi/pull/22), head `fec7936`, merged as `b30e726`. PR-reported database results were not independently rerun during synchronization.

## Preserve raw source problems

Raw shipment and transportation-cost tables are implemented without primary keys, foreign keys, NOT NULL, or business constraints so duplicates and missing references remain observable. Typed columns can still reject malformed values; this is not a guarantee that arbitrary source strings can be ingested. Preserve raw data as the traceable baseline and document rejected parse/load records where applicable.

data/raw holds defect-bearing sources. data/generated remains clean reference truth outside the initial shipment/cost ingestion pipeline. Any other master/reference ingestion must have explicit mappings.

## Shipment cleanup

The staging SQL keeps one shipment per shipment_id using ROW_NUMBER ordered by created_timestamp ascending. It converts nonpositive quantities and actual delivery dates preceding shipment_date to NULL. Missing carriers remain missing; no carrier ID or corrected value is fabricated.

quality_status is VALID or WARNING; quality_notes records the relevant reasons. VALID means no warning from the implemented rules, not complete business or referential validity. Warnings can have several reasons.

Ordering only by created_timestamp leaves equal-timestamp ties unresolved. To establish stable selection when source values differ, prove tied candidates are identical or add a stable documented tie-breaker. Staging primary keys enforce uniqueness but do not prove that the correct source record was selected.

## Cost cleanup

Missing shipment IDs and positive CREDIT/REVERSAL amounts receive warnings in the staging SQL. Extreme amounts are retained because an outlier may represent a real business event; outlier treatment requires an explicit later rule. Existing cost signs are preserved rather than silently corrected.

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

PR #22 reports passing reconciliation tests; captured execution output is not committed. The seven published Python tests do not compare all columns, cost IDs or totals, every warning record, or all relationships. Normalizing bad values to NULL also does not reconstruct original clean values. Do not describe these checks as complete field-by-field recovery.

The delivered-without-date SQL check compares quality_notes with a single exact reason. Compound notes can make that comparison misleading. Validate warning reasons independently or use structured flags before relying on it as a zero-failure gate.

## Evidence and remaining validation limits

Capture actual raw/staging counts, defect counts by category, exact SQL results, and pytest output against a recorded implementation SHA. Reconcile detections with the manifest and investigate overlapping defects instead of adding category counts blindly.

Phase 4 delivery is completed and merged. Timestamp ties, full reference existence, compound warnings, and restore integrity remain explicit limits rather than completed checks. Published constraints/indexes, initialization, backup, and restore scripts are present; the restore script prints counts without equality assertions, and initialization does not enable psql ON_ERROR_STOP. Phase 5 (#9) remains Todo / next; preserve the Phase 5/6 boundaries.

