# OpsIntel BI

OpsIntel BI is a production-oriented business intelligence portfolio project focused on building an end-to-end enterprise analytics solution using Power BI, SQL, PostgreSQL, Python, dimensional modeling, DAX, and governed reporting practices.

The project is designed to simulate a realistic operations and supply-chain analytics environment and to demonstrate the complete workflow from business requirements through data modeling, transformation, semantic modeling, dashboard development, validation, security, and executive storytelling.

## Project Goals

- Translate business requirements into measurable KPIs and analytics specifications.
- Generate and manage realistic operational data.
- Build a dimensional data warehouse using a star schema.
- Transform and validate data using SQL.
- Create a governed Power BI semantic model.
- Develop reusable and validated DAX measures.
- Implement Row-Level Security.
- Build interactive executive and operational dashboards.
- Validate Power BI results against SQL source calculations.
- Apply enterprise BI performance, documentation, and governance practices.
- Present the complete solution as a professional portfolio case study.

## Planned Architecture

```text
Synthetic Operational Data
        ↓
PostgreSQL
        ↓
Raw / Staging Layer
        ↓
SQL Transformations
        ↓
Dimensional Model
        ↓
Power BI Semantic Model
        ↓
DAX Measures
        ↓
Row-Level Security
        ↓
Interactive Reports
        ↓
Validation / QA
        ↓
Executive Insights
```

## Planned Technology Stack

- Power BI
- DAX
- SQL
- PostgreSQL
- Python
- Docker
- Git / GitHub

Additional enterprise BI tooling may be introduced as the project evolves, including DAX Studio and Tabular Editor.

## Repository Structure

```text
opsintel-bi/
├── data/
│   ├── raw/
│   └── generated/
├── database/
│   ├── schema/
│   ├── migrations/
│   └── seed/
├── sql/
│   ├── staging/
│   ├── transformations/
│   ├── validation/
│   └── analysis/
├── powerbi/
│   ├── reports/
│   └── themes/
├── docs/
│   ├── architecture/
│   ├── requirements/
│   ├── data-model/
│   └── decisions/
├── scripts/
└── tests/
```

## Development Approach

The project is developed incrementally using a phase-based workflow.

Each phase follows:

1. Define the requirement.
2. Learn the underlying concept.
3. Implement the solution.
4. Validate the result.
5. Document design decisions.
6. Commit changes using Git.
7. Review and merge through a pull request.

The project follows a **Build → Learn → Prove** approach so that each implementation step is supported by both technical understanding and measurable validation.

## Current Status

Last checked: **2026-10-13**.

