# Evaluation Specification: `startup-idea-screener-skill`

This specification defines the binary quality criteria and golden cases for `startup-idea-screener-skill`.

## Binary Criteria

1. **`valid-dossier-structure`**: Output is valid JSON containing `niche`, `summary`, `ranked_clusters`, `top_3_product_concepts`, and `verifiable_product_direction`.
2. **`clusters-sorted-and-vitamin-dropped`**: `ranked_clusters` are sorted in descending order by `final_screening_score_100` (among non-flagged clusters), all scores are in `[0, 100]`, and any cluster with `dominant_need_tier == "desire"` or `xiaoming_trap_flagged == true` receives verdict `"DROP_XIAOMING_TRAP"` and never `"COMMIT_AND_VALIDATE"`.
3. **`top-3-concepts-complete`**: `top_3_product_concepts` contains up to 3 reframed concepts, each preserving `sample_verbatim_evidence`, `horizontal_segmentation`, `vertical_emotion_timeline` (using valid Easy-Vibe core emotions), and `value_reframing_table`.
4. **`verifiable-direction-roadmap-and-tam`**: `verifiable_product_direction` targets the #1 ranked cluster (`winning_cluster_id == ranked_clusters[0].cluster_id`) and includes `one_person_one_job_one_entry`, a 3-phase `three_phase_mvp_roadmap`, 3 `solo_founder_concern_mitigations`, `bottom_up_tam`, `moat_strategy`, and 5 `five_round_ai_dialogue_prompts`.
5. **`appendix-f-20-item-checklist`**: `verifiable_product_direction.appendix_f_20_item_checklist` contains all 5 categories (`1_user_clarity`, `2_pain_intensity`, `3_solution_differentiation`, `4_business_viability`, `5_fast_validation_1_2_weeks`) totaling exactly 20 verification items.

```json
{
  "skill": "startup-idea-screener-skill",
  "run": "python3 scripts/run_pipeline.py --input {input} --output {output}",
  "criteria": [
    {
      "id": "valid-dossier-structure",
      "text": "Output is valid JSON containing niche, summary, ranked_clusters, top_3_product_concepts, and verifiable_product_direction",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert all(k in d for k in (\"niche\",\"summary\",\"ranked_clusters\",\"top_3_product_concepts\",\"verifiable_product_direction\"))' {output}"
    },
    {
      "id": "clusters-sorted-and-vitamin-dropped",
      "text": "Clusters have bounded scores in [0,100] and desire or Xiaoming-trap flagged clusters receive DROP_XIAOMING_TRAP",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); rc=d[\"ranked_clusters\"]; assert len(rc)>=2 and all(0<=c[\"final_screening_score_100\"]<=100 for c in rc) and all(c[\"screening_verdict\"]==\"DROP_XIAOMING_TRAP\" for c in rc if c[\"dominant_need_tier\"]==\"desire\" or c[\"gate_2_xiaoming_trap\"][\"xiaoming_trap_flagged\"])' {output}"
    },
    {
      "id": "top-3-concepts-complete",
      "text": "Every concept in top_3_product_concepts includes verbatim evidence, horizontal_segmentation, vertical_emotion_timeline, and value_reframing_table",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); tc=d[\"top_3_product_concepts\"]; assert 1<=len(tc)<=3 and all(all(bool(c.get(k)) for k in (\"sample_verbatim_evidence\",\"horizontal_segmentation\",\"vertical_emotion_timeline\",\"value_reframing_table\")) for c in tc)' {output}"
    },
    {
      "id": "verifiable-direction-roadmap-and-tam",
      "text": "verifiable_product_direction matches rank #1 cluster and includes 3-phase MVP roadmap, 3 concern mitigations, TAM, moat, and 5 AI dialogue rounds",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); vp=d[\"verifiable_product_direction\"]; assert vp[\"winning_cluster_id\"]==d[\"ranked_clusters\"][0][\"cluster_id\"] and len(vp[\"three_phase_mvp_roadmap\"])==3 and len(vp[\"solo_founder_concern_mitigations\"])==3 and len(vp[\"five_round_ai_dialogue_prompts\"])==5 and vp[\"bottom_up_tam\"][\"estimated_annual_tam_usd\"]>0' {output}"
    },
    {
      "id": "appendix-f-20-item-checklist",
      "text": "appendix_f_20_item_checklist contains 5 categories and exactly 20 verification items",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); chk=d[\"verifiable_product_direction\"][\"appendix_f_20_item_checklist\"]; assert len(chk)==5 and sum(len(v) for v in chk.values())==20' {output}"
    }
  ],
  "golden": [
    {
      "id": "case-1",
      "input": "golden/case-1/input.json",
      "expected": "golden/case-1/expected.json",
      "split": "val"
    },
    {
      "id": "case-2",
      "input": "golden/case-2/input.json",
      "expected": null,
      "split": "test",
      "expected_status": "pending-first-green"
    },
    {
      "id": "case-3",
      "input": "golden/case-3/input.json",
      "expected": null,
      "split": "val",
      "expected_status": "pending-first-green"
    }
  ]
}
```
