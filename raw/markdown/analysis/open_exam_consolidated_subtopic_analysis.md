# Consolidated USABO Open Exam Subtopic Analysis, 2003-2024

Generated from local files in `raw/markdown` on 2026-05-07. Extends the original 2003-2018 pass with the 2019-2024 exams. No web search or remote model APIs were used.

## Purpose

Subtopic-level prioritization for the BioBloom question-generation pipeline. Multi-label tagging across four stages, with reasoning skills (data, experiment, calculation, negation, multi-statement, select-all) attached to concrete biology subtopics rather than treated as standalone topics. The companion narrative reports (`open_exam_analysis_chatgpt.md`, `open_exam_analysis_claude.md`, `open_exam_analysis_gemini.md`) cover prose-level interpretation; this report keeps the numerics.

## Method And Caveats

The analysis parsed 1082 questions from 22 Markdown exams (2003-2024). Four stages, roughly equal length:

- Early: 2003-2008 (285 questions; 2003 has 35, others 50)
- Middle: 2009-2013 (250 questions)
- Late: 2014-2018 (250 questions)
- Recent: 2019-2024 (297 questions; 2019 has 47, others 50)

Two short years (2003: 35 Q, 2019: 47 Q) make raw stage counts asymmetric; rates and per-question normalizations are reported alongside.

Multi-label knowledge microtopic taxonomy. A question can count for more than one knowledge subtopic. The taxonomy generated 1618 knowledge-subtopic hits across 984 tagged questions, with 98 questions left for manual review (`data/open_exam_unclassified_questions.csv`).

Generator hardening:

- Plural and biology-inflection-tolerant keyword matcher; spaces and hyphens are interchangeable in multi-word phrases.
- High-specificity keywords (weight >= 8) force-include their subtopic so niche labels are not absorbed into broader siblings.
- Roman-numeral tag requires a real list context, not just a stray `i.e.`.
- Feature-based tier rules; priority formula uses independent features only.
- Year-level pillar trajectory, reasoning-tag co-occurrence, and difficulty-vs-recurrence plots are normalized against per-year question counts so 2003 and 2019 are not visually inflated.

## Reproducibility Artifacts

- `code/generate_consolidated_subtopic_analysis.py`
- `data/open_exam_subtopic_question_tags.jsonl` (per-question tags)
- `data/open_exam_subtopic_summary.csv`
- `data/open_exam_reasoning_by_topic.csv`
- `data/open_exam_unclassified_questions.csv` (manual-review queue)
- `data/open_exam_stage_summary.csv` (normalized stage rates)
- `data/open_exam_year_pillar_counts.csv`
- `data/open_exam_reasoning_tag_cooccurrence.csv`
- `data/open_exam_consolidated_subtopic_analysis_data.json` (machine-readable bundle)

## Stage Denominators And Tagging Coverage

| Stage | Years | Questions | Tagged | Unclassified | Subtopic hits | Hits / question |
| --- | --- | --- | --- | --- | --- | --- |
| Early | 2003-2008 | 285 | 259 | 26 | 427 | 1.5 |
| Middle | 2009-2013 | 250 | 223 | 27 | 358 | 1.43 |
| Late | 2014-2018 | 250 | 220 | 30 | 349 | 1.4 |
| Recent | 2019-2024 | 297 | 282 | 15 | 484 | 1.63 |

## Headline Findings, 2003-2024

- Syllabus is stable across all four stages; what changed is how it is tested.
- Difficulty rises through 2014-2017, peaks again in 2020-2021, and partially walks back in 2023-2024 (shorter stems, less data/experimental load).
- "Select all that apply" formatting is concentrated in 2010-2017 and absent from 2019-2024.
- Modern molecular tools (CRISPR/Cas9, NativePAGE, lipid nanoparticle delivery, ELISA-vs-PCR contrasts) become core in 2019-2024 rather than specialty.
- Highest-return practice target: mastering the templates this report ranks Tier 1 / Tier 2, not memorizing past items.

## Generated Plots

- ![knowledge_subtopic_stage_heatmap](plots/knowledge_subtopic_stage_heatmap.svg)
- ![knowledge_subtopic_priority_scores](plots/knowledge_subtopic_priority_scores.svg)
- ![knowledge_subtopic_early_late_delta](plots/knowledge_subtopic_early_late_delta.svg)
- ![knowledge_pillar_stage_distribution](plots/knowledge_pillar_stage_distribution.svg)
- ![data_figure_reasoning_by_knowledge_topic](plots/data_figure_reasoning_by_knowledge_topic.svg)
- ![experimental_reasoning_by_knowledge_topic](plots/experimental_reasoning_by_knowledge_topic.svg)
- ![knowledge_pillar_year_trajectory](plots/knowledge_pillar_year_trajectory.svg)
- ![reasoning_tag_cooccurrence](plots/reasoning_tag_cooccurrence.svg)
- ![difficulty_vs_subtopic_recurrence](plots/difficulty_vs_subtopic_recurrence.svg)

## Knowledge Pillar Distribution By Stage

