"""Generate consolidated USABO Open Exam subtopic analysis.

This script is intentionally self-contained and uses only the Python standard
library. It parses the cleaned Markdown exams in raw/markdown, assigns
heuristic knowledge subtopics and reasoning tags, exports data tables, renders
SVG plots, and writes the consolidated Markdown report.
"""

from __future__ import annotations

import csv
import html
import json
import math
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from statistics import mean


ANALYSIS_DIR = Path(__file__).resolve().parents[1]
MARKDOWN_ROOT = ANALYSIS_DIR.parent
DATA_DIR = ANALYSIS_DIR / "data"
PLOT_DIR = ANALYSIS_DIR / "plots"
DATA_DIR.mkdir(exist_ok=True)
PLOT_DIR.mkdir(exist_ok=True)

REPORT_PATH = ANALYSIS_DIR / "open_exam_consolidated_subtopic_analysis.md"
QUESTION_TAGS_JSONL = DATA_DIR / "open_exam_subtopic_question_tags.jsonl"
SUBTOPIC_SUMMARY_CSV = DATA_DIR / "open_exam_subtopic_summary.csv"
REASONING_TOPIC_CSV = DATA_DIR / "open_exam_reasoning_by_topic.csv"
UNCLASSIFIED_CSV = DATA_DIR / "open_exam_unclassified_questions.csv"
STAGE_SUMMARY_CSV = DATA_DIR / "open_exam_stage_summary.csv"
YEAR_PILLAR_CSV = DATA_DIR / "open_exam_year_pillar_counts.csv"
REASONING_COOCCURRENCE_CSV = DATA_DIR / "open_exam_reasoning_tag_cooccurrence.csv"
DATA_JSON = DATA_DIR / "open_exam_consolidated_subtopic_analysis_data.json"

Q_RE = re.compile(r"^### (\d+)\.\s*(.*)$", re.M)
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")

STAGES = [
    ("Early 2003-2008", range(2003, 2009)),
    ("Middle 2009-2013", range(2009, 2014)),
    ("Late 2014-2018", range(2014, 2019)),
    ("Recent 2019-2024", range(2019, 2025)),
]
STAGE_NAMES = [name for name, _ in STAGES]
STAGE_KEY = {
    "Early 2003-2008": "early",
    "Middle 2009-2013": "middle",
    "Late 2014-2018": "late",
    "Recent 2019-2024": "recent",
}
STAGE_SHORT = {
    "Early 2003-2008": "Early",
    "Middle 2009-2013": "Middle",
    "Late 2014-2018": "Late",
    "Recent 2019-2024": "Recent",
}
STAGE_KEY = {
    "Early 2003-2008": "early",
    "Middle 2009-2013": "middle",
    "Late 2014-2018": "late",
    "Recent 2019-2024": "recent",
}
STAGE_COLORS = {
    "Early 2003-2008": "#9ecae1",
    "Middle 2009-2013": "#74c476",
    "Late 2014-2018": "#fd8d3c",
    "Recent 2019-2024": "#6a51a3",
}


def kw(*items: tuple[str, int]) -> list[tuple[str, int]]:
    return list(items)


