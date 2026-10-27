# Easy-Vibe Stage 1B Playbook: How to Identify a Great Idea (`finding-great-idea`)

This playbook codifies the complete methodology from the Easy-Vibe chapter **Cách nhận biết một ý tưởng tốt (`finding-great-idea`)**, designed as the downstream screening and concept-synthesis layer after `startup-idea-hunter-skill`.

---

## 1. The Xiaoming Trap: Why "Good" Products Fail to Monetize

Developer Xiaoming spent 12 months and 200,000 RMB building a feature-complete fitness app (courses, check-ins, community, analytics). Month 1 brought 50,000 downloads, yet 7-day retention fell to 5% and paid conversion was near zero.

Every candidate startup idea must be screened against the **3 Xiaoming Trap Failure Modes**:
1. **Incumbent Sufficiency (`incumbent_sufficiency_risk`)**: Existing platforms (Keep, FitTime, ClassDojo, NetSuite) are already "good enough" for generic tasks; switching habits costs users too much effort.
2. **Behavioral Friction (`behavioral_friction_risk`)**: The product forces users to manually log, configure templates, or adopt new daily habits before receiving value.
3. **Free Substitution (`free_substitution_risk`)**: Abundant free alternatives cover the generic surface feature, eliminating urgency to pay.

**Core Rule**: *Fear drives payment; anxiety drives action.* Users do not buy features—they buy relief from fear, financial loss, compliance risk, or emotional exhaustion (like Meicai giving restaurant owners back 3 hours of sleep at 4:00 AM, or Xiaohongshu reducing the fear of buying the wrong product).

---

## 2. The 3 Need Tiers & 5-Tier Alternative Solution Matrix (Appendix A)

### Need Tiers (`pain` > `gratification` > `desire`)
- **Pain (`pain`, 1.15x)**: Driven by fear, acute financial loss, audit/compliance risk, or severe physical/time exhaustion. Immediate consequence if ignored.
- **Gratification (`gratification`, 1.00x)**: Instant speed or pleasure reward (30-minute delivery, 1-click formatting). Good for retention, harder to charge premium B2C prices unless tied to B2B ROI.
- **Desire (`desire`, 0.75x)**: Ideal self-image ("vitamin" — water tracking, aesthetic filters). Users procrastinate; never market a desire as if it were a painkiller.

### The 5-Tier Alternative Solution Matrix
| Tier | Current User Workaround | Market Meaning | Screening Verdict |
|---|---|---|---|
| **Tier 1** | **None (Silent Endurance)** | Users tolerate the problem without acting | Requires heavy market education (`-3.0` pts) |
| **Tier 2** | **Clumsy Manual Workaround** | Excel, manual copy-paste, hiring Upwork freelancers | **Golden Sweet Spot** (`+8.0` pts) |
| **Tier 3** | **Stitching Multiple Tools** | Exporting/importing across Tool A + Tool B + Tool C | **High-Value Workflow Glue** (`+6.5` pts) |
| **Tier 4** | **Unsatisfied Incumbent** | Paying for mature software but hating a specific step | Needs a 10x wedge on the broken step (`+2.0` pts) |
| **Tier 5** | **Satisfied Incumbent** | Existing solution is mature and users are happy | Avoid unless disruptive for an ignored segment (`-15.0` pts) |

---

## 3. Turning Scattered Clues into 3 Evidence-Backed Product Concepts (Act 2 & Appendices B–D)

### Step A: Clue Clustering
Raw tables from `startup-idea-hunter-skill` (such as `ideas_27_Oct.csv`) contain dozens of individual complaints. Group complaints that share the same **underlying workflow bottleneck and target buyer** into an **Opportunity Cluster** so multi-channel evidence (e.g., Reddit complaint + Upwork paid job + Capterra 2-star review) compounds.

### Step B: Horizontal Segmentation (Appendix B)
Never serve "all users." Split the broad domain into narrow horizontal sub-segments and score each across 5 dimensions (`1–5`):
1. **Pain Intensity**
2. **Willingness to Pay**
3. **Segment Size**
4. **Competition Headroom** (higher score = lower direct competition)
5. **Founder Reachability / Understanding**

### Step C: Vertical Context & Emotion Timeline (Appendix C)
Map the target user's day or workflow chronologically (`Before -> During -> After` or `06:00 -> 10:00 -> 15:00 -> 20:00 -> Long-term`). At each moment, record:
- Physical context (where are their hands? what screen/file is open?)
- Specific friction
- Active emotion from the **6 Core Emotions**: `fear`, `anxiety`, `helplessness`, `loneliness`, `anger`, `regret`.

### Step D: Value Reframing (Appendix D)
Transform a generic tool into a high-willingness-to-pay specialist copilot or concierge:
- *Generic Fitness App* $\rightarrow$ **Postpartum 15-Minute Recovery & Emotional Safety Coach**
- *Calorie Photo Counter* $\rightarrow$ **Diabetic Pre-Meal Glycemic Safety Copilot**
- *News Summarizer* $\rightarrow$ **Morning Investment Intelligence Officer**
- *Campus Flea Market* $\rightarrow$ **72-Hour Graduation Liquidation Concierge**
- *Expense Tracker* $\rightarrow$ **Study-Abroad Financial Steward for Parents**
- *Pomodoro Timer* $\rightarrow$ **Privacy-Safe Remote Work Proof Generator**
- *PDF-to-Excel Converter* $\rightarrow$ **Zero-Template Audit-Ready Line-Item & Visual-Snippet Verification Engine**

---

## 4. Refining the Winning Direction into an Actionable MVP Plan (Act 3 & Appendices E–F)

Follow the mantra: **"One Person, One Job, One Entry Point; Segment Horizontally, Dig Vertically, Refine with AI, Validate Before Building."**

1. **3-Phase MVP Roadmap**:
   - **Phase 1 (Months 1–2 — Concierge / Human-in-the-Loop Validation)**: Use off-the-shelf tools/scripts + manual review to test whether **100 target users yield $\ge 10\%$ paid conversion**.
   - **Phase 2 (Months 3–6 — SDK / AI Workflow Automation)**: Automate the bottleneck with existing APIs/SDKs (never train models from scratch initially).
   - **Phase 3 (Months 6–12 — Scale, Partnerships & Moat)**: Build institutional partnerships, data flywheels, and expand to adjacent segments.
2. **Mitigating the 3 Solo-Founder Concerns**:
   - **Technical Difficulty**: Use pre-built SDKs/APIs + human verification in Phase 1.
   - **Domain Authority Gap**: Partner with 2–3 domain specialists on a **70% product / 30% expert revenue split**, or curate verified standard rules.
   - **High Acquisition Cost (CAC)**: Run narrow-keyword guerrilla outreach in niche communities, trade 1-month trials for case-study reviews, and cap Phase 1 test budget (e.g., <$150 / 1,000 RMB for first 100 users).
3. **20-Item Demand Verification Checklist (Appendix F)**:
   - 5 groups × 4 binary checks: **User Clarity**, **Pain Intensity**, **Solution Differentiation**, **Business Viability**, and **1–2 Week Fast Validation**.
