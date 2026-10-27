# startup-idea-screener-skill

Screen, cluster, and reframe raw startup pain points from **`startup-idea-hunter-skill`** (CSV or JSON) into **3 Evidence-Backed Product Concepts** and **1 Verifiable MVP Direction** using the **Easy-Vibe Stage 1B (`finding-great-idea`)** methodology.

## How It Fits in the Easy-Vibe Stage 1 Pipeline

1. **Stage 1A (`startup-idea-hunter-skill`)**: Hunts raw verbatim complaints across Reddit/forums, Capterra/G2 1–3 star reviews, Indie Hackers/Product Hunt, and Upwork/Fiverr repetitive jobs $\rightarrow$ outputs a raw clue table (e.g., `ideas_27_Oct.csv` or `scorecard.json`).
2. **Stage 1B (`startup-idea-screener-skill` — This Skill)**: Ingests the raw clue table, clusters duplicate/related complaints into **Opportunity Clusters**, filters out the **Xiaoming Trap** (incumbent sufficiency, behavioral friction, free substitution), scores the **5-Tier Alternative Solution Matrix**, applies **Horizontal Segmentation** + **Vertical Emotion Timelines**, and outputs:
   - **Expected Output #1**: **3 Evidence-Backed Product Concepts** (with Before/After Value Reframing tables).
   - **Expected Output #2**: **1 Verifiable Product Direction** (*"One Person, One Job, One Entry Point"*, 3-Phase MVP Roadmap, 3 Solo-Founder Concern Mitigations, Bottom-Up TAM, 6-Moat Strategy, 5-Round AI Dialogue Prompts, and the 20-Item Demand Verification Checklist from Appendix F).

## Installation

### Universal Path (works with 6+ tools)

```bash
git clone https://github.com/aidino/startup-idea-screener-skill.git ~/.agents/skills/startup-idea-screener-skill
```

Works with Oh My Pi (`omp`), Codex CLI, Gemini CLI, Kiro, OpenCode, Goose, Antigravity, and other tools that read `~/.agents/skills/`.

### Claude Code (plugin — recommended)

```text
/plugin marketplace add aidino/startup-idea-screener-skill
/plugin install startup-idea-screener-skill@startup-idea-screener-skill
```

### Using `install.sh` (Recommended for all 17 platforms)

```bash
chmod +x install.sh
./install.sh                          # Auto-detect platform
./install.sh --platform claude-code   # Claude Code
./install.sh --platform cursor        # Cursor (auto-generates .mdc)
./install.sh --all                    # All detected platforms
./install.sh --dry-run                # Preview without installing
```

### Manual Installation

| Platform | Copy to |
|---|---|
| Universal / Oh My Pi (`omp`) | `~/.agents/skills/startup-idea-screener-skill/` |
| Claude Code | `~/.claude/skills/startup-idea-screener-skill/` |
| GitHub Copilot | `.github/skills/startup-idea-screener-skill/` |
| Cursor | `.cursor/rules/startup-idea-screener-skill/` |
| Windsurf | `.windsurf/rules/startup-idea-screener-skill/` |
| Cline | `.clinerules/startup-idea-screener-skill/` |
| Codex CLI | `~/.agents/skills/startup-idea-screener-skill/` |
| Gemini CLI | `~/.gemini/skills/startup-idea-screener-skill/` |

## Prerequisites

- Python 3.9+ (uses standard library only; zero external pip packages required).

```bash
python3 scripts/run_pipeline.py --check-prereqs
```

## How to Use in Your Coding Agent

> **Note for Oh My Pi (`omp`) users**:
> - Invoke skills with the `/skill:` prefix: **`/skill:startup-idea-screener-skill <your prompt>`**
> - If you installed the skill while an `omp` session was already open, run **`/reload-plugins`** (or start a new session) so the slash command autocomplete refreshes.

### 1. Screen a CSV Table Exported from `startup-idea-hunter-skill`
```text
# In Oh My Pi (omp):
/skill:startup-idea-screener-skill Hãy sàng lọc các nỗi đau trong file ideas-explore/ideas_27_Oct.csv theo phương pháp Easy-Vibe finding-great-idea, chọn ra 3 khái niệm sản phẩm có bằng chứng và 1 hướng đáng làm MVP nhất.

# In Claude Code / Cursor / Copilot:
/startup-idea-screener-skill Screen the pain points in ideas-explore/ideas_27_Oct.csv using Easy-Vibe finding-great-idea and produce the top 3 product concepts and 1 verifiable MVP direction.
```

### 2. Audit an Idea Against the Xiaoming Trap & Reframe Value
```text
/startup-idea-screener-skill Audit my candidate startup ideas against the Xiaoming Trap, apply horizontal segmentation and vertical emotion timeline analysis, and reframe them into high-WTP copilots.
```

## Deterministic CLI Usage

```bash
# End-to-end screening from a Hunter CSV or JSON file:
python3 scripts/run_pipeline.py \
  --input ideas-explore/ideas_27_Oct.csv \
  --output output/screening-dossier.json \
  --markdown output/screening-dossier.md

# Validate bundled evals and run rollout checks:
python3 scripts/run_evals.py --validate
python3 scripts/run_evals.py --rollout
python3 scripts/evolve.py
```

## Verification

See [VERIFICATION.md](VERIFICATION.md) for recorded gate results and representative run evidence.
