# Portfolio First-Principles Audit

**Status:** Baseline inventory — documentation review only  
**Date:** 2026-11-15  
**Scope:** Repositories visible under `DT-09` in the connected GitHub account.

This document is an audit register, not a certification. The initial pass establishes repository identity and records claims and limitations stated in each README. It does **not** establish that source code works, tests pass, deployments are live, users need the product, or buyers will pay. Those require separate verification.

## Decision rule

No repository is called complete, production-ready, secure, validated, or commercially successful without evidence appropriate to that claim.

For each repository, subsequent work must establish:

1. **Problem:** a real, bounded problem that exists independently of this implementation.
2. **User and buyer:** who experiences it, who uses a solution, who controls budget, and who bears risk.
3. **Current alternative:** what happens today, including doing nothing.
4. **Value:** a measurable outcome and a credible reason to change.
5. **Mechanism:** the smallest technically sufficient system that produces that outcome.
6. **Correctness:** explicit invariants, failure modes, tests, reproducible runs, and independent checks.
7. **Operational fitness:** deployment, security, privacy, recovery, support, cost, and observability appropriate to the use case.
8. **External validity:** evidence from real intended users and real workflows, not only synthetic fixtures.
9. **Falsification:** observations that would make us stop, narrow, redesign, or retire the project.

## Evidence discipline

Every claim must be tagged as one of:

- **Verified:** directly reproduced or independently checked.
- **Documented:** stated in project documentation but not independently reproduced.
- **Supported:** backed by relevant external or user evidence.
- **Hypothesis:** plausible but not yet established.
- **Unknown:** insufficient evidence.
- **Contradicted:** evidence conflicts with the claim.

Bayesian updates must record the hypothesis, prior rationale, evidence, likelihood direction/strength, updated confidence, and a falsification condition. Do not invent numeric probabilities where there is no defensible calibration. Separate technical correctness, problem validity, willingness to pay, and repeat demand.

## Repository register

