# Consolidated USABO Open Exam Subtopic Analysis, 2003-2018

Generated from local files in `raw/markdown` and the three existing reports in `raw/markdown/analysis` on 2026-05-05. No web search or remote model APIs were used.

## Purpose

This document consolidates the three prior analyses:

- `open_exam_analysis_chatgpt.md`: measured year-by-year structure, topic counts, format features, and answer-key issues.
- `open_exam_analysis_claude.md`: stable subtopics, mechanism-oriented solving, distractor taxonomy, and BioBloom generation parameters.
- `open_exam_analysis_gemini.md`: high-level exam evolution and student preparation narrative.

The new layer here is deeper subtopic prioritization. Unlike the previous version, broad skills such as data interpretation and experimental design are not treated as standalone knowledge topics. They are reasoning dimensions attached back to concrete biology subtopics.

## Saved Reproducibility Artifacts

- Generator code: `code/generate_consolidated_subtopic_analysis.py`
- Question-level tags: `data/open_exam_subtopic_question_tags.jsonl`
- Subtopic summary table: `data/open_exam_subtopic_summary.csv`
- Reasoning-by-topic table: `data/open_exam_reasoning_by_topic.csv`
- Consolidated machine-readable data: `data/open_exam_consolidated_subtopic_analysis_data.json`

## Method And Caveats

The analysis parsed 785 questions from 16 Markdown exams. The three stages are the same stages found across the prior reports:

- Early: 2003-2008
- Middle: 2009-2013
- Late: 2014-2018

This pass uses a multi-label knowledge microtopic taxonomy. A question can count for more than one knowledge subtopic, because many Open Exam items combine biology areas. The taxonomy generated 917 knowledge-subtopic hits across 669 tagged questions. Counts are useful for prioritization, but they are still heuristic and should be refined with manual labels later.

Reasoning skills are separate tags: negation, quantitative calculation, Roman/multi-statement logic, select-all format, data/figure/table reasoning, and experimental/control reasoning. The two broad methods/data categories are analyzed below by their associated knowledge topic.

## Consolidated Consensus From The Three Reports

All three analyses agree on the main exam story:

- The syllabus is stable, but the way the exam tests it changes substantially.
- Early `2003-2008` is more recall-heavy and one-step.
- Middle `2009-2013` adds more calculation, figures, and experimental framing.
- Late `2014-2018`, especially 2014-2017, adds longer stems, mechanism chains, multi-select formats, data interpretation, and experimental biology.
- The highest-return practice target is not memorizing exact old questions. It is mastering stable mechanism templates and learning to solve new variants.

## Generated Plots

- ![knowledge_subtopic_stage_heatmap](plots/knowledge_subtopic_stage_heatmap.svg)
- ![knowledge_subtopic_priority_scores](plots/knowledge_subtopic_priority_scores.svg)
- ![knowledge_subtopic_early_late_delta](plots/knowledge_subtopic_early_late_delta.svg)
- ![knowledge_pillar_stage_distribution](plots/knowledge_pillar_stage_distribution.svg)
- ![data_figure_reasoning_by_knowledge_topic](plots/data_figure_reasoning_by_knowledge_topic.svg)
- ![experimental_reasoning_by_knowledge_topic](plots/experimental_reasoning_by_knowledge_topic.svg)

## Knowledge Pillar Distribution By Stage

These are multi-label knowledge-topic hits, so totals exceed question count. Data/experiment is not a pillar here; it is analyzed as reasoning attached to these knowledge pillars.

| Pillar | Topic hits | Early | Middle | Late | Share of hits |
| --- | --- | --- | --- | --- | --- |
| Molecular/Cell | 260 | 89 | 84 | 87 | 28.4% |
| Animal Physiology | 233 | 83 | 77 | 73 | 25.4% |
| Genetics/Evolution | 170 | 70 | 57 | 43 | 18.5% |
| Ecology/Behavior | 102 | 40 | 34 | 28 | 11.1% |
| Plant | 85 | 34 | 26 | 25 | 9.3% |
| Microbiology/Pathogens | 49 | 20 | 7 | 22 | 5.3% |
| Molecular/Methods | 18 | 6 | 5 | 7 | 2.0% |

## Stable Knowledge Subtopics Across All Three Stages

These subtopics appear in early, middle, and late stages. They are the safest foundation for learning-objective prioritization.

