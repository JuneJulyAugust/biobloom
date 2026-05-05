# USABO Open Exam — Mechanism-Oriented Practitioner Analysis (2003–2018)

_Author: Claude (Opus 4.7). Generated 2026-05-05 from local archive at `raw/markdown/{2003..2018}`._

This report intentionally avoids reproducing exam content. It cites items only as `Y####/Q##` with a short paraphrased concept tag. Companion reports `open_exam_analysis_chatgpt.md` (quantitative survey, topic-keyword counts) and `open_exam_analysis_gemini.md` (high-level narrative, prep recommendations) already exist; this document complements them with a mechanism-first lens, a transparent difficulty rubric, distractor taxonomy, and concrete calibration parameters for the BioBloom question-generation pipeline.

---

## 0. Scope, Method, And Caveats

- **Corpus.** 16 exam files, 2003–2018. 2003 has 35 questions and 4 options. 2004 onward have 50 questions and 5 options (A–E). Total ≈ 785 stems. Answer keys present for every year (2010 manually transcribed; 2013 missing one item).
- **Method.** Manual sampling across early/middle/late eras (2003, 2005, 2007, 2010, 2012, 2014, 2016, 2017, 2018), plus structural skim of the remaining years. Counts and ratios shown below are intentionally rounded and labeled as estimates; they are derived from observable surface features (stem length, presence of figures/tables, negation cues, multi-select cues, calculation cues, Roman-numeral lists, paragraph-length scenarios), not from official USABO metadata.
- **What this report is.** A reading of question *mechanics* — what each item demands of the solver, what distractor traps appear, what skill it actually scores. Not a solution manual; not a content review.
- **Limits.** Difficulty is intrinsically student-relative. Scores below should be read as "expected cognitive load on a well-prepared high-school biology student," not as item response theory parameters. Where numeric counts are given without a denominator, they are illustrative, not authoritative.

---

## 1. Recurring Topic Pillars

Across all years, every exam draws from the same seven pillars (close to the IBO topic weighting, with USABO-specific drift):

| Pillar                                  | Typical share | Stable subtopics                                                                                                                             |
| --------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Cell & Molecular Biology / Biochemistry | 22–32 %       | Membranes & transport; enzyme kinetics; DNA replication; transcription/translation; protein structure & folding; respiration; photosynthesis |
| Genetics & Inheritance                  | 12–18 %       | Mendelian probability; linkage / map distance; pedigree mode-of-inheritance; epistasis; quantitative inheritance; imprinting (later years)   |
| Animal Anatomy & Physiology             | 18–24 %       | Neurophysiology; cardiovascular; renal; endocrine; immune; digestion; reproduction & development                                             |
| Plant Anatomy & Physiology              | 8–14 %        | Hormones (auxin/ethylene/gibberellin/ABA); transport (xylem/phloem); photosynthesis variants C3/C4/CAM; flower development (ABC model)       |
| Ecology                                 | 6–12 %        | Population growth (r/K, exponential/logistic); trophic efficiency; biogeochemical cycles; community interactions                             |
| Evolution & Phylogenetics               | 6–10 %        | Hardy–Weinberg; speciation modes; selection types; phylogeny reading; molecular evolution (dN/dS appears later)                              |
| Animal Behavior (Ethology)              | 4–8 %         | Habituation/imprinting; sexual selection; agonistic/territorial behavior; kin selection                                                      |
| Biosystematics                          | 2–6 %         | Domain-level differences (bacteria vs. archaea vs. eukarya); chordate / arthropod features; alternation of generations                       |

The "twin" pillar weight on Cell/Molecular plus Animal Physiology accounts for nearly half of every exam. The bottom three pillars combined (Behavior, Biosystematics, sometimes Ecology) frequently account for under 20 % of items, a consistent feature worth using when allocating study time.

### 1.1 Recurring problem archetypes

Within those pillars, eight problem archetypes recur, often with a fresh narrative skin from year to year:

