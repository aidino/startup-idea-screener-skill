#!/usr/bin/env python3
"""
Screen Opportunity Clusters and synthesize 3 Evidence-Backed Product Concepts + 1 Verifiable MVP Direction.

Implements the complete Easy-Vibe Stage 1B ('finding-great-idea') methodology:
- Gate 1: 5-Criteria Demand Score + Need-Tier Multiplier + Multi-Evidence Bonus
- Gate 2: Xiaoming Trap Audit (Incumbent Sufficiency, Behavioral Friction, Free Substitution)
- Gate 3: 5-Tier Alternative Solution Matrix (Appendix A)
- Gate 4: Horizontal Segmentation & Founder-Fit Matrix (Appendix B)
- Expected Output #1: Top 3 Evidence-Backed Product Concepts (with Vertical Emotion Timeline & Value Reframing)
- Expected Output #2: 1 Verifiable Product Direction (One-Person-One-Job-One-Entry, 3-Phase MVP Plan,
  3 Concern Mitigations, Bottom-Up TAM, 6-Moat Selection, 5-Round AI Prompts, and 20-Item Appendix F Checklist)

Example:
    $ python3 scripts/screen_and_reframe.py --input /tmp/clustered.json --output output/dossier.json --markdown output/dossier.md
"""

from __future__ import annotations

import argparse
from typing import Any, Dict, List, Tuple
import sys
from pathlib import Path
from typing import Any, Dict, List


CRITERIA_WEIGHTS: Dict[str, float] = {
    "frequency": 0.20,
    "pain_level": 0.25,
    "current_workaround": 0.20,
    "willingness_to_pay": 0.25,
    "market_size": 0.10,
}

NEED_TIER_MULTIPLIERS: Dict[str, float] = {
    "pain": 1.15,
    "gratification": 1.00,
    "desire": 0.75,
}

ALTERNATIVE_TIER_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "tier_1_silent_endurance": {
        "label": "No current solution (silent endurance)",
        "opportunity": "Potentially large, but requires costly market education",
        "modifier": -3.0,
    },
    "tier_2_clumsy_manual_patch": {
        "label": "Clumsy manual workaround (Excel, copy-paste, paid Upwork typists)",
        "opportunity": "Golden Sweet Spot — active spending of time/money proven",
        "modifier": 8.0,
    },
    "tier_3_multi_tool_stitching": {
        "label": "Stitching multiple tools (Tool A + Tool B + Tool C)",
        "opportunity": "High-value workflow integration & automation wedge",
        "modifier": 6.5,
    },
    "tier_4_unsatisfied_incumbent": {
        "label": "Mature product exists, but users hate specific friction",
        "opportunity": "Requires sharp 10x wedge on the broken step",
        "modifier": 2.0,
    },
    "tier_5_satisfied_incumbent": {
        "label": "Mature product exists and users are satisfied",
        "opportunity": "Low opportunity unless disruptive for an ignored segment",
        "modifier": -15.0,
    },
}


def _emit_error(
    message: str,
    error_type: str = "validation",
    details: List[Dict[str, str]] | None = None,
    hint: str = "",
) -> None:
    """Emit structured JSON error to stderr and exit with code 1."""
    payload: Dict[str, Any] = {
        "error": message,
        "error_type": error_type,
        "details": details or [],
        "hint": hint or "Verify that input JSON contains a non-empty 'clusters' list from ingest_hunter_clues.py.",
    }
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(1)


