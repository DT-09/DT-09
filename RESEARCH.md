# Research programme

> Questions first. Models second. Evidence throughout.

This document records the questions that connect the work published under **DT—09**. It is a direction of inquiry, not a claim that every question has been solved or every system is production-ready.

## 01 — Mathematical structure and computation

**Central question:** How can a problem be represented so that its hidden structure becomes tractable?

Areas of inquiry:
- Discrete mathematics, algebraic structure, probability and optimisation.
- Algorithms, complexity, invariants and formal reasoning.
- Numerical and computational models: what they preserve, approximate or discard.
- Reproducibility: whether an independent run can recover the same result.

A useful result is not merely an answer. It includes the assumptions, derivation or algorithm, and conditions under which the result holds.

## 02 — AI assurance and bounded agency

**Central question:** What must be true before an AI system should be allowed to act?

Areas of inquiry:
- Identity, authentication, delegated authority and least privilege.
- Policy evaluation before execution, not only after an incident.
- Tool-call constraints, audit trails, provenance and revocation.
- Evaluation of reliability, uncertainty, failure modes and unsafe behaviour.

The design objective is bounded capability: the system should be able to explain what it was permitted to do, what it actually did, and what evidence supports that account.

## 03 — Data provenance and decision integrity

**Central question:** Can a decision be traced back through the data and transformations that produced it?

Areas of inquiry:
- Source-to-output lineage and immutable evidence references.
- Reconciliation, change detection, exception classification and review queues.
- Deterministic processing, content hashes and reproducible reports.
- Separation of observed facts, derived values, assumptions and unresolved exceptions.

A polished report is not evidence by itself. The underlying records, transformations and limitations must remain inspectable.

## 04 — Systems engineering and resilient execution

**Central question:** How does a design remain understandable and dependable under real constraints?

Areas of inquiry:
- Explicit interfaces, dependency boundaries and failure containment.
- Local-first operation, portability and controlled external dependencies.
- State management, persistence, recovery, observability and testing.
- Security boundaries, input validation and safe defaults.

The goal is not complexity for its own sake. Every component should earn its place by improving correctness, clarity, resilience or usability.

## 05 — Learning, discovery and scientific inquiry

**Central question:** How can curiosity become a disciplined process of independent investigation?

Areas of inquiry:
- Moving from observation to question, hypothesis and test.
- Connecting foundational concepts to primary sources and experiments.
- Adaptive learning that responds to demonstrated understanding.
- Recording uncertainty, failed hypotheses and revised models.

Learning should produce transferable understanding, not merely a completed sequence of tasks.

## 06 — Design as an engineering discipline

**Central question:** How can an interface make a complex mechanism easier to inspect without hiding its limits?

Areas of inquiry:
- Information hierarchy, interaction design and cognitive load.
- Visualising state, provenance, uncertainty and system behaviour.
- Accessibility, responsive behaviour and reduced-motion support.
- Consistency between what a product claims and what it can demonstrate.

Design is part of system quality. It should clarify the mechanism rather than decorate an unsupported claim.

---

## A common method

| Stage | Working question | Expected artefact |
|---|---|---|
| Inquire | What is the actual problem? | Problem statement and scope |
| Model | What assumptions and constraints apply? | Model, schema or specification |
| Build | What mechanism implements the model? | Reproducible implementation |
| Verify | What evidence supports the result? | Tests, traces and reviewable outputs |
| Review | What failed, remains uncertain or should change? | Limitations and next decisions |

The stages are iterative. Verification can invalidate a model; review can redefine the problem.

## Evidence standard

When presenting a result, distinguish:

- **Observed:** directly present in a source, log, test or execution.
- **Derived:** calculated from stated inputs by a described method.
- **Assumed:** accepted for the purpose of the model but not independently established.
- **Unverified:** not yet tested or supported by sufficient evidence.
- **Out of scope:** deliberately not handled by the current system.

Do not turn an assumption into a fact by repeating it. Do not describe a prototype as production software. Do not imply a test passed unless it was run.

---

**DT—09** · Independent inquiry / systems engineering