| Repository | First-pass identity / scope | Initial epistemic status | Next decisive investigation |
|---|---|---|---|
| `Nodus` | Shopify shipping-economics reconciliation and policy replay | Documented capabilities; README explicitly says live billing lifecycle, carrier APIs, policy drift alerts, and merchant demand are unverified | Run full source/test audit; verify deployment and Shopify lifecycle; obtain merchant evidence for frequency, economic impact, willingness to pay, and repeat use |
| `ai-assurance-infrastructure` | AI assurance/control plane, protocol, benchmark, runtime controls | Substantial documented surface; synthetic harness is not customer assessment or certification | Trace every public/API surface to implementation; threat model and adversarial tests; validate a narrow buyer workflow |
| `Ortheon` | Rust structural computation across graphs, hypergraphs, and finite relations | Documented research foundation; broader inference/dynamics/optimization and formal proofs remain planned | Verify mathematical contracts and algorithms; define one research question with measurable baselines |
| `Vantage` | Go deterministic DAG workflow execution and durable journal | Documented implementation and tests; exactly-once effects, automatic replay, distributed execution, and transactional rollback are explicitly absent | Execute tests and fault-injection; define recovery semantics and a real workload that needs this engine |
| `Strata` | Local-first visual SQL/data engineering with DuckDB-Wasm | Documented functional foundation; preview-limited exports, in-memory source bytes, and no collaboration/versioning | Test large-file behavior and data correctness; measure against direct DuckDB/SQL workflows |
| `Lotwise` | Supplier-lot evidence and specification review for ingredient QA | Documented evaluation foundation; validated extraction, organisation tenancy, operational recovery, and commercial proof absent | Security and tenant-isolation review; extraction benchmark on representative, authorised documents; buyer workflow validation |
| `DealTie` | CIM/QoE/valuation-model evidence tie-out | Documented analyst workbench; prototype boundaries and professional review requirements explicit | Test extraction and reconciliation against labelled packs; determine whether a frequent, budgeted pre-issue workflow exists |
| `MOSAIC` | AI-factory capacity portfolio optimization research | Documented research implementation; greedy dispatch, bounded exponential search, and no real operator traces or benchmark superiority | Execute tests; compare against exact/specialist baselines on reproducible scenarios; state the narrow claim the algorithm can defend |
| `AIFX` | Governed financial-evidence and relationship analysis engine | Documented deterministic core; statistics are not calibrated relationship probabilities and outputs are not fraud/causal conclusions | Audit invariants and statistical interpretation; test against labelled synthetic and authorised real-world cases |
| `ZODRECAS` | Causal record/replay for concurrent asynchronous systems | Documented experimental recorder and adapter; incomplete synchronization coverage and no general execution replay | Establish a precise supported execution model; adversarially test missing dependencies, cancellation, races, and replay determinism |
| `LedgerTrace` | Repository README identifies the current product as Caseweft: local-first AP exception evidence workbench | Documented local workflow; no authenticated multi-tenant recurring SaaS, secure customer intake, or validated price | Verify product naming and all claims; test against labelled AP cases; interview intended AP buyers before expanding SaaS scope |
| `Vesper` | Adaptive self-directed learning and inquiry environment | Documented local learning workflow; learner-authored sources are not independently verified and no cloud learner profile exists | Test learning outcomes and source quality; distinguish engagement from durable learning; validate the core learning loop |
| `Migraven` | C17 migration-export comparison with source-row evidence | Documented evaluation-stage engine; exact equality and selected-field comparison; no security certification or commercial proof | Run cross-platform/sanitizer tests; benchmark against standard diff/migration tools; validate costly migration failure cases |
| `DatasheetDelta` | Engineering document revision comparison and evidence register | Documented extraction and comparison limits; scanned PDF OCR and complex-layout understanding absent | Build labelled extraction corpus; measure precision/recall by format; test whether review time or escaped changes improve |
| `CommitmentGraph` | Evidence-linked business commitment and event investigation | Documented single-workspace control system; not multi-tenant SaaS and findings do not establish legal truth | Audit access control, evidence lifecycle, and rule correctness; validate a recurring operational buyer problem |
| `ai-continuity` | Archived repository; README is empty | Unknown | Inspect repository metadata and tree before deciding whether to revive, merge, or retire |
| `procurement-intelligence` | Archived repository reported empty by GitHub contents API | Unknown / no inspectable README | Confirm repository state and decide whether it has any recoverable value |
| `aurelis-aci` | Broad AI operational control, assurance, evidence, and intelligence layer | Documented architecture and sandbox demo; production deployment details require verification | Compare overlap with AAI, AOA, and Aurelis Authority; choose one canonical product boundary |
| `aurelis-aoa` | AI outcome assurance against workflow contracts and execution traces | Documented bounded verifier; production integrations, auth, persistence, and billing are outside standalone core | Validate verdict semantics and regression generation; test against realistic traces; assess overlap with AAI |
| `aurelis-aai` | AI change and release assurance | Documented workflow and public synthetic demo; live customer evidence not claimed | Verify deployed controls and API; establish a differentiated release-assurance use case |
| `Aurelis-Authority` | Independent AI agent authority assessment | Documented scoped assessment and synthetic executable demo; placeholders and private assessment controls remain | Verify contact/deployment configuration; test assessment repeatability; assess whether this is the strongest commercial wedge |
| `AurelDesktop` | Windows desktop clock/status companion and cursor scheme utility | Documented desktop features; wider shell replacement intentionally absent | Test install/uninstall, settings recovery, Windows versions, and cursor restoration; establish a user need beyond aesthetic preference |
| `VentureLabs` | Evidence-led venture thesis and experiment workspace | Documented local-first tool; heuristic signals are not market-validation probabilities; no backend or payment system | Test whether founders repeatedly use the evidence/experiment workflow and whether a paid decision service is demanded |
| `IL-ROSSO` | Ferrari editorial fan museum and interactive concept experience | Documented fan project; 3D model is explicitly illustrative, not a real Ferrari model | Verify factual sourcing, image rights, performance, accessibility, and whether the experience meets the intended editorial standard |
| `Phantom` | x86-64 Assembly offline PCAP analyzer | Documented passive parser; bounded classic PCAP support and explicit protocol limits | Run malformed-input fuzzing and parser tests; verify assembly-only executable boundary and compare output with trusted PCAP tooling |
| `KERNIQ` | Repository listed in account inventory; README fetch returned 404 | Unknown; do not infer purpose from name | Resolve repository visibility/default branch/content before any judgment |
| `DT-09` | Portfolio/profile and selected-work index | README describes nine selected systems; prior profile commit exists, but linked project claims are not a substitute for individual audits | Verify every link, selected project evidence, rendering/accessibility, and consistency with audited repository status |

**Correction note:** The register above is a working inventory. Repository names are kept distinct even where projects overlap. The README for `KERNIQ` could not be retrieved, and the archived repositories `ai-continuity` and `procurement-intelligence` have no usable README content in this pass. Resolve these before assigning product conclusions.

## Portfolio-level questions

- Which projects solve distinct problems, and which are competing implementations of the same thesis?
- Which capabilities are genuinely reusable infrastructure rather than duplicated code?
- Which projects have a credible path to an external user and measurable outcome?
- Which projects should be research-only, merged, archived, or stopped?
- What evidence would justify spending another week on each project?
- What is the opportunity cost of keeping every repository active?

## Audit sequence

1. Resolve inventory and repository identity.
2. Inspect source tree, dependencies, CI, tests, security-sensitive paths, deployment configuration, and recent commits.
3. Execute existing tests and reproduce the documented demo/build from a clean environment where feasible.
4. Check public deployment and external claims without assuming that a URL or badge proves health.
5. Write a project-specific problem thesis, assumption ledger, Bayesian evidence log, and falsification criteria.
6. Choose one of: continue, narrow, redesign, merge, research-only, archive.
7. Implement only changes justified by the findings; preserve a reviewable commit trail.
8. Re-run verification and update the register with evidence and commit references.

## Non-negotiable stop conditions

- No invented users, customers, testimonials, revenue, benchmarks, or validation.
- No production-readiness claims based only on a successful build.
- No security claims without a threat model and relevant testing.
- No algorithmic novelty claims without literature review and comparative evidence.
- No new feature until its user, outcome, and acceptance test are defined.
- No irreversible repository changes based on an unverified assumption.