| Subtopic | Pillar | Hits | Early | Middle | Late | Years tested | Avg difficulty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 80 | 30 | 31 | 19 | 16 | 2.0 |
| Mendelian genetics and probability | Genetics/Evolution | 63 | 26 | 18 | 19 | 14 | 2.18 |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 50 | 20 | 17 | 13 | 16 | 1.87 |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 49 | 20 | 7 | 22 | 15 | 1.95 |
| Population/community ecology and biodiversity | Ecology/Behavior | 47 | 19 | 17 | 11 | 14 | 2.05 |
| Plant tissues, xylem/phloem and water transport | Plant | 38 | 16 | 10 | 12 | 16 | 1.84 |
| Endocrine feedback and homeostasis | Animal Physiology | 38 | 15 | 12 | 11 | 15 | 2.03 |
| Plant reproduction, development and life cycles | Plant | 38 | 14 | 14 | 10 | 15 | 1.9 |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 36 | 14 | 9 | 13 | 15 | 2.03 |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 35 | 9 | 17 | 9 | 12 | 2.0 |
| Development, reproduction and embryology | Animal Physiology | 32 | 5 | 11 | 16 | 11 | 1.92 |
| Behavior, learning and ethology | Ecology/Behavior | 31 | 8 | 11 | 12 | 15 | 2.02 |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 31 | 14 | 9 | 8 | 15 | 1.72 |
| Transcription, translation and gene regulation | Molecular/Cell | 30 | 12 | 6 | 12 | 14 | 2.06 |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 28 | 9 | 11 | 8 | 14 | 1.98 |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 27 | 10 | 5 | 12 | 13 | 1.91 |
| Protein structure, amino acids and enzymes | Molecular/Cell | 27 | 7 | 15 | 5 | 12 | 2.06 |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 24 | 13 | 6 | 5 | 15 | 1.97 |
| Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 23 | 10 | 7 | 6 | 12 | 2.02 |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 23 | 10 | 7 | 6 | 9 | 1.94 |
| DNA replication, chromosomes and telomeres | Molecular/Cell | 20 | 7 | 4 | 9 | 12 | 2.02 |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 20 | 6 | 2 | 12 | 10 | 1.74 |
| Pedigrees and inheritance modes | Genetics/Evolution | 19 | 10 | 6 | 3 | 11 | 2.18 |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 18 | 6 | 5 | 7 | 12 | 2.17 |
| Membrane structure, fluidity and permeability | Molecular/Cell | 17 | 7 | 7 | 3 | 13 | 1.94 |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 17 | 6 | 5 | 6 | 11 | 1.9 |
| Immunology, inflammation and host defense | Animal Physiology | 16 | 5 | 5 | 6 | 11 | 1.84 |
| Hardy-Weinberg and population genetics | Genetics/Evolution | 16 | 6 | 9 | 1 | 10 | 1.98 |
| Cell signaling, receptors and second messengers | Molecular/Cell | 10 | 2 | 3 | 5 | 5 | 2.31 |

Key reading:

- Stable does not mean low difficulty. Stable subtopics become harder when embedded in experiments, figures, multi-statement choices, or negated stems.
- The strongest stable objectives have high hit count and high year breadth.
- Students should master these before spending heavy time on low-frequency details.

## Prioritized Learning Objectives

This is the main action table. It ranks knowledge subtopics by frequency, stage stability, year breadth, late-stage relevance, and cognitive load.