# Knowledge subtopics only. Data/figure reading and experimental design are
# handled as reasoning tags and then associated back to these biology subtopics.
MICROTOPICS = [
    (
        "Molecular/Cell",
        "DNA replication, chromosomes and telomeres",
        "Explain replication machinery, chromosome structure, origins, telomeres, and replication errors.",
        kw(
            ("dna replication", 7),
            ("replication", 4),
            ("origin of replication", 8),
            ("ori site", 8),
            ("helicase", 5),
            ("dna polymerase", 5),
            ("chromosome", 3),
            ("linear chromosome", 7),
            ("telomere", 7),
            ("telomerase", 7),
            ("thymine dimer", 7),
            ("5'", 2),
            ("3'", 2),
        ),
    ),
    (
        "Molecular/Cell",
        "Transcription, translation and gene regulation",
        "Map DNA to RNA to protein, including promoters, operators, RNA processing, codons, ribosomes, and regulatory elements.",
        kw(
            ("transcription", 6),
            ("translation", 6),
            ("promoter", 6),
            ("operator", 6),
            ("operon", 7),
            ("lac", 4),
            ("mrna", 5),
            ("trna", 5),
            ("rrna", 5),
            ("ribosome", 6),
            ("codon", 5),
            ("intron", 5),
            ("exon", 5),
            ("splicing", 6),
            ("gene expression", 7),
            ("histone", 6),
            ("methylation", 6),
            ("acetylation", 6),
            ("utr", 5),
            ("rna polymerase", 6),
            ("shine-dalgarno", 7),
        ),
    ),
    (
        "Molecular/Cell",
        "Protein structure, amino acids and enzymes",
        "Connect amino-acid chemistry, folding, enzyme behavior, allostery, and protein function.",
        kw(
            ("enzyme", 4),
            ("enzymatic", 4),
            ("amino acid", 6),
            ("protein structure", 7),
            ("protein folding", 7),
            ("tertiary structure", 7),
            ("quaternary", 6),
            ("active site", 6),
            ("allosteric", 6),
            ("activation energy", 6),
            ("km", 4),
            ("vmax", 4),
            ("michaelis", 7),
            ("lysine", 3),
            ("glycine", 3),
            ("cysteine", 3),
            ("histidine", 3),
            ("disulfide", 5),
            ("peptide", 3),
            ("denature", 5),
            ("oligonucleotide", 3),
            ("melting point", 3),
        ),
    ),
    (
        "Molecular/Cell",
        "Membrane structure, fluidity and permeability",
        "Predict permeability and membrane behavior from lipid composition, saturation, hydrophobicity, and bilayer structure.",
        kw(
            ("lipid bilayer", 7),
            ("membrane fluidity", 8),
            ("fluidity", 6),
            ("unsaturation", 6),
            ("saturation", 4),
            ("fatty acid", 5),
            ("phospholipid", 5),
            ("cholesterol", 5),
            ("hydrophobic", 5),
            ("transmembrane", 6),
            ("permeability", 5),
            ("lipid monolayer", 7),
            ("bilayer", 5),
        ),
    ),
    (
        "Molecular/Cell",
        "Membrane transport, osmosis and electrochemical gradients",
        "Use gradients, channels, pumps, transporters, and membrane potentials to predict movement and physiological effect.",
        kw(
            ("active transport", 7),
            ("passive diffusion", 7),
            ("diffusion", 4),
            ("osmosis", 6),
            ("aquaporin", 7),
            ("channel", 4),
            ("transporter", 5),
            ("pump", 4),
            ("symporter", 6),
            ("uniporter", 6),
            ("gradient", 4),
            ("electrochemical", 6),
            ("nernst", 8),
            ("membrane potential", 7),
            ("sodium", 3),
            ("potassium", 3),
            ("chloride", 3),
            ("calcium", 3),
            ("proton", 3),
            ("water potential", 7),
            ("carrier-mediated", 7),
        ),
    ),
    (
        "Molecular/Cell",
        "Cellular respiration, ETC and ATP synthesis",
        "Trace electrons, proton gradients, ATP synthase, uncouplers, fermentation, and cellular energy yield.",
        kw(
            ("glycolysis", 7),
            ("glycolytic", 7),
            ("krebs", 7),
            ("citric acid", 7),
            ("cellular respiration", 7),
            ("oxidative phosphorylation", 8),
            ("electron transport", 7),
            ("atp synthase", 8),
            ("atp", 4),
            ("nadh", 5),
            ("fadh", 5),
            ("mitochond", 6),
            ("cristae", 5),
            ("uncoupler", 8),
            ("oxygen consumption", 6),
            ("fermentation", 5),
            ("alcohol dehydrogenase", 6),
            ("free energy", 5),
            ("redox", 5),
            ("cytochrome", 6),
            ("complex iii", 6),
        ),
    ),
    (
        "Molecular/Cell",
        "Photosynthesis, pigments and carbon fixation",
        "Explain pigments, light reactions, Calvin cycle, photosystems, C3/C4/CAM logic, and action spectra.",
        kw(
            ("photosynthesis", 7),
            ("photosynthetic", 6),
            ("chlorophyll", 6),
            ("chloroplast", 6),
            ("thylakoid", 6),
            ("photosystem", 7),
            ("calvin", 7),
            ("rubisco", 7),
            ("light reaction", 6),
            ("action spectrum", 8),
            ("pigment", 5),
            ("c4", 6),
            ("cam", 6),
            ("photorespiration", 6),
            ("carbon fixation", 6),
            ("ferredoxin", 5),
            ("nadp", 5),
            ("p700", 5),
            ("p680", 5),
        ),
    ),
    (
        "Molecular/Cell",
        "Organelles, cytoskeleton and intracellular trafficking",
        "Assign cell functions to organelles, cytoskeletal systems, vesicles, and intracellular compartments.",
        kw(
            ("organelle", 6),
            ("lysosome", 6),
            ("golgi", 6),
            ("endoplasmic", 6),
            ("peroxisome", 6),
            ("glyoxysome", 6),
            ("vacuole", 5),
            ("cytoskeleton", 6),
            ("actin", 5),
            ("myosin", 4),
            ("microtubule", 6),
            ("tubulin", 5),
            ("intermediate filament", 6),
            ("cilia", 6),
            ("flagella", 5),
            ("centriole", 6),
            ("basal body", 6),
            ("vesicle", 5),
            ("endomembrane", 6),
            ("exocytosis", 5),
        ),
    ),
    (
        "Molecular/Cell",
        "Cell cycle, meiosis and cancer checkpoints",
        "Predict effects of cell-cycle state, mitosis/meiosis errors, cyclins, oncogenes, tumor suppressors, and checkpoints.",
        kw(
            ("cell cycle", 8),
            ("mitosis", 6),
            ("meiosis", 6),
            ("meiosis ii", 7),
            ("cyclin", 7),
            ("checkpoint", 6),
            ("cancer", 6),
            ("tumor", 6),
            ("oncogene", 7),
            ("proto-oncogene", 7),
            ("tumor suppressor", 7),
            ("apoptosis", 6),
            ("g0", 6),
            ("g1", 5),
            ("g2", 5),
            ("s phase", 5),
            ("nondisjunction", 6),
            ("trisomy", 6),
            ("separation of parental homologs", 8),
            ("differentiated cells", 6),
        ),
    ),
    (
        "Molecular/Cell",
        "Cell signaling, receptors and second messengers",
        "Trace ligand-receptor binding through second messengers, kinases, and cellular response.",
        kw(
            ("receptor", 6),
            ("ligand", 6),
            ("second messenger", 8),
            ("g protein", 8),
            ("kinase", 5),
            ("phosphorylation", 5),
            ("signal transduction", 8),
            ("cascade", 5),
            ("camp", 6),
            ("ip3", 6),
            ("calmodulin", 6),
            ("neurotransmitter released", 6),
            ("toll-like", 6),
            ("tlr", 6),
            ("cytokine", 5),
            ("receptor tyrosine", 7),
            ("protein ligand", 6),
        ),
    ),
    (
        "Molecular/Cell",
        "Biomolecules, macromolecules and biochemical tests",
        "Recognize biomolecule classes, carbohydrates/lipids/nucleotides, pH chemistry, and reagent-test evidence.",
        kw(
            ("carbohydrate", 6),
            ("lipid", 6),
            ("nucleotide", 5),
            ("amino acids and nucleotides", 7),
            ("biuret", 7),
            ("benedict", 7),
            ("ninhydrin", 7),
            ("iodine", 5),
            ("sudan", 6),
            ("tollens", 6),
            ("reagent", 5),
            ("vitamin", 5),
            ("mineral", 5),
            ("ph", 4),
            ("pka", 6),
            ("hydrogen ions", 5),
            ("molar", 5),
            ("molecular weight", 5),
            ("concentration", 4),
            ("half-life", 5),
            ("half life", 5),
            ("rate constant", 5),
            ("alpha-1", 5),
        ),
    ),
    (
        "Genetics/Evolution",
        "Mendelian genetics and probability",
        "Set up genotypes, gametes, dominance, recessiveness, and conditional probability before choosing an answer.",
        kw(
            ("genotype", 6),
            ("phenotype", 5),
            ("offspring", 5),
            ("probability", 5),
            ("homozygous", 6),
            ("heterozygous", 6),
            ("dominant", 5),
            ("recessive", 5),
            ("allele", 5),
            ("segregation", 5),
            ("independent assortment", 8),
            ("blood type", 6),
            ("test cross", 6),
            ("dihybrid", 6),
            ("monohybrid", 6),
            ("f1", 3),
            ("f2", 3),
            ("crossed", 3),
            ("progeny", 4),
            ("mendel", 5),
        ),
    ),
    (
        "Genetics/Evolution",
        "Pedigrees and inheritance modes",
        "Eliminate autosomal/X-linked and dominant/recessive modes using pedigree constraints.",
        kw(
            ("pedigree", 9),
            ("mode of inheritance", 9),
            ("x-linked", 8),
            ("autosomal", 7),
            ("carrier", 6),
            ("affected child", 6),
            ("color-blind", 6),
            ("sex-linked", 7),
            ("complete penetrance", 7),
            ("genetic counselor", 6),
            ("inherited disease", 6),
            ("recessive disease", 6),
            ("unaffected parents", 6),
        ),
    ),
    (
        "Genetics/Evolution",
        "Linkage, recombination and map distance",
        "Identify parental/recombinant classes, map order, double crossovers, and recombination distance.",
        kw(
            ("genetic linkage", 8),
            ("partial linkage", 8),
            ("no linkage between", 8),
            ("linked genes", 8),
            ("linked loci", 8),
            ("recombination", 8),
            ("recombination frequency", 9),
            ("recombinant", 7),
            ("map distance", 9),
            ("centimorgan", 8),
            ("crossover", 7),
            ("low crossover", 8),
            ("double-crossover", 9),
            ("double recombinant", 9),
            ("gene order", 8),
            ("map unit", 8),
            ("chromosomal map", 9),
            ("trihybrid cross", 8),
            ("three-point", 8),
        ),
    ),
    (
        "Genetics/Evolution",
        "Hardy-Weinberg and population genetics",
        "Use allele frequencies, carrier frequencies, and equilibrium assumptions to predict genotype proportions.",
        kw(
            ("hardy", 9),
            ("weinberg", 9),
            ("allele frequency", 8),
            ("carrier frequency", 8),
            ("population genetics", 7),
            ("genetic drift", 6),
            ("founder effect", 6),
            ("bottleneck", 6),
            ("gene pool", 6),
            ("equilibrium", 4),
            ("p2", 5),
            ("2pq", 6),
            ("q2", 6),
        ),
    ),
    (
        "Genetics/Evolution",
        "Quantitative/polygenic traits and additive inheritance",
        "Infer locus number, additive effects, and phenotype frequencies from trait distributions.",
        kw(
            ("polygenic", 8),
            ("quantitative inheritance", 8),
            ("additive", 6),
            ("mean height", 8),
            ("each allele contributes", 8),
            ("trait extremes", 7),
            ("f2 plants", 6),
            ("continuous variation", 6),
            ("many genes", 5),
            ("teosinte", 5),
        ),
    ),
    (
        "Genetics/Evolution",
        "Evolution, selection, adaptation and speciation",
        "Separate selection mode, adaptation, isolation, gene flow, speciation, and evolutionary evidence.",
        kw(
            ("evolution", 6),
            ("selection", 6),
            ("natural selection", 7),
            ("sexual selection", 6),
            ("speciation", 7),
            ("sympatric", 7),
            ("allopatric", 7),
            ("fitness", 6),
            ("adaptation", 6),
            ("convergent", 6),
            ("divergent", 5),
            ("homologous", 5),
            ("analogous", 5),
            ("reproductive isolation", 6),
            ("gene flow", 6),
            ("molecular clock", 6),
            ("dn/ds", 7),
            ("adaptive", 5),
            ("fossil", 5),
        ),
    ),
    (
        "Genetics/Evolution",
        "Phylogeny, cladograms and systematics",
        "Read tree topology and distinguish common ancestry from superficial similarity or taxonomy rank.",
        kw(
            ("cladogram", 9),
            ("phylogeny", 8),
            ("phylogenetic", 8),
            ("taxonomic", 7),
            ("taxonomy", 6),
            ("clade", 6),
            ("monophyletic", 7),
            ("paraphyletic", 7),
            ("systematics", 6),
            ("domain", 5),
            ("archaea", 5),
            ("eukarya", 5),
            ("protist", 5),
            ("chordate", 5),
            ("vertebrate", 5),
            ("arthropod", 5),
            ("protostome", 6),
            ("deuterostome", 6),
            ("lichen", 5),
            ("segmented body", 5),
        ),
    ),
    (
        "Plant",
        "Plant tissues, xylem/phloem and water transport",
        "Relate plant structure to xylem/phloem flow, source-sink logic, stomata, tissues, and water potential.",
        kw(
            ("xylem", 8),
            ("phloem", 8),
            ("stomata", 6),
            ("guard cell", 6),
            ("leaf", 4),
            ("root", 4),
            ("vascular cambium", 7),
            ("periderm", 6),
            ("wood", 5),
            ("endodermis", 6),
            ("parenchyma", 6),
            ("sclerenchyma", 6),
            ("collenchyma", 6),
            ("water potential", 8),
            ("transpiration", 6),
            ("source", 3),
            ("sink", 3),
            ("phloem unloading", 8),
            ("plant cell", 3),
            ("apical meristem", 6),
        ),
    ),
    (
        "Plant",
        "Plant hormones, tropisms and environmental responses",
        "Predict plant growth and germination from auxin, ethylene, gibberellin, ABA, phytochrome, and environmental cues.",
        kw(
            ("auxin", 8),
            ("gibberellin", 8),
            ("ethylene", 8),
            ("abscisic", 8),
            ("aba", 7),
            ("cytokinin", 8),
            ("phototropism", 8),
            ("gravitropism", 8),
            ("tropism", 6),
            ("phytochrome", 8),
            ("red light", 5),
            ("far red", 6),
            ("vernalization", 6),
            ("dormancy", 5),
            ("germination", 5),
            ("plant hormone", 8),
            ("elongation", 4),
            ("apical dominance", 6),
        ),
    ),
    (
        "Plant",
        "Plant reproduction, development and life cycles",
        "Track ploidy, generations, flowers, endosperm, seeds, fruits, sporophytes, and gametophytes.",
        kw(
            ("flower", 6),
            ("sepal", 8),
            ("petal", 8),
            ("stamen", 8),
            ("carpel", 8),
            ("abc model", 9),
            ("flower development", 8),
            ("endosperm", 8),
            ("sporophyte", 8),
            ("gametophyte", 8),
            ("alternation of generations", 9),
            ("pollen", 6),
            ("ovule", 6),
            ("seed", 5),
            ("fruit", 5),
            ("monosporic", 8),
            ("fern", 5),
            ("moss", 5),
            ("angiosperm", 6),
            ("gymnosperm", 6),
            ("sporopollenin", 7),
            ("double fertilization", 7),
            ("embryo sac", 7),
        ),
    ),
    (
        "Animal Physiology",
        "Neurophysiology, muscle and sensory systems",
        "Predict nerve, sensory, muscle, synapse, and action-potential effects from mechanism.",
        kw(
            ("neuron", 7),
            ("nervous", 6),
            ("brain", 5),
            ("axon", 7),
            ("myelin", 7),
            ("synapse", 7),
            ("neurotransmitter", 7),
            ("action potential", 9),
            ("membrane potential", 7),
            ("muscle", 6),
            ("sarcomere", 6),
            ("neuromuscular", 8),
            ("nerve gas", 7),
            ("atropine", 7),
            ("sensory", 6),
            ("photoreceptor", 6),
            ("retina", 6),
            ("spinal", 6),
            ("pons", 5),
            ("medulla", 5),
            ("rods and cones", 7),
            ("supination", 5),
            ("autonomic", 6),
            ("reflex", 6),
        ),
    ),
    (
        "Animal Physiology",
        "Endocrine feedback and homeostasis",
        "Map endocrine axes, hormone source, target, feedback, and homeostatic response.",
        kw(
            ("hormone", 7),
            ("endocrine", 8),
            ("insulin", 8),
            ("glucagon", 8),
            ("pituitary", 8),
            ("thyroid", 6),
            ("adrenal", 7),
            ("cortisol", 7),
            ("acth", 8),
            ("crf", 8),
            ("prolactin", 6),
            ("estrogen", 6),
            ("progesterone", 6),
            ("feedback", 6),
            ("homeostasis", 6),
            ("blood glucose", 7),
            ("aldosterone", 6),
            ("adh", 6),
            ("vasopressin", 6),
            ("corpus luteum", 6),
        ),
    ),
    (
        "Animal Physiology",
        "Cardiovascular, respiratory and renal systems",
        "Use gas exchange, blood flow, renal transport, pH/CO2, and pressure-volume logic to predict homeostasis.",
        kw(
            ("heart", 6),
            ("blood", 5),
            ("hemoglobin", 8),
            ("oxygen", 4),
            ("co2", 5),
            ("ventilation", 8),
            ("respiratory", 6),
            ("lung", 6),
            ("kidney", 8),
            ("renal", 8),
            ("nephron", 8),
            ("urine", 6),
            ("loop of henle", 8),
            ("blood pressure", 7),
            ("artery", 5),
            ("capillary", 6),
            ("arterial", 5),
            ("acidosis", 7),
            ("osmoregulation", 7),
            ("erythrocyte", 6),
            ("gills", 5),
            ("fick", 6),
            ("mitral", 6),
            ("thrombi", 5),
        ),
    ),
    (
        "Animal Physiology",
        "Immunology, inflammation and host defense",
        "Distinguish innate/adaptive immunity, antibody classes, inflammation, immune cells, and pathogen recognition.",
        kw(
            ("immune", 8),
            ("immunity", 8),
            ("antibody", 8),
            ("antigen", 7),
            ("immunoglobulin", 8),
            ("iga", 6),
            ("igd", 6),
            ("ige", 6),
            ("igg", 6),
            ("igm", 6),
            ("allergic", 6),
            ("lymphocyte", 6),
            ("b cell", 6),
            ("t cell", 6),
            ("macrophage", 6),
            ("inflammation", 6),
            ("eosinophil", 7),
            ("pathogen", 6),
            ("vaccine", 6),
            ("tlr", 7),
            ("toll", 6),
            ("phagocytosis", 6),
            ("phagocyte", 6),
            ("chronic granulomatous", 8),
        ),
    ),
    (
        "Animal Physiology",
        "Digestion, nutrition, vitamins and metabolism",
        "Match organs, digestive enzymes, nutrient absorption, vitamins/minerals, and deficiency symptoms.",
        kw(
            ("digestion", 8),
            ("digestive", 8),
            ("intestine", 6),
            ("intestinal", 6),
            ("pancreas", 6),
            ("liver", 5),
            ("bile", 6),
            ("amylase", 6),
            ("pepsin", 6),
            ("chymotrypsin", 6),
            ("carboxypeptidase", 6),
            ("aminopeptidase", 6),
            ("nutrient", 5),
            ("vitamin", 6),
            ("mineral", 5),
            ("beriberi", 8),
            ("scurvy", 6),
            ("fat", 4),
            ("lymphatic", 6),
            ("glucose transporters", 6),
            ("pernicious anemia", 8),
        ),
    ),
    (
        "Animal Physiology",
        "Development, reproduction and embryology",
        "Connect fertilization, cleavage, germ layers, embryonic structures, developmental signals, and reproductive physiology.",
        kw(
            ("embryo", 6),
            ("embryonic", 6),
            ("development", 5),
            ("gestation", 6),
            ("fertilization", 6),
            ("reproduction", 6),
            ("placenta", 6),
            ("ovary", 5),
            ("testes", 5),
            ("neural crest", 8),
            ("extraembryonic", 8),
            ("chorion", 6),
            ("amnion", 6),
            ("allantois", 6),
            ("yolk sac", 6),
            ("maternal", 5),
            ("fetus", 5),
            ("bicoid", 8),
            ("morphogen", 8),
            ("germ layers", 8),
            ("cleavage", 7),
            ("holoblastic", 8),
            ("meroblastic", 8),
            ("cortical rotation", 8),
            ("blastopore", 6),
        ),
    ),
    (
        "Ecology/Behavior",
        "Population/community ecology and biodiversity",
        "Use population models, community interactions, biodiversity metrics, and ecological reasoning.",
        kw(
            ("population", 6),
            ("community", 6),
            ("biodiversity", 8),
            ("species richness", 8),
            ("evenness", 6),
            ("simpson", 8),
            ("shannon", 8),
            ("niche", 6),
            ("competition", 5),
            ("predation", 5),
            ("density", 5),
            ("logistic", 7),
            ("exponential", 6),
            ("r-selected", 8),
            ("k-selected", 8),
            ("carrying capacity", 8),
            ("keystone", 6),
            ("marine community", 6),
        ),
    ),
    (
        "Ecology/Behavior",
        "Ecosystems, productivity and biogeochemical cycles",
        "Trace energy, biomass, productivity, trophic efficiency, and elemental cycles.",
        kw(
            ("ecosystem", 7),
            ("energy flow", 8),
            ("productivity", 8),
            ("primary productivity", 8),
            ("net primary productivity", 9),
            ("trophic", 8),
            ("biomass", 7),
            ("food chain", 6),
            ("food web", 6),
            ("carbon cycle", 8),
            ("nitrogen cycle", 8),
            ("phosphorus", 6),
            ("biogeochemical", 8),
            ("decomposition", 5),
            ("recycle", 5),
            ("energy transfer", 8),
            ("biomass pyramid", 8),
            ("average net primary", 8),
        ),
    ),
    (
        "Ecology/Behavior",
        "Behavior, learning and ethology",
        "Separate innate behavior, habituation, conditioning, imprinting, kin selection, and proximate/ultimate explanations.",
        kw(
            ("behavior", 7),
            ("habituation", 8),
            ("imprinting", 8),
            ("learning", 7),
            ("associative learning", 8),
            ("conditioning", 7),
            ("fixed action pattern", 8),
            ("sign stimulus", 8),
            ("kin selection", 8),
            ("inclusive fitness", 8),
            ("territorial", 6),
            ("courtship", 6),
            ("sexual selection", 6),
            ("pheromone", 6),
            ("migration", 5),
            ("aggression", 5),
            ("schooling", 6),
            ("mate", 5),
            ("coefficient of relatedness", 8),
        ),
    ),
    (
        "Microbiology/Pathogens",
        "Microbiology, viruses, bacteria and pathogens",
        "Compare viruses, bacteria, fungi, protists, plasmids, antibiotics, conjugation, and host-pathogen interactions.",
        kw(
            ("virus", 8),
            ("viral", 8),
            ("hiv", 8),
            ("bacteriophage", 8),
            ("phage", 7),
            ("bacteria", 7),
            ("bacterial", 7),
            ("e. coli", 8),
            ("escherichia", 8),
            ("salmonella", 8),
            ("staphylococcus", 8),
            ("vibrio", 8),
            ("schistosoma", 8),
            ("fungi", 6),
            ("cyanobacteria", 6),
            ("prokaryote", 6),
            ("archaea", 5),
            ("pathogen", 6),
            ("plasmid", 6),
            ("conjugation", 7),
            ("endospore", 6),
            ("antibiotic", 6),
            ("tetracycline", 7),
            ("zika", 7),
        ),
    ),
    (
        "Molecular/Methods",
        "Lab methods, biotechnology and molecular tools",
        "Know what PCR, blots, gels, sequencing, plasmid maps, microarrays, CRISPR, and probes can show.",
        kw(
            ("pcr", 9),
            ("primer", 9),
            ("gel", 7),
            ("western blot", 9),
            ("southern blot", 9),
            ("northern blot", 9),
            ("elisa", 9),
            ("sequencing", 9),
            ("sanger", 9),
            ("ngs", 9),
            ("crispr", 9),
            ("cas9", 9),
            ("restriction", 7),
            ("plasmid map", 9),
            ("microarray", 9),
            ("clone", 6),
            ("vector", 6),
            ("electrophoresis", 7),
            ("probe", 6),
            ("recombinant", 6),
            ("transgenic", 6),
            ("transformation", 6),
            ("knockout", 7),
            ("patch clamp", 9),
            ("degenerate primer", 9),
            ("nativepage", 9),
            ("native page", 9),
            ("ion-exchange chromatography", 9),
            ("cre-lox", 9),
            ("rnai", 8),
            ("rna interference", 9),
            ("lipid nanoparticle", 9),
            ("mass spectrometry", 8),
            ("protospacer", 9),
            ("pam sequence", 9),
            ("seroprevalence", 8),
            ("immunoprecipitation", 8),
            ("knock-down", 8),
            ("knockdown", 8),
            ("gram stain", 8),
            ("antibiogram", 9),
            ("clearance zone", 9),
        ),
    ),
]