Multi-label knowledge-topic hits. Totals exceed question count because items frequently span pillars. Data/experiment is reasoning, not pillar; see later sections.

| Pillar | Hits | Early | Middle | Late | Recent | Modern share | Share of hits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Molecular/Cell | 440 | 115 | 107 | 102 | 116 | 50% | 27.2% |
| Animal Physiology | 406 | 104 | 90 | 90 | 122 | 52% | 25.1% |
| Genetics/Evolution | 307 | 85 | 77 | 55 | 90 | 47% | 19.0% |
| Ecology/Behavior | 174 | 48 | 38 | 36 | 52 | 51% | 10.8% |
| Plant | 155 | 41 | 32 | 34 | 48 | 53% | 9.6% |
| Microbiology/Pathogens | 88 | 25 | 9 | 24 | 30 | 61% | 5.4% |
| Molecular/Methods | 48 | 9 | 5 | 8 | 26 | 71% | 3.0% |

## Stable Knowledge Subtopics

Subtopics that appear in **all four** stages with at least 12 hits. These are the safest foundation for objective prioritization. The slash-separated column shows Early/Middle/Late/Recent counts.

| Subtopic | Pillar | Hits | E/M/L/R | Years tested | Avg difficulty |
| --- | --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 122 | 36/34/22/30 | 22 | 2.26 |
| Mendelian genetics and probability | Genetics/Evolution | 102 | 28/23/18/33 | 21 | 2.53 |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 88 | 25/9/24/30 | 21 | 2.39 |
| Population/community ecology and biodiversity | Ecology/Behavior | 86 | 22/20/17/27 | 22 | 2.43 |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 82 | 22/21/16/23 | 22 | 2.27 |
| Plant tissues, xylem/phloem and water transport | Plant | 69 | 18/11/15/25 | 22 | 2.27 |
| Plant reproduction, development and life cycles | Plant | 67 | 20/19/14/14 | 22 | 2.23 |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 64 | 12/22/16/14 | 18 | 2.47 |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 62 | 15/14/14/19 | 21 | 2.27 |
| Endocrine feedback and homeostasis | Animal Physiology | 57 | 18/12/12/15 | 21 | 2.24 |
| Immunology, inflammation and host defense | Animal Physiology | 56 | 9/7/13/27 | 18 | 2.41 |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 55 | 17/11/12/15 | 21 | 2.16 |
| Behavior, learning and ethology | Ecology/Behavior | 54 | 13/12/14/15 | 21 | 2.14 |
| Development, reproduction and embryology | Animal Physiology | 54 | 9/12/17/16 | 20 | 2.39 |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 52 | 18/9/13/12 | 21 | 2.17 |
| Protein structure, amino acids and enzymes | Molecular/Cell | 51 | 9/20/9/13 | 20 | 2.3 |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 48 | 9/5/8/26 | 19 | 2.76 |
| Transcription, translation and gene regulation | Molecular/Cell | 44 | 18/5/11/10 | 19 | 2.39 |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 42 | 9/13/8/12 | 20 | 2.27 |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 41 | 13/10/10/8 | 20 | 2.19 |
| Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 39 | 11/9/6/13 | 18 | 2.39 |
| Pedigrees and inheritance modes | Genetics/Evolution | 39 | 11/8/4/16 | 18 | 2.53 |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 37 | 11/7/8/11 | 14 | 2.37 |
| DNA replication, chromosomes and telomeres | Molecular/Cell | 36 | 10/6/13/7 | 16 | 2.28 |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 34 | 13/6/5/10 | 21 | 2.29 |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 32 | 7/2/11/12 | 15 | 2.1 |
| Hardy-Weinberg and population genetics | Genetics/Evolution | 25 | 8/11/2/4 | 16 | 2.45 |
| Membrane structure, fluidity and permeability | Molecular/Cell | 22 | 7/9/2/4 | 16 | 2.16 |
| Cell signaling, receptors and second messengers | Molecular/Cell | 21 | 3/5/5/8 | 11 | 2.46 |
| Plant hormones, tropisms and environmental responses | Plant | 19 | 3/2/5/9 | 14 | 2.48 |

## Prioritized Learning Objectives

Main action table. Ranks knowledge subtopics by frequency, stage stability, year breadth, modern (Late+Recent) relevance, and cognitive load.