| Rank | Tier | Subtopic | Pillar | Hits | Priority | Early/Middle/Late | Years | Learning objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Tier 1 - stable core | Cardiovascular, respiratory and renal systems | Animal Physiology | 80 | 138.9 | 30/31/19 | 2003-2018 | Use gas exchange, blood flow, renal transport, pH/CO2, and pressure-volume logic to predict homeostasis. |
| 2 | Tier 1 - stable core | Mendelian genetics and probability | Genetics/Evolution | 63 | 119.0 | 26/18/19 | 2003-2012, 2014-2016, 2018 | Set up genotypes, gametes, dominance, recessiveness, and conditional probability before choosing an answer. |
| 3 | Tier 1 - stable core | Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 49 | 110.1 | 20/7/22 | 2003-2009, 2011-2018 | Compare viruses, bacteria, fungi, protists, plasmids, antibiotics, conjugation, and host-pathogen interactions. |
| 4 | Tier 1 - stable core | Evolution, selection, adaptation and speciation | Genetics/Evolution | 50 | 101.1 | 20/17/13 | 2003-2018 | Separate selection mode, adaptation, isolation, gene flow, speciation, and evolutionary evidence. |
| 5 | Tier 1 - stable core | Population/community ecology and biodiversity | Ecology/Behavior | 47 | 92.2 | 19/17/11 | 2003-2011, 2013-2016, 2018 | Use population models, community interactions, biodiversity metrics, and ecological reasoning. |
| 6 | Tier 1 - stable core | Plant tissues, xylem/phloem and water transport | Plant | 38 | 87.8 | 16/10/12 | 2003-2018 | Relate plant structure to xylem/phloem flow, source-sink logic, stomata, tissues, and water potential. |
| 7 | Tier 1 - stable core | Neurophysiology, muscle and sensory systems | Animal Physiology | 36 | 85.5 | 14/9/13 | 2003-2012, 2014-2018 | Predict nerve, sensory, muscle, synapse, and action-potential effects from mechanism. |
| 8 | Tier 1 - stable core | Endocrine feedback and homeostasis | Animal Physiology | 38 | 84.9 | 15/12/11 | 2004-2018 | Map endocrine axes, hormone source, target, feedback, and homeostatic response. |
| 9 | Tier 1 - stable core | Plant reproduction, development and life cycles | Plant | 38 | 83.5 | 14/14/10 | 2003-2016, 2018 | Track ploidy, generations, flowers, endosperm, seeds, fruits, sporophytes, and gametophytes. |
| 10 | Tier 1 - stable core | Behavior, learning and ethology | Ecology/Behavior | 31 | 79.2 | 8/11/12 | 2003-2009, 2011-2018 | Separate innate behavior, habituation, conditioning, imprinting, kin selection, and proximate/ultimate explanations. |
| 11 | Tier 1 - stable core | Development, reproduction and embryology | Animal Physiology | 32 | 78.5 | 5/11/16 | 2003-2004, 2007, 2009, 2011-2013, 2015-2018 | Connect fertilization, cleavage, germ layers, embryonic structures, developmental signals, and reproductive physiology. |
| 12 | Tier 1 - stable core | Transcription, translation and gene regulation | Molecular/Cell | 30 | 76.6 | 12/6/12 | 2003-2004, 2006-2011, 2013-2018 | Map DNA to RNA to protein, including promoters, operators, RNA processing, codons, ribosomes, and regulatory elements. |
| 13 | Tier 1 - stable core | Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 35 | 74.1 | 9/17/9 | 2004-2006, 2009-2014, 2016-2018 | Recognize biomolecule classes, carbohydrates/lipids/nucleotides, pH chemistry, and reagent-test evidence. |
| 14 | Tier 1 - stable core | Digestion, nutrition, vitamins and metabolism | Animal Physiology | 31 | 73.9 | 14/9/8 | 2004-2018 | Match organs, digestive enzymes, nutrient absorption, vitamins/minerals, and deficiency symptoms. |
| 15 | Tier 2 - modern differentiator | Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 27 | 71.7 | 10/5/12 | 2004-2011, 2013-2015, 2017-2018 | Trace electrons, proton gradients, ATP synthase, uncouplers, fermentation, and cellular energy yield. |
| 16 | Tier 3 - periodic high-yield | Photosynthesis, pigments and carbon fixation | Molecular/Cell | 28 | 69.2 | 9/11/8 | 2003-2007, 2009-2011, 2013-2018 | Explain pigments, light reactions, Calvin cycle, photosystems, C3/C4/CAM logic, and action spectra. |
| 17 | Tier 3 - periodic high-yield | Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 24 | 63.0 | 13/6/5 | 2003-2011, 2013-2018 | Trace energy, biomass, productivity, trophic efficiency, and elemental cycles. |
| 18 | Tier 3 - periodic high-yield | Protein structure, amino acids and enzymes | Molecular/Cell | 27 | 61.1 | 7/15/5 | 2003-2006, 2008-2013, 2016, 2018 | Connect amino-acid chemistry, folding, enzyme behavior, allostery, and protein function. |
| 19 | Tier 2 - modern differentiator | Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 20 | 59.6 | 6/2/12 | 2003, 2005-2007, 2011-2012, 2014-2017 | Predict effects of cell-cycle state, mitosis/meiosis errors, cyclins, oncogenes, tumor suppressors, and checkpoints. |
| 20 | Tier 2 - modern differentiator | DNA replication, chromosomes and telomeres | Molecular/Cell | 20 | 59.2 | 7/4/9 | 2003, 2005, 2007-2008, 2010-2011, 2013-2018 | Explain replication machinery, chromosome structure, origins, telomeres, and replication errors. |
| 21 | Tier 3 - periodic high-yield | Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 23 | 58.3 | 10/7/6 | 2003, 2005-2008, 2010-2012, 2014, 2016-2018 | Use gradients, channels, pumps, transporters, and membrane potentials to predict movement and physiological effect. |
| 22 | Tier 2 - modern differentiator | Lab methods, biotechnology and molecular tools | Molecular/Methods | 18 | 55.0 | 6/5/7 | 2004, 2006-2012, 2015-2018 | Know what PCR, blots, gels, sequencing, plasmid maps, microarrays, CRISPR, and probes can show. |
| 23 | Tier 3 - periodic high-yield | Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 23 | 53.1 | 10/7/6 | 2005-2007, 2010-2011, 2013-2014, 2017-2018 | Assign cell functions to organelles, cytoskeletal systems, vesicles, and intracellular compartments. |
| 24 | Tier 2 - modern differentiator | Phylogeny, cladograms and systematics | Genetics/Evolution | 17 | 50.5 | 6/5/6 | 2004-2007, 2009-2011, 2014-2016, 2018 | Read tree topology and distinguish common ancestry from superficial similarity or taxonomy rank. |
| 25 | Tier 3 - periodic high-yield | Membrane structure, fluidity and permeability | Molecular/Cell | 17 | 50.0 | 7/7/3 | 2003-2012, 2015-2016, 2018 | Predict permeability and membrane behavior from lipid composition, saturation, hydrophobicity, and bilayer structure. |
| 26 | Tier 2 - modern differentiator | Immunology, inflammation and host defense | Animal Physiology | 16 | 49.5 | 5/5/6 | 2004-2009, 2012-2014, 2017-2018 | Distinguish innate/adaptive immunity, antibody classes, inflammation, immune cells, and pathogen recognition. |
| 27 | Tier 3 - periodic high-yield | Pedigrees and inheritance modes | Genetics/Evolution | 19 | 49.1 | 10/6/3 | 2004-2011, 2013, 2016, 2018 | Eliminate autosomal/X-linked and dominant/recessive modes using pedigree constraints. |
| 28 | Tier 3 - periodic high-yield | Hardy-Weinberg and population genetics | Genetics/Evolution | 16 | 41.3 | 6/9/1 | 2003-2007, 2010-2013, 2016 | Use allele frequencies, carrier frequencies, and equilibrium assumptions to predict genotype proportions. |
| 29 | Tier 3 - periodic high-yield | Plant hormones, tropisms and environmental responses | Plant | 9 | 34.2 | 4/2/3 | 2004, 2006-2009, 2013, 2015, 2018 | Predict plant growth and germination from auxin, ethylene, gibberellin, ABA, phytochrome, and environmental cues. |
| 30 | Tier 2 - modern differentiator | Cell signaling, receptors and second messengers | Molecular/Cell | 10 | 32.9 | 2/3/5 | 2004, 2010-2011, 2017-2018 | Trace ligand-receptor binding through second messengers, kinases, and cellular response. |

