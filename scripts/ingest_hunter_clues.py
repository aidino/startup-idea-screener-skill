#!/usr/bin/env python3
"""
Ingest and cluster raw startup clues from startup-idea-hunter-skill (CSV or JSON).

Supports:
1. CSV files exported from startup-idea-hunter-skill (e.g., ideas_27_Oct.csv) with Vietnamese
   or English headers.
2. JSON files from startup-idea-hunter-skill (clues.json or scorecard.json with ranked_clues).
3. Pre-clustered JSON payloads for direct screening.

Example:
    $ python3 scripts/ingest_hunter_clues.py --input ideas-explore/ideas_27_Oct.csv --output /tmp/clustered.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


CLUSTER_TAXONOMY: List[Dict[str, Any]] = [
    {
        "cluster_id": "cluster_b2b_ap_invoice_reconciliation",
        "cluster_title": "Audit-Proof B2B Invoice, Bank Statement & Payout Reconciliation Copilot",
        "ordinary_idea_label": "Generic PDF-to-Excel converter or bookkeeping spreadsheet template",
        "reframed_concept_title": "Zero-Template Audit-Trail AP & Payout Reconciliation Copilot",
        "domain_category": "B2B Finance & Accounting Operations",
        "keywords": [
            "invoice", "hóa đơn", "sao kê", "bank statement", "tally", "quickbooks",
            "3-way match", "3 way match", "netsuite", "payout", "shopify", "lease",
            "hợp đồng thuê", "corporate card", "thẻ tín dụng", "reconcil", "đối soát",
            "đối chiếu", "erp", "line-item", "bóc tách dữ liệu", "sharepoint", "amex",
        ],
        "alternative_tier": "tier_2_clumsy_manual_patch",
        "xiaoming_trap": {
            "incumbent_sufficiency_risk": 1.8,
            "behavioral_friction_risk": 1.5,
            "free_substitution_risk": 1.5,
            "trap_diagnosis": (
                "Low Xiaoming Trap risk: businesses are actively paying Upwork freelancers to type PDFs by hand "
                "because generic OCR tools silently corrupt numbers and require per-vendor templates."
            ),
        },
        "horizontal_segments": [
            {
                "segment_name": "Small Accounting / Bookkeeping Firms & E-commerce AP Teams (5–50 staff)",
                "core_pain": "Typing 200-page blurry bank statements, multi-vendor PDF invoices, and Shopify payouts into Excel/QuickBooks/Tally with high audit-error anxiety",
                "pain_intensity": 5.0,
                "willingness_to_pay": 5.0,
                "segment_size": 4.2,
                "competition_headroom": 4.2,
                "founder_reachability": 4.5,
                "selected": True,
            },
            {
                "segment_name": "Mid-Market ERP (NetSuite) Operations Controllers",
                "core_pain": "Exporting POs, delivery receipts, and invoices to Excel outside ERP for 3-way match and Slack approvals",
                "pain_intensity": 4.6,
                "willingness_to_pay": 4.8,
                "segment_size": 3.5,
                "competition_headroom": 3.8,
                "founder_reachability": 3.4,
                "selected": False,
            },
            {
                "segment_name": "Freelancers Tracking Personal Tax Receipts",
                "core_pain": "Occasional receipt sorting once a quarter",
                "pain_intensity": 2.5,
                "willingness_to_pay": 2.0,
                "segment_size": 4.8,
                "competition_headroom": 2.0,
                "founder_reachability": 4.5,
                "selected": False,
            },
        ],
        "vertical_emotion_timeline": [
            {
                "time_or_stage": "08:30 AM (Client File Drop)",
                "user_context": "Bookkeeper opens a 200-page scanned PDF bank statement or 80 vendor invoices with different layouts",
                "pain_point": "Free converters merge columns randomly; enterprise OCR demands custom template training per vendor",
                "emotion": "anxiety",
                "emotion_detail": "Dread of spending 6 hours on Ctrl+C / Ctrl+V and missing client filing deadlines",
            },
            {
                "time_or_stage": "11:30 AM (Line-by-Line Verification)",
                "user_context": "Cross-checking extracted numbers against blurry scanned digits and Shopify payout fees/refunds",
                "pain_point": "One silent OCR digit error breaks the entire balance sheet reconciliation",
                "emotion": "fear",
                "emotion_detail": "Fear of financial misstatement, client distrust, or audit failure (driving owners to hire manual typists on Upwork)",
            },
            {
                "time_or_stage": "03:00 PM (Chasing Missing Receipts & PO Approvals)",
                "user_context": "Messaging employees on Slack/Email for missing corporate card receipts and PO delivery sign-offs",
                "pain_point": "Approval state is scattered across Slack, email, Excel, and SharePoint",
                "emotion": "helplessness",
                "emotion_detail": "Feeling stuck doing repetitive police work outside one's core accounting expertise",
            },
            {
                "time_or_stage": "06:30 PM (ERP / QuickBooks / Tally Import)",
                "user_context": "Formatting the verified spreadsheet into strict XML/CSV schemas for QuickBooks, Tally, or NetSuite",
                "pain_point": "Import rejected due to mismatched date/account codes or unlinked supporting documents",
                "emotion": "anger",
                "emotion_detail": "Frustration that expensive accounting software still requires manual spreadsheet bridges",
            },
        ],
        "value_reframing": {
            "before_user": "Anyone who needs to convert a PDF table into Excel",
            "after_user": "Small bookkeeping firms, AP clerks, and e-commerce controllers processing multi-vendor invoices & bank statements",
            "before_pain": "Converting PDF files to spreadsheets",
            "after_pain": "Eliminating the fear of silent numerical OCR errors and manual balance-sheet reconciliation across messy vendor formats",
            "before_moat": "Generic LLM/OCR wrapper (easily copied by free online converters)",
            "after_moat": "Visual cropped-snippet proof beside every extracted number + deterministic row/payout balance equations + 1-click QuickBooks/Tally/NetSuite export",
            "before_wtp": "Low ($0–$9/mo; users bounce after 5 free rows)",
            "after_wtp": "High ($79–$299/mo per firm; directly replaces $35–$150/job Upwork manual data entry and saves 15+ billable hours/week)",
            "before_expansion": "Stuck as a single-purpose file utility",
            "after_expansion": "Expands into automated client document chasing, 3-way PO matching, and lease (ASC 842) audit schedules",
        },
        "tam_parameters": {
            "target_segment_users": 150000,
            "paid_conversion_rate": 0.08,
            "annual_arpu_usd": 1200,
            "primary_moat": "switching_costs",
            "secondary_moat": "data_accumulation",
        },
    },
    {
        "cluster_id": "cluster_b2b_ops_chasing_and_reporting",
        "cluster_title": "Automated Client Document Chaser, Spreadsheet Watchdog & Agency Report Builder",
        "ordinary_idea_label": "Generic reminder email tool or dashboard builder",
        "reframed_concept_title": "Zero-Chase Client Document Collector & Last-Mile Operations Copilot",
        "domain_category": "B2B Agency & Operations Automation",
        "keywords": [
            "chasing", "đòi hồ sơ", "chứng từ", "shared folders", "dropbox", "google slides",
            "client reports", "báo cáo khách hàng", "ga4", "meta ads", "inventory", "tồn kho",
            "reading spreadsheet", "đọc bằng mắt", "vlookup", "reorder email", "account manager",
        ],
        "alternative_tier": "tier_3_multi_tool_stitching",
        "xiaoming_trap": {
            "incumbent_sufficiency_risk": 2.2,
            "behavioral_friction_risk": 2.0,
            "free_substitution_risk": 2.0,
            "trap_diagnosis": (
                "Low-to-moderate risk: users currently stitch Google Drive, Excel trackers, Slack, and 4-5 ad platforms "
                "by hand every month, losing 20-30 hours per cycle."
            ),
        },
        "horizontal_segments": [
            {
                "segment_name": "Bookkeeping, Tax & Credit Advisory Firms Managing 20–50 Monthly Retainer Clients",
                "core_pain": "Spending 5–10 hours/week opening shared folders, verifying if uploaded files match the right month/type, updating Excel trackers, and sending 3rd follow-ups",
                "pain_intensity": 4.6,
                "willingness_to_pay": 4.5,
                "segment_size": 4.0,
                "competition_headroom": 4.0,
                "founder_reachability": 4.4,
                "selected": True,
            },
            {
                "segment_name": "B2B Marketing Agencies (10–25 Clients) Building Monthly Slide Reports",
                "core_pain": "Losing a full work week at month-start screenshotting GA4/Meta/LinkedIn metrics into Google Slides with executive commentary",
                "pain_intensity": 4.4,
                "willingness_to_pay": 4.4,
                "segment_size": 4.0,
                "competition_headroom": 3.5,
                "founder_reachability": 4.3,
                "selected": False,
            },
            {
                "segment_name": "Mid-Size Inventory & Purchasing Managers Living in Multi-Sheet Excel",
                "core_pain": "Spending 2 hours daily visually scanning VLOOKUP sheets to spot low stock and draft vendor PO emails",
                "pain_intensity": 4.2,
                "willingness_to_pay": 4.0,
                "segment_size": 3.8,
                "competition_headroom": 4.1,
                "founder_reachability": 3.8,
                "selected": False,
            },
        ],
        "vertical_emotion_timeline": [
            {
                "time_or_stage": "Day 1 of Month (09:00 AM)",
                "user_context": "Account manager sends 30 monthly document requests or opens 5 analytics platforms per client",
                "pain_point": "Manual folder creation, checklist copying, and screenshot pasting",
                "emotion": "anxiety",
                "emotion_detail": "Overwhelmed by a 30-hour manual backlog before real analytical work can even begin",
            },
            {
                "time_or_stage": "Day 5 of Month (02:00 PM)",
                "user_context": "Clicking through 25 Google Drive/Dropbox folders to check who uploaded what",
                "pain_point": "Clients upload wrong months or blurry files; manual tracker sheet gets out of sync",
                "emotion": "helplessness",
                "emotion_detail": "Exhaustion from chasing silent clients for the third time while deadlines slip",
            },
            {
                "time_or_stage": "Daily Morning Check (08:30 AM)",
                "user_context": "Operations manager stares at a 12-tab Excel workbook hunting for threshold drops",
                "pain_point": "Spreadsheets calculate numbers but cannot push last-mile Slack alerts or draft vendor reorder emails",
                "emotion": "regret",
                "emotion_detail": "Fear of missing a critical stockout row because human eyes got tired scanning thousands of cells",
            },
        ],
        "value_reframing": {
            "before_user": "General office workers using Google Drive or Excel",
            "after_user": "Client-service firms (bookkeeping/agencies) and Excel-bound purchasing managers",
            "before_pain": "Sending email reminders or viewing spreadsheet charts",
            "after_pain": "Automating the last-mile content verification of client uploads and turning passive spreadsheets into proactive Slack/email actions",
            "before_moat": "Simple cron reminder script",
            "after_moat": "AI content-inspection on upload (verifying document type & date range automatically) + zero-migration overlay on existing Drive/Excel",
            "before_wtp": "Low ($10/mo generic reminder plugin)",
            "after_wtp": "High ($99–$249/mo per team; recovers 20–30 billable hours every month)",
            "before_expansion": "Static form builder",
            "after_expansion": "Expands into automated client onboarding portals and pre-accounting data readiness pipelines",
        },
        "tam_parameters": {
            "target_segment_users": 120000,
            "paid_conversion_rate": 0.06,
            "annual_arpu_usd": 1080,
            "primary_moat": "switching_costs",
            "secondary_moat": "data_accumulation",
        },
    },
    {
        "cluster_id": "cluster_parenting_tutoring_homework_concierge",
        "cluster_title": "Diagnostic Micro-Tutoring, Evening Homework Triage & Custom Worksheet Concierge",
        "ordinary_idea_label": "Generic AI homework chatbot or static PDF worksheet store",
        "reframed_concept_title": "Working-Parent Evening Homework Triage & Diagnostic Printable Worksheet Copilot",
        "domain_category": "EdTech & High-Intent Parenting Support",
        "keywords": [
            "tutor", "gia sư", "homeschool", "homework", "bài tập về nhà", "worksheet",
            "printable", "coaching", "sleep consultant", "doula", "parenting-adjacent",
        ],
        "alternative_tier": "tier_2_clumsy_manual_patch",
        "xiaoming_trap": {
            "incumbent_sufficiency_risk": 2.4,
            "behavioral_friction_risk": 2.2,
            "free_substitution_risk": 2.5,
            "trap_diagnosis": (
                "Moderate risk if built as a generic chat wrapper, but low risk when anchored on what parents "
                "already pay for on Upwork/Fiverr ($45-$75/hr tutors, $50/hr parenting coaches, custom PDF worksheets)."
            ),
        },
        "horizontal_segments": [
            {
                "segment_name": "Homeschooling & Multi-Child Elementary Parents Priced Out of $45–$75/hr Private Tutors",
                "core_pain": "Evening homework for 2–3 kids consumes the entire night; private tutors cost $60+/hr; generic worksheets don't match the child's exact weak spot",
                "pain_intensity": 4.7,
                "willingness_to_pay": 4.4,
                "segment_size": 4.3,
                "competition_headroom": 3.7,
                "founder_reachability": 4.2,
                "selected": True,
            },
            {
                "segment_name": "Independent Parenting Coaches (Sleep Consultants, Doulas) Scaling Client Plans",
                "core_pain": "Manually drafting weekly sleep/feeding adjustments from messy parent logs",
                "pain_intensity": 4.3,
                "willingness_to_pay": 4.5,
                "segment_size": 3.2,
                "competition_headroom": 4.2,
                "founder_reachability": 3.8,
                "selected": False,
            },
        ],
        "vertical_emotion_timeline": [
            {
                "time_or_stage": "05:30 PM (Post-Work Arrival)",
                "user_context": "Parent comes home exhausted to 2–3 elementary kids with different teacher instructions and homework packets",
                "pain_point": "No clear 45-minute triage plan; chaos erupts at the kitchen table",
                "emotion": "anxiety",
                "emotion_detail": "Dread that homework battles will swallow the entire family evening again",
            },
            {
                "time_or_stage": "07:00 PM (Stuck on a Specific Concept)",
                "user_context": "Child cries over a math/reading mistake; parent doesn't know how to explain it using the school's rubric",
                "pain_point": "Private tutors cost $60/hr and generic chat apps distract kids on screens",
                "emotion": "helplessness",
                "emotion_detail": "Guilt over not affording a $60/hr tutor while fearing the child is falling behind",
            },
            {
                "time_or_stage": "08:30 PM (Bedtime Guilt)",
                "user_context": "Parent searches Fiverr/Etsy for printable practice sheets tailored to tomorrow's quiz",
                "pain_point": "Static PDF bundles aren't personalized to the exact 3 mistakes the child made tonight",
                "emotion": "loneliness",
                "emotion_detail": "Feeling alone in managing multiple children's learning gaps without professional backup",
            },
        ],
        "value_reframing": {
            "before_user": "All students and parents looking for study help",
            "after_user": "Working or homeschooling parents of K-6 children priced out of $45–$75/hr private tutors",
            "before_pain": "Answering homework questions on a screen",
            "after_pain": "Reclaiming the family evening via a 30-minute photo-to-paper diagnostic loop (snap child's mistake -> print targeted 1-page offline worksheet + parent coaching script)",
            "before_moat": "Prompting ChatGPT for practice questions",
            "after_moat": "Grade-aligned visual printable PDF generator + error-pattern memory across weeks + zero-screen child experience",
            "before_wtp": "Low (free chatbots)",
            "after_wtp": "High ($19–$39/mo family subscription; 1/10th the cost of a single hour with a human tutor)",
            "before_expansion": "Generic Q&A bot",
            "after_expansion": "Expands to B2B white-label tools for independent tutors, micro-schools, and parenting coaches",
        },
        "tam_parameters": {
            "target_segment_users": 250000,
            "paid_conversion_rate": 0.05,
            "annual_arpu_usd": 288,
            "primary_moat": "data_accumulation",
            "secondary_moat": "brand_mindshare",
        },
    },
    {
        "cluster_id": "cluster_parenting_screentime_offline_bridge",
        "cluster_title": "Single/Working Parent Screen-Time De-Escalation & Instant Offline Activity Copilot",
        "ordinary_idea_label": "Parental control app blocker or generic activity list",
        "reframed_concept_title": "Zero-Meltdown Screen Transition & Household-Inventory Offline Activity Concierge",
        "domain_category": "Family Digital Wellbeing & Behavioral Support",
        "keywords": [
            "screen time", "màn hình", "game", "tablet", "cáu bẳn", "agitated", "detox",
            "single mom", "mẹ đơn thân", "video ngắn", "nghiện điện thoại", "con ghét bố mẹ",
            "ruining their life", "housework",
        ],
        "alternative_tier": "tier_4_unsatisfied_incumbent",
        "xiaoming_trap": {
            "incumbent_sufficiency_risk": 3.4,
            "behavioral_friction_risk": 3.2,
            "free_substitution_risk": 3.0,
            "trap_diagnosis": (
                "Elevated Xiaoming Trap risk if built as another device-locking app (OS built-in Screen Time & Family Link "
                "are free). Must focus on the emotional transition ritual, co-signed family contracts, and zero-prep offline substitutes."
            ),
        },
        "horizontal_segments": [
            {
                "segment_name": "Overwhelmed Single / WFH Parents of Ages 5–11 Needing 45 Minutes of Uninterrupted Work/Chores",
                "core_pain": "Caving in to games during busy work/housework hours, followed by explosive meltdowns when turning the tablet off",
                "pain_intensity": 4.8,
                "willingness_to_pay": 3.6,
                "segment_size": 4.6,
                "competition_headroom": 3.2,
                "founder_reachability": 4.4,
                "selected": True,
            },
        ],
        "vertical_emotion_timeline": [
            {
                "time_or_stage": "04:30 PM (Work/Chore Crunch)",
                "user_context": "Single parent has urgent work or dinner prep and hands over the tablet for 'just 30 minutes'",
                "pain_point": "No zero-prep offline activity ready using items already in the living room",
                "emotion": "helplessness",
                "emotion_detail": "Exhaustion forces parent to use screens as an emergency babysitter",
            },
            {
                "time_or_stage": "06:00 PM (Turn-Off Explosion)",
                "user_context": "Parent asks child to put down the tablet; child screams 'you're ruining my life' or begs for 10 more minutes",
                "pain_point": "Hard OS cutoffs trigger dopamine-crash rage; parent lacks de-escalation scripts",
                "emotion": "fear",
                "emotion_detail": "Fear of damaging the parent-child relationship and raising a screen-addicted child",
            },
        ],
        "value_reframing": {
            "before_user": "All parents worried about phones",
            "after_user": "Single & WFH parents of 5–11 year-olds who need peaceful transitions during busy evening windows",
            "before_pain": "Blocking apps with a password",
            "after_pain": "Ending turn-off meltdowns and replacing emergency screen babysitting with instant 30-minute offline missions",
            "before_moat": "OS timer lock (already free on iOS/Android)",
            "after_moat": "Co-designed kid reward contracts + voice/audio mission narrator that guides the child offline without parent supervision",
            "before_wtp": "Low (free OS controls)",
            "after_wtp": "Moderate ($9–$15/mo for audio-guided offline missions + family peace)",
            "before_expansion": "Static parenting blog",
            "after_expansion": "Physical activity kit subscriptions and school counseling partnerships",
        },
        "tam_parameters": {
            "target_segment_users": 300000,
            "paid_conversion_rate": 0.03,
            "annual_arpu_usd": 120,
            "primary_moat": "brand_mindshare",
            "secondary_moat": "data_accumulation",
        },
    },
    {
        "cluster_id": "cluster_school_multi_app_digest",
        "cluster_title": "Unified Parent-Teacher Multi-App Inbox (ClassDojo / Seesaw / PowerSchool Digest)",
        "ordinary_idea_label": "New school communication app",
        "reframed_concept_title": "Zero-Switch Parent Overlay Digest for Fragmented School Apps",
        "domain_category": "Parent-School Workflow Aggregation",
        "keywords": [
            "classdojo", "seesaw", "brightwheel", "powerschool", "school apps",
            "liên lạc trường", "paperwork", "giáo viên", "teachers",
        ],
        "alternative_tier": "tier_3_multi_tool_stitching",
        "xiaoming_trap": {
            "incumbent_sufficiency_risk": 3.5,
            "behavioral_friction_risk": 3.0,
            "free_substitution_risk": 3.2,
            "trap_diagnosis": (
                "High Xiaoming Trap risk if you try to convince schools to switch away from ClassDojo/Seesaw. "
                "Only viable as a parent-side email/notification forwarding digest that requires zero school adoption."
            ),
        },
        "horizontal_segments": [
            {
                "segment_name": "Working Parents with 2+ Kids Across Multiple Teachers/Schools Using 4–6 Apps",
                "core_pain": "Missing permission slips, spirit days, and grade alerts buried across ClassDojo, Seesaw, Brightwheel, and email",
                "pain_intensity": 4.1,
                "willingness_to_pay": 3.2,
                "segment_size": 4.4,
                "competition_headroom": 3.4,
                "founder_reachability": 4.0,
                "selected": True,
            },
        ],
        "vertical_emotion_timeline": [
            {
                "time_or_stage": "07:45 AM (School Drop-off Surprise)",
                "user_context": "Parent realizes they missed a costume day or signed form buried in a noisy ClassDojo upsell feed",
                "pain_point": "4–6 separate school apps per family with no unified calendar or task extraction",
                "emotion": "regret",
                "emotion_detail": "Embarrassment and frustration from missing a school event despite checking multiple apps",
            },
        ],
        "value_reframing": {
            "before_user": "Schools and teachers",
            "after_user": "Busy multi-child parents who cannot force their school district to change apps",
            "before_pain": "Chatting with teachers",
            "after_pain": "Auto-extracting every deadline, permission slip, and event from 5 noisy school apps into 1 clean Sunday calendar briefing",
            "before_moat": "Yet another school chat app",
            "after_moat": "Zero-school-permission email/push parser + ad-free family calendar sync (.ics)",
            "before_wtp": "Low if pitched as a chat app",
            "after_wtp": "Moderate ($6–$10/mo family convenience subscription)",
            "before_expansion": "Single school tool",
            "after_expansion": "Family logistics & extracurricular schedule coordinator",
        },
        "tam_parameters": {
            "target_segment_users": 200000,
            "paid_conversion_rate": 0.03,
            "annual_arpu_usd": 84,
            "primary_moat": "switching_costs",
            "secondary_moat": "network_effects",
        },
    },
    {
        "cluster_id": "cluster_generic_vitamin_parenting_apps",
        "cluster_title": "Generic Baby Growth & Unvalidated Parenting Utility Apps (Vitamin / Desire Benchmark)",
        "ordinary_idea_label": "Generic baby tracker or unvalidated parenting app suite",
        "reframed_concept_title": "Disqualified Vitamin Concept (Hold Unless Anchored to Acute Clinical/Postpartum Pain)",
        "domain_category": "Consumer Lifestyle / Vitamin Benchmark",
        "keywords": [
            "15+ app", "15 apps", "not made a single sale", "baby growth chart", "desire",
            "skip_vitamin", "mood tracker", "water intake",
        ],
        "alternative_tier": "tier_5_satisfied_incumbent",
        "xiaoming_trap": {
            "incumbent_sufficiency_risk": 4.8,
            "behavioral_friction_risk": 4.5,
            "free_substitution_risk": 4.8,
            "trap_diagnosis": (
                "Classic Xiaoming Trap: indie team built 15+ parenting apps with 0 sales because generic tracking "
                "is a low-urgency desire already covered by free apps."
            ),
        },
        "horizontal_segments": [
            {
                "segment_name": "General New Parents Browsing Free App Stores",
                "core_pain": "Logging height/weight or browsing general tips without acute consequence",
                "pain_intensity": 2.0,
                "willingness_to_pay": 1.5,
                "segment_size": 4.8,
                "competition_headroom": 1.5,
                "founder_reachability": 3.0,
                "selected": True,
            },
        ],
        "vertical_emotion_timeline": [
            {
                "time_or_stage": "Day 3 After Download",
                "user_context": "User has to manually type daily measurements into the app",
                "pain_point": "High manual logging friction for a non-urgent 'nice-to-have' chart",
                "emotion": "regret",
                "emotion_detail": "User abandons the app within 7 days, matching Xiaoming's 5% retention trap",
            },
        ],
        "value_reframing": {
            "before_user": "All parents",
            "after_user": "Must pivot to acute clinical/postpartum recovery pain (e.g., Postpartum 0–6 Month Diastasis Recti Safety Coach)",
            "before_pain": "Logging baby growth percentiles",
            "after_pain": "Eliminate unless reframed around acute fear/injury prevention",
            "before_moat": "None",
            "after_moat": "Requires specialist co-creation (70/30 revenue share)",
            "before_wtp": "Near zero",
            "after_wtp": "Only viable after full pivot out of the desire tier",
            "before_expansion": "None",
            "after_expansion": "Pivot required",
        },
        "tam_parameters": {
            "target_segment_users": 50000,
            "paid_conversion_rate": 0.005,
            "annual_arpu_usd": 20,
            "primary_moat": "brand_mindshare",
            "secondary_moat": "data_accumulation",
        },
    },
]


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
        "hint": hint or "Provide a valid Hunter CSV (e.g. ideas_27_Oct.csv) or JSON clue file.",
    }
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(1)


def _detect_channel(source_text: str) -> Tuple[str, str]:
    """Extract normalized channel enum and first URL from a source cell."""
    lower = source_text.lower()
    url_match = re.search(r"https?://[^\s)\"'>]+", source_text)
    url = url_match.group(0).rstrip(".,;)") if url_match else source_text.strip() or "ref:local-clue"

    if "upwork" in lower or "fiverr" in lower:
        return "upwork_fiverr_repetitive_jobs", url
    if "capterra" in lower or "g2.com" in lower:
        return "capterra_low_star_reviews", url
    if "indiehackers" in lower or "producthunt" in lower:
        return "indie_hackers_product_hunt", url
    if "reddit" in lower:
        return "reddit_community_pain", url
    return "personal_or_peer_observation", url


def _parse_note_metadata(note_text: str) -> Tuple[float | None, str | None, str | None]:
    """Parse Easy-Vibe score, verdict, and need_tier from Hunter Note column."""
    score_val: float | None = None
    verdict_val: str | None = None
    tier_val: str | None = None

    score_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*100", note_text)
    if score_match:
        score_val = float(score_match.group(1))

    for v in ("BUILD_MVP_NOW", "NICHE_DOWN_FIRST", "SKIP_VITAMIN"):
        if v in note_text:
            verdict_val = v
            break

    tier_match = re.search(r"need-tier:\s*(pain|gratification|desire)", note_text, flags=re.IGNORECASE)
    if tier_match:
        tier_val = tier_match.group(1).lower()

    return score_val, verdict_val, tier_val


def _derive_scores_from_hunter(
    hunter_score: float | None,
    need_tier: str,
    channel: str,
    quote: str,
) -> Dict[str, float]:
    """Reconstruct 1-5 criteria ratings when ingesting compact CSV rows."""
    q_lower = quote.lower()
    if need_tier == "desire":
        return {
            "frequency": 3.0,
            "pain_level": 2.0,
            "current_workaround": 2.0,
            "willingness_to_pay": 1.5,
            "market_size": 3.5,
        }

    base = 4.2 if (hunter_score is not None and hunter_score >= 88.0) else 3.8
    if hunter_score is not None and hunter_score < 70.0:
        base = 3.2

    wtp = base
    if channel == "upwork_fiverr_repetitive_jobs" or "$" in q_lower or "paid" in q_lower or "trả tiền" in q_lower:
        wtp = min(5.0, base + 0.6)
    pain = min(5.0, base + (0.5 if need_tier == "pain" else 0.0))
    workaround = min(5.0, base + (0.4 if ("excel" in q_lower or "manual" in q_lower or "hand" in q_lower) else 0.0))

    return {
        "frequency": round(min(5.0, max(1.0, base)), 2),
        "pain_level": round(min(5.0, max(1.0, pain)), 2),
        "current_workaround": round(min(5.0, max(1.0, workaround)), 2),
        "willingness_to_pay": round(min(5.0, max(1.0, wtp)), 2),
        "market_size": round(min(5.0, max(1.0, base)), 2),
    }


def parse_csv_clues(csv_path: Path) -> Dict[str, Any]:
    """
    Parse a startup-idea-hunter-skill CSV file into a normalized clue list.

    Args:
        csv_path: Path to the CSV file (e.g., ideas-explore/ideas_27_Oct.csv).

    Returns:
        Dictionary with 'niche', 'source_file', and normalized 'clues' list.

    Raises:
        ValueError: If CSV has no valid rows or required columns are absent.
    """
    text = csv_path.read_text(encoding="utf-8-sig")
    reader = csv.reader(text.splitlines())
    rows = list(reader)
    if len(rows) < 2:
        raise ValueError(f"CSV file '{csv_path}' must contain a header row and at least one data row")

    clues: List[Dict[str, Any]] = []
    for row_idx, row in enumerate(rows[1:], start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        stt = row[0].strip() if len(row) > 0 else ""
        note_cell = row[5].strip() if len(row) > 5 else ""
        if stt == "0" or note_cell.lower() == "example":
            continue

        problem_cell = row[1].strip() if len(row) > 1 else ""
        context_cell = row[2].strip() if len(row) > 2 else ""
        source_cell = row[3].strip() if len(row) > 3 else ""
        date_cell = row[4].strip() if len(row) > 4 else "2026-10-27"

        if not problem_cell:
            continue

        prob_lines = [ln.strip() for ln in problem_cell.splitlines() if ln.strip()]
        title = prob_lines[0].strip('"') if prob_lines else f"Clue {stt or row_idx}"
        quote = " ".join(prob_lines[1:]).strip('"') if len(prob_lines) > 1 else title

        ctx_lines = [ln.strip() for ln in context_cell.splitlines() if ln.strip()]
        persona_context = ctx_lines[0] if ctx_lines else "Target user in workflow"
        input_data = "Unstructured user documents or workflow logs"
        output_data = "Validated structured actionable output"

        for ln in ctx_lines:
            if "input" in ln.lower() and ("output" in ln.lower() or "→" in ln or "->" in ln):
                cleaned = re.sub(r"^.*?input\s*(?:→|->)\s*output\s*ai\s*:\s*", "", ln, flags=re.IGNORECASE)
                parts = re.split(r"\s*(?:→|->)\s*", cleaned, maxsplit=1)
                if len(parts) == 2:
                    input_data = parts[0].strip()
                    output_data = parts[1].strip()
                elif cleaned.strip():
                    input_data = cleaned.strip()

        channel, source_url = _detect_channel(source_cell)
        hunter_score, hunter_verdict, need_tier = _parse_note_metadata(note_cell)
        resolved_tier = need_tier or ("desire" if "0 doanh thu" in problem_cell.lower() else "pain")
        scores = _derive_scores_from_hunter(hunter_score, resolved_tier, channel, quote)

        clues.append(
            {
                "id": f"c{stt}" if stt.isdigit() else f"c{len(clues) + 1}",
                "title": title,
                "quote": quote,
                "persona_context": persona_context,
                "input_data": input_data,
                "output_data": output_data,
                "channel": channel,
                "source_url": source_url,
                "source_date": date_cell or "2026-10-27",
                "need_tier": resolved_tier,
                "hunter_score_100": hunter_score,
                "hunter_verdict": hunter_verdict,
                "scores": scores,
            }
        )

    if not clues:
        raise ValueError(f"No valid non-example clue rows found in CSV '{csv_path}'")

    return {
        "niche": "Multi-Domain Hunter Clues (Parenting/EdTech & B2B Accounting/Ops)",
        "source_file": str(csv_path),
        "clues": clues,
    }


def match_cluster_blueprint(clue: Dict[str, Any]) -> Dict[str, Any]:
    """
    Match a single clue to the best semantic Opportunity Cluster blueprint.

    Args:
        clue: Normalized clue dictionary.

    Returns:
        Matching cluster blueprint dictionary.
    """
    explicit_cluster = clue.get("cluster_id")
    if explicit_cluster:
        for bp in CLUSTER_TAXONOMY:
            if bp["cluster_id"] == explicit_cluster:
                return bp

    haystack = " ".join(
        [
            str(clue.get("title", "")),
            str(clue.get("quote", "")),
            str(clue.get("persona_context", "")),
            str(clue.get("input_data", "")),
            str(clue.get("output_data", "")),
        ]
    ).lower()

    if clue.get("need_tier") == "desire":
        return CLUSTER_TAXONOMY[-1]

    best_bp = CLUSTER_TAXONOMY[0]
    best_hits = -1
    for bp in CLUSTER_TAXONOMY:
        hits = sum(1 for kw in bp["keywords"] if kw in haystack)
        if hits > best_hits:
            best_hits = hits
            best_bp = bp

    if best_hits <= 0:
        # Generic fallback cluster adapted from the clue itself
        cid = f"cluster_{re.sub(r'[^a-z0-9]+', '_', str(clue.get('id', 'custom')).lower()).strip('_')}"
        return {
            "cluster_id": cid,
            "cluster_title": str(clue.get("title", "Custom Opportunity Cluster")),
            "ordinary_idea_label": f"Generic tool for {clue.get('input_data', 'workflow')}",
            "reframed_concept_title": f"Dedicated Copilot for {clue.get('persona_context', 'Target Persona')}",
            "domain_category": "Specialized Workflow Automation",
            "keywords": [],
            "alternative_tier": str(clue.get("alternative_tier", "tier_2_clumsy_manual_patch")),
            "xiaoming_trap": clue.get(
                "xiaoming_trap",
                {
                    "incumbent_sufficiency_risk": 2.2,
                    "behavioral_friction_risk": 2.0,
                    "free_substitution_risk": 2.0,
                    "trap_diagnosis": "Validated manual friction; avoid generic feature bloat and focus on a single high-pain trigger.",
                },
            ),
            "horizontal_segments": [
                {
                    "segment_name": str(clue.get("persona_context", "Core High-Pain Segment")),
                    "core_pain": str(clue.get("title", "Acute workflow bottleneck")),
                    "pain_intensity": float(clue.get("scores", {}).get("pain_level", 4.2)),
                    "willingness_to_pay": float(clue.get("scores", {}).get("willingness_to_pay", 4.2)),
                    "segment_size": float(clue.get("scores", {}).get("market_size", 3.8)),
                    "competition_headroom": 4.0,
                    "founder_reachability": 4.2,
                    "selected": True,
                }
            ],
            "vertical_emotion_timeline": [
                {
                    "time_or_stage": "Before Task (Trigger Moment)",
                    "user_context": f"User receives {clue.get('input_data', 'raw inputs')}",
                    "pain_point": str(clue.get("title", "Manual bottleneck")),
                    "emotion": "anxiety",
                    "emotion_detail": "Stress from repetitive manual processing under time pressure",
                },
                {
                    "time_or_stage": "During Task (Manual Workaround)",
                    "user_context": f"Manually trying to produce {clue.get('output_data', 'target output')}",
                    "pain_point": "High error risk and wasted billable hours",
                    "emotion": "fear",
                    "emotion_detail": "Fear of costly mistakes or missed deadlines",
                },
            ],
            "value_reframing": {
                "before_user": "Broad general users",
                "after_user": str(clue.get("persona_context", "Focused high-pain persona")),
                "before_pain": f"Processing {clue.get('input_data', 'data')}",
                "after_pain": f"Guaranteed, anxiety-free delivery of {clue.get('output_data', 'outcome')}",
                "before_moat": "Generic prompt wrapper",
                "after_moat": "Domain-specific verification rules + workflow integration",
                "before_wtp": "Low (free alternatives)",
                "after_wtp": "High (anchored on saved hours and avoided losses)",
                "before_expansion": "Single feature",
                "after_expansion": "End-to-end vertical workflow copilot",
            },
            "tam_parameters": {
                "target_segment_users": 100000,
                "paid_conversion_rate": 0.05,
                "annual_arpu_usd": 600,
                "primary_moat": "switching_costs",
                "secondary_moat": "data_accumulation",
            },
        }
    return best_bp


def ingest_and_cluster(input_path: Path) -> Dict[str, Any]:
    """
    Load clues from CSV or JSON and group them into semantic Opportunity Clusters.

    Args:
        input_path: Path to CSV or JSON input file.

    Returns:
        Dictionary containing 'niche', 'total_raw_clues', 'raw_clues', and 'clusters'.

    Raises:
        ValueError: If file does not exist, is malformed, or contains zero valid clues.
    """
    if not input_path.is_file():
        raise ValueError(f"Input file does not exist: {input_path}")

    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        parsed = parse_csv_clues(input_path)
    elif suffix == ".json":
        try:
            raw_json = json.loads(input_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in '{input_path}': {exc}") from exc
        if not isinstance(raw_json, dict):
            raise ValueError("JSON root must be an object")
        clues_list = raw_json.get("clues") or raw_json.get("ranked_clues")
        if not isinstance(clues_list, list) or len(clues_list) == 0:
            raise ValueError("JSON input must contain a non-empty 'clues' or 'ranked_clues' list")
        parsed = {
            "niche": str(raw_json.get("niche", "Startup Idea Screening")).strip() or "Startup Idea Screening",
            "source_file": str(input_path),
            "clues": clues_list,
        }
    else:
        raise ValueError(f"Unsupported file extension '{suffix}'. Expected .csv or .json")

    raw_clues: List[Dict[str, Any]] = parsed["clues"]
    grouped: Dict[str, Dict[str, Any]] = {}

    for idx, clue in enumerate(raw_clues):
        if not isinstance(clue, dict):
            raise ValueError(f"clues[{idx}] must be an object")
        cid_raw = str(clue.get("id", f"c{idx + 1}")).strip()
        title_raw = str(clue.get("title", "")).strip()
        quote_raw = str(clue.get("quote", "")).strip()
        if not title_raw and not quote_raw:
            raise ValueError(f"clues[{idx}] must include a non-empty 'title' or 'quote'")

        channel, source_url = _detect_channel(str(clue.get("source_url", "ref:local")))
        if clue.get("channel"):
            channel = str(clue["channel"]).strip()
        need_tier = str(clue.get("need_tier", "pain")).strip().lower()
        if need_tier not in ("pain", "gratification", "desire"):
            raise ValueError(f"clues[{idx}].need_tier must be 'pain', 'gratification', or 'desire'")

        raw_scores = clue.get("scores")
        if isinstance(raw_scores, dict) and all(k in raw_scores for k in ("frequency", "pain_level", "current_workaround", "willingness_to_pay", "market_size")):
            scores = {k: float(raw_scores[k]) for k in ("frequency", "pain_level", "current_workaround", "willingness_to_pay", "market_size")}
            for k, val in scores.items():
                if val < 1.0 or val > 5.0:
                    raise ValueError(f"clues[{idx}].scores.{k} must be between 1 and 5 (got {val})")
        else:
            scores = _derive_scores_from_hunter(
                float(clue["hunter_score_100"]) if clue.get("hunter_score_100") is not None else None,
                need_tier,
                channel,
                quote_raw or title_raw,
            )

        normalized_clue: Dict[str, Any] = {
            "id": cid_raw,
            "title": title_raw or quote_raw[:80],
            "quote": quote_raw or title_raw,
            "persona_context": str(clue.get("persona_context", "Target workflow user")).strip(),
            "input_data": str(clue.get("input_data", "Raw unstructured workflow data")).strip(),
            "output_data": str(clue.get("output_data", "Structured actionable output")).strip(),
            "channel": channel,
            "source_url": source_url,
            "source_date": str(clue.get("source_date", "2026-10-27")).strip(),
            "need_tier": need_tier,
            "hunter_score_100": clue.get("hunter_score_100"),
            "scores": scores,
        }

        bp = match_cluster_blueprint({**clue, **normalized_clue})
        cluster_id = bp["cluster_id"]
        if cluster_id not in grouped:
            grouped[cluster_id] = {
                "blueprint": bp,
                "clues": [],
            }
        grouped[cluster_id]["clues"].append(normalized_clue)

    clusters_out: List[Dict[str, Any]] = []
    for cluster_id, bundle in grouped.items():
        bp = bundle["blueprint"]
        c_list = bundle["clues"]
        clusters_out.append(
            {
                "cluster_id": cluster_id,
                "cluster_title": bp["cluster_title"],
                "ordinary_idea_label": bp["ordinary_idea_label"],
                "reframed_concept_title": bp["reframed_concept_title"],
                "domain_category": bp["domain_category"],
                "alternative_tier": bp["alternative_tier"],
                "xiaoming_trap": bp["xiaoming_trap"],
                "horizontal_segments": bp["horizontal_segments"],
                "vertical_emotion_timeline": bp["vertical_emotion_timeline"],
                "value_reframing": bp["value_reframing"],
                "tam_parameters": bp["tam_parameters"],
                "clue_count": len(c_list),
                "unique_channels": sorted({c["channel"] for c in c_list}),
                "clues": c_list,
            }
        )

    return {
        "niche": parsed["niche"],
        "source_file": parsed["source_file"],
        "total_raw_clues": len(raw_clues),
        "total_clusters": len(clusters_out),
        "clusters": clusters_out,
    }


def main() -> None:
    """CLI entry point for ingesting and clustering Hunter clues."""
    parser = argparse.ArgumentParser(
        description="Ingest CSV/JSON clues from startup-idea-hunter-skill and group into Opportunity Clusters."
    )
    parser.add_argument("--input", required=True, help="Path to Hunter CSV or JSON file")
    parser.add_argument("--output", required=True, help="Path to write clustered JSON output")
    args = parser.parse_args()

    try:
        result = ingest_and_cluster(Path(args.input))
    except ValueError as exc:
        _emit_error(str(exc), error_type="validation")
        return
    except OSError as exc:
        _emit_error(str(exc), error_type="runtime")
        return

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Clustered {result['total_raw_clues']} clues into {result['total_clusters']} opportunity clusters -> {out_path}")


if __name__ == "__main__":
    main()