| Rank | Tier | Subtopic | Pillar | Hits | Priority | E/M/L/R | Years | Template archetype | Learning objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Tier 1 - stable core | Cardiovascular, respiratory and renal systems | Animal Physiology | 122 | 105.9 | 36/34/22/30 | 2003-2024 | Gas exchange / renal transport / pressure-flow | Use gas exchange, blood flow, renal transport, pH/CO2, and pressure-volume logic to predict homeostasis. |
| 2 | Tier 1 - stable core | Mendelian genetics and probability | Genetics/Evolution | 102 | 105.2 | 28/23/18/33 | 2003-2016, 2018-2024 | Cross setup / conditional probability | Set up genotypes, gametes, dominance, recessiveness, and conditional probability before choosing an answer. |
| 3 | Tier 1 - stable core | Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 88 | 104.1 | 25/9/24/30 | 2003-2009, 2011-2024 | Pathogen / plasmid / genetic-exchange scenario | Compare viruses, bacteria, fungi, protists, plasmids, antibiotics, conjugation, and host-pathogen interactions. |
| 4 | Tier 1 - stable core | Population/community ecology and biodiversity | Ecology/Behavior | 86 | 104.1 | 22/20/17/27 | 2003-2024 | Population/community model inference | Use population models, community interactions, biodiversity metrics, and ecological reasoning. |
| 5 | Tier 1 - stable core | Evolution, selection, adaptation and speciation | Genetics/Evolution | 82 | 102.0 | 22/21/16/23 | 2003-2024 | Selection / isolation / adaptation scenario | Separate selection mode, adaptation, isolation, gene flow, speciation, and evolutionary evidence. |
| 6 | Tier 1 - stable core | Plant tissues, xylem/phloem and water transport | Plant | 69 | 101.4 | 18/11/15/25 | 2003-2024 | Xylem/phloem / source-sink transport | Relate plant structure to xylem/phloem flow, source-sink logic, stomata, tissues, and water potential. |
| 7 | Tier 1 - stable core | Plant reproduction, development and life cycles | Plant | 67 | 98.5 | 20/19/14/14 | 2003-2024 | ABC flower model / generations | Track ploidy, generations, flowers, endosperm, seeds, fruits, sporophytes, and gametophytes. |
| 8 | Tier 1 - stable core | Neurophysiology, muscle and sensory systems | Animal Physiology | 62 | 98.0 | 15/14/14/19 | 2003-2022, 2024 | Action potential / synapse / muscle mechanism | Predict nerve, sensory, muscle, synapse, and action-potential effects from mechanism. |
| 9 | Tier 1 - stable core | Lab methods, biotechnology and molecular tools | Molecular/Methods | 48 | 97.8 | 9/5/8/26 | 2004-2012, 2015-2024 | PCR / blot / gel / sequencing method choice | Know what PCR, blots, gels, sequencing, plasmid maps, microarrays, CRISPR, and probes can show. |
| 10 | Tier 1 - stable core | Development, reproduction and embryology | Animal Physiology | 54 | 96.8 | 9/12/17/16 | 2003-2005, 2007-2009, 2011-2024 | Embryology fate-map / morphogen variant | Connect fertilization, cleavage, germ layers, embryonic structures, developmental signals, and reproductive physiology. |
| 11 | Tier 1 - stable core | Endocrine feedback and homeostasis | Animal Physiology | 57 | 96.0 | 18/12/12/15 | 2003-2022, 2024 | Feedback-axis homeostasis variant | Map endocrine axes, hormone source, target, feedback, and homeostatic response. |
| 12 | Tier 1 - stable core | Immunology, inflammation and host defense | Animal Physiology | 56 | 95.8 | 9/7/13/27 | 2004-2010, 2012-2014, 2017-2024 | Immune-cell / antibody / pathogen-response variant | Distinguish innate/adaptive immunity, antibody classes, inflammation, immune cells, and pathogen recognition. |
| 13 | Tier 1 - stable core | Behavior, learning and ethology | Ecology/Behavior | 54 | 95.5 | 13/12/14/15 | 2003-2009, 2011-2024 | Behavioral experiment / fitness explanation | Separate innate behavior, habituation, conditioning, imprinting, kin selection, and proximate/ultimate explanations. |
| 14 | Tier 1 - stable core | Digestion, nutrition, vitamins and metabolism | Animal Physiology | 55 | 95.2 | 17/11/12/15 | 2004-2024 | Digestive enzyme / nutrient-deficiency pathway | Match organs, digestive enzymes, nutrient absorption, vitamins/minerals, and deficiency symptoms. |
| 15 | Tier 1 - stable core | Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 52 | 94.5 | 18/9/13/12 | 2003-2015, 2017-2024 | ETC / ATP-yield perturbation | Trace electrons, proton gradients, ATP synthase, uncouplers, fermentation, and cellular energy yield. |
| 16 | Tier 1 - stable core | Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 64 | 94.3 | 12/22/16/14 | 2004, 2006, 2008-2021, 2023-2024 | Functional-group / reagent-identification variant | Recognize biomolecule classes, carbohydrates/lipids/nucleotides, pH chemistry, and reagent-test evidence. |
| 17 | Tier 1 - stable core | Protein structure, amino acids and enzymes | Molecular/Cell | 51 | 92.9 | 9/20/9/13 | 2003-2004, 2006, 2008-2024 | Enzyme kinetics / protein chemistry | Connect amino-acid chemistry, folding, enzyme behavior, allostery, and protein function. |
| 18 | Tier 1 - stable core | Photosynthesis, pigments and carbon fixation | Molecular/Cell | 42 | 91.1 | 9/13/8/12 | 2003-2007, 2009-2017, 2019-2024 | Action spectrum / carbon-fixation variant | Explain pigments, light reactions, Calvin cycle, photosystems, C3/C4/CAM logic, and action spectra. |
| 19 | Tier 1 - stable core | Transcription, translation and gene regulation | Molecular/Cell | 44 | 91.0 | 18/5/11/10 | 2003-2010, 2013-2022, 2024 | Operon / codon / regulatory perturbation | Map DNA to RNA to protein, including promoters, operators, RNA processing, codons, ribosomes, and regulatory elements. |
| 20 | Tier 1 - stable core | Phylogeny, cladograms and systematics | Genetics/Evolution | 41 | 89.7 | 13/10/10/8 | 2003-2012, 2014-2022, 2024 | Cladogram / tree-topology interpretation | Read tree topology and distinguish common ancestry from superficial similarity or taxonomy rank. |
| 21 | Tier 1 - stable core | Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 34 | 89.7 | 13/6/5/10 | 2003-2011, 2013-2024 | Productivity / trophic / cycle calculation | Trace energy, biomass, productivity, trophic efficiency, and elemental cycles. |
| 22 | Tier 1 - stable core | Pedigrees and inheritance modes | Genetics/Evolution | 39 | 89.6 | 11/8/4/16 | 2003-2014, 2018, 2020-2024 | Pedigree inheritance-mode elimination | Eliminate autosomal/X-linked and dominant/recessive modes using pedigree constraints. |
| 23 | Tier 1 - stable core | Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 39 | 88.2 | 11/9/6/13 | 2003, 2005-2008, 2010-2012, 2014, 2016-2024 | Nernst / osmosis / transporter gradient | Use gradients, channels, pumps, transporters, and membrane potentials to predict movement and physiological effect. |
| 24 | Tier 1 - stable core | DNA replication, chromosomes and telomeres | Molecular/Cell | 36 | 84.5 | 10/6/13/7 | 2003, 2005, 2007-2008, 2010-2011, 2013-2018, 2020-2023 | Replication fork / chromosome-end perturbation | Explain replication machinery, chromosome structure, origins, telomeres, and replication errors. |
| 25 | Tier 1 - stable core | Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 32 | 82.6 | 7/2/11/12 | 2003, 2005-2007, 2011-2012, 2014-2017, 2019-2023 | Meiosis / checkpoint / cancer-control variant | Predict effects of cell-cycle state, mitosis/meiosis errors, cyclins, oncogenes, tumor suppressors, and checkpoints. |
| 26 | Tier 1 - stable core | Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 37 | 81.8 | 11/7/8/11 | 2005-2008, 2010-2011, 2013-2014, 2017-2021, 2024 | Organelle-localization / trafficking inference | Assign cell functions to organelles, cytoskeletal systems, vesicles, and intracellular compartments. |
| 27 | Tier 2 - modern differentiator | Plant hormones, tropisms and environmental responses | Plant | 19 | 78.0 | 3/2/5/9 | 2004, 2006, 2008-2009, 2013-2016, 2018-2022, 2024 | Plant-hormone / tropism experiment | Predict plant growth and germination from auxin, ethylene, gibberellin, ABA, phytochrome, and environmental cues. |
| 28 | Tier 3 - periodic high-yield | Hardy-Weinberg and population genetics | Genetics/Evolution | 25 | 77.0 | 8/11/2/4 | 2003-2008, 2010-2014, 2016, 2021-2024 | Hardy-Weinberg allele-frequency calculation | Use allele frequencies, carrier frequencies, and equilibrium assumptions to predict genotype proportions. |
| 29 | Tier 3 - periodic high-yield | Membrane structure, fluidity and permeability | Molecular/Cell | 22 | 74.0 | 7/9/2/4 | 2003-2012, 2017-2019, 2021-2022, 2024 | Membrane-composition permeability variant | Predict permeability and membrane behavior from lipid composition, saturation, hydrophobicity, and bilayer structure. |
| 30 | Tier 2 - modern differentiator | Cell signaling, receptors and second messengers | Molecular/Cell | 21 | 72.9 | 3/5/5/8 | 2004-2005, 2010-2011, 2013, 2017-2019, 2022-2024 | Receptor / second-messenger cascade | Trace ligand-receptor binding through second messengers, kinases, and cellular response. |