### How To Use The Tiers

Tier 1 - stable core:
Master these first. They appear across all three stages and support many repeated templates.

Tier 2 - modern differentiator:
These matter especially for 2014-2018 style practice. They often separate students who know the content from students who can reason through modern stems.

Tier 3 - periodic high-yield:
These appear enough to matter, but not every year. Use them after the stable core or when targeting a student's weak area.

Tier 4 - selective / low-frequency:
Do not ignore them, but do not let them crowd out stable core objectives unless the student already has strong coverage.

## Data/Figure/Table Reasoning By Knowledge Topic

This replaces the overly broad `Data, graph, table & figure interpretation` subtopic. The skill is real, but it is most useful when attached to the biology content it tests.

| Knowledge subtopic | Pillar | Primary questions | Data/figure/table questions | Share |
| --- | --- | --- | --- | --- |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 14 | 8 | 57% |
| Population/community ecology and biodiversity | Ecology/Behavior | 29 | 8 | 28% |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 61 | 7 | 12% |
| Transcription, translation and gene regulation | Molecular/Cell | 21 | 6 | 29% |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 21 | 5 | 24% |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 39 | 5 | 13% |
| Plant reproduction, development and life cycles | Plant | 28 | 5 | 18% |
| Plant tissues, xylem/phloem and water transport | Plant | 37 | 5 | 14% |
| Behavior, learning and ethology | Ecology/Behavior | 26 | 4 | 15% |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 19 | 4 | 21% |
| Endocrine feedback and homeostasis | Animal Physiology | 29 | 4 | 14% |
| Mendelian genetics and probability | Genetics/Evolution | 42 | 4 | 10% |
| Pedigrees and inheritance modes | Genetics/Evolution | 13 | 4 | 31% |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 30 | 3 | 10% |
| Protein structure, amino acids and enzymes | Molecular/Cell | 24 | 3 | 12% |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 26 | 2 | 8% |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 36 | 2 | 6% |
| Immunology, inflammation and host defense | Animal Physiology | 13 | 2 | 15% |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 19 | 2 | 10% |
| Plant hormones, tropisms and environmental responses | Plant | 9 | 2 | 22% |

Interpretation:

- Visual and table-heavy questions are not a separate chapter. They cluster around physiology, genetics, plants, ecology, molecular methods, and development.
- Practice should tag both the knowledge objective and the representation skill, for example `cardiovascular/renal physiology + graph/table`, or `plant development + figure interpretation`.

## Experimental Design And Controls By Knowledge Topic

This replaces the overly broad `Experimental design, controls & inference` subtopic. Experimental design is a cross-cutting reasoning skill, but the exam usually anchors it in a concrete biological system.