TEMPLATE_ARCHETYPES = {
    "DNA replication, chromosomes and telomeres": "Replication fork / chromosome-end perturbation",
    "Transcription, translation and gene regulation": "Operon / codon / regulatory perturbation",
    "Protein structure, amino acids and enzymes": "Enzyme kinetics / protein chemistry",
    "Membrane structure, fluidity and permeability": "Membrane-composition permeability variant",
    "Membrane transport, osmosis and electrochemical gradients": "Nernst / osmosis / transporter gradient",
    "Cellular respiration, ETC and ATP synthesis": "ETC / ATP-yield perturbation",
    "Photosynthesis, pigments and carbon fixation": "Action spectrum / carbon-fixation variant",
    "Organelles, cytoskeleton and intracellular trafficking": "Organelle-localization / trafficking inference",
    "Cell cycle, meiosis and cancer checkpoints": "Meiosis / checkpoint / cancer-control variant",
    "Cell signaling, receptors and second messengers": "Receptor / second-messenger cascade",
    "Biomolecules, macromolecules and biochemical tests": "Functional-group / reagent-identification variant",
    "Mendelian genetics and probability": "Cross setup / conditional probability",
    "Pedigrees and inheritance modes": "Pedigree inheritance-mode elimination",
    "Linkage, recombination and map distance": "Linkage map / recombination-distance variant",
    "Hardy-Weinberg and population genetics": "Hardy-Weinberg allele-frequency calculation",
    "Quantitative/polygenic traits and additive inheritance": "Polygenic additive-trait distribution",
    "Evolution, selection, adaptation and speciation": "Selection / isolation / adaptation scenario",
    "Phylogeny, cladograms and systematics": "Cladogram / tree-topology interpretation",
    "Plant tissues, xylem/phloem and water transport": "Xylem/phloem / source-sink transport",
    "Plant hormones, tropisms and environmental responses": "Plant-hormone / tropism experiment",
    "Plant reproduction, development and life cycles": "ABC flower model / generations",
    "Neurophysiology, muscle and sensory systems": "Action potential / synapse / muscle mechanism",
    "Endocrine feedback and homeostasis": "Feedback-axis homeostasis variant",
    "Cardiovascular, respiratory and renal systems": "Gas exchange / renal transport / pressure-flow",
    "Immunology, inflammation and host defense": "Immune-cell / antibody / pathogen-response variant",
    "Digestion, nutrition, vitamins and metabolism": "Digestive enzyme / nutrient-deficiency pathway",
    "Development, reproduction and embryology": "Embryology fate-map / morphogen variant",
    "Population/community ecology and biodiversity": "Population/community model inference",
    "Ecosystems, productivity and biogeochemical cycles": "Productivity / trophic / cycle calculation",
    "Behavior, learning and ethology": "Behavioral experiment / fitness explanation",
    "Microbiology, viruses, bacteria and pathogens": "Pathogen / plasmid / genetic-exchange scenario",
    "Lab methods, biotechnology and molecular tools": "PCR / blot / gel / sequencing method choice",
}

