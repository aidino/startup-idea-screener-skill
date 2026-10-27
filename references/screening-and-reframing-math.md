# Screening & Reframing Mathematics (`startup-idea-screener-skill`)

This reference documents the deterministic formulas, clustering rules, 4-gate scoring equations, bottom-up TAM calculation, and verdict thresholds implemented in `scripts/ingest_hunter_clues.py` and `scripts/screen_and_reframe.py`.

---

## 1. Gate 1: Base 5-Criteria & Need-Tier Score

For each clue or cluster $c$, the five Easy-Vibe criteria $s_i \in [1.0, 5.0]$ are combined using canonical weights:

$$\text{WeightedSum}_5 = 0.20 \cdot s_{\text{freq}} + 0.25 \cdot s_{\text{pain}} + 0.20 \cdot s_{\text{workaround}} + 0.25 \cdot s_{\text{wtp}} + 0.10 \cdot s_{\text{market}}$$

$$\text{BaseScore}_{100} = \min\left(100.0, \text{round}(\text{WeightedSum}_5 \times 20.0 \times M_{\text{tier}}, 2)\right)$$

where $M_{\text{tier}} = 1.15$ for `pain`, $1.00$ for `gratification`, and $0.75$ for `desire`.

When multiple clues are grouped into an **Opportunity Cluster**, the cluster's base score aggregates the top constituent clue scores and awards a **Multi-Evidence Density Bonus**:

$$\text{EvidenceBonus} = \min\left(6.0, 1.5 \times (\text{UniqueChannels} - 1) + 0.75 \times \min(4, \text{ClueCount} - 1)\right)$$

---

## 2. Gate 2: Xiaoming Trap Penalty

Each opportunity cluster is audited across the 3 Xiaoming Trap dimensions on a `[1.0, 5.0]` risk scale (`1.0` = minimal risk, `5.0` = severe trap):
- $r_{\text{incumbent}}$: **Incumbent Sufficiency Risk** (existing free/giant tools already satisfy users)
- $r_{\text{friction}}$: **Behavioral Friction Risk** (requires manual logging/setup before value delivery)
- $r_{\text{free}}$: **Free Substitution Risk** (generic feature with abundant free substitutes)

$$\text{TrapRiskSum}_{15} = r_{\text{incumbent}} + r_{\text{friction}} + r_{\text{free}}$$

$$\text{XiaomingTrapPenalty} = \max\left(0.0, \text{round}((\text{TrapRiskSum}_{15} - 5.0) \times 2.2, 2)\right)$$

If $\text{TrapRiskSum}_{15} \ge 10.5$ or `need_tier == "desire"`, the cluster is flagged with `xiaoming_trap_flagged = true`.

---

## 3. Gate 3: 5-Tier Alternative Solution Modifier

Based on Appendix A of `finding-great-idea`, the current workaround tier contributes $A_{\text{tier}}$:
- `tier_2_clumsy_manual_patch` (Excel, manual data entry, hiring Upwork freelancers): **$+8.0$**
- `tier_3_multi_tool_stitching` (Export/import across 3+ apps, e.g., ERP + Excel + Slack): **$+6.5$**
- `tier_4_unsatisfied_incumbent` (1–3 star reviews on Capterra/G2 citing specific broken steps): **$+2.0$**
- `tier_1_silent_endurance` (No workaround, silent tolerance): **$-3.0$**
- `tier_5_satisfied_incumbent` (Mature incumbent, high user satisfaction): **$-15.0$**

---

## 4. Gate 4: Horizontal Segmentation & Founder-Fit Bonus

Each candidate sub-segment is scored on 5 axes ($h_k \in [1.0, 5.0]$):
1. `pain_intensity` ($0.25$)
2. `willingness_to_pay` ($0.25$)
3. `segment_size` ($0.15$)
4. `competition_headroom` ($0.15$)
5. `founder_reachability` ($0.20$)

$$\text{SegmentFit}_{5} = 0.25 h_{\text{pain}} + 0.25 h_{\text{wtp}} + 0.15 h_{\text{size}} + 0.15 h_{\text{comp}} + 0.20 h_{\text{reach}}$$

$$\text{FounderFitBonus} = \text{round}((\text{SegmentFit}_{5} - 3.0) \times 3.5, 2)$$

---

## 5. Final Screening Score & Verdict Rules

$$\text{FinalScreeningScore}_{100} = \text{clamp}_{[0, 100]}\left(\text{BaseScore}_{100} + \text{EvidenceBonus} + A_{\text{tier}} + \text{FounderFitBonus} - \text{XiaomingTrapPenalty}\right)$$

### Decision Verdicts
1. **`COMMIT_AND_VALIDATE`**: Rank #1 opportunity with $\text{FinalScreeningScore}_{100} \ge 78.0$, `need_tier == "pain"`, and `xiaoming_trap_flagged == false`.
2. **`KEEP_AS_BACKUP_CONCEPT`**: Ranks #2 and #3 with $\text{FinalScreeningScore}_{100} \ge 65.0$ and `xiaoming_trap_flagged == false`.
3. **`REFINE_NICHE_SEGMENT`**: Intermediate clusters ($52.0 \le \text{FinalScreeningScore}_{100} < 78.0$) that require narrower horizontal segmentation before building.
4. **`DROP_XIAOMING_TRAP`**: Any cluster with `need_tier == "desire"`, `xiaoming_trap_flagged == true`, or $\text{FinalScreeningScore}_{100} < 52.0$.

---

## 6. Bottom-Up Market Sizing (TAM) Formula

Following Appendix A Step 3–4:

$$\text{AnnualTAM} = \text{TargetSegmentUsers} \times \text{PaidConversionRate} \times \text{AnnualARPU}$$

Track classification:
- **`large_track`**: $\ge \$100\text{M}$ (or $\ge 1\text{B RMB}$) — venture/platform scale
- **`specialized_business`**: $\$10\text{M} – \$100\text{M}$ (or $100\text{M} – 1\text{B RMB}$) — dedicated vertical SaaS company
- **`indie_micro_saas`**: $< \$10\text{M}$ (or $< 100\text{M RMB}$) — ideal solo founder / micro-SaaS wedge