| Phase | Status | Evidence |
| --- | --- | --- |
| 1 — Project Foundation | Done / completed and merged | [PR #1](https://github.com/jorgefochezato-gif/opsintel-bi/pull/1), [issue #3](https://github.com/jorgefochezato-gif/opsintel-bi/issues/3) |
| 2 — Business Requirements | Done / completed and merged | [PR #2](https://github.com/jorgefochezato-gif/opsintel-bi/pull/2), [issue #4](https://github.com/jorgefochezato-gif/opsintel-bi/issues/4) |
| 3 — Synthetic Operational Dataset | Done / completed and merged | [PR #19](https://github.com/jorgefochezato-gif/opsintel-bi/pull/19), [issue #5](https://github.com/jorgefochezato-gif/opsintel-bi/issues/5) |
| 4 — PostgreSQL Foundation | Todo / not started; next phase | [Issue #6](https://github.com/jorgefochezato-gif/opsintel-bi/issues/6) |
| 5–15 — Dimensional modeling through portfolio release | Planned / Todo | [15-phase project roadmap](https://github.com/users/jorgefochezato-gif/projects/2) |

### Published and completed

The main branch contains the repository foundation, business scenario, KPI catalog, solution architecture, business-process matrix, stakeholder use cases, report requirements, business rules, data requirements, acceptance criteria, and Phase 1–3 documentation.

Phase 3 was merged through [PR #19](https://github.com/jorgefochezato-gif/opsintel-bi/pull/19). Its deterministic Python generator includes locked dependencies, regions, geographically coherent locations, customers, carriers with service profiles, routes, reusable assets, 100,000 shipments, transportation cost transactions, monthly regional budgets, asset movement history, and operational exceptions.

Clean reference datasets are generated under `data/generated/`. Source-like shipments and transportation costs with controlled defects are written to `data/raw/`. Defects include duplicates, missing carrier references, invalid delivery dates, invalid quantities, and extreme transportation costs; a data-quality issue manifest records the injected defects.

Published [dataset validation tests](tests/test_generated_data.py) cover counts, uniqueness, referential integrity, geographic consistency, business rules, and controlled defects. The [reproducibility test](tests/test_reproducibility.py) compares SHA-256 hashes across repeated generator runs. PR #19 records successful generator execution and passing validation; the status synchronization did not rerun those tests.

See the [Phase 3 summary](docs/phase-3-summary.md) and [Phase 3 checklist](docs/phase-3-checklist.md) for dataset scale, reporting dates, and implementation details.

### Next: PostgreSQL Foundation

[Phase 4](https://github.com/jorgefochezato-gif/opsintel-bi/issues/6) remains Todo. Planned work includes Docker PostgreSQL, database initialization, `raw`/`staging`/`analytics` schemas, raw table definitions, repeatable CSV ingestion, constraints and indexes, data-quality validation queries, staging cleanup, and backup/restore verification.

Database implementation, dimensional modeling, downstream SQL transformations, Power BI reports, SQL-to-DAX reconciliation, and Row-Level Security remain planned.

## Trust, Traceability, and Design Commitments

These commitments guide implementation; the requirements are published, while the downstream behavior remains to be built and validated.

- **SQL-to-dashboard traceability:** [KPI definitions](docs/requirements/kpi-catalog.md) and [business rules](docs/requirements/business-rules.md) establish calculation meaning, exclusions, date context, and edge cases. Equivalent SQL and Power BI results must reconcile under the same filters, including independent numerator and denominator checks.
- **Stakeholder-specific reporting:** [Stakeholder use cases](docs/requirements/stakeholder-use-cases.md) and [report requirements](docs/requirements/report-requirements.md) define the questions each audience needs to answer. Each visual should support a documented decision.
- **Security from the design stage:** Regional access restrictions are documented. Row-Level Security implementation and authorized/unauthorized access tests are planned in [Phase 13](https://github.com/jorgefochezato-gif/opsintel-bi/issues/15).
- **Synthetic data and visible quality issues:** Phase 3 provides synthetic operational data with controlled defects, a defect manifest, and automated validation. Clean reference data and source-like raw data are kept separate. SQL detection and staging treatment are planned in Phase 4.
- **Consistent business meaning:** Reusable definitions and independently reproducible calculations are intended to support a shared source of truth across teams. This is a design objective, not a demonstrated production outcome.

## Documentation and AI-Assisted Workflow

The project is a learning and portfolio exercise intended to refresh skills, organize knowledge, and demonstrate an end-to-end BI workflow. Its operations scenario draws on the author's professional experience.

The author uses AI assistance during development with the aim of keeping requirements, implementation, documentation, and validation aligned. This describes the working method, not a published automated synchronization system or a guarantee of correctness.

For each phase:

1. Link the phase issue, branch, commits, and pull request.
2. Update requirements and affected documentation alongside implementation.
3. Record decisions, unresolved assumptions, and validation evidence at each checkpoint.
4. Keep work In Progress until validation and review are complete and the final PR is merged.
5. Use `feat/phase-N-description`, reference the phase issue with `Refs #issue` for partial PRs, and use `Closes #issue` only in the final phase PR.
6. After the final PR is validated and merged into `main`, verify the merge, close the issue as completed, set the project item to Done, and update the README status and issue checklist together. Recheck the final project status after linking PRs, because project workflows may change it.

AI-assisted output must be reviewed and validated. Completed implementation claims should link to published artifacts and evidence; local reports and planned capabilities should remain explicitly labeled.

## Public Learning and Consulting

The repository and project roadmap are public and free to explore for learning from the requirements, decisions, and development process. A reuse license has not yet been added; public visibility alone does not grant unrestricted reuse rights.

For a use case tailored to a particular industry, business, or operational process, the author is available to collaborate through consulting services. Contact [Jorge D. Fochezato on LinkedIn](https://www.linkedin.com/in/jorge-d-fochezato-030bb830/).

## Roadmap

The planned development includes:

1. Project Foundation
2. Business Requirements
3. Synthetic Operational Dataset
4. PostgreSQL Foundation
5. Dimensional Data Model
6. SQL Transformation Layer
7. Power BI Data Connection
8. Power BI Semantic Model
9. DAX Fundamentals
10. Advanced DAX
11. Executive Dashboard
12. Operational Analysis
13. Row-Level Security
14. Performance and Enterprise Tooling
15. QA, Documentation, and Portfolio Release