| Knowledge subtopic | Pillar | Primary questions | Experimental/control questions | Share |
| --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 61 | 6 | 10% |
| Endocrine feedback and homeostasis | Animal Physiology | 29 | 6 | 21% |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 30 | 4 | 13% |
| Plant hormones, tropisms and environmental responses | Plant | 9 | 4 | 44% |
| Plant reproduction, development and life cycles | Plant | 28 | 4 | 14% |
| Population/community ecology and biodiversity | Ecology/Behavior | 29 | 4 | 14% |
| Transcription, translation and gene regulation | Molecular/Cell | 21 | 4 | 19% |
| Behavior, learning and ethology | Ecology/Behavior | 26 | 3 | 12% |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 36 | 3 | 8% |
| Mendelian genetics and probability | Genetics/Evolution | 42 | 3 | 7% |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 15 | 3 | 20% |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 19 | 3 | 16% |
| Development, reproduction and embryology | Animal Physiology | 21 | 2 | 10% |
| Protein structure, amino acids and enzymes | Molecular/Cell | 24 | 2 | 8% |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 15 | 1 | 7% |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 19 | 1 | 5% |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 26 | 1 | 4% |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 19 | 1 | 5% |
| Immunology, inflammation and host defense | Animal Physiology | 13 | 1 | 8% |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 11 | 1 | 9% |

Interpretation:

- Experimental reasoning is strongest in molecular/cell biology, microbiology/pathogens, development, physiology, plant mechanisms, and lab-method contexts.
- BioBloom should generate experimental questions by choosing a knowledge target first, then adding variables, controls, mutants, expected results, and distractors.

## Subtopics Rising In The Late Stage

These knowledge subtopics are more prominent in 2014-2018 than in 2003-2008.

| Subtopic | Pillar | Early | Middle | Late | Late-minus-early | Late share |
| --- | --- | --- | --- | --- | --- | --- |
| Development, reproduction and embryology | Animal Physiology | 5 | 11 | 16 | 11 | 50% |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 6 | 2 | 12 | 6 | 60% |
| Behavior, learning and ethology | Ecology/Behavior | 8 | 11 | 12 | 4 | 39% |
| Cell signaling, receptors and second messengers | Molecular/Cell | 2 | 3 | 5 | 3 | 50% |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 20 | 7 | 22 | 2 | 45% |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 10 | 5 | 12 | 2 | 44% |
| DNA replication, chromosomes and telomeres | Molecular/Cell | 7 | 4 | 9 | 2 | 45% |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 6 | 5 | 7 | 1 | 39% |
| Immunology, inflammation and host defense | Animal Physiology | 5 | 5 | 6 | 1 | 38% |
| Transcription, translation and gene regulation | Molecular/Cell | 12 | 6 | 12 | 0 | 40% |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 9 | 17 | 9 | 0 | 26% |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 6 | 5 | 6 | 0 | 35% |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 14 | 9 | 13 | -1 | 36% |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 9 | 11 | 8 | -1 | 29% |
| Protein structure, amino acids and enzymes | Molecular/Cell | 7 | 15 | 5 | -2 | 18% |
| Plant tissues, xylem/phloem and water transport | Plant | 16 | 10 | 12 | -4 | 32% |
| Endocrine feedback and homeostasis | Animal Physiology | 15 | 12 | 11 | -4 | 29% |
| Plant reproduction, development and life cycles | Plant | 14 | 14 | 10 | -4 | 26% |

Interpretation:

- Modern difficulty comes from combinations: molecular mechanisms plus experiments, genetics plus technology, physiology plus signaling, and plants plus molecular/developmental logic.
- Late-rising subtopics should anchor advanced practice sets and final-stage diagnostics.

## Early-Weighted Or Declining Subtopics

These knowledge subtopics appear more in early exams than late exams. They are useful for breadth, but they should not dominate a modern-practice plan.

| Subtopic | Pillar | Early | Middle | Late | Early-minus-late | Years |
| --- | --- | --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 30 | 31 | 19 | 11 | 2003-2018 |
| Population/community ecology and biodiversity | Ecology/Behavior | 19 | 17 | 11 | 8 | 2003-2011, 2013-2016, 2018 |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 13 | 6 | 5 | 8 | 2003-2011, 2013-2018 |
| Mendelian genetics and probability | Genetics/Evolution | 26 | 18 | 19 | 7 | 2003-2012, 2014-2016, 2018 |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 20 | 17 | 13 | 7 | 2003-2018 |
| Pedigrees and inheritance modes | Genetics/Evolution | 10 | 6 | 3 | 7 | 2004-2011, 2013, 2016, 2018 |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 14 | 9 | 8 | 6 | 2004-2018 |
| Hardy-Weinberg and population genetics | Genetics/Evolution | 6 | 9 | 1 | 5 | 2003-2007, 2010-2013, 2016 |
| Plant tissues, xylem/phloem and water transport | Plant | 16 | 10 | 12 | 4 | 2003-2018 |
| Endocrine feedback and homeostasis | Animal Physiology | 15 | 12 | 11 | 4 | 2004-2018 |
| Plant reproduction, development and life cycles | Plant | 14 | 14 | 10 | 4 | 2003-2016, 2018 |
| Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 10 | 7 | 6 | 4 | 2003, 2005-2008, 2010-2012, 2014, 2016-2018 |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 10 | 7 | 6 | 4 | 2005-2007, 2010-2011, 2013-2014, 2017-2018 |
| Membrane structure, fluidity and permeability | Molecular/Cell | 7 | 7 | 3 | 4 | 2003-2012, 2015-2016, 2018 |
| Protein structure, amino acids and enzymes | Molecular/Cell | 7 | 15 | 5 | 2 | 2003-2006, 2008-2013, 2016, 2018 |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 14 | 9 | 13 | 1 | 2003-2012, 2014-2018 |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 9 | 11 | 8 | 1 | 2003-2007, 2009-2011, 2013-2018 |
| Plant hormones, tropisms and environmental responses | Plant | 4 | 2 | 3 | 1 | 2004, 2006-2009, 2013, 2015, 2018 |

