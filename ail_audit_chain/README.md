# AIL Audit Chain — Composable Skill Mesh (CSM)

The **verification** half of the AIL + MoIE system. A 20-skill, evidence-gated chain that turns a task into a defensible deliverable: it decomposes the task, gathers evidence, tests claims, exposes omissions, and assembles only what passes verification.

CSM = **Composable Skill Mesh** (defined in [`00-meta-skill.md`](00-meta-skill.md)): skills are modular, ordered by dependency, and rerun when upstream evidence changes.

It pairs with [`../ail_research_loop/`](../ail_research_loop/), which *generates* hypotheses and evidence. This chain *checks* what the loop (or anyone) produces before it is released.

## Core rules (from the meta-skill)

- The model proposes; source material and tests decide.
- Never invent facts, citations, data, authorities, calculations, or execution results.
- Separate **FACT / INFERENCE / HYPOTHESIS / SPECULATION / OPINION / UNKNOWN**.
- A citation is not validation: the source must exist *and* support the exact claim.
- Fail closed: unresolved critical defects block a "verified" or "final" label.

## Files

| # | File | Skill |
|---|------|-------|
| 0 | [`00-meta-skill.md`](00-meta-skill.md) | Orchestration contract, release gates, required outputs, stop conditions |
| 1 | [`01-intake-contract.md`](01-intake-contract.md) | Intake & contract |
| 2 | [`02-domain-risk.md`](02-domain-risk.md) | Domain boundary & risk classification |
| 3 | [`03-requirements-map.md`](03-requirements-map.md) | Artifact requirements extraction |
| 4 | [`04-evidence-inventory.md`](04-evidence-inventory.md) | Evidence inventory & provenance |
| 5 | [`05-citation-verification.md`](05-citation-verification.md) | Source & citation verification |
| 6 | [`06-data-schema-validation.md`](06-data-schema-validation.md) | Data & schema validation |
| 7 | [`07-definition-audit.md`](07-definition-audit.md) | Definitions & inclusion-rule audit |
| 8 | [`08-calculation-reproduction.md`](08-calculation-reproduction.md) | Calculation & reproduction audit |
| 9 | [`09-method-design-audit.md`](09-method-design-audit.md) | Method & design audit |
| 10 | [`10-counter-hypothesis.md`](10-counter-hypothesis.md) | Counter-hypothesis / counterargument |
| 11 | [`11-bias-confounding-audit.md`](11-bias-confounding-audit.md) | Bias, confounding & alternative explanations |
| 12 | [`12-temporal-procedural-consistency.md`](12-temporal-procedural-consistency.md) | Temporal & procedural consistency |
| 13 | [`13-reasoning-audit.md`](13-reasoning-audit.md) | Causal / legal reasoning audit |
| 14 | [`14-uncertainty-missingness.md`](14-uncertainty-missingness.md) | Missingness & uncertainty register |
| 15 | [`15-adversarial-red-team.md`](15-adversarial-red-team.md) | Adversarial red-team review |
| 16 | [`16-stakeholder-impact.md`](16-stakeholder-impact.md) | Stakeholder & impact review |
| 17 | [`17-action-proportionality-gate.md`](17-action-proportionality-gate.md) | Recommendation / relief proportionality gate |
| 18 | [`18-artifact-format-completeness.md`](18-artifact-format-completeness.md) | Artifact format & completeness |
| 19 | [`19-independent-replication.md`](19-independent-replication.md) | Independent second-pass verification |
| 20 | [`20-final-synthesis-release-gate.md`](20-final-synthesis-release-gate.md) | Final synthesis, evidence ledger & release gate |

## How to use it

Load `00-meta-skill.md` into your agent (Claude Code, Hermes, FreeBuff, or any LLM that takes a system prompt), then run skills 01 → 20 in order. For each skill, record status (PASS / FAIL / BLOCKED / N/A), inputs, outputs, evidence references, defects, and downstream invalidations. Skipped skills are marked with a reason; N/A is never silently PASS.

There is no CLI. The chain is a set of instructions, not code.

## Release gates

`DRAFT` → `EVIDENCE-CHECKED` → `CALCULATION-CHECKED` → `ADVERSARIAL-REVIEWED` → `FINAL-READY`, or `BLOCKED`.
Nothing is called "proven," "court-ready," or "publication-ready" unless that external review has actually happened.

## Domain runs

Two preliminary artifacts produced with the chain:

- [`runs/run_epidemiology_foodborne_outbreak.md`](runs/run_epidemiology_foodborne_outbreak.md) — synthetic outbreak investigation (not a real outbreak).
- [`runs/run_constitutional_carpenter.md`](runs/run_constitutional_carpenter.md) — Fourth Amendment CSLI brief section with corrected circuit-split framing.

Neither is represented as a completed real-world investigation or a filing-ready brief.

## Core principle

**Do not scale the number of agents until the loop itself is stable.**
Scale questions → experiments → evidence → knowledge, not agents → tokens → transcripts.
