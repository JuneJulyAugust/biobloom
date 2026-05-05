# Validation & Improvement Review — `open_exam_consolidated_subtopic_analysis.md`

_Reviewer: Claude (Opus 4.7). Generated 2026-05-05. Independent audit of the report, the generator script, the exported data, and the rendered SVG plots._

---

## 0. TL;DR

The report is **reproducible**, **internally consistent on the surface numbers it cites**, and **architecturally sound** in separating reasoning skills from knowledge subtopics. It has, however, several **systematic detection bugs** that materially distort the subtopic counts, plus a handful of **methodological choices** that are debatable and one or two **plot-rendering decisions** that could be improved.

The headline finding (multi-label taxonomy → 917 hits across 669 tagged questions, 116 unclassified) is **off by a measurable margin**: a single-line fix to the keyword regex raises tag count by ≈ 59 % and shrinks the unclassified bucket by ≈ 28 % without retraining the taxonomy. The narrative conclusions (stable core; rising negation, data, and select-all formatting; difficulty peak in 2016–2017) survive, but the per-subtopic priority scores should be regenerated after the fixes.

| Aspect | Verdict |
| --- | --- |
| Script runs cleanly | ✅ runs end-to-end, no warnings |
| Question count (785) and per-year split | ✅ matches raw markdown exactly |
| Stage definitions and tag scaffolding | ✅ sensible |
| Keyword-matching robustness | ⚠️ **major bug** — singular-only, prefix-only, and space-only phrases miss 30+ % of intended hits |
| Linkage / map-distance subtopic | ❌ **only 1 / ~11 likely items detected** |
| Difficulty rubric | ⚠️ shallow; word-count-dominated |
| Tier classification | ⚠️ rank-index dependent |
| Stage-comparison denominators | ⚠️ 2003 has 35 questions (not 50); raw counts bias Early stage by ≈ +15 items |
| Plot quality | ✅ readable, ⚠️ priority bar reversed; heatmap palette dominated by max year |
| Reproducibility artifacts | ✅ JSON, CSV, JSONL, SVG all written, schemas consistent |

---

## 1. Reproducibility & Surface Validation

```text
$ .venv/bin/python raw/markdown/analysis/code/generate_consolidated_subtopic_analysis.py
Wrote ...open_exam_consolidated_subtopic_analysis.md
Wrote 5 data artifacts and 6 SVG plots
```

Re-ran a clean independent count against the markdown:

| Metric | Report claim | Measured | Δ |
| --- | --- | --- | --- |
| Total questions parsed | 785 | 785 | 0 |
| Per-year split (35, 50×15) | matches manifest | matches manifest | 0 |
| Multi-label hits | 917 | 917 | 0 |
| Tagged questions | 669 | 669 | 0 |
| Unclassified | 116 | 116 | 0 |
| Stage denominators (Early / Middle / Late) | (implied 350 / 250 / 250) | **285 / 250 / 250** | ⚠ |

**Issue 1.1 — stage denominator asymmetry.** Early stage covers six exams (2003–2008) but 2003 only has 35 questions, so Early has 285 questions, not 300 or 350. Every "Early vs. Late" raw-count comparison in the report is off by an asymmetric question-count denominator. This is acknowledged nowhere in the methods. Recommend reporting **per-stage rates** (hits / Q) alongside raw counts.

---

## 2. Detection Bugs (quantified)

### 2.1 Plural / inflection regex bug (most consequential)

The phrase scorer uses

```python
pattern = r"(?<![a-z0-9])" + escaped.replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
```

This wraps every keyword in a strict word boundary on both sides. Two consequences:

1. **Plurals do not match.** Keyword `"ribosome"` does not match `"ribosomes"`. Across the corpus:
   `"ribosomes"` appears 11×, `"organelles"` 10×, `"neurons"` 11×, `"enzymes"` 25×, `"genes"` 81×, `"cells"` 203×, `"antibodies"` 12×, `"muscles"` 16×, `"arteries"` 6×.
2. **Prefix-style stems do not match anything.** Keyword `"mitochond"` (intended to catch `"mitochondria"` / `"mitochondrial"`) matches **0** items because the trailing word boundary blocks the suffix. Same for `"phagocyt"`, etc.

I quantified the impact by patching the function to allow up to four trailing letters before the boundary (`r"[a-z]{0,4}(?![a-z0-9])"`):