Interpretation:

- Early-weighted does not mean obsolete. It means later exams are less likely to test the topic as a direct recognition item.
- For modern practice, convert early-weighted topics into mechanism, data, or experiment variants rather than repeating simple recall.

## Stage-Only Subtopics

Late-only knowledge subtopics in this heuristic pass:

| Subtopic | Pillar | Late hits | Years | Avg difficulty |
| --- | --- | --- | --- | --- |
| - | - | - | - | - |

Early-only knowledge subtopics in this heuristic pass:

| Subtopic | Pillar | Early hits | Years | Avg difficulty |
| --- | --- | --- | --- | --- |
| - | - | - | - | - |

Caution: stage-only classification is sensitive to keyword rules and the available 2003-2018 window. Use this as a manual-review prompt, not as a reason to delete a topic.

## Format And Reasoning Tags By Stage

These are not knowledge subtopics, but they strongly affect difficulty and should become separate BioBloom metadata fields.

| Reasoning / format tag | Questions | Early | Middle | Late | Share of corpus |
| --- | --- | --- | --- | --- | --- |
| Negation trap | 214 | 61 | 67 | 86 | 27.3% |
| Calculation / quantitative | 121 | 43 | 43 | 35 | 15.4% |
| Data/figure/table reasoning | 100 | 25 | 29 | 46 | 12.7% |
| Experimental design/control reasoning | 64 | 25 | 11 | 28 | 8.2% |
| Multi-statement / Roman | 31 | 7 | 8 | 16 | 3.9% |
| Select-all / multi-answer | 31 | 0 | 10 | 21 | 3.9% |

Implications:

- Negation traps are common throughout and especially visible in late exams.
- Calculation and data reasoning must be trained across topics, not isolated into one chapter.
- Visual/table interpretation becomes a recurring execution skill. BioBloom should support image/table questions.

## What Is Truly Stable?

A stable USABO learning objective usually has four properties:

1. It appears in all three stages.
2. It appears in many separate years, not only as a cluster in one year.
3. It can be tested as recall, mechanism, calculation, or experiment.
4. It has reusable templates that can be rewritten without copying official wording.

Using those criteria, the most stable objectives are:

1. Transcription, translation, gene regulation, chromosomes, and cell cycle control.
2. Membrane structure, permeability, transport, osmosis, and electrochemical gradients.
3. Protein structure, enzyme behavior, biomolecules, and biochemical tests.
4. Mendelian probability, pedigrees, Hardy-Weinberg, recombination, and quantitative traits.
5. Cardiovascular, respiratory, renal, endocrine, immune, neural, and digestion physiology.
6. Plant tissues, transport, hormones, reproduction, development, photosynthesis, and life cycles.
7. Evolution, selection, phylogeny, systematics, ecology, ecosystems, and behavior.
8. Experimental design, lab methods, data interpretation, and figure/table reading as cross-cutting reasoning skills.

## How To Prioritize Student Study

1. Build the stable core first.
   Start with Tier 1 objectives. They recur across years and support many templates.

2. Add modern differentiators second.
   Add lab methods, molecular tools, signaling, experimental design, and multi-step physiology after the stable core is not shaky.

3. Train task forms explicitly.
   Drill negation, Roman numerals, select-all, data tables, figures, pedigrees, and calculations as separate skills.

4. Use stage-aware practice.
   Early questions build recall fluency. Middle questions build calculation and diagram skill. Late questions are best for final preparation because they combine reading load, mechanism, and experiment.

5. Review misses by objective and form.
   A miss should update both tags, such as `membrane gradients` plus `calculation`, or `plant development` plus `data table`.

## Recommended BioBloom Module Order