### Tier Rules

Tier 1 - stable core: present in every stage; at least 30 hits; at least 14 distinct years tested.
Tier 2 - modern differentiator: at least 6 hits in Late+Recent combined, with modern share >= 45 % or modern count >= early count.
Tier 3 - periodic high-yield: at least 10 hits but does not satisfy Tier 1 / Tier 2.
Tier 4 - selective / low-frequency: everything else.

Priority score = `12*log1p(hits) + 1.5*year_breadth + 6*all_four_stages + 14*modern_share + 7*max(0, avg_difficulty - 1.8)`. Independent features only; sequencing aid, not a psychometric difficulty model.

## Data/Figure/Table Reasoning By Knowledge Topic

This replaces the overly broad `Data, graph, table & figure interpretation` subtopic. The skill is real, but it is most useful when attached to the biology content it tests.

| Knowledge subtopic | Pillar | Primary questions | Data/figure/table questions | Share |
| --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 89 | 15 | 17% |
| Population/community ecology and biodiversity | Ecology/Behavior | 47 | 14 | 30% |
| Plant tissues, xylem/phloem and water transport | Plant | 56 | 10 | 18% |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 22 | 9 | 41% |
| Pedigrees and inheritance modes | Genetics/Evolution | 19 | 8 | 42% |
| Plant reproduction, development and life cycles | Plant | 47 | 8 | 17% |
| Mendelian genetics and probability | Genetics/Evolution | 56 | 7 | 12% |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 53 | 7 | 13% |
| Transcription, translation and gene regulation | Molecular/Cell | 23 | 7 | 30% |
| Protein structure, amino acids and enzymes | Molecular/Cell | 35 | 6 | 17% |
| Behavior, learning and ethology | Ecology/Behavior | 39 | 5 | 13% |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 29 | 5 | 17% |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 50 | 5 | 10% |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 21 | 5 | 24% |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 29 | 4 | 14% |
| Endocrine feedback and homeostasis | Animal Physiology | 37 | 4 | 11% |
| Immunology, inflammation and host defense | Animal Physiology | 36 | 4 | 11% |
| Development, reproduction and embryology | Animal Physiology | 30 | 3 | 10% |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 35 | 3 | 9% |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 40 | 3 | 8% |