def score_cluster(cluster: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate a single Opportunity Cluster across all 4 Easy-Vibe Screening Gates.

    Args:
        cluster: Cluster dictionary from ingest_hunter_clues.py.

    Returns:
        Enriched cluster dictionary with gate breakdown and final_screening_score_100.
    """
    clues = cluster.get("clues", [])
    if not clues:
        raise ValueError(f"Cluster '{cluster.get('cluster_id')}' contains zero clues")

    # Aggregate 5-criteria scores using the top 3 clues in the cluster (or all if <3)
    clue_weighted_sums: List[Tuple[float, Dict[str, float], str]] = []
    for c in clues:
        sc = c["scores"]
        w_sum = sum(float(sc[k]) * w for k, w in CRITERIA_WEIGHTS.items())
        clue_weighted_sums.append((w_sum, sc, c.get("need_tier", "pain")))

    clue_weighted_sums.sort(key=lambda x: x[0], reverse=True)
    top_slice = clue_weighted_sums[: min(3, len(clue_weighted_sums))]

    avg_criteria: Dict[str, float] = {}
    for k in CRITERIA_WEIGHTS:
        avg_criteria[k] = round(sum(item[1][k] for item in top_slice) / len(top_slice), 2)

    # Dominant need tier
    tier_counts = {"pain": 0, "gratification": 0, "desire": 0}
    for c in clues:
        t = str(c.get("need_tier", "pain")).lower()
        tier_counts[t if t in tier_counts else "pain"] += 1

    if tier_counts["desire"] > len(clues) / 2:
        dominant_tier = "desire"
    elif tier_counts["pain"] >= tier_counts["gratification"]:
        dominant_tier = "pain"
    else:
        dominant_tier = "gratification"

    multiplier = NEED_TIER_MULTIPLIERS[dominant_tier]
    weighted_sum_5 = sum(avg_criteria[k] * w for k, w in CRITERIA_WEIGHTS.items())
    raw_score_100 = round(weighted_sum_5 * 20.0, 2)
    base_score_100 = round(min(100.0, raw_score_100 * multiplier), 2)

    unique_channels = cluster.get("unique_channels") or sorted({c.get("channel", "reddit_community_pain") for c in clues})
    clue_count = len(clues)
    evidence_bonus = round(
        min(6.0, 1.5 * max(0, len(unique_channels) - 1) + 0.75 * min(4, max(0, clue_count - 1))),
        2,
    )

    # Gate 2: Xiaoming Trap Audit
    trap = cluster.get("xiaoming_trap", {})
    r_inc = float(trap.get("incumbent_sufficiency_risk", 2.5))
    r_fric = float(trap.get("behavioral_friction_risk", 2.5))
    r_free = float(trap.get("free_substitution_risk", 2.5))
    trap_risk_sum = round(r_inc + r_fric + r_free, 2)
    xiaoming_penalty = round(max(0.0, (trap_risk_sum - 5.0) * 2.2), 2)
    xiaoming_flagged = bool(trap_risk_sum >= 10.5 or dominant_tier == "desire")

    # Gate 3: 5-Tier Alternative Solution Matrix
    alt_key = str(cluster.get("alternative_tier", "tier_2_clumsy_manual_patch"))
    if alt_key not in ALTERNATIVE_TIER_MODIFIERS:
        alt_key = "tier_2_clumsy_manual_patch"
    alt_info = ALTERNATIVE_TIER_MODIFIERS[alt_key]
    alt_modifier = float(alt_info["modifier"])

    # Gate 4: Horizontal Segmentation & Founder-Fit Score
    segments = cluster.get("horizontal_segments", [])
    selected_seg = segments[0] if segments else {
        "segment_name": clues[0]["persona_context"],
        "core_pain": clues[0]["title"],
        "pain_intensity": avg_criteria["pain_level"],
        "willingness_to_pay": avg_criteria["willingness_to_pay"],
        "segment_size": avg_criteria["market_size"],
        "competition_headroom": 3.8,
        "founder_reachability": 4.0,
        "selected": True,
    }
    for seg in segments:
        seg_score = round(
            0.25 * float(seg["pain_intensity"])
            + 0.25 * float(seg["willingness_to_pay"])
            + 0.15 * float(seg["segment_size"])
            + 0.15 * float(seg["competition_headroom"])
            + 0.20 * float(seg["founder_reachability"]),
            2,
        )
        seg["segment_fit_score_5"] = seg_score
        if seg.get("selected"):
            selected_seg = seg

    seg_fit_5 = float(selected_seg.get("segment_fit_score_5", 4.0))
    founder_fit_bonus = round((seg_fit_5 - 3.0) * 3.5, 2)

    final_score = round(
        max(0.0, min(100.0, base_score_100 + evidence_bonus + alt_modifier + founder_fit_bonus - xiaoming_penalty)),
        2,
    )

    return {
        **cluster,
        "dominant_need_tier": dominant_tier,
        "need_tier_multiplier": multiplier,
        "aggregated_criteria_scores": avg_criteria,
        "gate_1_base_demand": {
            "raw_score_100": raw_score_100,
            "base_score_100": base_score_100,
            "evidence_density_bonus": evidence_bonus,
            "clue_count": clue_count,
            "unique_channels": unique_channels,
        },
        "gate_2_xiaoming_trap": {
            "incumbent_sufficiency_risk": r_inc,
            "behavioral_friction_risk": r_fric,
            "free_substitution_risk": r_free,
            "trap_risk_sum_15": trap_risk_sum,
            "xiaoming_trap_penalty": xiaoming_penalty,
            "xiaoming_trap_flagged": xiaoming_flagged,
            "trap_diagnosis": str(trap.get("trap_diagnosis", "")),
        },
        "gate_3_alternative_solution": {
            "tier_key": alt_key,
            "tier_label": alt_info["label"],
            "opportunity_meaning": alt_info["opportunity"],
            "score_modifier": alt_modifier,
        },
        "gate_4_horizontal_fit": {
            "winning_segment": selected_seg["segment_name"],
            "segment_fit_score_5": seg_fit_5,
            "founder_fit_bonus": founder_fit_bonus,
        },
        "final_screening_score_100": final_score,
    }


def build_verifiable_product_direction(winner: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construct Expected Output #2: The 1 Verifiable Product Direction with 3-Phase MVP,
    3 Concern Mitigations, Bottom-Up TAM, 6-Moat Selection, 5-Round AI Prompts, and 20-Item Checklist.
    """
    top_clue = winner["clues"][0]
    winning_seg = winner["gate_4_horizontal_fit"]["winning_segment"]
    reframed_title = winner["reframed_concept_title"]
    tam_params = winner.get("tam_parameters", {})
    target_users = int(tam_params.get("target_segment_users", 100000))
    conv_rate = float(tam_params.get("paid_conversion_rate", 0.05))
    arpu_usd = float(tam_params.get("annual_arpu_usd", 600))
    annual_tam_usd = round(target_users * conv_rate * arpu_usd, 2)

    if annual_tam_usd >= 100_000_000:
        tam_track = "large_track (>=$100M/yr — Venture / Platform Track)"
    elif annual_tam_usd >= 10_000_000:
        tam_track = "specialized_business ($10M–$100M/yr — Dedicated Vertical SaaS Company)"
    else:
        tam_track = "indie_micro_saas (<$10M/yr — Ideal Solo Founder / Micro-SaaS Wedge)"

    return {
        "winning_cluster_id": winner["cluster_id"],
        "reframed_product_title": reframed_title,
        "final_screening_score_100": winner["final_screening_score_100"],
        "one_person_one_job_one_entry": {
            "one_person": winning_seg,
            "one_job": winner["value_reframing"]["after_pain"],
            "one_entry_point": (
                f"Upload or forward {top_clue['input_data']} -> receive {top_clue['output_data']} "
                "in under 60 seconds with visual verification snippets and zero template setup."
            ),
            "mantra_summary": (
                f"For {winning_seg}, solve '{winner['value_reframing']['after_pain']}' starting from a single "
                f"drop-zone entry point ('{top_clue['input_data']}')."
            ),
        },
        "three_phase_mvp_roadmap": [
            {
                "phase": "Phase 1 (Months 1–2): Concierge / Human-in-the-Loop Validation MVP",
                "objective": "Verify real willingness to pay before building complex autonomous pipelines",
                "implementation": (
                    "Build a lightweight web upload / email-forwarding intake using an AI IDE + existing VLM/OCR APIs, "
                    "with a human-in-the-loop review check on flagged low-confidence cells before returning the verified Excel/ERP file."
                ),
                "target_metrics": "Acquire 100 target users in the niche; achieve >=10% paid conversion (>=10 paying customers or paid pilot deposits).",
            },
            {
                "phase": "Phase 2 (Months 3–6): SDK & Deterministic Verification Automation",
                "objective": "Automate 95%+ of routine documents and lock in daily/weekly retention",
                "implementation": (
                    "Integrate off-the-shelf document vision SDKs + deterministic row/column balance checks, "
                    "visual cropped-snippet sidecars for every questionable digit, and 1-click QuickBooks/Tally/CSV export."
                ),
                "target_metrics": "Reduce manual review time per 100 pages to <3 minutes; reach >40% 30-day cohort retention.",
            },
            {
                "phase": "Phase 3 (Months 6–12): Workflow Ecosystem, Partnerships & Adjacent Expansion",
                "objective": "Build high switching costs and expand across the adjacent back-office workflow",
                "implementation": (
                    "Add automated client document chasing, 3-way PO matching, and partner revenue-share channels "
                    "with bookkeeping communities and fractional CFO networks."
                ),
                "target_metrics": "Scale to 500+ paying firms/teams with net negative churn via multi-workflow lock-in.",
            },
        ],
        "solo_founder_concern_mitigations": [
            {
                "concern": "Technical Complexity (Fear of needing custom ML/OCR models from scratch)",
                "easy_vibe_solution": (
                    "Never train vision models from scratch in Phase 1. Combine existing multimodal APIs with "
                    "deterministic math checks (sum of rows == statement total) and cropped image snippets so the user trusts the output immediately."
                ),
                "estimated_phase1_cost": "$30–$100/mo in API tokens during the 100-user pilot",
            },
            {
                "concern": "Domain Authority Gap (Lack of deep CPA / audit / specialist credentials)",
                "easy_vibe_solution": (
                    "Partner with 2–3 practicing bookkeepers/auditors on a 70% product / 30% domain-partner revenue share "
                    "(or free lifetime access in exchange for co-designing the chart-of-accounts & audit validation rules)."
                ),
                "estimated_phase1_cost": "$0 upfront cash (revenue-share or pilot co-design exchange)",
            },
            {
                "concern": "User Acquisition & Marketing Budget (Fear of expensive paid ads)",
                "easy_vibe_solution": (
                    "Run narrow-keyword guerrilla outreach in r/Accounting, r/Bookkeeping, r/smallbusiness, and Upwork job threads; "
                    "offer to process a firm's nastiest 50-page blurry statement for free to prove 10x speed, then convert to a monthly plan."
                ),
                "estimated_phase1_cost": "<$150 total outreach budget; target CAC <$15 per trial user",
            },
        ],
        "bottom_up_tam": {
            "formula": "Target Segment Users × Paid Conversion Rate × Annual ARPU",
            "target_segment_users": target_users,
            "paid_conversion_rate": conv_rate,
            "annual_arpu_usd": arpu_usd,
            "estimated_annual_tam_usd": annual_tam_usd,
            "track_classification": tam_track,
        },
        "moat_strategy": {
            "primary_moat": str(tam_params.get("primary_moat", "switching_costs")),
            "secondary_moat": str(tam_params.get("secondary_moat", "data_accumulation")),
            "defensibility_explanation": winner["value_reframing"]["after_moat"],
        },
        "five_round_ai_dialogue_prompts": [
            {
                "round": 1,
                "goal": "State the reframed concept and surface the #1 solo-builder bottleneck",
                "prompt": (
                    f"I want to build '{reframed_title}' for {winning_seg}. "
                    "My biggest concern is guaranteeing 100% numerical accuracy on messy multi-vendor inputs as a solo builder. "
                    "Help me design a 3-phase MVP plan, concrete technical implementation using existing SDKs, cost estimate, and validation metrics."
                ),
            },
            {
                "round": 2,
                "goal": "Cut feature bloat down to a 2-week Phase 1 Concierge MVP",
                "prompt": (
                    f"Strip '{reframed_title}' down to the smallest workflow I can ship in 14 days to test whether "
                    "10 out of 100 target users will pay a deposit or monthly fee. What should be automated vs human-assisted?"
                ),
            },
            {
                "round": 3,
                "goal": "Resolve domain compliance & trust objections",
                "prompt": (
                    "Users in this niche fear silent AI hallucinations. What deterministic validation checks and UI trust signals "
                    "(like side-by-side cropped source snippets) will make them trust this over manual human data entry?"
                ),
            },
            {
                "round": 4,
                "goal": "Design a <$150 guerrilla acquisition experiment for the first 100 users",
                "prompt": (
                    f"How do I recruit the first 100 {winning_seg} from Reddit, Upwork, and niche communities with under $150 "
                    "in acquisition spend? Give me exact outreach hooks and a free-sample-to-paid conversion script."
                ),
            },
            {
                "round": 5,
                "goal": "Lock in Go / Pivot / Kill decision thresholds",
                "prompt": (
                    "Consolidate our plan into a 30-day execution schedule with strict Go (>10% paid), Refine (5-10% paid), "
                    "and Kill (<5% paid) gates."
                ),
            },
        ],
        "appendix_f_20_item_checklist": {
            "1_user_clarity": [
                {"item": "Can you describe the target user in one specific sentence?", "status": "READY", "evidence": winning_seg},
                {"item": "Do you know their exact current workaround?", "status": "READY", "evidence": winner["gate_3_alternative_solution"]["tier_label"]},
                {"item": "Can you recount their concrete daily context and emotional trigger?", "status": "READY", "evidence": winner["vertical_emotion_timeline"][0]["user_context"]},
                {"item": "Do they have proven budget / ability to pay?", "status": "READY", "evidence": winner["value_reframing"]["after_wtp"]},
            ],
            "2_pain_intensity": [
                {"item": "How much time, money, or energy do they currently lose?", "status": "READY", "evidence": top_clue["quote"][:140]},
                {"item": "What is the concrete consequence if left unsolved?", "status": "READY", "evidence": winner["vertical_emotion_timeline"][1]["emotion_detail"] if len(winner["vertical_emotion_timeline"]) > 1 else "Direct financial or operational loss"},
                {"item": "Have they already actively searched for or cobbled together a solution?", "status": "READY", "evidence": f"Verified across {len(winner['clues'])} independent clues in {winner['gate_1_base_demand']['unique_channels']}"},
                {"item": "How much are they actually paying today (freelancers, tools, overtime)?", "status": "READY", "evidence": winner["value_reframing"]["after_wtp"]},
            ],
            "3_solution_differentiation": [
                {"item": "What is the clear 10x advantage over their current workaround?", "status": "READY", "evidence": winner["value_reframing"]["after_pain"]},
                {"item": "Is the benefit strong enough to overcome switching habits?", "status": "READY", "evidence": "Zero-template drop-zone outputs native Excel/QuickBooks/Tally files without changing their ERP"},
                {"item": "Why won't giant incumbents or generic chat wrappers easily copy it?", "status": "READY", "evidence": winner["value_reframing"]["after_moat"]},
                {"item": "Does the differentiation justify the subscription price?", "status": "READY", "evidence": winner["value_reframing"]["after_wtp"]},
            ],
            "4_business_viability": [
                {"item": "Have you defined the payment test and pricing tier?", "status": "ACTION_REQUIRED", "evidence": "Run pre-order / paid pilot test (>10% = Go, 5–10% = Refine, <5% = Pivot)"},
                {"item": "Is customer acquisition cost (CAC) bounded and low?", "status": "READY", "evidence": "Target CAC <$15 via community pain threads and free sample audits"},
                {"item": "Does LTV comfortably exceed CAC?", "status": "READY", "evidence": f"Estimated Annual ARPU ${arpu_usd:.0f} vs <$15 guerrilla CAC"},
                {"item": "Are there clear expansion revenue paths?", "status": "READY", "evidence": winner["value_reframing"]["after_expansion"]},
            ],
            "5_fast_validation_1_2_weeks": [
                {"item": "Can you build a working prototype in 1–2 weeks?", "status": "READY", "evidence": "Phase 1 Concierge MVP uses existing VLM/OCR APIs + deterministic balance script"},
                {"item": "Can you interview 10 target users about their current workflow?", "status": "ACTION_REQUIRED", "evidence": f"Recruit 10 {winning_seg} from cited Reddit/Upwork threads"},
                {"item": "Can you run a controlled experiment for the core hypothesis?", "status": "READY", "evidence": "Process 10 real multi-page statements/invoices and measure verification time & error rate"},
                {"item": "Can you ask for a real deposit or paid pilot commitment?", "status": "ACTION_REQUIRED", "evidence": "Enforce >10% pre-order deposit gate before building Phase 2"},
            ],
        },
    }


def screen_and_reframe(clustered_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Screen all Opportunity Clusters and generate the complete Easy-Vibe Stage 1B Dossier.

    Args:
        clustered_payload: Output dictionary from ingest_and_cluster().

    Returns:
        Full screening dossier dictionary.
    """
    if not isinstance(clustered_payload, dict):
        raise ValueError("Input payload must be a JSON object")

    raw_clusters = clustered_payload.get("clusters")
    if not isinstance(raw_clusters, list) or len(raw_clusters) == 0:
        raise ValueError("Input payload must contain a non-empty 'clusters' list")

    scored_clusters: List[Dict[str, Any]] = []
    for cl in raw_clusters:
        scored_clusters.append(score_cluster(cl))

    scored_clusters.sort(
        key=lambda item: (
            not item["gate_2_xiaoming_trap"]["xiaoming_trap_flagged"],
            item["final_screening_score_100"],
            -item["gate_2_xiaoming_trap"]["xiaoming_trap_penalty"],
            item["gate_4_horizontal_fit"]["founder_fit_bonus"],
            item["gate_1_base_demand"]["clue_count"],
            item["gate_1_base_demand"]["base_score_100"],
        ),
        reverse=True,
    )

    for rank_idx, item in enumerate(scored_clusters, start=1):
        item["rank"] = rank_idx
        score = item["final_screening_score_100"]
        flagged = item["gate_2_xiaoming_trap"]["xiaoming_trap_flagged"]
        if flagged or item["dominant_need_tier"] == "desire" or score < 52.0:
            item["screening_verdict"] = "DROP_XIAOMING_TRAP"
        elif rank_idx == 1 and score >= 78.0 and item["dominant_need_tier"] == "pain":
            item["screening_verdict"] = "COMMIT_AND_VALIDATE"
        elif rank_idx <= 3 and score >= 65.0:
            item["screening_verdict"] = "KEEP_AS_BACKUP_CONCEPT"
        else:
            item["screening_verdict"] = "REFINE_NICHE_SEGMENT"

    viable_concepts = [c for c in scored_clusters if c["screening_verdict"] != "DROP_XIAOMING_TRAP"]
    top_3_source = viable_concepts[:3] if len(viable_concepts) >= 3 else scored_clusters[: min(3, len(scored_clusters))]

    top_3_concepts: List[Dict[str, Any]] = []
    for idx, c in enumerate(top_3_source, start=1):
        top_3_concepts.append(
            {
                "concept_rank": idx,
                "cluster_id": c["cluster_id"],
                "ordinary_idea_label": c["ordinary_idea_label"],
                "reframed_concept_title": c["reframed_concept_title"],
                "domain_category": c["domain_category"],
                "final_screening_score_100": c["final_screening_score_100"],
                "screening_verdict": c["screening_verdict"],
                "dominant_need_tier": c["dominant_need_tier"],
                "evidence_count": c["gate_1_base_demand"]["clue_count"],
                "evidence_channels": c["gate_1_base_demand"]["unique_channels"],
                "sample_verbatim_evidence": [
                    {
                        "id": cl["id"],
                        "title": cl["title"],
                        "quote": cl["quote"],
                        "source_url": cl["source_url"],
                        "channel": cl["channel"],
                    }
                    for cl in c["clues"][:4]
                ],
                "horizontal_segmentation": c["horizontal_segments"],
                "vertical_emotion_timeline": c["vertical_emotion_timeline"],
                "value_reframing_table": c["value_reframing"],
            }
        )

    winner = scored_clusters[0]
    verifiable_direction = build_verifiable_product_direction(winner)

    warnings: List[str] = []
    dropped_count = sum(1 for c in scored_clusters if c["screening_verdict"] == "DROP_XIAOMING_TRAP")
    if dropped_count > 0:
        warnings.append(
            f"Filtered out {dropped_count} cluster(s) flagged as DROP_XIAOMING_TRAP (desire/vitamin tier or high incumbent/friction risk)."
        )

    return {
        "niche": clustered_payload.get("niche", "Startup Idea Screening"),
        "source_file": clustered_payload.get("source_file", ""),
        "summary": {
            "total_raw_clues_ingested": clustered_payload.get("total_raw_clues", sum(len(c["clues"]) for c in scored_clusters)),
            "total_opportunity_clusters": len(scored_clusters),
            "commit_and_validate_count": sum(1 for c in scored_clusters if c["screening_verdict"] == "COMMIT_AND_VALIDATE"),
            "keep_as_backup_count": sum(1 for c in scored_clusters if c["screening_verdict"] == "KEEP_AS_BACKUP_CONCEPT"),
            "refine_niche_count": sum(1 for c in scored_clusters if c["screening_verdict"] == "REFINE_NICHE_SEGMENT"),
            "drop_xiaoming_trap_count": dropped_count,
            "winning_cluster_id": winner["cluster_id"],
            "winning_reframed_title": winner["reframed_concept_title"],
            "winning_score_100": winner["final_screening_score_100"],
        },
        "ranked_clusters": scored_clusters,
        "top_3_product_concepts": top_3_concepts,
        "verifiable_product_direction": verifiable_direction,
        "_warnings": warnings,
    }


def render_markdown_dossier(dossier: Dict[str, Any]) -> str:
    """Render a comprehensive human-readable Markdown screening report."""
    lines: List[str] = []
    summary = dossier["summary"]
    direction = dossier["verifiable_product_direction"]

    lines.append(f"# Easy-Vibe Idea Screening & Value Reframing Dossier: {dossier['niche']}")
    lines.append("")
    lines.append(
        f"- **Raw Clues Ingested**: **{summary['total_raw_clues_ingested']}** clues clustered into "
        f"**{summary['total_opportunity_clusters']}** distinct Opportunity Clusters"
    )
    lines.append(
        f"- **#1 Verifiable Direction (`COMMIT_AND_VALIDATE`)**: **{summary['winning_reframed_title']}** "
        f"(`{summary['winning_cluster_id']}` — Score: **{summary['winning_score_100']}/100**)"
    )
    lines.append("")

    lines.append("## 1. 4-Gate Opportunity Cluster Screening Matrix")
    lines.append("")
    lines.append(
        "| Rank | Cluster / Reframed Concept | Clues | Need Tier | Base /100 | Alt Tier Mod | Founder Fit | Xiaoming Penalty | Final /100 | Verdict |"
    )
    lines.append("|---:|---|---:|---|---:|---:|---:|---:|---:|---|")
    for c in dossier["ranked_clusters"]:
        g1 = c["gate_1_base_demand"]
        g2 = c["gate_2_xiaoming_trap"]
        g3 = c["gate_3_alternative_solution"]
        g4 = c["gate_4_horizontal_fit"]
        lines.append(
            f"| {c['rank']} | **{c['reframed_concept_title']}**<br>*({c['domain_category']})* | "
            f"{g1['clue_count']} | `{c['dominant_need_tier']}` | {g1['base_score_100']:.1f} | "
            f"{g3['score_modifier']:+.1f} | {g4['founder_fit_bonus']:+.1f} | "
            f"-{g2['xiaoming_trap_penalty']:.1f} | **{c['final_screening_score_100']:.2f}** | `{c['screening_verdict']}` |"
        )
    lines.append("")

    lines.append("## 2. Expected Output #1: Top 3 Evidence-Backed Product Concepts")
    lines.append("")
    for concept in dossier["top_3_product_concepts"]:
        lines.append(
            f"### Concept #{concept['concept_rank']}: {concept['reframed_concept_title']} "
            f"(Score: {concept['final_screening_score_100']}/100 · `{concept['screening_verdict']}`)"
        )
        lines.append(f"- **Ordinary Idea (Before Reframing)**: *{concept['ordinary_idea_label']}*")
        lines.append(
            f"- **Behavioral Evidence**: {concept['evidence_count']} clues across `{', '.join(concept['evidence_channels'])}`"
        )
        lines.append("")
        lines.append("#### Supporting Verbatim Clues")
        for ev in concept["sample_verbatim_evidence"]:
            short_q = ev["quote"] if len(ev["quote"]) <= 180 else ev["quote"][:177] + "..."
            lines.append(f"- **`{ev['id']}` ({ev['title']})**: *\"{short_q}\"* ([Source]({ev['source_url']}))")
        lines.append("")

        lines.append("#### Horizontal Segmentation (Appendix B)")
        lines.append("| Segment | Core Pain | Pain | WTP | Size | Comp Headroom | Reachability | Fit /5 | Selected |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
        for seg in concept["horizontal_segmentation"]:
            sel = "**YES**" if seg.get("selected") else "No"
            lines.append(
                f"| {seg['segment_name']} | {seg['core_pain']} | {seg['pain_intensity']} | "
                f"{seg['willingness_to_pay']} | {seg['segment_size']} | {seg['competition_headroom']} | "
                f"{seg['founder_reachability']} | **{seg.get('segment_fit_score_5', 4.0)}** | {sel} |"
            )
        lines.append("")

        lines.append("#### Vertical Context & Emotion Timeline (Appendix C)")
        lines.append("| Time / Stage | User Context | Friction / Pain Point | Core Emotion |")
        lines.append("|---|---|---|---|")
        for step in concept["vertical_emotion_timeline"]:
            lines.append(
                f"| **{step['time_or_stage']}** | {step['user_context']} | {step['pain_point']} | "
                f"**`{step['emotion'].upper()}`** — {step['emotion_detail']} |"
            )
        lines.append("")

        vr = concept["value_reframing_table"]
        lines.append("#### Value Reframing Comparison (Appendix D)")
        lines.append("| Dimension | Ordinary Idea (Before) | Reframed Concept (After) |")
        lines.append("|---|---|---|")
        lines.append(f"| **Target User** | {vr['before_user']} | {vr['after_user']} |")
        lines.append(f"| **Core Pain Solved** | {vr['before_pain']} | {vr['after_pain']} |")
        lines.append(f"| **Defensibility (Moat)** | {vr['before_moat']} | {vr['after_moat']} |")
        lines.append(f"| **Willingness to Pay** | {vr['before_wtp']} | {vr['after_wtp']} |")
        lines.append(f"| **Expansion Path** | {vr['before_expansion']} | {vr['after_expansion']} |")
        lines.append("")

    lines.append("## 3. Expected Output #2: The #1 Verifiable Product Direction & MVP Plan")
    lines.append("")
    op = direction["one_person_one_job_one_entry"]
    lines.append(f"### Positioning Mantra: `{direction['reframed_product_title']}`")
    lines.append(f"- **One Person (Target Wedge)**: {op['one_person']}")
    lines.append(f"- **One Job (Fear-Driven Outcome)**: {op['one_job']}")
    lines.append(f"- **One Entry Point (Zero-Friction Hook)**: {op['one_entry_point']}")
    lines.append("")

    lines.append("### 3-Phase MVP Roadmap (Act 3 & Appendix E)")
    lines.append("| Phase | Objective | Implementation Strategy | Go/Pivot Target Metrics |")
    lines.append("|---|---|---|---|")
    for ph in direction["three_phase_mvp_roadmap"]:
        lines.append(
            f"| **{ph['phase']}** | {ph['objective']} | {ph['implementation']} | {ph['target_metrics']} |"
        )
    lines.append("")

    lines.append("### Mitigating the 3 Solo-Founder Concerns")
    lines.append("| Solo-Founder Concern | Easy-Vibe Pragmatic Solution | Phase 1 Budget |")
    lines.append("|---|---|---|")
    for cm in direction["solo_founder_concern_mitigations"]:
        lines.append(f"| **{cm['concern']}** | {cm['easy_vibe_solution']} | `{cm['estimated_phase1_cost']}` |")
    lines.append("")

    tam = direction["bottom_up_tam"]
    moat = direction["moat_strategy"]
    lines.append("### Bottom-Up Market Sizing (TAM) & 6-Moat Strategy (Appendix A)")
    lines.append(
        f"- **Formula**: `{tam['target_segment_users']:,} target users × {tam['paid_conversion_rate']*100:.1f}% paid conversion × ${tam['annual_arpu_usd']:,.0f}/yr ARPU = ${tam['estimated_annual_tam_usd']:,.0f}/yr`"
    )
    lines.append(f"- **Track Classification**: `{tam['track_classification']}`")
    lines.append(f"- **Primary Moat**: `{moat['primary_moat']}` | **Secondary Moat**: `{moat['secondary_moat']}`")
    lines.append(f"- **Defensibility Mechanism**: {moat['defensibility_explanation']}")
    lines.append("")

    lines.append("### 5-Round AI Refinement Dialogue Prompts (Appendix E)")
    for rd in direction["five_round_ai_dialogue_prompts"]:
        lines.append(f"{rd['round']}. **{rd['goal']}**:\n   > `{rd['prompt']}`")
    lines.append("")

    lines.append("### 20-Item Demand Verification Checklist (Appendix F)")
    lines.append("| Category | Verification Question | Status | Empirical Evidence / Next Action |")
    lines.append("|---|---|---|---|")
    for cat_key, items in direction["appendix_f_20_item_checklist"].items():
        for row in items:
            badge = "READY" if row["status"] == "READY" else "ACTION_REQUIRED"
            lines.append(f"| `{cat_key}` | {row['item']} | `{badge}` | {row['evidence']} |")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point for screening clustered opportunities."""
    parser = argparse.ArgumentParser(
        description="Screen clustered startup clues and synthesize 3 product concepts + 1 verifiable MVP plan."
    )
    parser.add_argument("--input", required=True, help="Path to clustered JSON file from ingest_hunter_clues.py")
    parser.add_argument("--output", required=True, help="Path to write screening dossier JSON")
    parser.add_argument("--markdown", default="", help="Optional path to write Markdown dossier report")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.is_file():
        _emit_error(f"Input file does not exist: {in_path}", error_type="validation")
        return

    try:
        payload = json.loads(in_path.read_text(encoding="utf-8"))
        dossier = screen_and_reframe(payload)
    except json.JSONDecodeError as exc:
        _emit_error(f"Malformed JSON in '{in_path}': {exc}", error_type="validation")
        return
    except ValueError as exc:
        _emit_error(str(exc), error_type="validation")
        return

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(dossier, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.markdown:
        md_path = Path(args.markdown)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown_dossier(dossier), encoding="utf-8")

    print(f"Saved screening dossier to {out_path}")


if __name__ == "__main__":
    main()