1. Molecular foundations: proteins, enzymes, membranes, organelles, biomolecules, bioenergetics.
2. Gene flow: DNA replication, transcription, translation, gene regulation, cell cycle, cancer.
3. Core genetics: Mendelian probability, pedigrees, linkage, Hardy-Weinberg, quantitative traits.
4. Physiology systems: endocrine, renal/respiratory/cardiovascular, immune, neural/muscle, digestion.
5. Plant systems: transport, hormones, photosynthesis, reproduction, life cycles, development.
6. Evolution and ecology: selection, speciation, phylogeny, population/community ecology, energy flow, behavior.
7. Experimental biology: PCR/blots/gels/sequencing/CRISPR, controls, mutants, tables, graphs, figures.
8. Exam execution: negation, Roman numerals, select-all, time triage, and distractor-family recognition.

## Concrete Practice-Set Design

For a 50-question modern-style practice set:

- 13-15 questions: molecular/cell and gene-expression mechanisms.
- 8-10 questions: physiology mechanisms across endocrine, neural, immune, renal/respiratory/cardiovascular.
- 7-9 questions: genetics, pedigrees, linkage, Hardy-Weinberg, quantitative inheritance.
- 5-7 questions: plant transport, hormones, reproduction/development, photosynthesis.
- 5-7 questions: ecology/evolution/behavior/systematics.
- 6-10 questions across the set should include figures, tables, or data.
- 5-8 questions should include negation or Roman-numeral/multi-statement logic.
- 3-6 questions should use modern lab or experimental-method reasoning.

The exact counts can vary, but every set should include both content coverage and task-form coverage. A text-only single-answer set will undertrain the modern exam.

## Project Recommendations

1. Add subtopic metadata to the question bank.
   Use `pillar`, `subtopics`, `reasoning_tags`, `stage`, `difficulty_estimate`, and `template_family` as first-class fields.

2. Preserve stage labels.
   Store `early`, `middle`, and `late` metadata so the app can generate era-faithful practice.

3. Build objective-level diagnostics.
   A student report should say `weak on membrane gradients in visual/data questions`, not just `weak on cell biology`.

4. Generate from templates, not from official wording.
   Stable subtopics should become parameterized BioBloom templates with new organisms, numbers, diagrams, and distractor roles.

5. Make late-stage practice the advanced default.
   For serious USABO preparation, calibrate hard questions against 2014-2017. Use earlier exams for foundations and fluency.

## Data Quality Notes To Resolve

The prior reports and this pass surface the same cleanup items:

- Add a separate `2003_answer_key.json` for consistency.
- Verify missing 2013 answer-key entry Q33.
- Normalize 2015 Q2 from `AB` to `A+B` if plus-delimited multi-answer keys are the project convention.
- Preserve special answer keys such as `DISREGARDED`, `A OR B`, and `B OR E` as explicit metadata.
- Keep 2018's shared pre-question option block attached to Questions 1-2.

## Appendix: Knowledge Microtopic Count Table