Interpretation:

- Visual and table-heavy questions are not a separate chapter. They cluster around physiology, genetics, plants, ecology, molecular methods, and development.
- Practice should tag both the knowledge objective and the representation skill, for example `cardiovascular/renal physiology + graph/table`, or `plant development + figure interpretation`.

## Experimental Design And Controls By Knowledge Topic

This replaces the overly broad `Experimental design, controls & inference` subtopic. Experimental design is a cross-cutting reasoning skill, but the exam usually anchors it in a concrete biological system.

| Knowledge subtopic | Pillar | Primary questions | Experimental/control questions | Share |
| --- | --- | --- | --- | --- |
| Plant reproduction, development and life cycles | Plant | 47 | 9 | 19% |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 89 | 7 | 8% |
| Endocrine feedback and homeostasis | Animal Physiology | 37 | 6 | 16% |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 50 | 6 | 12% |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 21 | 6 | 29% |
| Population/community ecology and biodiversity | Ecology/Behavior | 47 | 6 | 13% |
| Behavior, learning and ethology | Ecology/Behavior | 39 | 5 | 13% |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 40 | 5 | 12% |
| Transcription, translation and gene regulation | Molecular/Cell | 23 | 5 | 22% |
| Development, reproduction and embryology | Animal Physiology | 30 | 4 | 13% |
| Immunology, inflammation and host defense | Animal Physiology | 36 | 4 | 11% |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 21 | 4 | 19% |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 22 | 3 | 14% |
| Mendelian genetics and probability | Genetics/Evolution | 56 | 3 | 5% |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 26 | 3 | 12% |
| Plant hormones, tropisms and environmental responses | Plant | 14 | 3 | 21% |
| Plant tissues, xylem/phloem and water transport | Plant | 56 | 3 | 5% |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 26 | 2 | 8% |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 35 | 2 | 6% |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 53 | 2 | 4% |

Interpretation:

- Experimental reasoning is strongest where concrete mechanisms can be perturbed: physiology, plant mechanisms, gene regulation, organelles/trafficking, evolution/ecology setups, and lab-method contexts.
- BioBloom should generate experimental questions by choosing a knowledge target first, then adding variables, controls, mutants, expected results, and distractors.

## Modern-Rising Subtopics (Late + Recent vs. Early)

Subtopics with more hits in 2014-2024 than in 2003-2008. These anchor advanced practice sets and final-stage diagnostics.

| Subtopic | Pillar | Early | Middle | Late | Recent | Modern - Early | Modern share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Immunology, inflammation and host defense | Animal Physiology | 9 | 7 | 13 | 27 | 31 | 71% |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 25 | 9 | 24 | 30 | 29 | 61% |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 9 | 5 | 8 | 26 | 25 | 71% |
| Development, reproduction and embryology | Animal Physiology | 9 | 12 | 17 | 16 | 24 | 61% |
| Mendelian genetics and probability | Genetics/Evolution | 28 | 23 | 18 | 33 | 23 | 50% |
| Population/community ecology and biodiversity | Ecology/Behavior | 22 | 20 | 17 | 27 | 22 | 51% |
| Plant tissues, xylem/phloem and water transport | Plant | 18 | 11 | 15 | 25 | 22 | 58% |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 15 | 14 | 14 | 19 | 18 | 53% |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 12 | 22 | 16 | 14 | 18 | 47% |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 22 | 21 | 16 | 23 | 17 | 48% |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 36 | 34 | 22 | 30 | 16 | 43% |
| Behavior, learning and ethology | Ecology/Behavior | 13 | 12 | 14 | 15 | 16 | 54% |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 7 | 2 | 11 | 12 | 16 | 72% |
| Protein structure, amino acids and enzymes | Molecular/Cell | 9 | 20 | 9 | 13 | 13 | 43% |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 9 | 13 | 8 | 12 | 11 | 48% |
| Plant hormones, tropisms and environmental responses | Plant | 3 | 2 | 5 | 9 | 11 | 74% |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 17 | 11 | 12 | 15 | 10 | 49% |
| DNA replication, chromosomes and telomeres | Molecular/Cell | 10 | 6 | 13 | 7 | 10 | 56% |