REASONING_TAGS = {
    "Negation trap": [
        r"\bnot\b",
        r"\bfalse\b",
        r"\bexcept\b",
        r"\bleast\b",
        r"\bincorrect\b",
    ],
    "Calculation / quantitative": [
        r"\bprobability\b",
        r"\bratio\b",
        r"\bcalculate\b",
        r"\bpercentage\b",
        r"\bfraction\b",
        r"\bpka\b",
        r"\bph\b",
        r"\bconcentration\b",
        r"\brate\b",
        r"\bhalf[- ]life\b",
        r"\bmolar\b",
    ],
    # Roman numerals only count when at least two markers appear in the same block,
    # so single occurrences of "i.e." don't trigger this tag.
    "Multi-statement / Roman": [],
    "Select-all / multi-answer": [
        r"select all",
        r"all that apply",
        r"select the correct response\(s\)",
        r"multiple true-false",
    ],
    "Data/figure/table reasoning": [
        r"!\[",
        r"^\|",
        r"\bgraph\b",
        r"\btable\b",
        r"\bdata\b",
        r"\bfigure\b",
        r"\bshown below\b",
        r"\bimage below\b",
        r"\bdiagram\b",
        r"\bcurve\b",
        r"\baxis\b",
        r"\bspectrophotometer\b",
        r"\babsorbance\b",
    ],
    "Experimental design/control reasoning": [
        r"\bexperiment\b",
        r"\bresearcher\b",
        r"\bcontrol\b",
        r"\bplacebo\b",
        r"\bhypothesis\b",
        r"\bassay\b",
        r"\bmutant\b",
        r"\bwild[- ]type\b",
        r"\bconsistent with\b",
        r"\bnot consistent\b",
        r"\bvariable\b",
        r"\bconclusion\b",
        r"\btest whether\b",
        r"\bwhat evidence\b",
        r"\bsupport the hypothesis\b",
        r"\btreatment\b",
    ],
}

REASONING_TAG_ORDER = list(REASONING_TAGS)
ROMAN_LIST_MARKER_RE = re.compile(r"(?im)^\s*(i{1,3}|iv|v)\.\s+\S")


def stage_for_year(year: int) -> str:
    for name, years in STAGES:
        if year in years:
            return name
    raise ValueError(f"Year outside configured stages: {year}")


def question_region(text: str) -> str:
    cuts = [len(text)]
    for marker in ["\n# Explanations", "\n# Answer Key"]:
        if marker in text:
            cuts.append(text.index(marker))
    return text[: min(cuts)]


def split_questions(text: str) -> list[tuple[int, str]]:
    text = question_region(text)
    matches = list(Q_RE.finditer(text))
    questions: list[tuple[int, str]] = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = (match.group(2) + "\n" + text[start:end]).strip()
        questions.append((int(match.group(1)), block))
    return questions


BIOLOGY_SUFFIX_RE = (
    r"(?:s|es|ed|ing|er|ers|or|ors|ic|ical|ate|ated|ates|ation|ations|"
    r"ial|ially|ous|ously|ity|ities|ly|al|ally|able|ible|ar|ary|ant|ants|"
    r"ent|ents|ase|ases|on|ons|um|ums|a|ae|i|us|ria|rial|osis|otic|"
    r"some|somes|ome|omes)?"
)


def keyword_body_pattern(phrase: str) -> str:
    escaped = re.escape(phrase.strip().lower())
    return re.sub(r"(?:\\ |\\-)+", lambda _match: r"[\s\-]+", escaped)


def allows_inflection(phrase: str) -> bool:
    if "'" in phrase or any(ch.isdigit() for ch in phrase):
        return False
    tokens = re.findall(r"[a-z]+", phrase.lower())
    return bool(tokens) and len(tokens[-1]) >= 4


@lru_cache(maxsize=None)
def keyword_regex(phrase: str) -> re.Pattern[str] | None:
    if not re.match(r"^[a-z0-9][a-z0-9 \-]*[a-z0-9]$", phrase):
        return None
    body = keyword_body_pattern(phrase)
    suffix = BIOLOGY_SUFFIX_RE if allows_inflection(phrase) else ""
    alternatives = [body + suffix]
    if allows_inflection(phrase) and phrase.endswith("y"):
        alternatives.append(keyword_body_pattern(phrase[:-1]) + r"ies")
    pattern = r"(?<![a-z0-9])(?:" + "|".join(alternatives) + r")(?![a-z0-9])"
    return re.compile(pattern)


def phrase_count(low_text: str, phrase: str) -> int:
    phrase = phrase.strip().lower()
    if phrase in {"![", "|"}:
        return low_text.count(phrase)
    pattern = keyword_regex(phrase)
    if pattern:
        return sum(1 for _ in pattern.finditer(low_text))
    return low_text.count(phrase)


HIGH_SPECIFICITY_WEIGHT = 8


def score_microtopics(block: str) -> list[dict[str, object]]:
    """Score every microtopic against a question block.

    A subtopic is kept when (a) its raw score clears the absolute floor and
    is at least 35 % of the top-scoring subtopic, OR (b) at least one
    high-specificity keyword (weight >= 8) fired. The override prevents
    Linkage/Map distance items from being absorbed into Mendelian when a
    single rare keyword like "recombination" is the only direct signal.
    """
    low = block.lower()
    scored: list[tuple[int, bool, str, str, str, list[str]]] = []
    for pillar, subtopic, objective, keywords in MICROTOPICS:
        score = 0
        matched: list[str] = []
        had_high_spec = False
        for phrase, weight in keywords:
            hits = phrase_count(low, phrase)
            if hits:
                score += hits * weight
                matched.append(phrase)
                if weight >= HIGH_SPECIFICITY_WEIGHT:
                    had_high_spec = True
        if score >= 5 or had_high_spec:
            scored.append((score, had_high_spec, pillar, subtopic, objective, matched[:6]))
    scored.sort(key=lambda item: (-item[0], item[3]))
    if not scored:
        return []
    top_score = scored[0][0]
    kept = []
    for score, had_high_spec, pillar, subtopic, objective, matched in scored:
        passes_relative = score >= max(5, top_score * 0.35)
        if passes_relative or had_high_spec:
            kept.append(
                {
                    "score": score,
                    "pillar": pillar,
                    "subtopic": subtopic,
                    "objective": objective,
                    "matched_terms": matched,
                }
            )
        if len(kept) >= 5:
            break
    return kept


def has_roman_list(block: str) -> bool:
    markers = [match.group(1).lower() for match in ROMAN_LIST_MARKER_RE.finditer(block)]
    marker_set = set(markers)
    return "i" in marker_set and any(marker in marker_set for marker in {"ii", "iii", "iv", "v"})


def reasoning_tags(block: str) -> list[str]:
    low = block.lower()
    tags = []
    for tag, patterns in REASONING_TAGS.items():
        if tag == "Multi-statement / Roman":
            if has_roman_list(block):
                tags.append(tag)
            continue
        for pattern in patterns:
            flags = re.M if pattern.startswith("^") else 0
            if re.search(pattern, low, flags):
                tags.append(tag)
                break
    return tags


def difficulty(block: str, tags: list[str], topics: list[dict[str, object]]) -> float:
    words = len(WORD_RE.findall(block))
    score = 1.5
    if words > 80:
        score += 0.4
    if words > 130:
        score += 0.45
    if words > 190:
        score += 0.45
    if "Data/figure/table reasoning" in tags:
        score += 0.35
    if "Experimental design/control reasoning" in tags:
        score += 0.35
    if "Select-all / multi-answer" in tags:
        score += 0.75
    if "Negation trap" in tags:
        score += 0.3
    if "Calculation / quantitative" in tags:
        score += 0.4
    if "Multi-statement / Roman" in tags:
        score += 0.3
    topic_count = len(topics)
    pillar_count = len({topic["pillar"] for topic in topics})
    if topic_count >= 2:
        score += 0.25
    if topic_count >= 3:
        score += 0.2
    if pillar_count >= 2:
        score += 0.2
    return min(5.0, round(score, 2))


def parse_questions() -> list[dict[str, object]]:
    parsed = []
    for path in sorted(MARKDOWN_ROOT.glob("20*/20*_OpenExam.md")):
        year = int(path.parent.name)
        for qn, block in split_questions(path.read_text()):
            tags = reasoning_tags(block)
            topics = score_microtopics(block)
            primary = topics[0] if topics else None
            difficulty_estimate = difficulty(block, tags, topics)
            parsed.append(
                {
                    "year": year,
                    "stage": stage_for_year(year),
                    "question_number": qn,
                    "source_path": str(path.relative_to(MARKDOWN_ROOT)),
                    "word_count": len(WORD_RE.findall(block)),
                    "difficulty_estimate": difficulty_estimate,
                    "reasoning_tags": tags,
                    "primary_pillar": primary["pillar"] if primary else "Unclassified",
                    "primary_subtopic": primary["subtopic"] if primary else "Unclassified",
                    "subtopics": topics,
                    "preview": block.splitlines()[0][:140],
                }
            )
    return parsed


def aggregate_subtopics(questions: list[dict[str, object]]) -> list[dict[str, object]]:
    lookup = {name: (pillar, objective) for pillar, name, objective, _ in MICROTOPICS}
    by_subtopic: dict[str, list[dict[str, object]]] = defaultdict(list)
    for question in questions:
        seen = set()
        for topic in question["subtopics"]:
            name = topic["subtopic"]
            if name not in seen:
                by_subtopic[name].append(question)
                seen.add(name)

    n_stages = len(STAGE_NAMES)
    rows = []
    for subtopic, qs in by_subtopic.items():
        pillar, objective = lookup[subtopic]
        stage_counts = Counter(q["stage"] for q in qs)
        years = sorted({int(q["year"]) for q in qs})
        total = len(qs)
        early = stage_counts["Early 2003-2008"]
        middle = stage_counts["Middle 2009-2013"]
        late = stage_counts["Late 2014-2018"]
        recent = stage_counts["Recent 2019-2024"]
        stage_breadth = sum(1 for stage in STAGE_NAMES if stage_counts[stage])
        avg_diff = mean(float(q["difficulty_estimate"]) for q in qs)
        # Independent features only.
        early_share = early / total
        late_share = late / total
        recent_share = recent / total
        modern_share = (late + recent) / total
        frequency_score = 12.0 * math.log1p(total)
        breadth_score = 1.5 * len(years) + 6.0 * (stage_breadth == n_stages)
        modernity_score = 14.0 * modern_share
        difficulty_score = 7.0 * max(0.0, avg_diff - 1.8)
        priority = frequency_score + breadth_score + modernity_score + difficulty_score
        if stage_breadth == 1 and (late + recent) == 0:
            priority *= 0.65
        rows.append(
            {
                "subtopic": subtopic,
                "pillar": pillar,
                "objective": objective,
                "hits": total,
                "early": early,
                "middle": middle,
                "late": late,
                "recent": recent,
                "stage_breadth": stage_breadth,
                "year_breadth": len(years),
                "years": years,
                "avg_difficulty": round(avg_diff, 2),
                "priority_score": round(priority, 1),
                "early_share": round(early_share, 3),
                "late_share": round(late_share, 3),
                "recent_share": round(recent_share, 3),
                "modern_share": round(modern_share, 3),
                "template_archetype": TEMPLATE_ARCHETYPES.get(subtopic, "Mechanism / inference variant"),
            }
        )
    return sorted(rows, key=lambda row: (-row["priority_score"], -row["hits"], row["subtopic"]))