| Subtopic | Pillar | Hits | Early | Middle | Late | Stage breadth | Year breadth | Years | Avg diff | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cardiovascular, respiratory and renal systems | Animal Physiology | 80 | 30 | 31 | 19 | 3 | 16 | 2003-2018 | 2.0 | 138.9 |
| Mendelian genetics and probability | Genetics/Evolution | 63 | 26 | 18 | 19 | 3 | 14 | 2003-2012, 2014-2016, 2018 | 2.18 | 119.0 |
| Evolution, selection, adaptation and speciation | Genetics/Evolution | 50 | 20 | 17 | 13 | 3 | 16 | 2003-2018 | 1.87 | 101.1 |
| Microbiology, viruses, bacteria and pathogens | Microbiology/Pathogens | 49 | 20 | 7 | 22 | 3 | 15 | 2003-2009, 2011-2018 | 1.95 | 110.1 |
| Population/community ecology and biodiversity | Ecology/Behavior | 47 | 19 | 17 | 11 | 3 | 14 | 2003-2011, 2013-2016, 2018 | 2.05 | 92.2 |
| Endocrine feedback and homeostasis | Animal Physiology | 38 | 15 | 12 | 11 | 3 | 15 | 2004-2018 | 2.03 | 84.9 |
| Plant reproduction, development and life cycles | Plant | 38 | 14 | 14 | 10 | 3 | 15 | 2003-2016, 2018 | 1.9 | 83.5 |
| Plant tissues, xylem/phloem and water transport | Plant | 38 | 16 | 10 | 12 | 3 | 16 | 2003-2018 | 1.84 | 87.8 |
| Neurophysiology, muscle and sensory systems | Animal Physiology | 36 | 14 | 9 | 13 | 3 | 15 | 2003-2012, 2014-2018 | 2.03 | 85.5 |
| Biomolecules, macromolecules and biochemical tests | Molecular/Cell | 35 | 9 | 17 | 9 | 3 | 12 | 2004-2006, 2009-2014, 2016-2018 | 2.0 | 74.1 |
| Development, reproduction and embryology | Animal Physiology | 32 | 5 | 11 | 16 | 3 | 11 | 2003-2004, 2007, 2009, 2011-2013, 2015-2018 | 1.92 | 78.5 |
| Behavior, learning and ethology | Ecology/Behavior | 31 | 8 | 11 | 12 | 3 | 15 | 2003-2009, 2011-2018 | 2.02 | 79.2 |
| Digestion, nutrition, vitamins and metabolism | Animal Physiology | 31 | 14 | 9 | 8 | 3 | 15 | 2004-2018 | 1.72 | 73.9 |
| Transcription, translation and gene regulation | Molecular/Cell | 30 | 12 | 6 | 12 | 3 | 14 | 2003-2004, 2006-2011, 2013-2018 | 2.06 | 76.6 |
| Photosynthesis, pigments and carbon fixation | Molecular/Cell | 28 | 9 | 11 | 8 | 3 | 14 | 2003-2007, 2009-2011, 2013-2018 | 1.98 | 69.2 |
| Cellular respiration, ETC and ATP synthesis | Molecular/Cell | 27 | 10 | 5 | 12 | 3 | 13 | 2004-2011, 2013-2015, 2017-2018 | 1.91 | 71.7 |
| Protein structure, amino acids and enzymes | Molecular/Cell | 27 | 7 | 15 | 5 | 3 | 12 | 2003-2006, 2008-2013, 2016, 2018 | 2.06 | 61.1 |
| Ecosystems, productivity and biogeochemical cycles | Ecology/Behavior | 24 | 13 | 6 | 5 | 3 | 15 | 2003-2011, 2013-2018 | 1.97 | 63.0 |
| Membrane transport, osmosis and electrochemical gradients | Molecular/Cell | 23 | 10 | 7 | 6 | 3 | 12 | 2003, 2005-2008, 2010-2012, 2014, 2016-2018 | 2.02 | 58.3 |
| Organelles, cytoskeleton and intracellular trafficking | Molecular/Cell | 23 | 10 | 7 | 6 | 3 | 9 | 2005-2007, 2010-2011, 2013-2014, 2017-2018 | 1.94 | 53.1 |
| Cell cycle, meiosis and cancer checkpoints | Molecular/Cell | 20 | 6 | 2 | 12 | 3 | 10 | 2003, 2005-2007, 2011-2012, 2014-2017 | 1.74 | 59.6 |
| DNA replication, chromosomes and telomeres | Molecular/Cell | 20 | 7 | 4 | 9 | 3 | 12 | 2003, 2005, 2007-2008, 2010-2011, 2013-2018 | 2.02 | 59.2 |
| Pedigrees and inheritance modes | Genetics/Evolution | 19 | 10 | 6 | 3 | 3 | 11 | 2004-2011, 2013, 2016, 2018 | 2.18 | 49.1 |
| Lab methods, biotechnology and molecular tools | Molecular/Methods | 18 | 6 | 5 | 7 | 3 | 12 | 2004, 2006-2012, 2015-2018 | 2.17 | 55.0 |
| Membrane structure, fluidity and permeability | Molecular/Cell | 17 | 7 | 7 | 3 | 3 | 13 | 2003-2012, 2015-2016, 2018 | 1.94 | 50.0 |
| Phylogeny, cladograms and systematics | Genetics/Evolution | 17 | 6 | 5 | 6 | 3 | 11 | 2004-2007, 2009-2011, 2014-2016, 2018 | 1.9 | 50.5 |
| Hardy-Weinberg and population genetics | Genetics/Evolution | 16 | 6 | 9 | 1 | 3 | 10 | 2003-2007, 2010-2013, 2016 | 1.98 | 41.3 |
| Immunology, inflammation and host defense | Animal Physiology | 16 | 5 | 5 | 6 | 3 | 11 | 2004-2009, 2012-2014, 2017-2018 | 1.84 | 49.5 |
| Cell signaling, receptors and second messengers | Molecular/Cell | 10 | 2 | 3 | 5 | 3 | 5 | 2004, 2010-2011, 2017-2018 | 2.31 | 32.9 |
| Plant hormones, tropisms and environmental responses | Plant | 9 | 4 | 2 | 3 | 3 | 8 | 2004, 2006-2009, 2013, 2015, 2018 | 2.23 | 34.2 |
| Quantitative/polygenic traits and additive inheritance | Genetics/Evolution | 4 | 2 | 1 | 1 | 3 | 4 | 2005, 2008, 2010, 2018 | 2.73 | 21.3 |
| Linkage, recombination and map distance | Genetics/Evolution | 1 | 0 | 1 | 0 | 1 | 1 | 2013 | 2.2 | 2.1 |
