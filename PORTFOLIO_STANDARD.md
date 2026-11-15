# Portfolio evidence standard

> A project is understood by what a reader can inspect, not by how confidently it is described.

This standard governs how projects are presented in the DT—09 portfolio. It applies to software, research experiments, demonstrations and design studies.

## 1. Describe the work without inflating it

Every project page should make these points easy to find:

1. **Problem** — the specific problem and intended user or research audience.
2. **Boundary** — what the current version does and does not do.
3. **Mechanism** — the architecture, algorithm or method that produces the result.
4. **Inputs** — supported formats, assumptions, constraints and validation rules.
5. **Outputs** — what the user receives and how to inspect it.
6. **Verification** — commands, tests, fixtures and reproducible examples.
7. **Limitations** — known gaps, unsupported cases and conditions that invalidate a result.
8. **Operation** — installation, configuration, deployment and recovery where applicable.
9. **Data and security** — where data travels, where it is stored, access boundaries and sensitive-data cautions.
10. **Maintenance** — release state, known issues, compatibility and a realistic next step.

A feature is not established merely because it appears in a roadmap, mock-up, screenshot or marketing page.

## 2. Use explicit maturity labels

Choose the highest label whose evidence is actually present. A project may move backwards if its dependencies, deployment or tests stop working.

| Label | Minimum evidence |
|---|---|
| **Concept** | A defined problem, intended outcome and documented assumptions. |
| **Prototype** | An executable or inspectable proof of concept with a stated boundary. |
| **Functional** | The documented core workflow runs from supported inputs to expected outputs. |
| **Verified** | Repeatable tests cover the critical workflow, important edge cases and failure paths. |
| **Maintained** | Reproducible setup, current dependencies, issue handling and a repeatable release process. |
| **Production-ready** | Deployment, security, privacy, reliability, observability, recovery, support and operational controls have been tested for the stated use case. |

A passing unit-test suite does not, by itself, establish production readiness. A successful deployment does not establish product-market fit, security assurance or customer adoption.

## 3. Evidence hierarchy

Prefer evidence in this order:

1. Reproducible execution with documented inputs and outputs.
2. Automated tests and captured test results.
3. Source code, schemas, architecture and explicit algorithms.
4. Reproducible synthetic examples, clearly labelled as synthetic.
5. Screenshots and demonstrations that correspond to the current implementation.
6. Narrative descriptions and roadmap statements.

Do not present synthetic records as customer evidence. Do not turn a test fixture into a performance claim. Do not imply external review, certification, adoption or revenue without verifiable evidence and permission to disclose it.

## 4. Claims and language

Use precise verbs:

- **Implements** when the code performs the described operation.
- **Supports** when the input, output and constraints are documented and tested.
- **Demonstrates** for a bounded example or simulation.
- **Explores** for research directions and incomplete approaches.
- **Plans** for work that is not implemented.
- **Does not support** for known exclusions.

Avoid unqualified terms such as *secure*, *accurate*, *autonomous*, *enterprise-grade*, *real-time* and *production-ready*. State the scope and evidence that justify them.

## 5. Release review

Before featuring or releasing a project, check:

- [ ] The README matches the current code and deployed behaviour.
- [ ] A new reader can install or run the project from a clean environment.
- [ ] The main workflow has a reproducible example.
- [ ] Tests cover normal, boundary and failure cases.
- [ ] Errors are actionable and do not expose secrets or sensitive data.
- [ ] Configuration and secrets are documented without publishing credentials.
- [ ] Data flow, persistence and deletion behaviour are explained.
- [ ] Dependencies and licences are reviewed.
- [ ] Links, screenshots and deployment destinations work.
- [ ] Known limitations and unimplemented features are visible.
- [ ] The maturity label matches the available evidence.

## 6. Portfolio-level rule

The profile is an index, not a substitute for project documentation. Each project repository remains the source of truth for its implementation, tests, releases and current status. The profile should summarize only what that source can support.

**A claim without evidence is not a stronger claim. It is a liability.**