| Metric | Current | Plural-tolerant | Δ |
| --- | --- | --- | --- |
| Unclassified questions | 116 | 84 | −28 % |
| Raw subtopic hits (pre-cap, pre-relative-threshold) | 917 | 1 457 | +59 % |

The narrative still holds, but **per-subtopic counts are noisy**, especially for subtopics whose canonical keyword stem is naturally pluralized (Organelles, Neurophysiology, Immunology, Transcription/Translation, Cellular Respiration).

### 2.2 Linkage / recombination detection collapse

A manual scan finds at least **11 candidate linkage-style items** across the corpus:

```text
2004/Q21, 2007/Q38, 2010/Q08, 2010/Q12, 2010/Q16, 2012/Q34,
2014/Q42, 2015/Q35, 2016/Q08, 2017/Q43, 2018/Q43
```

The script reports **1** (`2013/Q37`).

Root cause: the secondary keep-rule is `score >= max(5, top_score * 0.45)`. On 2010/Q12 (a recombination-frequency item), Mendelian wins with 26 points (homozygous×3 + offspring×1 + f1×1), and the Linkage subtopic scores only 8 (recombination×1) — below the 11.7 cutoff. So the linkage label is dropped.

The 0.45 multiplier is too aggressive when a high-specificity keyword (`recombination`, `linkage`, `centimorgan`) is paired with low-specificity Mendelian fillers. Recommend an **override rule**: any keyword with weight ≥ 8 firing at least once should force-include its subtopic, regardless of the relative threshold.

### 2.3 Space-vs-hyphen literal mismatches

Several multi-word keywords use space, but real text uses hyphen. The scorer converts space to `\s+`, which does not match `-`.

| Keyword | Real text occurrences | Matched |
| --- | --- | --- |
| `"patch clamp"` | 0 (text uses `patch-clamp`, **2** occ.) | 0 |
| `"wild type"` | 1 (text uses `wild-type`, **17** occ.) | 1 |
| `"half life"` | 1 (text uses `half-life`, **1** occ.) | 1 |

`wild-type` is also handled by the **reasoning-tag** regex (`\bwild[- ]type\b`), so the experimental-design tag is unaffected. The microtopic side, however, loses the signal.

Fix: replace `\s+` with `[\s\-]+` in the matcher.

### 2.4 `"ph "` keyword can never fire

The keyword `"ph "` (trailing space) under the current rule becomes the regex
`(?<![a-z0-9])ph\s+(?![a-z0-9])`. After `\s+` consumes the space(s), the next character is the start of the next token (e.g., `7` in `"ph 7"` or `r` in `"ph reading"`), which is alphanumeric, so the lookahead fails. **`"ph "` matches nothing in the corpus.**

The keyword is presumably meant to catch pH context for the Biomolecules subtopic. Either drop it (`"pka"` already covers most of the same items) or use `\bph\b` and accept the `pH 7` ↔ `pH-dependent` confusion.

### 2.5 Roman-numeral tag false-positive

The reasoning-tag regex for Roman numerals contains `r"\bi\."`, which also matches `"i.e."` — a benign Latin abbreviation common in question stems. Spot-checks suggest at least a handful of false positives. Replace with `r"(?<![A-Za-z])I{1,3}V?\."` (case-aware) or require multi-statement context (e.g., `\bI\.\s+\S` plus `\bII\.\s+\S` in the same block).

### 2.6 Difficulty rubric is shallow

`difficulty(block, tags)` is a deterministic linear sum of word-count thresholds (≥ 80, ≥ 130, ≥ 190 words) and binary tag presence. This means:

- A 200-word factual-recall item without any tag triggers a near-maximum word-count bonus.
- A 60-word genuinely hard mechanism item without negation/multi-select is scored at the floor (1.5).
- Variance is dominated by reading load, not cognitive load.

Empirically, the year averages this produces are:

| Year | This script | Companion `chatgpt` rubric | Companion `claude` rubric (R+C+D+E+I)/5 |
| --- | --- | --- | --- |
| 2003 | 1.61 | 1.72 | 1.9 |
| 2010 | 2.01 | 2.20 | 2.8 |
| 2016 | 2.39 | 2.54 | 3.7 |
| 2018 | 2.02 | 2.15 | 3.5 |

The three rubrics agree on the **direction** but disagree on the **magnitude**. This script's scores are flatter than they should be because they ignore mechanism-chain length and integration. Recommend adding at least one structural feature for "multiple disjoint biological systems referenced in the same stem" (a proxy: number of distinct microtopics that score ≥ 5 within the question — currently computed but not used in difficulty).