## Declining Or Early-Weighted Subtopics

Subtopics with more hits in 2003-2008 than in Late + Recent combined. Still useful for foundational recall but should not dominate a modern-practice plan.

| Subtopic | Pillar | Early | Middle | Late | Recent | Early - Modern | Years |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hardy-Weinberg and population genetics | Genetics/Evolution | 8 | 11 | 2 | 4 | 2 | 2003-2008, 2010-2014, 2016, 2021-2024 |
| Membrane structure, fluidity and permeability | Molecular/Cell | 7 | 9 | 2 | 4 | 1 | 2003-2012, 2017-2019, 2021-2022, 2024 |

## Stage-Skewed Subtopics

Subtopics where one stage carries a disproportionate share of hits. The broad taxonomy means truly stage-only subtopics are rare; these tables surface near-stage-only signals instead.

Recent-skewed (>= 30 % of hits in 2019-2024 with at least 4 Recent hits):

| Subtopic | Pillar | E/M/L/R | Recent share | Years |
| --- | --- | --- | --- | --- |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 9/5/8/26 | 54% | 2004-2012, 2015-2024 |
| Immunology, inflammation and host defense | Animal Physiology | 9/7/13/27 | 48% | 2004-2010, 2012-2014, 2017-2024 |
| Plant hormones, tropisms and environmental responses | Plant | 3/2/5/9 | 47% | 2004, 2006, 2008-2009, 2013-2016, 2018-2022, 2024 |
| Pedigrees and inheritance modes | Genetics/Evolution | 11/8/4/16 | 41% | 2003-2014, 2018, 2020-2024 |
| Linkage, recombination and map distance | Genetics/Evolution | 1/3/4/5 | 38% | 2004, 2010, 2012, 2014-2015, 2017-2022 |
| Cell signaling, receptors and second messengers | Molecular/Cell | 3/5/5/8 | 38% | 2004-2005, 2010-2011, 2013, 2017-2019, 2022-2024 |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 7/2/11/12 | 38% | 2003, 2005-2007, 2011-2012, 2014-2017, 2019-2023 |
| Plant tissues, xylem/phloem and water transport | Plant | 18/11/15/25 | 36% | 2003-2024 |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 25/9/24/30 | 34% | 2003-2009, 2011-2024 |
| Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 11/9/6/13 | 33% | 2003, 2005-2008, 2010-2012, 2014, 2016-2024 |
| Mendelian genetics and probability | Genetics/Evolution | 28/23/18/33 | 32% | 2003-2016, 2018-2024 |
| Population/community ecology and biodiversity | Ecology/Behavior | 22/20/17/27 | 31% | 2003-2024 |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 15/14/14/19 | 31% | 2003-2022, 2024 |

Early-skewed (>= 45 % of hits in 2003-2008 with at least 5 Early hits):

| Subtopic | Pillar | E/M/L/R | Early share | Years |
| --- | --- | --- | --- | --- |
| - | - | - | - | - |

## Format And Reasoning Tags By Stage

Not knowledge subtopics, but strong difficulty multipliers and BioBloom metadata fields. Percentages are normalized to per-stage question count.

| Reasoning / format tag | Total Q | Early % | Middle % | Late % | Recent % | Share of corpus |
| --- | --- | --- | --- | --- | --- | --- |
| Negation trap | 288 | 21.4% | 26.8% | 34.4% | 24.9% | 26.6% |
| Calculation / quantitative | 167 | 15.1% | 17.2% | 14.0% | 15.5% | 15.4% |
| Data/figure/table reasoning | 159 | 8.8% | 11.6% | 18.4% | 19.9% | 14.7% |
| Experimental design/control reasoning | 96 | 8.8% | 4.4% | 11.2% | 10.8% | 8.9% |
| Multi-statement / Roman | 53 | 2.5% | 3.2% | 4.8% | 8.8% | 4.9% |
| Select-all / multi-answer | 31 | 0.0% | 4.0% | 8.4% | 0.0% | 2.9% |

Notes:

- Negation density rises Early -> Late then partially eases in Recent.
- Data/figure reasoning rises monotonically Early -> Recent.
- Roman / multi-statement format almost doubles in Recent and absorbs much of the cognitive load that select-all used to carry.
- Select-all formatting is concentrated in 2010-2017; absent from 2019-2024.
- Calculation rate stays roughly flat across all four stages.
- See `data/open_exam_reasoning_tag_cooccurrence.csv` for compound forms (data + experiment, negation + Roman, etc.).

## Practice-Set Composition

For a 50-question modern-style practice set, target the following composition (numbers approximate; choose by Tier and reasoning tag rather than topic name alone):

