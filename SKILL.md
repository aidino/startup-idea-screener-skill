---
name: startup-idea-screener-skill
description: >-
  Screen, cluster, and reframe raw startup pain points from startup-idea-hunter-skill
  (CSV or JSON) into 3 evidence-backed product concepts and 1 verifiable MVP direction
  using the Easy-Vibe Stage 1B (finding-great-idea) methodology. Activates when users
  ask to filter or screen startup ideas, analyze Hunter CSV or JSON clue tables, check
  for the Xiaoming Trap (incumbent sufficiency, behavioral friction, free substitution),
  apply the 5-tier alternative solution matrix, segment users horizontally, map vertical
  context and emotion timelines (fear, anxiety, helplessness, loneliness, anger, regret),
  reframe ordinary features into high-willingness-to-pay copilots, estimate bottom-up TAM
  and 6 moats, or run the 20-item demand verification checklist.
activation: /startup-idea-screener-skill
license: MIT
metadata:
  author: aidino
  version: 1.0.0
  created: "2026-10-27"
  last_reviewed: "2026-10-27"
  review_interval_days: 90
provenance:
  maintainer: aidino
  version: 1.0.0
  created: "2026-10-27"
  source_references:
    - https://datawhalechina.github.io/easy-vibe/vi-vn/stage-1/finding-great-idea/
    - https://raw.githubusercontent.com/datawhalechina/easy-vibe/main/docs/vi-vn/stage-1/finding-great-idea/index.md
---

# /startup-idea-screener-skill

Turn a noisy table of raw complaints from `startup-idea-hunter-skill` (such as `ideas_27_Oct.csv` or `scorecard.json`) into the two canonical deliverables of the Easy-Vibe **Finding a Great Idea (`finding-great-idea`)** chapter:
1. **3 Evidence-Backed Product Concepts (`top_3_product_concepts`)**: Deduplicated Opportunity Clusters enriched with multi-channel behavioral proof, Horizontal User Segmentation (Appendix B), Vertical Context & Emotion Timelines (Appendix C), and Before/After Value Reframing tables (Appendix D).
2. **1 Verifiable Product Direction (`verifiable_product_direction`)**: The #1 winning opportunity framed via *"One Person, One Job, One Entry Point"*, complete with a 3-Phase MVP Roadmap, 3 Solo-Founder Concern Mitigations, Bottom-Up TAM & 6-Moat Strategy (Appendix A), 5-Round AI Refinement Prompts (Appendix E), and the 20-Item Demand Verification Checklist (Appendix F).

## When to Use This Skill

Invoke `/startup-idea-screener-skill` when you want to:
- Screen and cluster raw pain points exported from `startup-idea-hunter-skill` (`.csv` or `.json`) to decide which direction is actually worth building.
- Audit candidate startup ideas against the **Xiaoming Trap** (Incumbent Sufficiency, Behavioral Friction, Free Substitution) and the **5-Tier Alternative Solution Matrix**.
- Reframe an ordinary tool idea (e.g., *"PDF to Excel converter"*, *"fitness tracker"*, *"parental screen blocker"*) into a fear-relieving specialist copilot via **Horizontal Segmentation** and **Vertical Emotion Timelines**.
- Produce a concrete **3-Phase MVP Validation Plan**, **Bottom-Up TAM calculation**, and **20-Item Demand Checklist** before writing application code.

**Language adaptability**:
- Always respond in the language used by the user (Vietnamese, English, etc.), while preserving canonical English JSON keys and verdict enums (`COMMIT_AND_VALIDATE`, `KEEP_AS_BACKUP_CONCEPT`, `REFINE_NICHE_SEGMENT`, `DROP_XIAOMING_TRAP`).

**Anti-goals**:
- Do NOT activate for general software engineering, database tuning, or infrastructure deployment tasks.
- Never promote a `"desire"` (vitamin) cluster to `COMMIT_AND_VALIDATE`; fear and acute loss drive payment, whereas desire leads to procrastination.