---

## 3. Methodological Concerns

### 3.1 Tier classification is rank-index dependent

```python
def tier(index, row):
    if int(row["stage_breadth"]) == 3 and index < 14:
        return "Tier 1 - stable core"
    ...
```

The Tier 1 cutoff is "stage_breadth == 3 AND rank index < 14". Two consequences:

- A subtopic with stage breadth 3 but priority rank 15 is downgraded out of Tier 1 even if its profile is essentially identical to rank 14.
- Because priority rank depends on a hand-tuned formula, the tier boundaries are not principled.

Recommend an explicit tier rule on the same features used in the priority score (e.g., `Tier 1 ↔ stage_breadth == 3 AND hits >= 25 AND year_breadth >= 12`, with the cutoffs published).

### 3.2 Priority formula is opaque

```python
priority = (
    total
    + 1.7 * len(years)
    + 7 * (stage_breadth == 3)
    + 1.3 * late
    + 3 * max(0, avg_diff - 2.0)
)
if stage_breadth == 1 and late == 0: priority *= 0.65
```

The weights are unjustified in the report. They look reasonable but are sensitive to scaling — `total` and `late` overlap (late is a subset of total), so the formula partially double-counts late-stage items. A clean version would use **independent features** (e.g., `total`, `coefficient_of_variation_across_stages`, `year_breadth`, `late_stage_share`, `avg_difficulty`).

### 3.3 Stage-only tables are empty

The "Stage-Only Subtopics" tables print `-` for every row because the taxonomy is broad enough that every subtopic has at least one hit in every stage. The section is currently noise — either remove it, or surface **near-stage-only** subtopics (e.g., late_share ≥ 0.7) as the actually-useful signal.

### 3.4 Stage denominators not normalized

Already noted in §1. The "Knowledge Pillar Distribution By Stage" and "Format And Reasoning Tags By Stage" tables show raw counts; readers will compute mental ratios off them and be misled by the 285/250/250 split.

Below: the same reasoning-tag table normalized to per-stage Q count (recomputed independently):

| Reasoning / format tag | Early % | Middle % | Late % | Direction |
| --- | --- | --- | --- | --- |
| Negation trap | 21.4 | 26.8 | 34.4 | ↑ clear |
| Calculation / quantitative | 15.1 | 17.2 | 14.0 | flat |
| Data/figure/table reasoning | 8.8 | 11.6 | 18.4 | ↑ strong |
| Experimental design/control reasoning | 8.8 | 4.4 | 11.2 | U-shaped |
| Multi-statement / Roman | 2.5 | 3.2 | 6.4 | ↑ |
| Select-all / multi-answer | 0.0 | 4.0 | 8.4 | ↑ (modern) |

The **directional trends** in the report's narrative are correct after normalization. The **specific share-of-corpus** percentages it cites (e.g., "27.3 %" for negation) are corpus-wide, not stage-specific, and obscure the rising trajectory.

### 3.5 116 unclassified questions hidden from view

The unclassified bucket is 14.8 % of the corpus. None of the report's tables surface these items. Spot-checking the previews shows many are plainly classifiable but missed because of the §2.1 bug:

- `2003/Q05` Chargaff base composition → DNA replication / Biomolecules
- `2003/Q12` Glycolytic product → Cellular respiration (`"glycolytic"` not in keywords; `"glycolysis"` is)
- `2003/Q23` Functional groups in amino acids → Protein structure (blocked by plural)
- `2004/Q44` Why ATP is important → Cellular respiration / Biomolecules
- `2006/Q35` Nitrogen-fixing requirement → Microbiology / Plant
- `2007/Q01` Golden rice → Plant + Biotech (recurring template item)

The pipeline should emit a **manual-review CSV of unclassified questions** to drive incremental keyword tuning.

---

## 4. Plot Quality

