# startup-idea-screener-skill

> Screen, cluster, and reframe raw startup pain points from `startup-idea-hunter-skill` (CSV or JSON) into 3 evidence-backed product concepts and 1 verifiable MVP direction using the Easy-Vibe Stage 1B (`finding-great-idea`) methodology.

## Purpose

`startup-idea-screener-skill` is the downstream screening and concept-synthesis skill paired with `startup-idea-hunter-skill`. While Hunter collects raw complaints across forums, reviews, and job boards, Screener groups those scattered complaints into **Opportunity Clusters**, filters out the **Xiaoming Trap** (incumbent sufficiency, behavioral friction, free substitution), applies **Horizontal Segmentation** and **Vertical Emotion Timelines**, and produces:
1. **3 Evidence-Backed Product Concepts** with Before/After Value Reframing tables.
2. **1 Verifiable Product Direction** with *"One Person, One Job, One Entry Point"* positioning, a 3-Phase MVP Roadmap, 3 Solo-Founder Concern Mitigations, Bottom-Up TAM & 6-Moat analysis, 5-Round AI Dialogue Prompts, and the 20-Item Demand Verification Checklist (Appendix F).

## Activation

This skill activates when users ask to screen, filter, cluster, or reframe pain points collected from `startup-idea-hunter-skill` (such as `ideas_27_Oct.csv` or `clues.json`), check ideas against the Xiaoming Trap, or build an Easy-Vibe Stage 1B MVP validation dossier. Invoke with `/startup-idea-screener-skill` or natural language in any language.

**Example queries:**
- `/startup-idea-screener-skill --input ideas-explore/ideas_27_Oct.csv --output output/screening-dossier.json --markdown output/screening-dossier.md`
- `/startup-idea-screener-skill Screen the pain points in ideas_27_Oct.csv using Easy-Vibe finding-great-idea and recommend the #1 direction to build`
- "Filter these startup clues against the Xiaoming Trap, reframe the top 3 product concepts, and generate a 3-phase MVP plan"

## Usage

Run the deterministic pipeline on a Hunter CSV or JSON file:

```bash
python3 scripts/run_pipeline.py \
  --input ideas-explore/ideas_27_Oct.csv \
  --output output/screening-dossier.json \
  --markdown output/screening-dossier.md
```

## Gotchas

- **Hunter CSV files include a template example row at `STT == 0`**: `scripts/ingest_hunter_clues.py` automatically skips rows where `STT == "0"` or `Note == "Example"` so template instructions never pollute cluster scoring.
- **High complaint volume on consumer/parenting topics can mask a Xiaoming Trap**: A topic with many Reddit rants (e.g., kids' screen time or school chat apps) still receives `REFINE_NICHE_SEGMENT` if built as a generic app blocker or school-wide chat replacement where free OS controls or district-mandated apps (ClassDojo/Seesaw) already lock in habits. B2B workflows where buyers actively pay humans on Upwork (`tier_2_clumsy_manual_patch`) consistently outscore consumer habit apps on true willingness to pay.
- **Never promote a `"desire"` (vitamin) cluster to `COMMIT_AND_VALIDATE`**: Even if surface market size looks huge, `scripts/screen_and_reframe.py` flags any cluster with `dominant_need_tier == "desire"` or `trap_risk_sum_15 >= 10.5` as `DROP_XIAOMING_TRAP`.

## Implementation

Full skill definition, scripts, and references are in `SKILL.md` and accompanying directories. Read `SKILL.md` for complete instructions.

## Files

- `SKILL.md` — Full skill definition (agentskills.io format), including the `## Gotchas` section
- `scripts/` — Executable pipeline (`run_pipeline.py` orchestrator, `ingest_hunter_clues.py`, `screen_and_reframe.py`, `run_evals.py`, `evolve.py`)
- `references/` — Detailed documentation (`finding-great-idea-playbook.md`, `screening-and-reframing-math.md`, `troubleshooting.md`)
- `assets/` — Default screening weights, Xiaoming Trap thresholds, and 5-tier alternative matrix (`config.json`)
- `evals/` — Bundled eval spec: binary checks + golden cases; `evals/caliper/` holds the agent-run (Caliper) spec
- `install.sh` / `install.ps1` — Cross-platform installers
