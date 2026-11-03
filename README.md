# DT—09 / Engineering Portfolio

> **Build systems that make important outcomes inspectable.**

I design and engineer software around a recurring question: *what happened, why did it happen, and what evidence lets someone verify the answer?*

My work spans business-data investigation, AI assurance, agent authority, adaptive learning, desktop software and interactive 3D. I prefer working systems, explicit boundaries and inspectable evidence over impressive claims.

<p>
  <a href="https://github.com/DT-09/LedgerTrace">FLAGSHIP · LEDGERTRACE</a>
  &nbsp; / &nbsp;
  <a href="https://github.com/DT-09/Aurelis-Authority">AGENT AUTHORITY</a>
  &nbsp; / &nbsp;
  <a href="https://github.com/DT-09/ai-assurance-infrastructure">AI ASSURANCE INFRASTRUCTURE</a>
  &nbsp; / &nbsp;
  <a href="https://www.linkedin.com/in/dhairy-topia/">LINKEDIN</a>
</p>

---

## 01 / Engineering focus

<table>
  <tr>
    <td width="33%" valign="top">
      <sub>01 — BUSINESS SYSTEMS</sub>
      <h3>Find the discrepancy.</h3>
      Reconcile operational records, expose exceptions and preserve the source evidence behind each finding.
    </td>
    <td width="33%" valign="top">
      <sub>02 — AI ASSURANCE</sub>
      <h3>Verify the behavior.</h3>
      Define expected outcomes, evaluate observed behavior and produce evidence that can be reviewed and retested.
    </td>
    <td width="33%" valign="top">
      <sub>03 — INTERACTIVE SOFTWARE</sub>
      <h3>Make complexity usable.</h3>
      Turn technical models and dense information into clear, responsive tools and experiences.
    </td>
  </tr>
</table>

The common engineering pattern:

<pre>INPUTS → RULES / MODEL → OBSERVATION → EVIDENCE → HUMAN DECISION</pre>

## 02 / Selected systems

These are distinct projects, not one umbrella product. Each has its own purpose, implementation and limitations.

### 01 — LedgerTrace
**Supplier-payment and invoice-reconciliation investigation**

