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

Last checked: **2026-10-05**.

| Phase | Status | Evidence |
| --- | --- | --- |
| 1 — Project Foundation | Completed and merged | [PR #1](https://github.com/jorgefochezato-gif/opsintel-bi/pull/1), [issue #3](https://github.com/jorgefochezato-gif/opsintel-bi/issues/3) |
| 2 — Business Requirements | Completed and merged | [PR #2](https://github.com/jorgefochezato-gif/opsintel-bi/pull/2), [issue #4](https://github.com/jorgefochezato-gif/opsintel-bi/issues/4) |
| 3 — Synthetic Operational Dataset | In progress; local progress reported by the owner | [Issue #5](https://github.com/jorgefochezato-gif/opsintel-bi/issues/5) |
| 4–15 — Database through portfolio release | Planned / Todo | [15-phase project roadmap](https://github.com/users/jorgefochezato-gif/projects/2) |

### Published and completed

The main branch contains the repository structure, business scenario, 16-entry KPI catalog, solution architecture, business-process matrix, stakeholder use cases, report requirements, business rules and edge cases, data requirements, acceptance criteria, and Phase 1–2 checklists.

### Dataset development in progress

Issue #5 records owner-reported local progress on the Python environment, deterministic generator foundation, regions, locations, customers, carrier service profiles, routes, assets, shipments, and transportation costs.

The reported branch, `feat/phase-3-synthetic-dataset`, has not yet been pushed and has no published PR as of the date above. These items are not independently validated from public code and do not represent completion of Phase 3.

Remaining work includes transportation budgets, asset movements, operational exceptions, controlled data-quality defects, automated validation, a reproducibility test, documentation, and PR review/merge.

The public data, database, SQL, Power BI, scripts, and tests directories currently contain placeholders. No working dashboard, SQL-to-DAX reconciliation, implemented security roles, or released end-to-end solution is published yet.

## Trust, Traceability, and Design Commitments

These commitments guide implementation; the requirements are published, while the downstream behavior remains to be built and validated.

- **SQL-to-dashboard traceability:** [KPI definitions](docs/requirements/kpi-catalog.md) and [business rules](docs/requirements/business-rules.md) establish calculation meaning, exclusions, date context, and edge cases. Equivalent SQL and Power BI results must reconcile under the same filters, including independent numerator and denominator checks.
- **Stakeholder-specific reporting:** [Stakeholder use cases](docs/requirements/stakeholder-use-cases.md) and [report requirements](docs/requirements/report-requirements.md) define the questions each audience needs to answer. Each visual should support a documented decision.
- **Security from the design stage:** Regional access restrictions are documented. Row-Level Security implementation and authorized/unauthorized access tests are planned in [Phase 13](https://github.com/jorgefochezato-gif/opsintel-bi/issues/15).
- **Synthetic data and visible quality issues:** The dataset is intended to be fully fabricated, with no real customer or employer records. Controlled defects will be introduced deliberately to exercise detection, flagging, handling, and validation. Defect injection and its validation are still pending in Phase 3.
- **Consistent business meaning:** Reusable definitions and independently reproducible calculations are intended to support a shared source of truth across teams. This is a design objective, not a demonstrated production outcome.

## Documentation and AI-Assisted Workflow

The project is a learning and portfolio exercise intended to refresh skills, organize knowledge, and demonstrate an end-to-end BI workflow. Its operations scenario draws on the author's professional experience.

The author uses AI assistance during development with the aim of keeping requirements, implementation, documentation, and validation aligned. This describes the working method, not a published automated synchronization system or a guarantee of correctness.

For each phase:

1. Link the phase issue, branch, commits, and pull request.
2. Update requirements and affected documentation alongside implementation.
3. Record decisions, unresolved assumptions, and validation evidence at each checkpoint.
4. Keep work In Progress until validation and review are complete and the final PR is merged.
5. Update the README status, issue checklist, and project-board status together when progress changes.

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