1. **Hardy–Weinberg / carrier frequency** — appears in nearly every year (e.g., 2003/Q06, 2005/Q02, 2007/Q02, 2018/Q36).
2. **ABC model of flower development** — virtually identical mechanism reused (2005/Q08, 2010/Q49, 2014/Q14).
3. **Two- or three-point linkage map** — recombination-frequency arithmetic on a trihybrid cross (2010/Q12, 2018/Q43).
4. **Membrane-potential / Nernst** — using the equilibrium-potential equation to identify which ion is being described (2010/Q48; conceptual variants throughout).
5. **Pedigree mode-of-inheritance** — autosomal vs. X-linked, dominant vs. recessive (2007/Q14, 2010/Q32, and many more).
6. **Hydrophobic transmembrane sequence** — identifying the right amino-acid string for an alpha-helical TM region (2003/Q04, 2018/Q06).
7. **Polygenic / additive trait extremes** — given F2 extremes, infer number of loci and intermediate frequency (2005/Q09, 2010/Q44).
8. **Reagent / spot-test identification** — Biuret / Benedict / Ninhydrin / Iodine / Sudan / Tollens combinations (2012/Q06, 2016/Q07).

A practical implication: practice that drills these eight templates — each in two or three narrative skins — should yield outsize return.

---

## 2. Topic Trends Over Time

The topic mix is broadly stable, but four directional drifts are clear:

| Drift                              | 2003–2008                               | 2009–2013                                                           | 2014–2018                                                                      |
| ---------------------------------- | --------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Biotechnology / experimental tools | rare; conceptual PCR or cloning gist    | gel/Western blots, restriction maps appear                          | NGS, CRISPR/cas9, microarray, patch-clamp, degenerate primers (e.g., 2016/Q08) |
| Quantitative content               | a handful of arithmetic items           | calculation peaks (Henderson–Hasselbalch, half-life, recombination) | calculation persists but moves toward biological reasoning *with* numbers      |
| Cross-domain integration           | one-pillar items                        | mixed (e.g., physiology + signal transduction)                      | scenario items pull from 3+ pillars in one stem                                |
| Plant biology depth                | survey-level (xylem/phloem, life cycle) | hormone & development emphasis                                      | molecular plant biology (ethylene-receptor mutants, doubled-haploid, tb1)      |

Quantitatively, multi-select / "select all that apply" formatting appeared in 2010, peaked around 2014–2017, and was deliberately reduced in 2018 (which moved the load into longer prose stems and tables instead). Roman-numeral combination items appear in every year and are the single most common "difficulty multiplier" across the entire corpus.

---

## 3. Transparent Difficulty Rubric

I scored each year on five orthogonal axes, each 1–5, by sampling roughly 10 stems per year and judging the dominant load. The axes are:

| Axis                                    | What it measures                                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **R — Factual recall**                  | Can be solved by remembering a single named fact, structure, term, or pathway step               |
| **C — Conceptual reasoning**            | Requires applying a mechanism (e.g., charge → membrane crossing; gradient → flux direction)      |
| **D — Data / table / graph reading**    | Requires extracting a numeric or visual signal before reasoning                                  |
| **E — Experimental design / inference** | Requires understanding controls, treatments, mutants, or "which test would answer this question" |
| **I — Multi-step integration**          | Requires combining ≥ 2 pillars or ≥ 2 mechanism steps in one chain                               |

Estimated mean scores per year (1 = trivial for a strong student, 5 = expert / olympiad final):