[Repository ↗](https://github.com/DT-09/LedgerTrace) · [Live workbench ↗](https://ledgertrace.pages.dev/)

A browser-based accounts-payable workbench that compares invoice lines with purchase orders and goods receipts. It surfaces rule-triggered exceptions, links findings to source rows and exports a review worklist.

- **Engineering:** browser-side CSV processing, normalized input headers, deterministic comparison rules, source-row traceability and evidence exports.
- **Demonstration:** load the synthetic sample, inspect the exceptions and open the supporting row references.
- **Boundary:** a review aid, not an autonomous payment system. A flagged value is not confirmed loss or recoverable cash.

<details>
  <summary><strong>Inspect the implementation</strong></summary>

  The repository documents supported input schemas, matching rules, data handling, known limitations and the bounded commercial review scope. The sample is illustrative, not customer evidence.

  Start with the [README](https://github.com/DT-09/LedgerTrace#readme) and [sales-readiness audit](https://github.com/DT-09/LedgerTrace/blob/main/SALES-READINESS-AUDIT.md).
</details>

### 02 — Aurelis Authority
**Independent AI agent authority assurance**

[Repository ↗](https://github.com/DT-09/Aurelis-Authority) · [Live experience ↗](https://aurelis-authority.pages.dev/)

An assessment workflow for examining whether an AI agent's tool-call behavior stays within a defined authority policy.

- **Engineering:** deterministic policy checks, expected-versus-observed decisions, trace evidence, remediation guidance and retesting.
- **Demonstration:** run the local assessment and inspect the generated JSON report.
- **Boundary:** the trace checker audits supplied records. It does not intercept live tools, prove trace completeness or certify security.

<details>
  <summary><strong>Inspect the implementation</strong></summary>

  Run <code>npm test</code> and <code>npm run demo:assessment</code>. The repository includes an offline trace-audit utility, a public synthetic workspace and a scoped first-pilot definition.

  [Technical documentation ↗](https://github.com/DT-09/Aurelis-Authority#readme)
</details>

### 03 — AI Assurance Infrastructure
**Persistent assurance and control-plane foundations**

[Repository ↗](https://github.com/DT-09/ai-assurance-infrastructure)

A vendor-neutral infrastructure project built around AI asset identity, authority, evidence provenance, policy decisions, trust state and runtime control.

- **Engineering:** protocol definitions, benchmark suite, evidence hashes, policy evaluation and API surfaces.
- **Architecture:** Identity → Authority → Evidence → Policy → Trust → Runtime Control.
- **Boundary:** benchmark results are engineering evidence, not a safety, security, compliance or production certification.

[Architecture and protocol ↗](https://github.com/DT-09/ai-assurance-infrastructure#readme)

### 04 — AI Evaluation Evidence Validator
**Buyer-owned AI acceptance and change-control workbench**

[Repository ↗](https://github.com/DT-09/AI-Evaluation-Evidence-Validator)

A local-first tool for evaluating third-party AI outputs against a versioned acceptance protocol, recording human adjudication and comparing candidate runs with an accepted baseline.

- **Engineering:** structured CSV/JSON inputs, explicit thresholds, hard gates, case-level outcomes and portable evidence packages.
- **Boundary:** no hosted multi-tenant service, live vendor connectors or automatic proof that a test set is representative.

[Run instructions and input contract ↗](https://github.com/DT-09/AI-Evaluation-Evidence-Validator#readme)

### 05 — LUMEN ALS
**Source-grounded adaptive learning system**

[Repository ↗](https://github.com/DT-09/lumen-als)

An adaptive-learning prototype connecting indexed course material, source-grounded tutoring, practice, progress estimates and an interactive concept universe.

- **Engineering:** FastAPI, SQLite, source-aware retrieval, document ingestion, a spatial concept graph and a browser-based learning workspace.
- **Boundary:** mastery and grading are heuristic baselines, not validated educational measurements.

[Architecture and deployment notes ↗](https://github.com/DT-09/lumen-als#readme)

### 06 — AUREL Desktop
**Native Windows desktop companion**

[Repository ↗](https://github.com/DT-09/AurelDesktop)

A standalone Windows application with a translucent desktop widget, live system indicators, configurable themes and a restorable cursor-scheme utility.

- **Engineering:** C# / .NET 8, Windows APIs, local settings and self-contained Windows builds.
- **Boundary:** a focused desktop companion, not a Windows shell replacement.

[Build and control guide ↗](https://github.com/DT-09/AurelDesktop#readme)

### 07 — IL ROSSO
**Interactive 3D engineering and editorial experience**

[Repository ↗](https://github.com/DT-09/IL-ROSSO)

An independent interactive experience combining a 3D concept-car study, historical archive and guided interface.

- **Engineering:** React, TypeScript, Vite, Three.js, React Three Fiber and Motion.
- **Boundary:** an independent fan project; the 3D model and strategy exercises are illustrative, not official vehicle data or team telemetry.

[Experience architecture ↗](https://github.com/DT-09/IL-ROSSO#readme)

### 08 — VentureLabs
**Evidence-led venture validation workspace**

[Repository ↗](https://github.com/DT-09/VentureLabs) · [Live workspace ↗](https://venturelabs.pages.dev/)

A browser-based workspace for turning a business thesis into explicit assumptions, an evidence ledger, pre-registered experiments and a decision report.

- **Engineering:** local multi-project persistence, evidence records, experiment tracking, Markdown reports and JSON backup/restore.
- **Boundary:** it organizes user-entered evidence; it does not independently verify customer demand or market claims.

[Product workflow ↗](https://github.com/DT-09/VentureLabs#readme)

---

## 03 / How the systems relate

Different domains. A shared preference for explicit inputs, observable behavior and evidence that survives inspection.

~~~mermaid
flowchart LR
    A[Operational records] --> B[LedgerTrace]
    C[Agent actions / traces] --> D[Aurelis Authority]
    E[AI assets / policies] --> F[AI Assurance Infrastructure]
    G[AI outputs / test cases] --> H[Evaluation Evidence Validator]
    I[Learning sources] --> J[LUMEN ALS]
    B --> K[Inspectable findings]
    D --> K
    F --> K
    H --> K
    J --> L[Grounded learning]
~~~

## 04 / Engineering principles

| Principle | What it means in practice |
|---|---|
| Evidence before assertion | Keep source references, inputs and calculation paths close to the result. |
| Deterministic where possible | Prefer explicit rules for checks that must be reproducible. |
| Boundaries are part of the design | State what a tool does not establish, not only what it can do. |
| Human review stays visible | Surface uncertainty and escalation points instead of hiding them behind a score. |
| Demonstrate the real system | Prefer runnable examples, tests and inspectable outputs to decorative claims. |

## 05 / Technical range

**Languages & application engineering**  
Python · JavaScript · TypeScript · C# · HTML · CSS

**Systems & interfaces**  
FastAPI · React · Streamlit · .NET · SQLite · REST APIs · browser APIs

**Data & assurance**  
CSV/JSON pipelines · deterministic validation · policy evaluation · evidence provenance · regression testing

**Build & delivery**  
Git · GitHub Actions · Cloudflare Pages · CI workflows · deployment and release verification

This is a map of technologies used across the projects above, not a claim of equal depth or production experience in every tool.

---

## 06 / Live repository pulse

A small, automatically refreshed view of the repositories: current public metadata and the latest commit recorded by GitHub. It is activity context, not a quality score.

<!-- PROFILE_PULSE:START -->
_Profile telemetry is being prepared. The scheduled workflow will populate this section._
<!-- PROFILE_PULSE:END -->

---

## 07 / Research, notes & contact

I am interested in the engineering questions beneath product surfaces: trustworthy automation, AI authority, evidence quality, decision systems, learning and the design of useful technical interfaces.

- **GitHub:** [github.com/DT-09](https://github.com/DT-09)
- **LinkedIn:** [dhairy-topia](https://www.linkedin.com/in/dhairy-topia/)
- **Email:** [dhairytopia@gmail.com](mailto:dhairytopia@gmail.com)

<sub>DT—09 / INDEPENDENT ENGINEERING · SYSTEMS · RESEARCH</sub>