| Plot | Rendering | Issues |
| --- | --- | --- |
| `knowledge_subtopic_stage_heatmap.svg` | clear | linear color scale dominated by the max value (80 for cardio/respiratory/renal). Mid-frequency cells (10–25) all look pale. Recommend square-root or quantile scaling. |
| `knowledge_subtopic_priority_scores.svg` | clear | bars are plotted with the **highest priority at the bottom of the chart** (because of `list(reversed(...))`). Convention for ranked bar charts is highest-at-top. Visually inverted. |
| `knowledge_subtopic_early_late_delta.svg` | clear | green/red diverging bars are intuitive. ✓ |
| `knowledge_pillar_stage_distribution.svg` | clear | stacked bars are readable. The "Microbiology/Pathogens" stack visibly drops in the middle stage; this is a real signal in the data. ✓ |
| `data_figure_reasoning_by_knowledge_topic.svg` | clear | same reversed-order issue as priority chart. |
| `experimental_reasoning_by_knowledge_topic.svg` | clear | same reversed-order issue. |

None of the SVGs include a legend for the underlying number scale on the heatmap, and none include axis ticks. Acceptable for a quick-look chart; sub-optimal for a published artifact.

---

## 5. Cross-Validation Against The Three Companion Reports

The consolidated report claims agreement with `chatgpt`, `claude`, and `gemini`. Spot-checks:

| Claim | chatgpt source | claude source | gemini source | Match? |
| --- | --- | --- | --- | --- |
| Three-stage trajectory | ✅ same buckets | ✅ same buckets | ✅ same buckets | ✓ |
| Difficulty peak around 2016 | ✅ (2.54) | ✅ (3.7 composite) | ✅ ("modern era") | ✓ |
| Multi-select introduced ~2010 | ✅ | ✅ | ✅ | ✓ |
| 80–85 % of items from Cell+Animal+Genetics+Plant | ✅ within 1 pp | ✅ ditto | ✅ ditto | ✓ |
| Hardy–Weinberg recurs every era | ✅ | ✅ | ✅ | ✓ |
| ABC flower-development model is repeated archetype | ✅ | ✅ | partially | ✓ |
| Microbiology drops in middle stage | implicit | not discussed | not discussed | ✓ (this report adds a real signal) |

Two genuine **new** contributions of the consolidated report relative to its predecessors:

1. **Reasoning-by-knowledge cross-tabulation** (data/figure × subtopic, experimental × subtopic). This is a useful structural insight — e.g., 57 % of Phylogeny items use figures/tables, 44 % of Plant-hormone items have explicit experimental setups.
2. **Priority-tier ranking with explicit weights**. Even though the formula is debatable (§3.2), having one number per subtopic is operationally useful for module sequencing.

---

## 6. Recommended Improvements (in priority order)

### 6.1 High-leverage code fixes (estimated < 1 hr each)

1. **Plural/inflection-tolerant matching.** Replace
   ```python
   r"(?![a-z0-9])"
   ```
   with
   ```python
   r"(?:s|es|ed|ing|al|ic|ria|ion|ial|ous|ity|ly)?(?![a-z0-9])"
   ```
   or a curated allowlist of common biology suffixes. Re-run; expect ~28 % drop in unclassified and noticeably higher counts on Organelles, Neuro, Transcription/Translation, Cell respiration.
2. **Replace `\s+` with `[\s\-]+`** in the matcher for multi-word keywords. Recovers `patch-clamp`, `wild-type`, `half-life`.
3. **Force-include override** for high-specificity keywords (weight ≥ 8). Recovers Linkage detection from 1 → ≥ 9.
4. **Drop `"ph "`** keyword; rely on `"pka"`, `"pH"` (lowercased), `"pH-dependent"`.
5. **Replace `\bi\.`** with a pattern that only matches Roman numerals in a true list context (e.g., require ≥ 2 consecutive Roman markers within 200 chars).

### 6.2 Methodology improvements

6. **Normalize counts to per-stage rates** wherever stage comparisons are made.
7. **Publish tier rules in feature space, not rank space.** Replace `index < 14` with explicit thresholds.
8. **De-overlap the priority formula.** Use independent features:
   ```text
   priority = w1*log(hits) + w2*year_breadth + w3*late_share + w4*avg_difficulty
   ```
   with weights chosen by fitting against a small hand-graded validation set.
9. **Add a year-level trajectory plot** (one line per pillar). Stage averaging hides 2014/2016 spikes that are real.
10. **Add a tag co-occurrence matrix.** Likely high pairwise correlations: Negation × Select-all, Data × Experimental, Roman × Multi-select. This drives the BioBloom item-generator's distractor planning.
11. **Surface the unclassified bucket** as `data/open_exam_unclassified_questions.csv` for manual taxonomy tuning.
12. **Emit per-stage shares table** (rather than corpus-wide shares) for reasoning tags.

