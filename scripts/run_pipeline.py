#!/usr/bin/env python3
"""
Single deterministic orchestrator for startup-idea-screener-skill.

Ingests raw pain clues from startup-idea-hunter-skill (CSV like ideas_27_Oct.csv or JSON),
clusters related complaints into Opportunity Clusters, screens them through the 4 Easy-Vibe
gates (5-Criteria + Need Tier, Xiaoming Trap Audit, 5-Tier Alternative Matrix, Horizontal
Segmentation & Founder-Fit), and outputs:
1. Top 3 Evidence-Backed Product Concepts (with Vertical Emotion Timelines & Value Reframing)
2. 1 Verifiable Product Direction (with 3-Phase MVP Roadmap, 3 Concern Mitigations,
   Bottom-Up TAM, 6-Moat Strategy, 5-Round AI Dialogue Prompts, and 20-Item Appendix F Checklist).

Example:
    $ python3 scripts/run_pipeline.py --input ideas-explore/ideas_27_Oct.csv --output output/dossier.json --markdown output/dossier.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ingest_hunter_clues import ingest_and_cluster  # noqa: E402
from screen_and_reframe import render_markdown_dossier, screen_and_reframe  # noqa: E402

try:
    from success_ledger import record_event  # type: ignore
except Exception:  # pragma: no cover
    record_event = None  # type: ignore


SKILL_NAME = "startup-idea-screener-skill"
SKILL_VERSION = "1.0.0"


def _emit_error(
    message: str,
    error_type: str = "validation",
    details: List[Dict[str, str]] | None = None,
    hint: str = "",
) -> None:
    """Emit structured JSON error to stderr and exit 1."""
    payload: Dict[str, Any] = {
        "error": message,
        "error_type": error_type,
        "details": details or [],
        "hint": hint or "Run with --input <clues.csv|clues.json> --output <dossier.json> or --check-prereqs.",
    }
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(1)


def check_prereqs() -> Dict[str, Any]:
    """Verify runtime prerequisites (Python >= 3.9, config asset presence)."""
    py_ok = sys.version_info >= (3, 9)
    config_ok = (SCRIPT_DIR.parent / "assets" / "config.json").is_file()
    checks = [
        {
            "check": "python_version",
            "required": ">=3.9",
            "found": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "ok": py_ok,
        },
        {
            "check": "config_asset",
            "required": "assets/config.json",
            "found": str(config_ok),
            "ok": config_ok,
        },
    ]
    return {"ready": all(item["ok"] for item in checks), "checks": checks}


def diagnostics() -> Dict[str, Any]:
    """Return skill metadata and enabled harness capabilities."""
    return {
        "skill": SKILL_NAME,
        "version": SKILL_VERSION,
        "harness_level": "standard-v1",
        "commands": [
            "python3 scripts/run_pipeline.py --input <clues.csv|clues.json> --output <dossier.json> [--markdown <dossier.md>]",
            "python3 scripts/run_pipeline.py --check-prereqs",
            "python3 scripts/run_pipeline.py --diagnostics",
            "python3 scripts/ingest_hunter_clues.py --input <clues.csv|clues.json> --output <clustered.json>",
            "python3 scripts/screen_and_reframe.py --input <clustered.json> --output <dossier.json>",
        ],
        "harness_features": {
            "csv_and_json_ingestion": True,
            "opportunity_clustering": True,
            "xiaoming_trap_audit": True,
            "appendix_f_20_item_checklist": True,
            "structured_errors": True,
            "success_ledger": True,
        },
    }


def run_pipeline(input_path: Path, output_path: Path, markdown_path: Path | None = None) -> Dict[str, Any]:
    """
    Execute the full Easy-Vibe Stage 1B idea screening and value reframing pipeline.

    Args:
        input_path: Path to Hunter CSV or JSON clue file.
        output_path: Path to write JSON screening dossier.
        markdown_path: Optional path to write Markdown screening dossier.

    Returns:
        Complete screening dossier dictionary.
    """
    started = time.monotonic()
    if not input_path.is_file():
        raise ValueError(f"Input file not found: {input_path}")

    # Step 1: Ingest CSV/JSON clues and group into semantic Opportunity Clusters in code
    clustered = ingest_and_cluster(input_path)

    # Step 2: Screen through the 4 Easy-Vibe gates and synthesize Top 3 Concepts + #1 Verifiable MVP Plan
    dossier = screen_and_reframe(clustered)

    combined: Dict[str, Any] = {
        "skill": SKILL_NAME,
        "version": SKILL_VERSION,
        "niche": dossier["niche"],
        "source_file": dossier["source_file"],
        "summary": dossier["summary"],
        "ranked_clusters": dossier["ranked_clusters"],
        "top_3_product_concepts": dossier["top_3_product_concepts"],
        "verifiable_product_direction": dossier["verifiable_product_direction"],
        "_warnings": dossier["_warnings"],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_target = markdown_path or output_path.with_suffix(".md")
    md_target.parent.mkdir(parents=True, exist_ok=True)
    md_target.write_text(render_markdown_dossier(combined), encoding="utf-8")

    if record_event is not None:
        try:
            event = os.environ.get("ASC_RUN_EVENT", "skill_run")
            record_event(
                event,
                skill=SKILL_NAME,
                run_id=os.environ.get("ASC_RUN_ID"),
                duration_seconds=time.monotonic() - started,
            )
        except (OSError, ValueError) as exc:
            sys.stderr.write(f"Warning: success_ledger recording skipped: {exc}\n")

    return combined


def main() -> None:
    """CLI entry point for startup-idea-screener-skill."""
    parser = argparse.ArgumentParser(
        description="Run the end-to-end Easy-Vibe Startup Idea Screener & Value Reframing pipeline."
    )
    parser.add_argument("--input", help="Path to input Hunter CSV (e.g. ideas_27_Oct.csv) or JSON clue file")
    parser.add_argument("--output", default="output/screening-dossier.json", help="Path to output JSON file")
    parser.add_argument("--markdown", default="", help="Optional path to output Markdown report")
    parser.add_argument("--check-prereqs", action="store_true", help="Check runtime prerequisites and exit")
    parser.add_argument("--diagnostics", action="store_true", help="Print skill diagnostics JSON and exit")
    args = parser.parse_args()

    if args.check_prereqs:
        prereq_result = check_prereqs()
        print(json.dumps(prereq_result, indent=2))
        sys.exit(0 if prereq_result["ready"] else 1)

    if args.diagnostics:
        print(json.dumps(diagnostics(), indent=2))
        sys.exit(0)

    if not args.input:
        _emit_error(
            "Missing required argument: --input",
            error_type="validation",
            details=[{"field": "input", "error": "required"}],
        )
        return

    try:
        md_path = Path(args.markdown) if args.markdown else None
        run_pipeline(Path(args.input), Path(args.output), md_path)
    except ValueError as exc:
        _emit_error(str(exc), error_type="validation", details=[{"field": "input", "error": str(exc)}])
        return
    except OSError as exc:
        _emit_error(str(exc), error_type="runtime", details=[{"field": "io", "error": str(exc)}])
        return


if __name__ == "__main__":
    main()
