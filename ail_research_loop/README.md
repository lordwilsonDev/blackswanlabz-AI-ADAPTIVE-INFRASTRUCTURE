# AIL + MoIE Research Loop

The **generation** half of the AIL + MoIE system. A recursive research loop:

> problem → AIL assumptions → inversion → MoIE competing mechanisms → hypothesis → preregistered prediction → experiment → evidence → JEV routing → updated theory → re-entry

- **AIL (Axiom Inversion Logic)** — surface the load-bearing assumptions in a problem and invert them to open new hypothesis space.
- **MoIE (Mixture of Inversion Experts)** — generate competing mechanisms and design tests that discriminate between them.
- **JEV** — the decision procedure that classifies how evidence relates to a claim (e.g. supports, contradicts, conditional, unknown), with explicit gates for uncertainty, contradiction, confounding, scope, and novelty.

Its output goes to [`../ail_audit_chain/`](../ail_audit_chain/) for verification before release.

## Files

| File | What it is |
|---|---|
| [`spec.md`](spec.md) | Formal protocol specification v1.0: objects, state machine, transition guards, AIL / MoIE / JEV procedures, evidence-weighting rules |
| [`schemas.json`](schemas.json) | JSON Schema (Draft 2020-12) for the core objects |
| [`reference_implementation.py`](reference_implementation.py) | Standard-library-only state machine, JEV decision procedure, evidence weighting, theory update |
| [`test_reference.py`](test_reference.py) | Unit tests for the core invariants |
| [`execution-plan.md`](execution-plan.md) | Execution Plan v1.0: architecture, FreeBuff/Hermes division of labor, Phases 0–6 (freeze evidence → reference implementation → JEV → expert calibration → provenance → re-entry → real cycles) |

## Run it

```bash
cd ail_research_loop
python -m unittest -v test_reference.py   # 8 tests
python reference_implementation.py        # smoke example: one cycle, prints its JSON record
```

Python 3.10+; no dependencies.

## State machine

The reference implementation follows `spec.md` §5:

```
DRAFT → PROBLEM_DEFINED → HYPOTHESIS_FORMED → PREREGISTERED → READY_TO_EXECUTE
→ EXECUTING → RESULTS_AVAILABLE → EVIDENCE_SYNTHESIZED → JEV_EVALUATED
→ THEORY_UPDATED → REENTRY_READY → COMPLETE   (or back to PROBLEM_DEFINED)

Exceptional: BLOCKED · FAILED_EXECUTION · INVALIDATED
```

A state cannot advance unless its required artifact exists; predictions are frozen at `PREREGISTERED`.

> **Known inconsistency:** `execution-plan.md` ("State machine") lists a different, finer-grained set of 15 states (`INTAKE`, `ASSUMPTIONS`, `INVERSION`, `MECHANISMS`, …, `ARCHIVED`) that makes the AIL and MoIE steps explicit states. The spec and code do not yet have those states; AIL and MoIE happen inside `PROBLEM_DEFINED → HYPOTHESIS_FORMED`. Reconciling the two is open work.

## What this does not claim

- It does not claim evidence automatically proves universal truth. JEV classifies the relationship between a claim and the available evidence.
- The runs listed in `execution-plan.md` §1 (DRB-001 … DRB-005) are described there but their records are not included in this repository.
- Not an autonomous research swarm; human escalation gates are part of the design.