def aggregate_reasoning_by_topic(questions: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    by_primary: dict[str, list[dict[str, object]]] = defaultdict(list)
    for question in questions:
        if question["primary_subtopic"] != "Unclassified":
            by_primary[question["primary_subtopic"]].append(question)

    for subtopic, qs in by_primary.items():
        pillar = qs[0]["primary_pillar"]
        total = len(qs)
        data_count = sum("Data/figure/table reasoning" in q["reasoning_tags"] for q in qs)
        experiment_count = sum("Experimental design/control reasoning" in q["reasoning_tags"] for q in qs)
        quantitative_count = sum("Calculation / quantitative" in q["reasoning_tags"] for q in qs)
        negation_count = sum("Negation trap" in q["reasoning_tags"] for q in qs)
        rows.append(
            {
                "subtopic": subtopic,
                "pillar": pillar,
                "primary_questions": total,
                "data_figure_table": data_count,
                "experimental_design": experiment_count,
                "calculation_quantitative": quantitative_count,
                "negation": negation_count,
                "data_share": round(data_count / total, 3),
                "experiment_share": round(experiment_count / total, 3),
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            -(row["data_figure_table"] + row["experimental_design"]),
            -row["primary_questions"],
            row["subtopic"],
        ),
    )


def aggregate_stage_summary(questions: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    by_stage: dict[str, list[dict[str, object]]] = defaultdict(list)
    for question in questions:
        by_stage[question["stage"]].append(question)

    for stage in STAGE_NAMES:
        qs = by_stage[stage]
        question_count = len(qs)
        subtopic_hits = sum(len(q["subtopics"]) for q in qs)
        tagged = sum(q["primary_subtopic"] != "Unclassified" for q in qs)
        row = {
            "stage": stage,
            "years": f"{min(year for year in dict(STAGES)[stage])}-{max(year for year in dict(STAGES)[stage])}",
            "question_count": question_count,
            "tagged_questions": tagged,
            "unclassified_questions": question_count - tagged,
            "subtopic_hits": subtopic_hits,
            "subtopic_hits_per_question": round(subtopic_hits / question_count, 2),
        }
        for tag in REASONING_TAG_ORDER:
            tag_count = sum(tag in q["reasoning_tags"] for q in qs)
            key = re.sub(r"[^a-z0-9]+", "_", tag.lower()).strip("_")
            row[f"{key}_count"] = tag_count
            row[f"{key}_rate"] = round(tag_count / question_count, 3)
        rows.append(row)
    return rows


def aggregate_year_pillars(questions: list[dict[str, object]]) -> list[dict[str, object]]:
    years = sorted({int(q["year"]) for q in questions})
    pillars = sorted({pillar for pillar, _, _, _ in MICROTOPICS} | {"Unclassified"})
    counts = Counter((int(q["year"]), q["primary_pillar"]) for q in questions)
    totals = Counter(int(q["year"]) for q in questions)
    rows = []
    for year in years:
        for pillar in pillars:
            value = counts[(year, pillar)]
            rows.append(
                {
                    "year": year,
                    "pillar": pillar,
                    "primary_questions": value,
                    "share": round(value / totals[year], 3),
                }
            )
    return rows


def aggregate_reasoning_cooccurrence(questions: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row_tag in REASONING_TAG_ORDER:
        for column_tag in REASONING_TAG_ORDER:
            count = sum(
                row_tag in q["reasoning_tags"] and column_tag in q["reasoning_tags"]
                for q in questions
            )
            rows.append(
                {
                    "row_tag": row_tag,
                    "column_tag": column_tag,
                    "question_count": count,
                    "share_of_corpus": round(count / len(questions), 3),
                }
            )
    return rows


def export_data(
    questions: list[dict[str, object]],
    subtopic_rows: list[dict[str, object]],
    reasoning_rows: list[dict[str, object]],
    stage_rows: list[dict[str, object]],
    year_pillar_rows: list[dict[str, object]],
    cooccurrence_rows: list[dict[str, object]],
) -> None:
    with QUESTION_TAGS_JSONL.open("w") as f:
        for question in questions:
            f.write(json.dumps(question, ensure_ascii=False) + "\n")

    with SUBTOPIC_SUMMARY_CSV.open("w", newline="") as f:
        fieldnames = [
            "subtopic",
            "pillar",
            "hits",
            "early",
            "middle",
            "late",
            "recent",
            "stage_breadth",
            "year_breadth",
            "years",
            "avg_difficulty",
            "priority_score",
            "early_share",
            "late_share",
            "recent_share",
            "modern_share",
            "template_archetype",
            "objective",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in subtopic_rows:
            out = dict(row)
            out["years"] = " ".join(str(y) for y in row["years"])
            writer.writerow(out)

    with UNCLASSIFIED_CSV.open("w", newline="") as f:
        fieldnames = ["year", "question_number", "word_count", "difficulty_estimate", "reasoning_tags", "preview"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for q in questions:
            if q["primary_subtopic"] == "Unclassified":
                writer.writerow(
                    {
                        "year": q["year"],
                        "question_number": q["question_number"],
                        "word_count": q["word_count"],
                        "difficulty_estimate": q["difficulty_estimate"],
                        "reasoning_tags": "|".join(q["reasoning_tags"]),
                        "preview": q["preview"],
                    }
                )

    with STAGE_SUMMARY_CSV.open("w", newline="") as f:
        fieldnames = list(stage_rows[0].keys()) if stage_rows else []
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(stage_rows)

    with YEAR_PILLAR_CSV.open("w", newline="") as f:
        fieldnames = ["year", "pillar", "primary_questions", "share"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(year_pillar_rows)

    with REASONING_COOCCURRENCE_CSV.open("w", newline="") as f:
        fieldnames = ["row_tag", "column_tag", "question_count", "share_of_corpus"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(cooccurrence_rows)

    with REASONING_TOPIC_CSV.open("w", newline="") as f:
        fieldnames = [
            "subtopic",
            "pillar",
            "primary_questions",
            "data_figure_table",
            "experimental_design",
            "calculation_quantitative",
            "negation",
            "data_share",
            "experiment_share",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(reasoning_rows)

    DATA_JSON.write_text(
        json.dumps(
            {
                "metadata": {
                    "question_count": len(questions),
                    "tagged_question_count": sum(q["primary_subtopic"] != "Unclassified" for q in questions),
                    "unclassified_question_count": sum(q["primary_subtopic"] == "Unclassified" for q in questions),
                    "subtopic_hit_count": sum(row["hits"] for row in subtopic_rows),
                    "stage_question_counts": {
                        stage: sum(q["stage"] == stage for q in questions) for stage in STAGE_NAMES
                    },
                    "stages": {name: [min(years), max(years)] for name, years in STAGES},
                },
                "subtopic_summary": subtopic_rows,
                "reasoning_by_topic": reasoning_rows,
                "stage_summary": stage_rows,
                "year_pillar_counts": year_pillar_rows,
                "reasoning_tag_cooccurrence": cooccurrence_rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap_label(value: object, width: int = 30) -> list[str]:
    words = str(value).split()
    lines: list[str] = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:3]


STAGE_HEATMAP_LABELS = [
    ("Early\n2003-08", "early"),
    ("Middle\n2009-13", "middle"),
    ("Late\n2014-18", "late"),
    ("Recent\n2019-24", "recent"),
]


def save_heatmap(path: Path, rows: list[dict[str, object]], title: str) -> None:
    cell_w = 64
    cell_h = 24
    left = 310
    top = 64
    right = 115
    bottom = 38
    n_cols = len(STAGE_HEATMAP_LABELS)
    width = left + cell_w * n_cols + right
    height = top + cell_h * len(rows) + bottom
    max_value = max(
        max(int(r[key]) for _, key in STAGE_HEATMAP_LABELS) for r in rows
    ) or 1
    max_root = math.sqrt(max_value)

    def color(value: int) -> str:
        t = math.sqrt(value) / max_root if max_root else 0.0
        red = int(236 + (27 - 236) * t)
        green = int(245 + (94 - 245) * t)
        blue = int(255 + (120 - 255) * t)
        return f"#{red:02x}{green:02x}{blue:02x}"

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}.head{font-weight:700}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
    ]
    for j, (label, _key) in enumerate(STAGE_HEATMAP_LABELS):
        for k, line in enumerate(label.split("\n")):
            out.append(
                f'<text x="{left + j * cell_w + cell_w / 2}" y="{top - 24 + k * 12}" text-anchor="middle" class="head small">{esc(line)}</text>'
            )
    for i, row in enumerate(rows):
        y = top + i * cell_h
        for k, line in enumerate(wrap_label(row["subtopic"], 42)):
            out.append(f'<text x="8" y="{y + 13 + k * 10}" class="small">{esc(line)}</text>')
        for j, (_label, key) in enumerate(STAGE_HEATMAP_LABELS):
            value = int(row[key])
            x = left + j * cell_w
            out.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 2}" height="{cell_h - 2}" fill="{color(value)}" stroke="#ffffff"/>'
            )
            out.append(
                f'<text x="{x + cell_w / 2}" y="{y + 15}" text-anchor="middle" class="small">{value}</text>'
            )
    legend_x = left + cell_w * n_cols + 16
    legend_y = top
    out.append(f'<text x="{legend_x}" y="{legend_y - 8}" class="small head">sqrt scale</text>')
    legend_values = [0, max_value // 4, max_value]
    for i, value in enumerate(legend_values):
        y = legend_y + i * 24
        out.append(f'<rect x="{legend_x}" y="{y}" width="18" height="16" fill="{color(value)}" stroke="#d1d5db"/>')
        out.append(f'<text x="{legend_x + 24}" y="{y + 12}" class="small">{value}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def save_barh(
    path: Path,
    rows: list[dict[str, object]],
    value_key: str,
    title: str,
    xlabel: str,
    color: str = "#2f6f9f",
) -> None:
    bar_h = 20
    gap = 7
    left = 330
    right = 70
    top = 56
    bottom = 42
    width = 940
    height = top + (bar_h + gap) * len(rows) + bottom
    max_value = max(float(r[value_key]) for r in rows) or 1.0
    scale = (width - left - right) / max_value
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
    ]
    for i, row in enumerate(rows):
        y = top + i * (bar_h + gap)
        for k, line in enumerate(wrap_label(row["subtopic"], 44)):
            out.append(f'<text x="8" y="{y + 12 + k * 10}" class="small">{esc(line)}</text>')
        value = float(row[value_key])
        bar_w = value * scale
        out.append(f'<rect x="{left}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}"/>')
        out.append(f'<text x="{left + bar_w + 5}" y="{y + 14}" class="small">{value:.1f}</text>')
    out.append(f'<text x="{left}" y="{height - 12}" class="small">{esc(xlabel)}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def save_delta(path: Path, rows: list[dict[str, object]], title: str) -> None:
    bar_h = 20
    gap = 7
    left = 390
    right = 55
    top = 56
    bottom = 35
    width = 980
    height = top + (bar_h + gap) * len(rows) + bottom
    max_abs = max(abs(int(r["delta"])) for r in rows) or 1
    mid = left + (width - left - right) / 2
    scale = (width - left - right) / 2 / max_abs
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
        f'<line x1="{mid}" x2="{mid}" y1="{top - 8}" y2="{height - bottom + 5}" stroke="#333" stroke-width="1"/>',
    ]
    for i, row in enumerate(rows):
        y = top + i * (bar_h + gap)
        for k, line in enumerate(wrap_label(row["subtopic"], 50)):
            out.append(f'<text x="8" y="{y + 12 + k * 10}" class="small">{esc(line)}</text>')
        delta = int(row["delta"])
        bar_w = abs(delta) * scale
        x = mid if delta >= 0 else mid - bar_w
        color = "#357a55" if delta >= 0 else "#b04a4a"
        out.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}"/>')
        text_x = x + bar_w + 4 if delta >= 0 else x - 6
        anchor = "start" if delta >= 0 else "end"
        out.append(
            f'<text x="{text_x}" y="{y + 14}" text-anchor="{anchor}" class="small">{delta:+d}</text>'
        )
    out.append("</svg>")
    path.write_text("\n".join(out))


def save_stacked(path: Path, rows: list[tuple[str, Counter]], title: str) -> None:
    bar_w = 56
    gap = 34
    left = 65
    top = 58
    bottom = 125
    right = 30
    height = 430
    width = left + (bar_w + gap) * len(rows) + right
    max_total = max(sum(counts.values()) for _, counts in rows) or 1
    colors = STAGE_COLORS
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
    ]
    plot_h = height - top - bottom
    out.append(f'<line x1="{left - 8}" x2="{width - right}" y1="{top + plot_h}" y2="{top + plot_h}" stroke="#333"/>')
    for i, (pillar, counts) in enumerate(rows):
        x = left + i * (bar_w + gap)
        y_base = top + plot_h
        acc = 0.0
        for stage in STAGE_NAMES:
            value = counts[stage]
            bar_h = plot_h * value / max_total
            y = y_base - acc - bar_h
            acc += bar_h
            out.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{colors[stage]}"/>')
        out.append(f'<text x="{x + bar_w / 2}" y="{top + plot_h + 14}" text-anchor="middle" class="small">{sum(counts.values())}</text>')
        for k, line in enumerate(wrap_label(pillar, 13)):
            out.append(
                f'<text x="{x + bar_w / 2}" y="{top + plot_h + 32 + k * 10}" text-anchor="middle" class="small">{esc(line)}</text>'
            )
    legend_x = width - 185
    legend_y = 48
    for j, stage in enumerate(STAGE_NAMES):
        out.append(f'<rect x="{legend_x}" y="{legend_y + j * 16}" width="11" height="11" fill="{colors[stage]}"/>')
        out.append(f'<text x="{legend_x + 16}" y="{legend_y + 10 + j * 16}" class="small">{esc(STAGE_SHORT[stage])}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def save_year_pillar_lines(path: Path, rows: list[dict[str, object]], title: str) -> None:
    years = sorted({int(row["year"]) for row in rows})
    totals = Counter()
    for row in rows:
        if row["pillar"] != "Unclassified":
            totals[row["pillar"]] += int(row["primary_questions"])
    pillars = [pillar for pillar, _ in totals.most_common(4)]
    colors = ["#2f6f9f", "#b45f06", "#357a55", "#6a51a3"]
    left = 58
    right = 160
    top = 56
    bottom = 54
    width = 920
    height = 430
    plot_w = width - left - right
    plot_h = height - top - bottom
    value_lookup = {(int(row["year"]), row["pillar"]): float(row["share"]) for row in rows}
    max_share = max((value_lookup.get((year, pillar), 0.0) for year in years for pillar in pillars), default=0.01)
    max_share = max(0.25, math.ceil(max_share * 10) / 10)

    def x_for(year: int) -> float:
        if len(years) == 1:
            return left + plot_w / 2
        return left + (year - years[0]) / (years[-1] - years[0]) * plot_w

    def y_for(share: float) -> float:
        return top + plot_h - (share / max_share) * plot_h

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
        f'<line x1="{left}" x2="{left}" y1="{top}" y2="{top + plot_h}" stroke="#333"/>',
        f'<line x1="{left}" x2="{left + plot_w}" y1="{top + plot_h}" y2="{top + plot_h}" stroke="#333"/>',
    ]
    for tick in range(0, int(max_share * 100) + 1, 10):
        share = tick / 100
        y = y_for(share)
        out.append(f'<line x1="{left - 4}" x2="{left + plot_w}" y1="{y}" y2="{y}" stroke="#eef2f7"/>')
        out.append(f'<text x="{left - 8}" y="{y + 4}" text-anchor="end" class="small">{tick}%</text>')
    for year in years:
        x = x_for(year)
        out.append(f'<line x1="{x}" x2="{x}" y1="{top + plot_h}" y2="{top + plot_h + 4}" stroke="#333"/>')
        out.append(f'<text x="{x}" y="{top + plot_h + 18}" text-anchor="middle" class="small">{year}</text>')
    for idx, pillar in enumerate(pillars):
        color = colors[idx % len(colors)]
        points = [(x_for(year), y_for(value_lookup.get((year, pillar), 0.0))) for year in years]
        point_text = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        out.append(f'<polyline points="{point_text}" fill="none" stroke="{color}" stroke-width="2"/>')
        for x, y in points:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="{color}"/>')
        legend_y = top + idx * 18
        legend_x = left + plot_w + 24
        out.append(f'<rect x="{legend_x}" y="{legend_y - 9}" width="12" height="12" fill="{color}"/>')
        out.append(f'<text x="{legend_x + 18}" y="{legend_y + 1}" class="small">{esc(pillar)}</text>')
    out.append('<text x="10" y="410" class="small">Y-axis: share of questions by primary pillar; 2003 has 35 questions.</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def save_cooccurrence_heatmap(path: Path, rows: list[dict[str, object]], title: str) -> None:
    tags = REASONING_TAG_ORDER
    cell = 62
    left = 230
    top = 112
    width = left + cell * len(tags) + 35
    height = top + cell * len(tags) + 45
    lookup = {(row["row_tag"], row["column_tag"]): int(row["question_count"]) for row in rows}
    max_value = max(lookup.values()) or 1

    def color(value: int) -> str:
        t = math.sqrt(value) / math.sqrt(max_value)
        red = int(242 + (49 - 242) * t)
        green = int(248 + (130 - 248) * t)
        blue = int(255 + (189 - 255) * t)
        return f"#{red:02x}{green:02x}{blue:02x}"

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
    ]
    for j, tag in enumerate(tags):
        x = left + j * cell + cell / 2
        for k, line in enumerate(wrap_label(tag, 12)):
            out.append(f'<text x="{x}" y="{top - 48 + k * 10}" text-anchor="middle" class="small">{esc(line)}</text>')
    for i, row_tag in enumerate(tags):
        y = top + i * cell
        for k, line in enumerate(wrap_label(row_tag, 28)):
            out.append(f'<text x="8" y="{y + 24 + k * 10}" class="small">{esc(line)}</text>')
        for j, column_tag in enumerate(tags):
            value = lookup[(row_tag, column_tag)]
            x = left + j * cell
            out.append(f'<rect x="{x}" y="{y}" width="{cell - 2}" height="{cell - 2}" fill="{color(value)}" stroke="#fff"/>')
            out.append(f'<text x="{x + cell / 2}" y="{y + 35}" text-anchor="middle" class="small">{value}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def save_difficulty_scatter(path: Path, rows: list[dict[str, object]], title: str) -> None:
    colors = {
        "Molecular/Cell": "#2f6f9f",
        "Genetics/Evolution": "#6a51a3",
        "Plant": "#357a55",
        "Animal Physiology": "#b45f06",
        "Ecology/Behavior": "#7a6a35",
        "Microbiology/Pathogens": "#b04a4a",
        "Molecular/Methods": "#4f6f52",
    }
    left = 70
    right = 210
    top = 56
    bottom = 58
    width = 920
    height = 430
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_hits = max(int(row["hits"]) for row in rows) or 1
    min_diff = 1.4
    max_diff = 3.4

    def x_for(hits: int) -> float:
        return left + math.log1p(hits) / math.log1p(max_hits) * plot_w

    def y_for(diff: float) -> float:
        return top + plot_h - (diff - min_diff) / (max_diff - min_diff) * plot_h

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:12px;fill:#1f2933}.title{font-size:18px;font-weight:700}.small{font-size:10px}</style>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="10" y="28" class="title">{esc(title)}</text>',
        f'<line x1="{left}" x2="{left}" y1="{top}" y2="{top + plot_h}" stroke="#333"/>',
        f'<line x1="{left}" x2="{left + plot_w}" y1="{top + plot_h}" y2="{top + plot_h}" stroke="#333"/>',
    ]
    for tick in [2, 5, 10, 20, 40, 80]:
        if tick <= max_hits:
            x = x_for(tick)
            out.append(f'<line x1="{x}" x2="{x}" y1="{top}" y2="{top + plot_h}" stroke="#eef2f7"/>')
            out.append(f'<text x="{x}" y="{top + plot_h + 16}" text-anchor="middle" class="small">{tick}</text>')
    for tick in [1.5, 2.0, 2.5, 3.0]:
        y = y_for(tick)
        out.append(f'<line x1="{left - 4}" x2="{left + plot_w}" y1="{y}" y2="{y}" stroke="#eef2f7"/>')
        out.append(f'<text x="{left - 8}" y="{y + 4}" text-anchor="end" class="small">{tick:.1f}</text>')
    for row in rows:
        x = x_for(int(row["hits"]))
        y = y_for(float(row["avg_difficulty"]))
        color = colors.get(str(row["pillar"]), "#666")
        radius = 3.5 + min(7.0, float(row["priority_score"]) / 14.0)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{color}" fill-opacity="0.72" stroke="#1f2933" stroke-width="0.5"/>')
    label_rows = sorted(rows, key=lambda row: -float(row["priority_score"]))[:8]
    for row in label_rows:
        x = x_for(int(row["hits"]))
        y = y_for(float(row["avg_difficulty"]))
        label = str(row["subtopic"]).split(",")[0][:28]
        out.append(f'<text x="{x + 8:.1f}" y="{y - 6:.1f}" class="small">{esc(label)}</text>')
    legend_x = left + plot_w + 25
    legend_y = top
    for idx, (pillar, color) in enumerate(colors.items()):
        y = legend_y + idx * 17
        out.append(f'<circle cx="{legend_x}" cy="{y}" r="5" fill="{color}" fill-opacity="0.72"/>')
        out.append(f'<text x="{legend_x + 12}" y="{y + 4}" class="small">{esc(pillar)}</text>')
    out.append(f'<text x="{left}" y="{height - 14}" class="small">X: subtopic hits, log scale. Y: heuristic average difficulty.</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def render_plots(
    subtopic_rows: list[dict[str, object]],
    reasoning_rows: list[dict[str, object]],
    year_pillar_rows: list[dict[str, object]],
    cooccurrence_rows: list[dict[str, object]],
) -> list[Path]:
    heat_rows = sorted(
        [row for row in subtopic_rows if int(row["hits"]) >= 8],
        key=lambda row: (-float(row["priority_score"]), row["subtopic"]),
    )[:26]
    save_heatmap(PLOT_DIR / "knowledge_subtopic_stage_heatmap.svg", heat_rows, "Knowledge subtopic hits by exam stage")

    priority_rows = subtopic_rows[:22]
    save_barh(
        PLOT_DIR / "knowledge_subtopic_priority_scores.svg",
        priority_rows,
        "priority_score",
        "Learning-objective priority score",
        "priority score",
    )

    delta_candidates = [
        dict(row, delta=int(row["late"]) - int(row["early"]))
        for row in subtopic_rows
        if int(row["hits"]) >= 4
    ]
    delta_sorted = sorted(delta_candidates, key=lambda row: row["delta"])
    save_delta(
        PLOT_DIR / "knowledge_subtopic_early_late_delta.svg",
        delta_sorted[:10] + delta_sorted[-10:],
        "Early-to-late knowledge subtopic shifts",
    )

    by_pillar: dict[str, Counter] = defaultdict(Counter)
    for row in subtopic_rows:
        by_pillar[row["pillar"]]["Early 2003-2008"] += int(row["early"])
        by_pillar[row["pillar"]]["Middle 2009-2013"] += int(row["middle"])
        by_pillar[row["pillar"]]["Late 2014-2018"] += int(row["late"])
    save_stacked(
        PLOT_DIR / "knowledge_pillar_stage_distribution.svg",
        sorted(by_pillar.items(), key=lambda item: -sum(item[1].values())),
        "Knowledge pillar distribution by stage",
    )

    data_rows = sorted(
        [row for row in reasoning_rows if int(row["data_figure_table"]) > 0],
        key=lambda row: (-int(row["data_figure_table"]), -int(row["primary_questions"]), row["subtopic"]),
    )[:18]
    save_barh(
        PLOT_DIR / "data_figure_reasoning_by_knowledge_topic.svg",
        data_rows,
        "data_figure_table",
        "Data/figure/table reasoning by knowledge topic",
        "question count",
        "#6a51a3",
    )

    experiment_rows = sorted(
        [row for row in reasoning_rows if int(row["experimental_design"]) > 0],
        key=lambda row: (-int(row["experimental_design"]), -int(row["primary_questions"]), row["subtopic"]),
    )[:18]
    save_barh(
        PLOT_DIR / "experimental_reasoning_by_knowledge_topic.svg",
        experiment_rows,
        "experimental_design",
        "Experimental/control reasoning by knowledge topic",
        "question count",
        "#b45f06",
    )

    save_year_pillar_lines(
        PLOT_DIR / "knowledge_pillar_year_trajectory.svg",
        year_pillar_rows,
        "Year-level trajectory for largest knowledge pillars",
    )

    save_cooccurrence_heatmap(
        PLOT_DIR / "reasoning_tag_cooccurrence.svg",
        cooccurrence_rows,
        "Reasoning / format tag co-occurrence",
    )

    save_difficulty_scatter(
        PLOT_DIR / "difficulty_vs_subtopic_recurrence.svg",
        subtopic_rows,
        "Difficulty vs. subtopic recurrence",
    )

    plot_paths = [
        PLOT_DIR / "knowledge_subtopic_stage_heatmap.svg",
        PLOT_DIR / "knowledge_subtopic_priority_scores.svg",
        PLOT_DIR / "knowledge_subtopic_early_late_delta.svg",
        PLOT_DIR / "knowledge_pillar_stage_distribution.svg",
        PLOT_DIR / "data_figure_reasoning_by_knowledge_topic.svg",
        PLOT_DIR / "experimental_reasoning_by_knowledge_topic.svg",
        PLOT_DIR / "knowledge_pillar_year_trajectory.svg",
        PLOT_DIR / "reasoning_tag_cooccurrence.svg",
        PLOT_DIR / "difficulty_vs_subtopic_recurrence.svg",
    ]
    clean_unused_plots(plot_paths)
    return plot_paths


def clean_unused_plots(plot_paths: list[Path]) -> None:
    keep = {path.resolve() for path in plot_paths}
    for path in PLOT_DIR.glob("*.svg"):
        if path.resolve() not in keep:
            path.unlink()


def percent(value: int, total: int) -> str:
    return f"{100 * value / total:.1f}%"


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        clean = [str(value).replace("\n", "<br>").replace("|", "/") for value in row]
        lines.append("| " + " | ".join(clean) + " |")
    return "\n".join(lines)


def render_report(
    questions: list[dict[str, object]],
    subtopic_rows: list[dict[str, object]],
    reasoning_rows: list[dict[str, object]],
    stage_rows: list[dict[str, object]],
    plot_paths: list[Path],
) -> None:
    tagged_count = sum(q["primary_subtopic"] != "Unclassified" for q in questions)
    unclassified_count = len(questions) - tagged_count
    topic_hit_count = sum(int(row["hits"]) for row in subtopic_rows)
    stage_q_counts = Counter(q["stage"] for q in questions)

    def stage_per_50(count: int, stage: str) -> str:
        return f"{50 * count / stage_q_counts[stage]:.1f}"

    def stage_pct(count: int, stage: str) -> str:
        return f"{100 * count / stage_q_counts[stage]:.1f}%"

    stage_table_rows = [
        [
            STAGE_SHORT[row["stage"]],
            row["years"],
            row["question_count"],
            row["tagged_questions"],
            row["unclassified_questions"],
            row["subtopic_hits"],
            row["subtopic_hits_per_question"],
        ]
        for row in stage_rows
    ]

    by_pillar: dict[str, Counter] = defaultdict(Counter)
    for row in subtopic_rows:
        for stage in STAGE_NAMES:
            by_pillar[row["pillar"]][stage] += int(row[STAGE_KEY[stage]])
    pillar_rows = []
    for pillar, counts in sorted(by_pillar.items(), key=lambda item: -sum(item[1].values())):
        total = sum(counts.values())
        modern = counts["Late 2014-2018"] + counts["Recent 2019-2024"]
        pillar_rows.append(
            [
                pillar,
                total,
                counts["Early 2003-2008"],
                counts["Middle 2009-2013"],
                counts["Late 2014-2018"],
                counts["Recent 2019-2024"],
                f"{100 * modern / total:.0f}%" if total else "-",
                percent(total, topic_hit_count),
            ]
        )

    priority_rows = []
    for index, row in enumerate(subtopic_rows[:12]):
        priority_rows.append(
            [
                index + 1,
                row["subtopic"],
                row["pillar"],
                row["hits"],
                row["priority_score"],
                f'{100 * float(row["modern_share"]):.0f}%',
                f'{row["early"]}/{row["middle"]}/{row["late"]}/{row["recent"]}',
                row["template_archetype"],
            ]
        )

    def modern(row: dict[str, object]) -> int:
        return int(row["late"]) + int(row["recent"])

    rising_rows = []
    for row in sorted(
        [r for r in subtopic_rows if modern(r) >= 5],
        key=lambda r: (-(modern(r) - int(r["early"])), -modern(r), r["subtopic"]),
    )[:10]:
        rising_rows.append(
            [
                row["subtopic"],
                row["pillar"],
                f'{row["early"]}/{row["middle"]}/{row["late"]}/{row["recent"]}',
                modern(row) - int(row["early"]),
                f'{100 * float(row["modern_share"]):.0f}%',
            ]
        )

    declining_rows = []
    for row in sorted(
        [r for r in subtopic_rows if int(r["early"]) >= 4 and int(r["early"]) > modern(r)],
        key=lambda r: (-(int(r["early"]) - modern(r)), -int(r["early"]), r["subtopic"]),
    )[:8]:
        declining_rows.append(
            [
                row["subtopic"],
                row["pillar"],
                f'{row["early"]}/{row["middle"]}/{row["late"]}/{row["recent"]}',
                int(row["early"]) - modern(row),
                f'{100 * float(row["early_share"]):.0f}%',
            ]
        )

    low_priority_rows = [
        [
            row["subtopic"],
            row["pillar"],
            row["hits"],
            row["stage_breadth"],
            row["priority_score"],
            row["template_archetype"],
        ]
        for row in sorted(subtopic_rows, key=lambda r: (float(r["priority_score"]), int(r["hits"]), r["subtopic"]))[:6]
    ]

    tag_stage: dict[str, Counter] = defaultdict(Counter)
    for question in questions:
        for tag in question["reasoning_tags"]:
            tag_stage[tag][question["stage"]] += 1
    tag_rows = []
    for tag, counts in sorted(tag_stage.items(), key=lambda item: -sum(item[1].values())):
        total = sum(counts.values())
        tag_rows.append(
            [
                tag,
                total,
                stage_pct(counts["Early 2003-2008"], "Early 2003-2008"),
                stage_pct(counts["Middle 2009-2013"], "Middle 2009-2013"),
                stage_pct(counts["Late 2014-2018"], "Late 2014-2018"),
                stage_pct(counts["Recent 2019-2024"], "Recent 2019-2024"),
                percent(total, len(questions)),
            ]
        )

    data_topic_rows = [
        [
            row["subtopic"],
            row["pillar"],
            row["primary_questions"],
            row["data_figure_table"],
            f'{100 * float(row["data_share"]):.0f}%',
        ]
        for row in sorted(
            [row for row in reasoning_rows if int(row["data_figure_table"]) > 0],
            key=lambda row: (-int(row["data_figure_table"]), row["subtopic"]),
        )[:10]
    ]
    experiment_topic_rows = [
        [
            row["subtopic"],
            row["pillar"],
            row["primary_questions"],
            row["experimental_design"],
            f'{100 * float(row["experiment_share"]):.0f}%',
        ]
        for row in sorted(
            [row for row in reasoning_rows if int(row["experimental_design"]) > 0],
            key=lambda row: (-int(row["experimental_design"]), row["subtopic"]),
        )[:10]
    ]

    key_plot_names = {
        "knowledge_subtopic_priority_scores.svg",
        "knowledge_subtopic_stage_heatmap.svg",
        "knowledge_pillar_year_trajectory.svg",
        "reasoning_tag_cooccurrence.svg",
        "difficulty_vs_subtopic_recurrence.svg",
    }
    key_plot_lines = "\n".join(
        f"- ![{path.stem}](plots/{path.name})" for path in plot_paths if path.name in key_plot_names
    )

    content = f"""# Consolidated USABO Open Exam Subtopic Analysis, 2003-2024

Generated from local files in `raw/markdown` on 2026-05-08. No web search or remote model APIs were used.

## Bottom Line

This report should be read as a **prioritization memo**, not a complete topic encyclopedia. The long tables live in `data/`; this Markdown keeps the decisions that matter for BioBloom.

The exam has a stable content backbone, but the modern exam is harder because the same topics are wrapped in figures, experiments, multi-statement choices, and biomedical/lab contexts. The most valuable learning objective is therefore not "know more isolated facts"; it is "recognize the recurring mechanism template and solve it under modern task forms."

## Coverage And Reliability

{md_table(["Stage", "Years", "Questions", "Tagged", "Unclassified", "Subtopic hits", "Hits / question"], stage_table_rows)}

Critical caveats:

- The taxonomy is keyword-based and directional. It is strong enough for prioritization, not strong enough to be treated as ground truth.
- Recent has {stage_q_counts["Recent 2019-2024"]} questions, while Middle and Late each have 250; raw counts must be read with this denominator difference.
- {unclassified_count} questions remain unclassified. That is a real audit queue, not a rounding error.
- Tier labels are useful for sequencing, but they compress nuance. A Tier 1 item with 122 hits and a Tier 1 item with 32 hits should not receive equal study time.
- Remaining data-quality issues include 2013 Q33 missing from the answer key and 2019 having 47 parsed questions despite source notes suggesting 50 items.

## Critical Findings

1. **The stable core is broad but not flat.** Animal physiology, molecular/cell biology, genetics/evolution, plant biology, and ecology all recur. The highest priority should go to subtopics that combine high frequency, many tested years, and modern-stage presence.

2. **Modernity is a task-form shift, not a syllabus replacement.** 2019-2024 adds more lab/molecular methods, immunology/pathogen scenarios, plant mechanisms, and figure-heavy physiology. It does not make older topics obsolete.

3. **Select-all is no longer the main modern difficulty signal.** Select-all is concentrated in 2010-2017. In 2019-2024, difficulty shifts toward single-answer questions with Roman statements, figures, and dense mechanism reasoning.

4. **Methods and data are not standalone study chapters.** They attach to concrete biology: cardiovascular/renal physiology, population ecology, plant transport/development, pedigrees, molecular methods, and gene regulation.

5. **The current priority model likely over-includes stable topics.** It is better for ordering modules than for declaring exact exam probabilities. Use it to choose what to teach first, then validate against manually labeled questions.

## Priority Learning Objectives

Start here. These are the strongest module candidates because they are frequent, broadly distributed, and still active in Late + Recent exams.

{md_table(["Rank", "Subtopic", "Pillar", "Hits", "Priority", "Modern share", "E/M/L/R", "Template archetype"], priority_rows)}

The first five are the clearest cross-era anchors. `Lab methods, biotechnology and molecular tools` is lower by raw frequency than the big physiology/genetics/ecology groups, but it deserves early attention because Recent exams make it a differentiator.

## What Changed After 2018

Subtopics rising most clearly in Late + Recent relative to Early:

{md_table(["Subtopic", "Pillar", "E/M/L/R", "Modern - Early", "Modern share"], rising_rows)}

Practical reading:

- Treat immunology/pathogens, molecular methods, developmental mechanisms, and plant transport as modern differentiators.
- Do not remove older genetics or physiology templates. Mendelian probability and cardiovascular/renal logic still rank near the top.
- Build modern variants by adding data, experimental setup, or multi-statement interpretation to stable content.

## What Not To Overprioritize

These are not topics to delete. They are topics to keep behind the core if time is limited.

Early-weighted signals:

{md_table(["Subtopic", "Pillar", "E/M/L/R", "Early - Modern", "Early share"], declining_rows or [["-", "-", "-", "-", "-"]])}

Lowest-priority subtopic rows by the current score:

{md_table(["Subtopic", "Pillar", "Hits", "Stage breadth", "Priority", "Template archetype"], low_priority_rows)}

Critical reading: "low priority" here usually means low frequency or narrower representation, not low biological importance. These topics should enter mixed review after the core template bank is healthy.

## Reasoning Skills By Topic

Data/figure/table reasoning is most useful when attached to a real knowledge target:

{md_table(["Knowledge subtopic", "Pillar", "Primary Q", "Data/figure Q", "Share"], data_topic_rows)}

Experimental/control reasoning clusters differently:

{md_table(["Knowledge subtopic", "Pillar", "Primary Q", "Experiment Q", "Share"], experiment_topic_rows)}

Format pressure by stage:

{md_table(["Reasoning / format tag", "Total Q", "Early %", "Middle %", "Late %", "Recent %", "Share"], tag_rows)}

Critical reading:

- Recent exams use more Roman/multi-statement logic than earlier stages.
- Data/figure pressure keeps rising into Recent.
- Select-all pressure is a 2010-2017 phenomenon; do not overfit modern practice to select-all just because it felt hard in 2016-2017.

## Knowledge Pillars

Use this only for broad module balance. It is less actionable than the subtopic tables because multi-label counts blur topic boundaries.

{md_table(["Pillar", "Hits", "Early", "Middle", "Late", "Recent", "Modern share", "Share of hits"], pillar_rows)}

## BioBloom Action Plan

1. Build the template bank from the top priority rows, not from exact official wording.
2. Store `pillar`, `subtopics`, `reasoning_tags`, `stage`, `difficulty_estimate`, and `template_archetype` on every generated question.
3. Default advanced practice to `Late + Recent`, but vary style: 2014-2017 for select-all pressure; 2020-2021 for long-stem/data pressure; 2023-2024 for shorter modern single-answer items.
4. Diagnose misses as `knowledge target + task form`, for example `plant transport + data figure` or `Mendelian probability + Roman statements`.
5. Hand-label a gold set before tuning scores further. Start with the unclassified queue and a stratified sample of the top 12 priority topics.

## Limitations And Audit Queue

- `data/open_exam_unclassified_questions.csv` contains {unclassified_count} items that need manual classification.
- The keyword set still underrepresents newer method vocabulary such as lipid nanoparticles, NativePAGE, Cre-Lox, hyperactive transposon screens, and sequence-analysis workflows.
- The difficulty score is feature-based. It sees length, figures, calculations, and task-form markers; it does not directly measure conceptual depth.
- The priority score is a sequencing heuristic. It should not be used as a probability forecast without a hand-labeled validation set.
- Data issues still to resolve: add `2003_answer_key.json`, verify 2013 Q33, normalize 2015 Q2 if desired, preserve special answer keys, keep 2018's shared option block, and verify whether 2019 truly has only 47 exam questions.

## Artifacts

Primary data files:

- `data/open_exam_subtopic_summary.csv`
- `data/open_exam_subtopic_question_tags.jsonl`
- `data/open_exam_reasoning_by_topic.csv`
- `data/open_exam_stage_summary.csv`
- `data/open_exam_unclassified_questions.csv`
- `data/open_exam_consolidated_subtopic_analysis_data.json`

Most useful plots:

{key_plot_lines}

Generator: `code/generate_consolidated_subtopic_analysis.py`
"""
    REPORT_PATH.write_text(content)


def validate_integrity(
    questions: list[dict[str, object]],
    subtopic_rows: list[dict[str, object]],
    stage_rows: list[dict[str, object]],
) -> None:
    per_year = Counter(int(q["year"]) for q in questions)
    assert sum(per_year.values()) == len(questions), "per-year question counts do not sum to total"
    assert set(per_year) == set(range(2003, 2025)), "expected years 2003-2024"
    # Two known short years: 2003 (35 Q, 4-option) and 2019 (47 Q).
    short_years = {2003: 35, 2019: 47}
    for year, expected in short_years.items():
        assert per_year[year] == expected, f"{year} should have {expected} parsed questions"
    for year in range(2003, 2025):
        if year in short_years:
            continue
        assert per_year[year] == 50, f"{year} should have 50 parsed questions"

    tagged = sum(q["primary_subtopic"] != "Unclassified" for q in questions)
    unclassified = sum(q["primary_subtopic"] == "Unclassified" for q in questions)
    assert tagged + unclassified == len(questions), "tagged + unclassified mismatch"

    question_hit_total = sum(len(q["subtopics"]) for q in questions)
    summary_hit_total = sum(int(row["hits"]) for row in subtopic_rows)
    assert question_hit_total == summary_hit_total, "question-level hits do not match summary hits"

    stage_question_total = sum(int(row["question_count"]) for row in stage_rows)
    assert stage_question_total == len(questions), "stage question counts do not sum to total"


def main() -> None:
    questions = parse_questions()
    subtopic_rows = aggregate_subtopics(questions)
    reasoning_rows = aggregate_reasoning_by_topic(questions)
    stage_rows = aggregate_stage_summary(questions)
    year_pillar_rows = aggregate_year_pillars(questions)
    cooccurrence_rows = aggregate_reasoning_cooccurrence(questions)
    validate_integrity(questions, subtopic_rows, stage_rows)
    export_data(questions, subtopic_rows, reasoning_rows, stage_rows, year_pillar_rows, cooccurrence_rows)
    plot_paths = render_plots(subtopic_rows, reasoning_rows, year_pillar_rows, cooccurrence_rows)
    render_report(questions, subtopic_rows, reasoning_rows, stage_rows, plot_paths)
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {QUESTION_TAGS_JSONL}")
    print(f"Wrote {SUBTOPIC_SUMMARY_CSV}")
    print(f"Wrote {REASONING_TOPIC_CSV}")
    print(f"Wrote {UNCLASSIFIED_CSV}")
    print(f"Wrote {STAGE_SUMMARY_CSV}")
    print(f"Wrote {YEAR_PILLAR_CSV}")
    print(f"Wrote {REASONING_COOCCURRENCE_CSV}")
    print(f"Wrote {DATA_JSON}")
    for path in plot_paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