### 6.3 Plot improvements

13. **Reverse the bar-chart sort** so highest priority appears at the top.
14. **Use sqrt or quantile color scaling** in the heatmap so mid-range cells are distinguishable.
15. **Add value labels on every cell** of the heatmap (already present) and a one-line color legend.
16. **Add per-year trajectory line plot** for the four largest pillars.
17. **Add a difficulty-vs-pillar scatter** so the relationship between subtopic recurrence and difficulty is directly visible.

### 6.4 Validation improvements

18. **Build a hand-labeled gold set of ~50 questions** (≈ 3 per year) with manually-assigned subtopics. Use it to compute precision/recall of the auto-tagger and report those numbers in the methods section.
19. **Cross-check claims against year-level item counts.** E.g., "Cell cycle, meiosis and cancer checkpoints — 6/2/12" — verify by manual scan that mid-stage really is anomalously low.
20. **Add an integrity test** that runs every release: total parsed = sum of per-year counts, tagged + unclassified = total, hits sum to subtopic_summary.csv totals.

### 6.5 Content improvements

21. **Surface the *real* near-stage-only subtopics** (late_share ≥ 0.6, early_share ≥ 0.6) instead of the empty stage-only tables. From the data: `Cell signaling, receptors and second messengers` has late_share 0.50; `Development, reproduction and embryology` has late_share 0.50 — both clearly modern-leaning.
22. **Add explicit warning that 2003 is shorter** (35 vs 50 questions) wherever Early-stage counts are presented.
23. **Add a "syllabus-coverage gap" section** — subtopics likely to appear on USABO but not yet captured by the keyword set. Candidates: bioinformatics / sequence analysis, epigenetics beyond methylation, microbiome ecology, RNAi / non-coding RNA, neuroplasticity.
24. **Add a "template archetype" column** to the priority table tying each subtopic back to the eight archetypes identified in `claude` (Hardy-Weinberg, ABC, linkage map, Nernst, pedigree, transmembrane, polygenic, reagent ID). The current report stops at subtopic; the next-most-actionable artifact is the archetype.

---

## 7. What The Report Gets Right

- The **architectural decision** to demote "data interpretation" and "experimental design" from standalone topics to reasoning tags attached to biology subtopics is correct and is genuinely the most useful thing in this report.
- The **multi-label tagging** is the right design; overlapping subtopics are how the exam actually works.
- The **reproducibility artifacts** (`code/`, `data/`, `plots/`) match the report exactly and re-running the script produces identical output. This is a real strength relative to the three single-shot text reports.
- The **stable-core / modern-differentiator / periodic-high-yield / low-frequency tier model** is a clean four-bucket framework that maps to a study plan even before any fixes are applied.
- The **agreement with the three companion reports** on every directional trend that I cross-checked is real and reassuring.

---

## 8. Suggested Next Steps For The BioBloom Project

1. Apply the five high-leverage code fixes (§6.1) and re-publish the report. Most numbers will shift by single-digit percent; some subtopics (Linkage, Organelles) will jump materially.
2. Add a `gold_set/` directory with hand-labeled questions and a `pytest` integrity test that checks tag precision/recall and corpus invariants.
3. Promote the `priority_score` and `tier` fields to first-class metadata in the question bank schema, but only after weights are calibrated against the gold set.
4. Build a year-level interactive view — even a static `plotly`/`bokeh` HTML — so a student can see e.g. "Endocrine homeostasis questions across years" with one click.
5. Treat the consolidated report as a **living document**, not a snapshot. Add a CHANGELOG section at the top that records bug fixes and threshold changes so future re-runs are auditable.

---

## 9. Caveats On This Review

- All defect counts in §2 are derived from the same corpus the report uses. I did not re-OCR or re-clean the markdown; latent extraction errors in the source files would propagate.
- The "≈ 11 likely linkage items" in §2.2 is a manual scan, not a gold standard. Some of those may be Mendelian-only items that mention recombination as background.
- The plural-tolerant patch in §2.1 is a quick estimate, not a fully tuned replacement; it could over-match if deployed naively (e.g., `"actin"` would match `"acting"` under a 4-letter suffix). A real fix needs a per-keyword tolerance flag.
- The difficulty-rubric comparison in §2.6 is informal because each rubric uses different inputs and units. The directional agreement is what matters; the absolute numbers are not directly comparable.

End of review.