## Prerequisites

- **Runtime**: Python 3.9+ (100% standard library; zero third-party packages required).
- **Input**: A `.csv` or `.json` file containing raw clues from `startup-idea-hunter-skill` (or user-collected pain points).

Verify environment readiness anytime:

```bash
python3 scripts/run_pipeline.py --check-prereqs
python3 scripts/run_pipeline.py --diagnostics
```

## Workflows

### Workflow 1: Screen a Hunter CSV or JSON Clue Table End-to-End (Deterministic Happy Path)

**Run** `python3 scripts/run_pipeline.py` directly on a CSV file exported from `startup-idea-hunter-skill` (like `ideas-explore/ideas_27_Oct.csv`) or a JSON clue file:

```bash
python3 scripts/run_pipeline.py \
  --input ideas-explore/ideas_27_Oct.csv \
  --output output/screening-dossier.json \
  --markdown output/screening-dossier.md
```

This single command ingests the rows, skips template example rows (`STT == 0`), groups related complaints into Opportunity Clusters, evaluates all 4 Easy-Vibe screening gates, and writes both the structured JSON dossier and the full Markdown report.

### Workflow 2: Two-Step Custom Clustering & Screening

When you want to inspect or customize the intermediate Opportunity Clusters before final scoring:

1. **Run** `python3 scripts/ingest_hunter_clues.py` to parse and cluster raw clues:
   ```bash
   python3 scripts/ingest_hunter_clues.py \
     --input evals/golden/case-1/input.json \
     --output /tmp/clustered-clues.json
   ```
2. **Run** `python3 scripts/screen_and_reframe.py` on the clustered JSON to compute the 4-gate scores, Top 3 Product Concepts, and #1 Verifiable MVP Plan:
   ```bash
   python3 scripts/screen_and_reframe.py \
     --input /tmp/clustered-clues.json \
     --output output/dossier.json \
     --markdown output/dossier.md
   ```

## Available Scripts

- **Run** `python3 scripts/run_pipeline.py --input <clues.csv|clues.json> --output <dossier.json> [--markdown <dossier.md>]` — end-to-end deterministic orchestrator.
- **Run** `python3 scripts/ingest_hunter_clues.py --input <clues.csv|clues.json> --output <clustered.json>` — parses Hunter CSV/JSON files and groups individual quotes into semantic Opportunity Clusters.
- **Run** `python3 scripts/screen_and_reframe.py --input <clustered.json> --output <dossier.json> [--markdown <dossier.md>]` — runs the 4-gate screening engine and builds the Top 3 Product Concepts + #1 Verifiable Direction.
- **Run** `python3 scripts/run_evals.py --validate` — validates the bundled evaluation specification and golden cases.
- **Run** `python3 scripts/evolve.py --correct "<what the result got wrong>"` — records a domain correction into `EVOLUTION.md`, `## Gotchas`, and regression tests.

## Available Analyses

**Read** `references/finding-great-idea-playbook.md` and **Read** `references/screening-and-reframing-math.md` for full formulas and rubrics:

1. **Opportunity Clustering & Multi-Channel Evidence Density**: Combines scattered complaints from Reddit, Upwork/Fiverr, Capterra/G2, and Indie Hackers into unified problem clusters.
2. **Gate 1–2: Base Demand & Xiaoming Trap Audit**: Penalizes ideas where existing free incumbents are "good enough" (`incumbent_sufficiency_risk`), where users must manually log data before getting value (`behavioral_friction_risk`), or where free substitutes abound (`free_substitution_risk`).
3. **Gate 3: 5-Tier Alternative Solution Matrix (Appendix A)**: Rewards Tier 2 (`tier_2_clumsy_manual_patch` — Excel/manual typing/Upwork freelancers, `+8.0` pts) and Tier 3 (`tier_3_multi_tool_stitching`, `+6.5` pts) while penalizing Tier 5 (`tier_5_satisfied_incumbent`, `-15.0` pts).
4. **Gate 4: Horizontal Segmentation & Vertical Emotion Timeline (Appendices B–D)**: Scores sub-segments across Pain, WTP, Size, Competition Headroom, and Founder Reachability; traces the 6 Core Emotions (`fear`, `anxiety`, `helplessness`, `loneliness`, `anger`, `regret`); and reframes tools into specialist copilots.
5. **3-Phase MVP Roadmap, Bottom-Up TAM & 20-Item Checklist (Appendices E–F)**: Produces the Phase 1–3 plan, 3 solo-founder concern mitigations, TAM calculation, 6-moat selection, 5-round AI dialogue prompts, and the 20-item verification checklist.

