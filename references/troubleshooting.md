# Troubleshooting Guide (`startup-idea-screener-skill`)

## 1. Input Format & CSV Parsing Errors

### Symptom
`scripts/run_pipeline.py` exits with code `1` and emits `"error_type": "validation"` regarding missing or empty clues.

### Cause & Fix
- **CSV Header Mismatch**: When passing a CSV file exported from `startup-idea-hunter-skill` (such as `ideas-explore/ideas_27_Oct.csv`), ensure it contains standard Hunter columns (`STT`, `Vấn đề / Câu nói gốc...`, `Bối cảnh...`, `Nguồn / Link...`, `Ngày tháng`, `Note`) or English equivalents (`id`, `quote`, `context`, `source_url`, `date`, `note`).
- **Template Example Row (`STT == 0`)**: `scripts/ingest_hunter_clues.py` automatically skips template example rows where `STT == "0"` or `Note == "Example"`. Make sure your CSV has at least one real clue row (`STT >= 1`).

---

## 2. Why a High-Scoring Hunter Clue Was Downgraded to `REFINE_NICHE_SEGMENT` or `DROP_XIAOMING_TRAP`

### Symptom
A clue that had an 85–90 score in `startup-idea-hunter-skill` receives a lower rank or `REFINE_NICHE_SEGMENT` in `startup-idea-screener-skill`.

### Cause & Fix
`startup-idea-hunter-skill` scores individual quotes on raw complaint intensity. `startup-idea-screener-skill` applies the **Easy-Vibe Stage 1B (`finding-great-idea`)** filters:
1. **Xiaoming Trap Penalty**: Consumer/parenting habit apps where users must log behavior daily or where incumbents (Keep, Apple Screen Time, ClassDojo) already exist suffer higher `behavioral_friction_risk` and `incumbent_sufficiency_risk` than B2B workflows where companies already pay freelancers on Upwork.
2. **Alternative Solution Tier**: Clues backed by **Tier 2 (`tier_2_clumsy_manual_patch` — Excel + paid Upwork manual data entry)** or **Tier 3 (`tier_3_multi_tool_stitching`)** receive `+8.0` and `+6.5` modifiers because willingness to pay is already proven by behavior.

To override a cluster's segment focus or Xiaoming Trap rating, pass structured JSON with explicit `xiaoming_trap` or `alternative_tier` fields, or record a permanent domain rule via:

```bash
python3 scripts/evolve.py --correct "Your domain correction rule here"
```
