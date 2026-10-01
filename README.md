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

## Technology Stack

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

**Phase 1 — Project Foundation: In Progress**

Current work:

- Repository structure created.
- Git repository initialized.
- Initial documentation being established.

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