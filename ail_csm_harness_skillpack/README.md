# AIL CSM Harness — Case State Machine Skillpack

Canonical operational harness for the AIL + MoIE recursive research system.

CSM = **Case State Machine** — the 13-state guarded workflow that turns a problem into a falsifiable hypothesis, executes a test, synthesizes evidence, routes the result through JEV, updates the working theory, and re-enters with the next test.

This package is the 21-file operational surface. Each file is a single responsibility. Load the ones you need; the full harness is the union.

## What this is

A reproducible research harness that enforces, in order:

1. Problem framing
2. Assumption inventory
3. Axiom inversion
4. Competing mechanisms (MoIE)
5. Falsifiable hypothesis
6. Preregistered prediction
7. Experimental design with controls
8. Deterministic execution
10. Raw results preservation
11. Statistical analysis
12. JEV evidence routing
13. Evidence synthesis
14. Theory update
15. Recursive re-entry
16. Provenance / lineage
17. Human escalation gates
18. State machine enforcement
19. Cross-domain validation template
20. Expert calibration protocol
21. Benchmark run record

## What this is not

- Not a claim that every hypothesis will be correct.
- Not a substitute for domain expertise on consequential questions.
- Not an autonomous research swarm.
- Not a dashboard without a stable loop underneath.

## Quick start

```bash
# One command should be able to bootstrap a new case:
ailmoie new-case "research question"
```

Expected output for a complete case:

```text
case.json
preregistration.json
hypotheses.json
experiment/
results/raw.json
results/summary.md
evidence/summary.md
evidence/detail.json
jev/decision.json
theory/version-2.json
reentry/next-test.json
provenance/lineage.json
```

## Files in this package

| # | File | Responsibility |
|---|------|---------------|
| 1 | README.md | This file. Package overview and quick start. |
| 2 | MANIFEST.md | File inventory with purpose, inputs, and outputs for each file. |
| 3 | 01_problem_intake.md | What makes a problem suitable for CSM. Intake criteria. |
| 4 | 02_assumption_inventory.md | Assumption elicitation, load-bearing selection, catalog. |
| 5 | 03_axiom_inversion.md | The inversion method: stages, examples, falsification conditions. |
| 6 | 04_rederivation.md | Re-deriving hypothesis from inverted assumption. |
| 7 | 05_moie_mechanisms.md | Five MoIE roles, competing mechanisms, discrimination design. |
| 8 | 06_hypothesis.md | Hypothesis formulation, falsifiability, H0/H1/alternatives. |
| 9 | 07_prediction.md | Preregistered predictions, frozen before execution. |
| 10 | 08_experimental_design.md | Controls, parameters, metrics, replication, statistical plan. |
| 11 | 09_execution.md | Code execution, determinism, seeds, reproducibility. |
| 12 | 10_raw_results.md | Raw output preservation, no silent editing. |
| 13 | 11_statistical_results.md | Analysis, uncertainty, confidence, effect thresholds. |
| 14 | 12_jev_routing.md | JEV decision procedure, evidence object, weights, thresholds. |
| 15 | 13_evidence_synthesis.md | Three evidence layers: summary, overview, detailed breakdown. |
| 16 | 14_theory_update.md | Updated theory, remaining unknowns, next-test lineage. |
| 17 | 15_recursive_reentry.md | Re-entry protocol, re-entry invariants. |
| 18 | 16_provenance.md | Lineage graph, immutable records, amendment discipline. |
| 19 | 17_human_escalation.md | When to escalate, what to ask, authority boundaries. |
| 20 | 18_state_machine.md | Full 13-state spec with guarded transitions and invariants. |
| 21 | 19_cross_domain_validation.md | Cross-domain validation template and comparison structure. |

## Reading order

For a first pass, read in file-number order. For a working operator, the core loop files are:

- 01 → 02 → 03 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15
- 16 and 17 are governance.
- 18 is the enforcement contract.
- 19 is the cross-domain template.

## Core principle

**Do not scale the number of agents until the research loop itself is stable.**

Scale:

**questions → experiments → evidence → knowledge**

not:

**agents → tokens → transcripts**

## Domain artifacts in this repo

Two repaired domain artifacts demonstrate CSM applied:

- `runs/run_epidemiology_foodborne_outbreak.md` — synthetic outbreak investigation with explicit falsification and evidence thresholds.
- `runs/run_constitutional_carpenter.md` — Fourth Amendment CSLI brief with corrected circuit-split framing and case-holding accuracy.

Both are preliminary research artifacts. Neither is represented as a completed real-world investigation or a filing-ready brief without the missing evidence and procedural information.