| Year | R   | C   | D   | E   | I   | Composite (avg) | Notes                                                              |
| ---- | --- | --- | --- | --- | --- | --------------- | ------------------------------------------------------------------ |
| 2003 | 3.5 | 2.5 | 1.0 | 1.0 | 1.5 | 1.9             | Short stems, 4-option, definition-heavy                            |
| 2004 | 3.5 | 2.5 | 1.5 | 1.5 | 1.5 | 2.1             | Stems lengthen; first table figures appear                         |
| 2005 | 3.5 | 3.0 | 1.5 | 1.5 | 2.0 | 2.3             | ABC model, Hardy-Weinberg, polygenic introduced                    |
| 2006 | 3.5 | 3.0 | 2.0 | 1.5 | 2.0 | 2.4             | Quant items (probability, percentages) ramp up                     |
| 2007 | 3.5 | 3.0 | 2.0 | 1.5 | 2.0 | 2.4             | Cladogram & pedigree reading                                       |
| 2008 | 3.5 | 3.0 | 2.0 | 1.5 | 2.0 | 2.4             | Physiology dominant; mechanism chains lengthen                     |
| 2009 | 3.5 | 3.0 | 2.0 | 2.0 | 2.0 | 2.5             | More figure-bound items                                            |
| 2010 | 3.5 | 3.5 | 2.5 | 2.0 | 2.5 | 2.8             | Multi-select introduced; Nernst & polygenic re-asked               |
| 2011 | 3.5 | 3.0 | 2.5 | 2.0 | 2.5 | 2.7             | Many figures; biochemistry deepens                                 |
| 2012 | 3.5 | 3.5 | 2.5 | 2.5 | 2.5 | 2.9             | Reagent-table identification; Western-blot reasoning               |
| 2013 | 3.5 | 3.5 | 2.5 | 2.5 | 2.5 | 2.9             | Strong negation density                                            |
| 2014 | 4.0 | 4.0 | 3.0 | 3.0 | 3.5 | 3.5             | Long stems; T/F sub-bubbling; mechanism + pharmacology integration |
| 2015 | 3.5 | 3.5 | 2.5 | 2.5 | 3.0 | 3.0             | Slight dip vs. 2014, but still demanding                           |
| 2016 | 4.0 | 4.0 | 3.5 | 3.5 | 3.5 | 3.7             | Hardest year by composite; image-heavy; many select-all            |
| 2017 | 4.0 | 4.0 | 3.0 | 3.5 | 3.5 | 3.6             | Quant + experimental design dense; Zika scenario, NADPH oxidase    |
| 2018 | 4.0 | 4.0 | 3.0 | 3.0 | 3.5 | 3.5             | Multi-question stems return; less multi-select but heavier prose   |

Reading the rubric:

- **R climbs from 3.5 → 4.0** between 2013 and 2014 because raw recall is no longer enough; the *facts* expected (chronic granulomatous disease, prolactinoma, Hurler syndrome, Pompe's disease) are more clinical and specific.
- **C rises in lockstep** because mechanism chains lengthen (signal in → second messenger → cellular response → phenotype).
- **D peaks 2016–2017** as figures, plasmid maps, and tables become dominant.
- **E (experimental design)** is the single largest jump from 2003 to 2018 — early years rarely test "how would you set this up"; recent years routinely test it.
- **I (integration)** roughly tracks composite difficulty and is the axis most predictive of student score variance, in my judgment.

A reasonable working hypothesis is that the *modal* well-prepared student lost roughly one cognitive load level between the 2008-era exam and the 2016-era exam — the same student who could comfortably finish 2008 in 50 minutes will run out of clock on 2016.

---

## 4. Question Patterns And Distractor Taxonomy

### 4.1 Stem patterns

| Pattern                                       | Frequency                                     | Notes                                                                                                 |
| --------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Direct ID ("which structure / term / X is …") | High (all years)                              | Lowest cognitive load. Solvable by recall.                                                            |
| **NOT / EXCEPT / FALSE / LEAST / incorrect**  | ~25–35 % of items                             | Most common difficulty multiplier. Requires evaluating *all* options, not just finding one correct.   |
| Roman-numeral combination (I/II/III/IV)       | ≈ 1–4 / exam                                  | Forces independent evaluation of each statement; one weak statement collapses several option choices. |
| **"Select all that apply" / multi-key**       | Concentrated 2010, 2014–2017                  | Penalizes guessing; rewards mechanism mastery on every option.                                        |
| True/False sub-bubbling (A/B/C/D each scored) | Mainly 2014, 2018                             | Each option is a separate scored item; partial credit possible.                                       |
| Long applied scenario (≥ 80 words)            | Rises sharply 2014+                           | Reading-speed test as much as biology test.                                                           |
| Quantitative single-step                      | All years                                     | pH, allele frequency, simple ratios.                                                                  |
| Quantitative multi-step                       | 2010, 2014, 2016+                             | Half-life chains, recombination + map order, energy-flow efficiency products.                         |
| Figure / image interpretation                 | Concentrated 2007–2008, 2011–2012, 2014, 2016 | Pedigrees, gels, plasmids, leaf cross-sections, phylogenies.                                          |
| Multi-question shared stem                    | 2018 (revived)                                | Lead-in vignette gates two or more sub-items.                                                         |

### 4.2 Distractor taxonomy

Recognizing the family of trap reduces error rate sharply:

| Distractor family                  | Mechanism of the trap                                                                                     | Defense                                                    |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Vocabulary swap**                | Two real terms with adjacent meaning (e.g., proto-oncogene ↔ tumor suppressor; oligodendrocyte ↔ Schwann) | Restate the textbook definition before scanning options    |
| **Direction reversal**             | Same chain in reverse order (e.g., heart blood flow; hormone cascade I/II/III)                            | Draw the directed arrow first, then read options           |
| **Magnitude / sign flip**          | Same equation, opposite sign or off-by-one log unit                                                       | Solve to one significant figure before looking at choices  |
| **All-of-the-above bait**          | "All of the above" with one mildly wrong sub-statement                                                    | Test each sub-statement against a definite counter-example |
| **Mechanism-correct, scope-wrong** | True statement, but for the wrong organism / tissue / phase                                               | Anchor the *system* before the *fact*                      |
| **Spurious causation**             | Plausible-sounding "because" that pairs a real fact with the wrong reason                                 | Treat the conjunction as two independent claims            |
| **Negation flip**                  | Converting "X promotes Y" into "X inhibits Y" by single word                                              | Read the verb twice; underline NOT/EXCEPT/FALSE            |
| **Unit / dimension trap**          | Wrong unit but right numeric value, or right unit but right *order of magnitude*-off                      | Carry units explicitly through every step                  |
| **Synonym for the right answer**   | Disguising the keyed answer in unfamiliar phrasing while a wrong-but-canonical term distracts             | Predict the answer before scanning options                 |
| **Half-mechanism**                 | Option states first half of mechanism correctly; the consequence half is wrong                            | Force yourself to read each option to its end              |

Every year contains at least three of these families; 2014, 2016, and 2017 use eight or more.

---

## 5. Skills Inventory

Solving the modern Open Exam reliably requires roughly the following skill set, in rough order of leverage:

1. **Compact mental models** of ~25 core mechanisms (action potential, Na⁺/K⁺ ATPase, oxidative phosphorylation, Calvin cycle, glycolysis ↔ gluconeogenesis switch, hormonal cascades HPA / HPT / HPG, kidney nephron, immune cell hierarchy, protein synthesis & QC, signal transduction families).
2. **Probability fluency** — Mendelian, conditional probability for carriers given an affected sibling, two-locus recombination, and chi-square style intuition.
3. **Quantitative literacy** — pH/pKa, log scales, half-life, dilution, ratio reasoning, simple stoichiometry, percent yield, energy-transfer products in ecology.
4. **Pathway directionality** — every cascade question is testable as a directed graph; the first move is to draw it.
5. **Genome-to-phenotype reasoning** — synonymous vs. nonsynonymous, frameshift, missense, nonsense, regulatory vs. coding mutations, dominant-negative vs. loss-of-function.
6. **Experimental literacy** — controls (positive, negative, vehicle, time-zero), what a mutant phenotype rules in vs. rules out, how Western/Northern/Southern/microarray/CRISPR experiments map to specific kinds of evidence.
7. **Visual decoding** — pedigree, cladogram, gel, plasmid map, anatomy cross-section, biochemical pathway diagram, kinetics curve.
8. **Format discipline** — disciplined elimination on Roman numerals; explicit handling of NOT/EXCEPT; awareness that "select all that apply" reverses partial credit logic.
9. **Time triage** — recognizing within ≤ 15 seconds whether a question is a 30-second recall or a 2-minute integration item, and committing accordingly.

Skills 4–6 separate the ~80th-percentile score from the ~95th-percentile score; skill 1 is the floor.

---

## 6. Practitioner Study Framework

Below: how to *attack* each item type, written as repeatable procedures. None of these depend on memorizing a specific answer key.

### 6.1 Recall items

1. **Predict before scanning.** Cover the options. State your answer in one phrase. Only then read the choices and select the closest match. This single habit kills 60–70 % of vocabulary-swap and synonym-distractor errors.
2. **Anchor the system, then the fact.** "Schwann vs. oligodendrocyte" is decided by *which nervous system* (PNS vs. CNS), not by which word feels familiar. The system anchor wins almost every time.
3. **If unsure, eliminate by impossibility, not plausibility.** Two options that contradict each other are usually a forced choice — one must be wrong. Resolve that pair first.

### 6.2 Mechanism items

1. **Draw the directed graph.** Cause → intermediate → effect. Two-arrow chains are usually enough. Then walk the chain forward (forward problem) or invert it (inverse / "what would happen if X were blocked" problem).
2. **State the invariant.** Charge balance. Mass balance. Stoichiometry. Conservation of probability. The right answer never violates the invariant.
3. **Convert "if-then" into a controlled experiment in your head.** "If aquaporins are deleted, water reabsorption falls" is the same statement as "ADH cannot rescue water uptake without aquaporins."
4. **Watch for the half-mechanism trap.** Each option has two clauses. Both must be true. If one is true and one is false, the option is false.

### 6.3 Data / experiment items

1. **Read the figure caption first, axes second, data third.** USABO figures often hide the variable of interest in the caption.
2. **Identify control vs. treatment before drawing any conclusion.** A "mutant phenotype" claim cannot be evaluated without the wild-type baseline.
3. **State the null.** "What would the data look like if the proposed mechanism were wrong?" If you cannot answer this in one sentence, you have not understood the experiment.
4. **Use the sign of the effect, not its size.** Multi-step calculations are usually decided by direction (greater / less / no change), not by precise numerics. If you can rule out four options by sign, the fifth is the answer.
5. **For NOT-CONSISTENT-WITH stems** (very common 2014+): each correct mechanism would *predict* the data; the answer is the one that would predict something different. Force yourself to articulate the predicted observation under each option.

### 6.4 Genetics items

1. **Hardy–Weinberg.** Compute `q` from `q²`, then `p = 1 − q`, then `2pq` for carriers. Recompute even when the answer "feels" obvious.
2. **Pedigree.** Two unaffected parents with an affected child ⇒ recessive. An affected daughter from an unaffected father ⇒ not X-linked recessive. Run those two checks before anything else.
3. **Linkage / mapping.** Identify the parental classes (largest counts) and the double-recombinant classes (smallest counts). The middle gene is the one whose allele is "flipped" between parental and double-recombinant. Compute distances as percent recombinants.
4. **Conditional carrier probability** (e.g., "your sibling is affected, what's *your* carrier probability?"). The unaffected siblings' prior is `2/3` carrier × `1/2` transmission, not `1/2`.
5. **Polygenic / additive trait.** Identify number of loci `n` from the F2 extreme frequency (`(1/4)^n` per extreme phenotype class). Then use binomial for intermediate classes.

### 6.5 Evolution items

1. **Selection sign.** Stabilizing reduces variance; directional shifts the mean; disruptive raises variance. Match the verbal description to the change in the distribution.
2. **Speciation mode** is decided by the geometry of the gene-flow barrier, not by the trait under selection.
3. **Phylogeny reading.** Tree topology is invariant under rotation around any node. Two trees that differ only in rotation are the *same* tree; trees that differ in nesting order are different.
4. **dN/dS / ω.** ω > 1 ⇒ positive selection (host-immune escape, antigenic drift). ω ≈ 1 ⇒ neutral / pseudogene. ω < 1 ⇒ purifying / housekeeping.

### 6.6 Ecology items

1. **Trophic efficiency** is a chain of multiplicative ratios. Sequence: ingested → assimilated → produced. Multiply the efficiencies you are given; do not add.
2. **Population growth.** dN/dt = 0 in HW equilibrium also corresponds to "no allele-frequency change," not "no individuals dying." Watch for the conceptual conflation.
3. **Cycles (C, N, P, H₂O).** Fluxes vs. pools. Most cycle questions test which step is rate-limiting or which step injects vs. removes the element from the biotic compartment.
4. **Biodiversity metrics.** Richness counts species; evenness penalizes dominance; Simpson and Shannon are different transforms of the same intuition.

### 6.7 Behavior items

1. **Proximate vs. ultimate.** Proximate = mechanistic cause (hormones, neural pathway). Ultimate = evolutionary fitness consequence. Many behavior items hinge on which class the question is asking for.
2. **Innate vs. learned.** Habituation, classical conditioning, operant, imprinting, cognition are listed in roughly increasing complexity. If multiple options fit, choose the *least complex* learning that explains the data (parsimony).
3. **Sexual selection.** Female choice favors costly signals (handicap principle). Mate copying and territorial display are common distractor families.

### 6.8 Time-management protocol

A working protocol that fits 50 items in 50 minutes:

- Pass 1 (≈ 25 min): answer every item you can resolve in ≤ 30 seconds. Mark the rest. Do *not* skip multi-select items just because they look long; the easy ones are often hidden in the long-stem items.
- Pass 2 (≈ 18 min): return to marked items. Spend up to 90 seconds each. If still uncertain, eliminate to two and commit.
- Pass 3 (≈ 5 min): review NOT/EXCEPT/FALSE items for negation flips. This single sweep typically recovers 1–3 points.
- Last 2 minutes: ensure every item has *some* answer; blank answers cost more than guessed answers under standard scoring.

---

## 7. Calibration For The BioBloom Practice-Question Generator

Concrete parameters for the question-generation pipeline, derived from the patterns above:

### 7.1 Topic mix per generated practice set

| Pillar            | Target share | Rationale                                              |
| ----------------- | ------------ | ------------------------------------------------------ |
| Cell & Molecular  | 26 %         | Largest pillar; matches observed average               |
| Animal Physiology | 22 %         | Stable second-largest pillar                           |
| Genetics          | 16 %         | Includes Hardy-Weinberg, linkage, pedigree, imprinting |
| Plant Physiology  | 12 %         | Hormones + transport + reproduction                    |
| Ecology           | 8 %          | Population, trophic, cycles                            |
| Evolution         | 8 %          | Selection, speciation, phylogeny, dN/dS                |
| Behavior          | 5 %          | Proximate/ultimate, innate/learned                     |
| Biosystematics    | 3 %          | Domain comparisons, alternation of generations         |

For an era-faithful 50-question set, pull `floor(50 × share)` per pillar and distribute the rounding remainder to Cell & Molecular and Animal Physiology.

### 7.2 Difficulty mix

| Difficulty band        | 2003-style set | 2010-style set | 2018-style set |
| ---------------------- | -------------- | -------------- | -------------- |
| Pure recall (R-heavy)  | 60 %           | 40 %           | 25 %           |
| Mechanism (C-heavy)    | 30 %           | 35 %           | 30 %           |
| Data/figure (D-heavy)  | 5 %            | 10 %           | 20 %           |
| Experimental (E-heavy) | 3 %            | 8 %            | 15 %           |
| Multi-step (I-heavy)   | 2 %            | 7 %            | 10 %           |

Generated items should carry these axis tags as structured metadata so practice sets can be calibrated to the era the student is preparing for.

### 7.3 Format mix

- Single-best-answer 5-option (A–E): default.
- Roman-numeral combination: 6–10 % of items.
- "Select all that apply" / multi-key: 8–15 % when emulating 2014–2017; ≤ 3 % otherwise.
- T/F sub-bubbled (option-as-item): rare, only for 2014/2018 emulation.
- Multi-question shared stem: 1–2 vignettes per 50-item set when emulating 2018.

### 7.4 Distractor specification

Each generated item should include explicit distractor *roles* (one per non-key option), drawn from the taxonomy in §4.2. A reasonable default per stem:

1. Vocabulary-swap distractor (closest sibling concept).
2. Direction-reversal distractor (correct chain, wrong direction).
3. Half-mechanism distractor (right cause, wrong consequence).
4. Mechanism-correct, scope-wrong distractor (right idea, wrong system).

Holding distractor roles fixed forces the generator to produce items that are *educational under elimination* — students who eliminate a half-mechanism trap learn the consequence half on review.

### 7.5 Metadata schema (recommended)

```json
{
  "year_style": "2016",
  "pillar": "cell_molecular",
  "subtopic": "membrane_transport",
  "archetype": "transmembrane_sequence_id",
  "difficulty": { "R": 4, "C": 4, "D": 2, "E": 1, "I": 3 },
  "format": "single_best_5option",
  "negation": "NOT",
  "uses_figure": false,
  "uses_table": true,
  "distractor_roles": ["vocab_swap", "scope_wrong", "half_mech", "direction_reverse"],
  "skills": ["compact_mental_model", "format_discipline"],
  "expected_solve_time_seconds": 70
}
```

This schema lets the generator (or a downstream analytics layer) measure whether a student's miss rate is concentrated on a specific pillar, archetype, or distractor family.

### 7.6 Recommended generation policy

- **Train templates, not items.** Author one template per archetype (§1.1) parameterized by organism, numbers, and narrative skin. Generate a family of items by varying parameters; the underlying mechanism stays.
- **Prefer mechanism-mapped items over fact-mapped items.** A mechanism-mapped item ("which step would be inhibited by X?") teaches the chain. A fact-mapped item ("which enzyme catalyzes Y?") teaches a single node and is replaceable by a flashcard.
- **Reuse distractors across items in a topic** so that students learn to recognize the *family* of trap, not the specific phrasing. The exam itself does this.
- **Avoid AI-style giveaways.** Real USABO items rarely have an option that is obviously the longest, or that contains a hedge word ("usually," "often") in the keyed answer. Generated items should respect the same surface-feature parity to avoid trainable-shortcut artifacts.

---

## 8. Comparison To Existing Reports

This report is intentionally narrower in scope than the two prior analyses in this folder:

- The **chatgpt** report covers the same corpus with keyword-derived topic counts and a heuristic difficulty index. It is the right document for "how many items in 2014 used negation." This one is the right document for "what should the BioBloom generator do about that observation."
- The **gemini** report covers high-level narrative trends and study advice. It is the right document for an introductory orientation. This one assumes the orientation and goes one layer deeper into solving procedures and generation parameters.
- All three reports converge on the same headline finding — difficulty rose sharply in the mid-2010s and the modern exam rewards mechanism + experimental literacy more than recall — but they disagree on the *peak year* (chatgpt: 2016; gemini: 2014–2018 range; this report: 2016 by composite, 2017 close behind). The disagreement is small and reflects different rubrics, not different data.

---

## 9. Headline Recommendations For This Project

1. **Tag every generated item along the five-axis rubric (R/C/D/E/I).** This is the smallest piece of metadata that supports both era-faithful practice set assembly and student-level diagnostics.
2. **Implement the eight archetype templates first.** They cover an outsize fraction of items and offer the highest-value per unit of authoring effort.
3. **Treat 2014–2017 as the reference era for difficulty calibration.** Train students on that target; 2018 and beyond are slightly easier on average and 2003–2009 are far easier.
4. **Generate items with explicit distractor roles.** This is the single largest authoring discipline that distinguishes "looks like an exam item" from "behaves like an exam item."
5. **Preserve the negation / multi-select / Roman-numeral format mix.** A practice corpus that uses only single-best-answer single-stems will under-prepare students for the formats that cause most of the score variance.
6. **Track student performance by *distractor family*, not just by topic.** A 30 % miss rate on "half-mechanism" distractors is a different deficiency from a 30 % miss rate on "scope-wrong" distractors and should drive different remediation.
7. **Keep this analysis decoupled from any specific answer key.** This document references items only by `Y####/Q##` plus paraphrase; the generation pipeline should never train on or reproduce verbatim USABO content. Use this analysis as a design specification, not a content source.

---

## 10. Caveats

- All counts are estimates from sampling, not exhaustive census. The chatgpt companion report has more complete keyword-based counts; treat its numerics as the authoritative baseline and treat the *interpretive* judgments here (rubric scores, distractor role tags) as the contribution.
- Difficulty scoring is unavoidably subjective. The five-axis rubric is presented partly so a human reviewer can disagree with any specific year's score and re-score on a transparent basis.
- "Era-faithful" practice sets should be treated as preparation aids, not as predictions of next year's exam. USABO has historically introduced new formats without warning (multi-select in 2010, T/F sub-bubbling in 2014, multi-question stems in 2018), and any future-year emulation should explicitly assume that *something* novel will appear and budget time accordingly.
- This report does not attempt content fact-checking against current biology; the mechanism descriptions in §6 are deliberately textbook-level and should be cross-checked against Campbell, Alberts, or equivalent before being baked into a production generator.
