# BlackSwanLabz — AI Adaptive Infrastructure

Research infrastructure for Axiom Inversion Logic (AIL) and the Mixture of Inversion Experts (MoIE), by [Lord Wilson](https://github.com/lordwilsonDev).

The system has two halves, one that **generates** and one that **verifies**:

```
ail_research_loop/   problem → inversion → competing mechanisms → preregistered test
        │            → evidence → JEV routing → theory update → re-entry
        ▼
ail_audit_chain/     20-skill evidence-gated audit → release gate
        │            (DRAFT … FINAL-READY or BLOCKED)
        ▼
    released artifact
```

| Path | What it is |
|---|---|
| [`ail_research_loop/`](ail_research_loop/) | Formal spec, JSON schemas, reference implementation + tests, execution plan |
| [`ail_audit_chain/`](ail_audit_chain/) | Composable Skill Mesh: 20 audit skills + meta-skill, two domain runs |
| [`AIL_MoIE_Recursive_Research_Protocol.pdf`](AIL_MoIE_Recursive_Research_Protocol.pdf) | The protocol as a document |
| [`assets/`](assets/) | Four preliminary artifacts: Common Substrate (AIL/MoIE), AURORA-6 SSO mission design, HelixChem–Northbond merger analysis, K0 launch closure test protocol |
| [`reproduce.py`](reproduce.py) / [`reproduce_results.txt`](reproduce_results.txt) | Recomputes the numbers in the AURORA-6 and HelixChem artifacts (orbit, power, thermal, revisit, HHI) |

## Reproduce

```bash
python reproduce.py | diff - reproduce_results.txt      # needs numpy; no output = match
cd ail_research_loop && python -m unittest -v test_reference.py
```

Both were run on 2026-09-28: `reproduce.py` output is byte-identical to `reproduce_results.txt`, and the 8 reference tests pass.