- 13-15 molecular/cell and gene-expression mechanisms.
- 8-10 physiology mechanisms (endocrine, neural, immune, renal/respiratory/cardiovascular).
- 7-9 genetics (Mendelian, pedigree, linkage, Hardy-Weinberg, quantitative).
- 5-7 plant biology (transport, hormones, reproduction, photosynthesis).
- 5-7 ecology / evolution / behavior / systematics.
- 6-10 with figures, tables, or data.
- 5-8 with negation or Roman-numeral / multi-statement logic.
- 3-6 with modern lab / experimental-method reasoning.
- 0 select-all when emulating 2019-2024; 4-7 select-all when emulating 2014-2017.

Every set should mix content coverage with task-form coverage; a text-only single-answer set undertrains modern items.

## Project Recommendations

1. Tag every generated question with `pillar`, `subtopics`, `reasoning_tags`, `stage`, `difficulty_estimate`, and `template_archetype` as first-class metadata.
2. Preserve all four stage labels (`early`, `middle`, `late`, `recent`) so the app can generate era-faithful practice. Use `late + recent` as the default "modern" target for advanced preparation.
3. Diagnose at objective + form granularity: "weak on membrane gradients in visual/data questions", not just "weak on cell biology".
4. Generate from parameterized archetype templates rather than from official wording. The 11 archetypes in `open_exam_analysis_claude.md` cover most of the priority table.
5. Calibrate hard questions against the 2014-2017 / 2020-2021 difficulty cluster. Treat 2003-2009 and 2023-2024 as the lower-bound reference.

## Manual Review Queue

`data/open_exam_unclassified_questions.csv` is the first audit file for taxonomy refinement. Workflow: hand-label a small sample, add the missing high-signal keywords, regenerate, check that precision does not drop.

Likely coverage gaps in the current keyword set:

- Bioinformatics and sequence analysis.
- Epigenetics beyond methylation/acetylation (chromatin remodeling, ncRNA-mediated silencing).
- RNAi, non-coding RNA, post-transcriptional regulation.
- Microbiome ecology and host-associated communities.
- 2019-2024 method vocabulary (lipid nanoparticle, NativePAGE, hyperactive transposon screens, Cre-Lox, ELISA-vs-PCR contrasts, antibiogram clearance-zone reading).

## Data Quality Notes

- Add a separate `2003_answer_key.json` for consistency.
- Verify missing 2013 answer-key entry Q33.
- Normalize 2015 Q2 from `AB` to `A+B` if plus-delimited multi-answer keys are the project convention.
- Preserve special answer keys such as `DISREGARDED`, `A OR B`, and `B OR E` as explicit metadata.
- Keep 2018's shared pre-question option block attached to Questions 1-2.
- 2019 has 47 questions, not 50; treat that as data, not corruption.

## Appendix: Knowledge Microtopic Count Table