## Error Handling

All scripts emit structured JSON errors to `stderr` with `"error"`, `"error_type"` (`"validation"` or `"runtime"`), `"details"`, and `"hint"`, then exit with code `1`. **Read** `references/troubleshooting.md` for recovery steps.

## Gotchas

- **Hunter CSV files include a template example row at `STT == 0`**: `scripts/ingest_hunter_clues.py` automatically skips rows where `STT == "0"` or `Note == "Example"` so template instructions never pollute cluster scoring.
- **High complaint volume on consumer/parenting topics can mask a Xiaoming Trap**: A topic with many Reddit rants (e.g., kids' screen time or school chat apps) still receives `REFINE_NICHE_SEGMENT` if built as a generic app blocker or school-wide chat replacement where free OS controls or district-mandated apps (ClassDojo/Seesaw) already lock in habits. B2B workflows where buyers actively pay humans on Upwork (`tier_2_clumsy_manual_patch`) consistently outscore consumer habit apps on true willingness to pay.
- **Never promote a `"desire"` (vitamin) cluster to `COMMIT_AND_VALIDATE`**: Even if surface market size looks huge, `scripts/screen_and_reframe.py` flags any cluster with `dominant_need_tier == "desire"` or `trap_risk_sum_15 >= 10.5` as `DROP_XIAOMING_TRAP`.

## Keywords for Automatic Detection

**Entities**: startup-idea-screener-skill, Easy-Vibe, finding-great-idea, Xiaoming Trap, Opportunity Cluster, horizontal segmentation, vertical emotion timeline, value reframing, bottom-up TAM, 6 moats, Appendix F 20-item checklist
**Metrics**: final_screening_score_100, xiaoming_trap_penalty, alternative_tier, segment_fit_score_5, pre-order conversion rate (>10% Go, 5-10% Refine, <5% Kill)
**Actions**: screen startup ideas, filter hunter clues, cluster pain points, audit Xiaoming Trap, reframe product value, build 3-phase MVP plan

**Activation examples**:
- `/startup-idea-screener-skill --input ideas-explore/ideas_27_Oct.csv --output output/dossier.json`
- `/startup-idea-screener-skill Screen the clues from startup-idea-hunter-skill and pick the best MVP direction`
- "Use Easy-Vibe finding-great-idea to filter my pain points, avoid the Xiaoming Trap, and reframe the top 3 product concepts"
**Does NOT activate for**:
- "Set up a GitHub Actions workflow for Docker builds"
- "Write a SQL query to calculate monthly churn"

## References

| File | When to read this |
|---|---|
| `references/finding-great-idea-playbook.md` | **Read** when explaining the Xiaoming Trap, the 5-Tier Alternative Matrix, Horizontal/Vertical segmentation, Value Reframing, or the 3-Phase MVP & 20-Item Checklist |
| `references/screening-and-reframing-math.md` | **Read** when inspecting the exact 4-Gate mathematical formulas, Evidence Density Bonus, Xiaoming Trap Penalty, or Bottom-Up TAM thresholds |
| `references/troubleshooting.md` | **Read** when resolving CSV/JSON ingestion errors or understanding why a high-volume consumer complaint was downgraded by the Xiaoming Trap gate |