| Subtopic | Pillar | Hits | Early | Middle | Late | Recent | Stage breadth | Year breadth | Years | Avg diff | Priority | Template archetype |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 122 | 36 | 34 | 22 | 30 | 4 | 22 | 2003-2024 | 2.26 | 105.9 | Gas exchange / renal transport / pressure-flow |
| Mendelian genetics and probability | Genetics/Evolution | 102 | 28 | 23 | 18 | 33 | 4 | 21 | 2003-2016, 2018-2024 | 2.53 | 105.2 | Cross setup / conditional probability |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 88 | 25 | 9 | 24 | 30 | 4 | 21 | 2003-2009, 2011-2024 | 2.39 | 104.1 | Pathogen / plasmid / genetic-exchange scenario |
| Population/community ecology and biodiversity | Ecology/Behavior | 86 | 22 | 20 | 17 | 27 | 4 | 22 | 2003-2024 | 2.43 | 104.1 | Population/community model inference |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 82 | 22 | 21 | 16 | 23 | 4 | 22 | 2003-2024 | 2.27 | 102.0 | Selection / isolation / adaptation scenario |
| Plant tissues, xylem/phloem and water transport | Plant | 69 | 18 | 11 | 15 | 25 | 4 | 22 | 2003-2024 | 2.27 | 101.4 | Xylem/phloem / source-sink transport |
| Plant reproduction, development and life cycles | Plant | 67 | 20 | 19 | 14 | 14 | 4 | 22 | 2003-2024 | 2.23 | 98.5 | ABC flower model / generations |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 64 | 12 | 22 | 16 | 14 | 4 | 18 | 2004, 2006, 2008-2021, 2023-2024 | 2.47 | 94.3 | Functional-group / reagent-identification variant |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 62 | 15 | 14 | 14 | 19 | 4 | 21 | 2003-2022, 2024 | 2.27 | 98.0 | Action potential / synapse / muscle mechanism |
| Endocrine feedback and homeostasis | Animal Physiology | 57 | 18 | 12 | 12 | 15 | 4 | 21 | 2003-2022, 2024 | 2.24 | 96.0 | Feedback-axis homeostasis variant |
| Immunology, inflammation and host defense | Animal Physiology | 56 | 9 | 7 | 13 | 27 | 4 | 18 | 2004-2010, 2012-2014, 2017-2024 | 2.41 | 95.8 | Immune-cell / antibody / pathogen-response variant |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 55 | 17 | 11 | 12 | 15 | 4 | 21 | 2004-2024 | 2.16 | 95.2 | Digestive enzyme / nutrient-deficiency pathway |
| Behavior, learning and ethology | Ecology/Behavior | 54 | 13 | 12 | 14 | 15 | 4 | 21 | 2003-2009, 2011-2024 | 2.14 | 95.5 | Behavioral experiment / fitness explanation |
| Development, reproduction and embryology | Animal Physiology | 54 | 9 | 12 | 17 | 16 | 4 | 20 | 2003-2005, 2007-2009, 2011-2024 | 2.39 | 96.8 | Embryology fate-map / morphogen variant |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 52 | 18 | 9 | 13 | 12 | 4 | 21 | 2003-2015, 2017-2024 | 2.17 | 94.5 | ETC / ATP-yield perturbation |
| Protein structure, amino acids and enzymes | Molecular/Cell | 51 | 9 | 20 | 9 | 13 | 4 | 20 | 2003-2004, 2006, 2008-2024 | 2.3 | 92.9 | Enzyme kinetics / protein chemistry |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 48 | 9 | 5 | 8 | 26 | 4 | 19 | 2004-2012, 2015-2024 | 2.76 | 97.8 | PCR / blot / gel / sequencing method choice |
| Transcription, translation and gene regulation | Molecular/Cell | 44 | 18 | 5 | 11 | 10 | 4 | 19 | 2003-2010, 2013-2022, 2024 | 2.39 | 91.0 | Operon / codon / regulatory perturbation |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 42 | 9 | 13 | 8 | 12 | 4 | 20 | 2003-2007, 2009-2017, 2019-2024 | 2.27 | 91.1 | Action spectrum / carbon-fixation variant |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 41 | 13 | 10 | 10 | 8 | 4 | 20 | 2003-2012, 2014-2022, 2024 | 2.19 | 89.7 | Cladogram / tree-topology interpretation |
| Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 39 | 11 | 9 | 6 | 13 | 4 | 18 | 2003, 2005-2008, 2010-2012, 2014, 2016-2024 | 2.39 | 88.2 | Nernst / osmosis / transporter gradient |
| Pedigrees and inheritance modes | Genetics/Evolution | 39 | 11 | 8 | 4 | 16 | 4 | 18 | 2003-2014, 2018, 2020-2024 | 2.53 | 89.6 | Pedigree inheritance-mode elimination |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 37 | 11 | 7 | 8 | 11 | 4 | 14 | 2005-2008, 2010-2011, 2013-2014, 2017-2021, 2024 | 2.37 | 81.8 | Organelle-localization / trafficking inference |
| DNA replication, chromosomes and telomeres | Molecular/Cell | 36 | 10 | 6 | 13 | 7 | 4 | 16 | 2003, 2005, 2007-2008, 2010-2011, 2013-2018, 2020-2023 | 2.28 | 84.5 | Replication fork / chromosome-end perturbation |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 34 | 13 | 6 | 5 | 10 | 4 | 21 | 2003-2011, 2013-2024 | 2.29 | 89.7 | Productivity / trophic / cycle calculation |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 32 | 7 | 2 | 11 | 12 | 4 | 15 | 2003, 2005-2007, 2011-2012, 2014-2017, 2019-2023 | 2.1 | 82.6 | Meiosis / checkpoint / cancer-control variant |
| Hardy-Weinberg and population genetics | Genetics/Evolution | 25 | 8 | 11 | 2 | 4 | 4 | 16 | 2003-2008, 2010-2014, 2016, 2021-2024 | 2.45 | 77.0 | Hardy-Weinberg allele-frequency calculation |
| Membrane structure, fluidity and permeability | Molecular/Cell | 22 | 7 | 9 | 2 | 4 | 4 | 16 | 2003-2012, 2017-2019, 2021-2022, 2024 | 2.16 | 74.0 | Membrane-composition permeability variant |
| Cell signaling, receptors and second messengers | Molecular/Cell | 21 | 3 | 5 | 5 | 8 | 4 | 11 | 2004-2005, 2010-2011, 2013, 2017-2019, 2022-2024 | 2.46 | 72.9 | Receptor / second-messenger cascade |
| Plant hormones, tropisms and environmental responses | Plant | 19 | 3 | 2 | 5 | 9 | 4 | 14 | 2004, 2006, 2008-2009, 2013-2016, 2018-2022, 2024 | 2.48 | 78.0 | Plant-hormone / tropism experiment |
| Linkage, recombination and map distance | Genetics/Evolution | 13 | 1 | 3 | 4 | 5 | 4 | 11 | 2004, 2010, 2012, 2014-2015, 2017-2022 | 2.56 | 69.2 | Linkage map / recombination-distance variant |
| Quantitative/polygenic traits and additive inheritance | Genetics/Evolution | 5 | 2 | 1 | 1 | 1 | 4 | 5 | 2005, 2008, 2010, 2018, 2022 | 2.83 | 47.8 | Polygenic additive-trait distribution |
