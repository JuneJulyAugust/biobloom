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
import re
from collections import Counter, defaultdict
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
DATA_JSON = DATA_DIR / "open_exam_consolidated_subtopic_analysis_data.json"

Q_RE = re.compile(r"^### (\d+)\.\s*(.*)$", re.M)
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")

STAGES = [
    ("Early 2003-2008", range(2003, 2009)),
    ("Middle 2009-2013", range(2009, 2014)),
    ("Late 2014-2018", range(2014, 2019)),
]
STAGE_NAMES = [name for name, _ in STAGES]
STAGE_SHORT = {
    "Early 2003-2008": "Early",
    "Middle 2009-2013": "Middle",
    "Late 2014-2018": "Late",
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
            ("ph ", 4),
            ("pka", 6),
            ("hydrogen ions", 5),
            ("molar", 5),
            ("molecular weight", 5),
            ("concentration", 4),
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
            ("linkage", 8),
            ("linked genes", 8),
            ("recombination", 8),
            ("recombinant", 7),
            ("map distance", 9),
            ("centimorgan", 8),
            ("crossover", 7),
            ("double recombinant", 9),
            ("gene order", 8),
            ("map unit", 8),
            ("linked", 4),
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
        ),
    ),
]

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
    "Multi-statement / Roman": [
        r"\bi\.",
        r"\bii\.",
        r"\biii\.",
        r"\biv\.",
        r"\bv\.",
    ],
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


def phrase_count(low_text: str, phrase: str) -> int:
    phrase = phrase.lower()
    if phrase in {"![", "|"}:
        return low_text.count(phrase)
    escaped = re.escape(phrase)
    if re.match(r"^[a-z0-9 ]+$", phrase):
        pattern = r"(?<![a-z0-9])" + escaped.replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        return len(re.findall(pattern, low_text))
    return low_text.count(phrase)


def score_microtopics(block: str) -> list[dict[str, object]]:
    low = block.lower()
    scored: list[tuple[int, str, str, str, list[str]]] = []
    for pillar, subtopic, objective, keywords in MICROTOPICS:
        score = 0
        matched: list[str] = []
        for phrase, weight in keywords:
            hits = phrase_count(low, phrase)
            if hits:
                score += hits * weight
                matched.append(phrase)
        if score >= 5:
            scored.append((score, pillar, subtopic, objective, matched[:6]))
    scored.sort(reverse=True)
    if not scored:
        return []
    top_score = scored[0][0]
    kept = []
    for score, pillar, subtopic, objective, matched in scored:
        if score >= max(5, top_score * 0.45):
            kept.append(
                {
                    "score": score,
                    "pillar": pillar,
                    "subtopic": subtopic,
                    "objective": objective,
                    "matched_terms": matched,
                }
            )
        if len(kept) >= 4:
            break
    return kept


def reasoning_tags(block: str) -> list[str]:
    low = block.lower()
    tags = []
    for tag, patterns in REASONING_TAGS.items():
        for pattern in patterns:
            flags = re.M if pattern.startswith("^") else 0
            if re.search(pattern, low, flags):
                tags.append(tag)
                break
    return tags


def difficulty(block: str, tags: list[str]) -> float:
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
    return min(5.0, round(score, 2))


def parse_questions() -> list[dict[str, object]]:
    parsed = []
    for path in sorted(MARKDOWN_ROOT.glob("20*/20*_OpenExam.md")):
        year = int(path.parent.name)
        for qn, block in split_questions(path.read_text()):
            tags = reasoning_tags(block)
            topics = score_microtopics(block)
            primary = topics[0] if topics else None
            parsed.append(
                {
                    "year": year,
                    "stage": stage_for_year(year),
                    "question_number": qn,
                    "source_path": str(path.relative_to(MARKDOWN_ROOT)),
                    "word_count": len(WORD_RE.findall(block)),
                    "difficulty_estimate": difficulty(block, tags),
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

    rows = []
    for subtopic, qs in by_subtopic.items():
        pillar, objective = lookup[subtopic]
        stage_counts = Counter(q["stage"] for q in qs)
        years = sorted({int(q["year"]) for q in qs})
        total = len(qs)
        early = stage_counts["Early 2003-2008"]
        middle = stage_counts["Middle 2009-2013"]
        late = stage_counts["Late 2014-2018"]
        stage_breadth = sum(1 for stage in STAGE_NAMES if stage_counts[stage])
        avg_diff = mean(float(q["difficulty_estimate"]) for q in qs)
        priority = (
            total
            + 1.7 * len(years)
            + 7 * (stage_breadth == 3)
            + 1.3 * late
            + 3 * max(0, avg_diff - 2.0)
        )
        if stage_breadth == 1 and late == 0:
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
                "stage_breadth": stage_breadth,
                "year_breadth": len(years),
                "years": years,
                "avg_difficulty": round(avg_diff, 2),
                "priority_score": round(priority, 1),
                "late_share": round(late / total, 3),
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


def export_data(
    questions: list[dict[str, object]],
    subtopic_rows: list[dict[str, object]],
    reasoning_rows: list[dict[str, object]],
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
            "stage_breadth",
            "year_breadth",
            "years",
            "avg_difficulty",
            "priority_score",
            "late_share",
            "objective",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in subtopic_rows:
            out = dict(row)
            out["years"] = " ".join(str(y) for y in row["years"])
            writer.writerow(out)

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
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reasoning_rows)

    DATA_JSON.write_text(
        json.dumps(
            {
                "metadata": {
                    "question_count": len(questions),
                    "tagged_question_count": sum(q["primary_subtopic"] != "Unclassified" for q in questions),
                    "subtopic_hit_count": sum(row["hits"] for row in subtopic_rows),
                    "stages": {name: [min(years), max(years)] for name, years in STAGES},
                },
                "subtopic_summary": subtopic_rows,
                "reasoning_by_topic": reasoning_rows,
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


def save_heatmap(path: Path, rows: list[dict[str, object]], title: str) -> None:
    cell_w = 70
    cell_h = 24
    left = 310
    top = 58
    right = 30
    bottom = 25
    width = left + cell_w * 3 + right
    height = top + cell_h * len(rows) + bottom
    max_value = max(max(int(r["early"]), int(r["middle"]), int(r["late"])) for r in rows) or 1

    def color(value: int) -> str:
        t = value / max_value
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
    for j, label in enumerate(["Early\n2003-08", "Middle\n2009-13", "Late\n2014-18"]):
        for k, line in enumerate(label.split("\n")):
            out.append(
                f'<text x="{left + j * cell_w + cell_w / 2}" y="{top - 24 + k * 12}" text-anchor="middle" class="head small">{esc(line)}</text>'
            )
    for i, row in enumerate(rows):
        y = top + i * cell_h
        for k, line in enumerate(wrap_label(row["subtopic"], 42)):
            out.append(f'<text x="8" y="{y + 13 + k * 10}" class="small">{esc(line)}</text>')
        for j, value in enumerate([int(row["early"]), int(row["middle"]), int(row["late"])]):
            x = left + j * cell_w
            out.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 2}" height="{cell_h - 2}" fill="{color(value)}" stroke="#ffffff"/>'
            )
            out.append(
                f'<text x="{x + cell_w / 2}" y="{y + 15}" text-anchor="middle" class="small">{value}</text>'
            )
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
    colors = {
        "Early 2003-2008": "#9ecae1",
        "Middle 2009-2013": "#74c476",
        "Late 2014-2018": "#fd8d3c",
    }
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


def render_plots(
    subtopic_rows: list[dict[str, object]],
    reasoning_rows: list[dict[str, object]],
) -> list[Path]:
    heat_rows = sorted(
        [row for row in subtopic_rows if int(row["hits"]) >= 8],
        key=lambda row: (-float(row["priority_score"]), row["subtopic"]),
    )[:26]
    save_heatmap(PLOT_DIR / "knowledge_subtopic_stage_heatmap.svg", heat_rows, "Knowledge subtopic hits by exam stage")

    priority_rows = list(reversed(subtopic_rows[:22]))
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
        list(reversed(data_rows)),
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
        list(reversed(experiment_rows)),
        "experimental_design",
        "Experimental/control reasoning by knowledge topic",
        "question count",
        "#b45f06",
    )

    return [
        PLOT_DIR / "knowledge_subtopic_stage_heatmap.svg",
        PLOT_DIR / "knowledge_subtopic_priority_scores.svg",
        PLOT_DIR / "knowledge_subtopic_early_late_delta.svg",
        PLOT_DIR / "knowledge_pillar_stage_distribution.svg",
        PLOT_DIR / "data_figure_reasoning_by_knowledge_topic.svg",
        PLOT_DIR / "experimental_reasoning_by_knowledge_topic.svg",
    ]


def fmt_years(years: list[int]) -> str:
    if not years:
        return "-"
    runs: list[tuple[int, int]] = []
    start = prev = years[0]
    for year in years[1:]:
        if year == prev + 1:
            prev = year
        else:
            runs.append((start, prev))
            start = prev = year
    runs.append((start, prev))
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in runs)


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


def tier(index: int, row: dict[str, object]) -> str:
    if int(row["stage_breadth"]) == 3 and index < 14:
        return "Tier 1 - stable core"
    if int(row["late"]) >= 5 and int(row["late"]) >= int(row["early"]):
        return "Tier 2 - modern differentiator"
    if int(row["hits"]) >= 8:
        return "Tier 3 - periodic high-yield"
    return "Tier 4 - selective / low-frequency"


def render_report(
    questions: list[dict[str, object]],
    subtopic_rows: list[dict[str, object]],
    reasoning_rows: list[dict[str, object]],
    plot_paths: list[Path],
) -> None:
    tagged_count = sum(q["primary_subtopic"] != "Unclassified" for q in questions)
    topic_hit_count = sum(int(row["hits"]) for row in subtopic_rows)

    by_pillar: dict[str, Counter] = defaultdict(Counter)
    for row in subtopic_rows:
        by_pillar[row["pillar"]]["Early 2003-2008"] += int(row["early"])
        by_pillar[row["pillar"]]["Middle 2009-2013"] += int(row["middle"])
        by_pillar[row["pillar"]]["Late 2014-2018"] += int(row["late"])
    pillar_rows = []
    for pillar, counts in sorted(by_pillar.items(), key=lambda item: -sum(item[1].values())):
        total = sum(counts.values())
        pillar_rows.append(
            [
                pillar,
                total,
                counts["Early 2003-2008"],
                counts["Middle 2009-2013"],
                counts["Late 2014-2018"],
                percent(total, topic_hit_count),
            ]
        )

    stable = sorted(
        [row for row in subtopic_rows if int(row["stage_breadth"]) == 3 and int(row["hits"]) >= 10],
        key=lambda row: (-int(row["hits"]), -int(row["year_breadth"]), row["subtopic"]),
    )
    stable_rows = [
        [
            row["subtopic"],
            row["pillar"],
            row["hits"],
            row["early"],
            row["middle"],
            row["late"],
            row["year_breadth"],
            row["avg_difficulty"],
        ]
        for row in stable[:30]
    ]

    priority_rows = []
    for index, row in enumerate(subtopic_rows[:30]):
        priority_rows.append(
            [
                index + 1,
                tier(index, row),
                row["subtopic"],
                row["pillar"],
                row["hits"],
                row["priority_score"],
                f'{row["early"]}/{row["middle"]}/{row["late"]}',
                fmt_years(row["years"]),
                row["objective"],
            ]
        )

    late_rows = []
    for row in sorted(
        [row for row in subtopic_rows if int(row["late"]) >= 4],
        key=lambda row: (-(int(row["late"]) - int(row["early"])), -int(row["late"]), row["subtopic"]),
    )[:18]:
        late_rows.append(
            [
                row["subtopic"],
                row["pillar"],
                row["early"],
                row["middle"],
                row["late"],
                int(row["late"]) - int(row["early"]),
                f'{100 * float(row["late_share"]):.0f}%',
            ]
        )

    early_rows = []
    for row in sorted(
        [
            row
            for row in subtopic_rows
            if int(row["early"]) >= 3 and int(row["early"]) > int(row["late"])
        ],
        key=lambda row: (-(int(row["early"]) - int(row["late"])), -int(row["early"]), row["subtopic"]),
    )[:18]:
        early_rows.append(
            [
                row["subtopic"],
                row["pillar"],
                row["early"],
                row["middle"],
                row["late"],
                int(row["early"]) - int(row["late"]),
                fmt_years(row["years"]),
            ]
        )

    late_only_rows = [
        [row["subtopic"], row["pillar"], row["late"], fmt_years(row["years"]), row["avg_difficulty"]]
        for row in subtopic_rows
        if int(row["late"]) > 0 and int(row["early"]) == 0 and int(row["middle"]) == 0
    ]
    early_only_rows = [
        [row["subtopic"], row["pillar"], row["early"], fmt_years(row["years"]), row["avg_difficulty"]]
        for row in subtopic_rows
        if int(row["early"]) > 0 and int(row["middle"]) == 0 and int(row["late"]) == 0
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
                counts["Early 2003-2008"],
                counts["Middle 2009-2013"],
                counts["Late 2014-2018"],
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
        )[:20]
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
        )[:20]
    ]

    appendix_rows = [
        [
            row["subtopic"],
            row["pillar"],
            row["hits"],
            row["early"],
            row["middle"],
            row["late"],
            row["stage_breadth"],
            row["year_breadth"],
            fmt_years(row["years"]),
            row["avg_difficulty"],
            row["priority_score"],
        ]
        for row in sorted(subtopic_rows, key=lambda row: (-int(row["hits"]), row["subtopic"]))
    ]

    plot_lines = "\n".join(
        f"- ![{path.stem}](plots/{path.name})" for path in plot_paths
    )

    content = f"""# Consolidated USABO Open Exam Subtopic Analysis, 2003-2018

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

The analysis parsed {len(questions)} questions from 16 Markdown exams. The three stages are the same stages found across the prior reports:

- Early: 2003-2008
- Middle: 2009-2013
- Late: 2014-2018

This pass uses a multi-label knowledge microtopic taxonomy. A question can count for more than one knowledge subtopic, because many Open Exam items combine biology areas. The taxonomy generated {topic_hit_count} knowledge-subtopic hits across {tagged_count} tagged questions. Counts are useful for prioritization, but they are still heuristic and should be refined with manual labels later.

Reasoning skills are separate tags: negation, quantitative calculation, Roman/multi-statement logic, select-all format, data/figure/table reasoning, and experimental/control reasoning. The two broad methods/data categories are analyzed below by their associated knowledge topic.

## Consolidated Consensus From The Three Reports

All three analyses agree on the main exam story:

- The syllabus is stable, but the way the exam tests it changes substantially.
- Early `2003-2008` is more recall-heavy and one-step.
- Middle `2009-2013` adds more calculation, figures, and experimental framing.
- Late `2014-2018`, especially 2014-2017, adds longer stems, mechanism chains, multi-select formats, data interpretation, and experimental biology.
- The highest-return practice target is not memorizing exact old questions. It is mastering stable mechanism templates and learning to solve new variants.

## Generated Plots

{plot_lines}

## Knowledge Pillar Distribution By Stage

These are multi-label knowledge-topic hits, so totals exceed question count. Data/experiment is not a pillar here; it is analyzed as reasoning attached to these knowledge pillars.

{md_table(["Pillar", "Topic hits", "Early", "Middle", "Late", "Share of hits"], pillar_rows)}

## Stable Knowledge Subtopics Across All Three Stages

These subtopics appear in early, middle, and late stages. They are the safest foundation for learning-objective prioritization.

{md_table(["Subtopic", "Pillar", "Hits", "Early", "Middle", "Late", "Years tested", "Avg difficulty"], stable_rows)}

Key reading:

- Stable does not mean low difficulty. Stable subtopics become harder when embedded in experiments, figures, multi-statement choices, or negated stems.
- The strongest stable objectives have high hit count and high year breadth.
- Students should master these before spending heavy time on low-frequency details.

## Prioritized Learning Objectives

This is the main action table. It ranks knowledge subtopics by frequency, stage stability, year breadth, late-stage relevance, and cognitive load.

{md_table(["Rank", "Tier", "Subtopic", "Pillar", "Hits", "Priority", "Early/Middle/Late", "Years", "Learning objective"], priority_rows)}

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

{md_table(["Knowledge subtopic", "Pillar", "Primary questions", "Data/figure/table questions", "Share"], data_topic_rows)}

Interpretation:

- Visual and table-heavy questions are not a separate chapter. They cluster around physiology, genetics, plants, ecology, molecular methods, and development.
- Practice should tag both the knowledge objective and the representation skill, for example `cardiovascular/renal physiology + graph/table`, or `plant development + figure interpretation`.

## Experimental Design And Controls By Knowledge Topic

This replaces the overly broad `Experimental design, controls & inference` subtopic. Experimental design is a cross-cutting reasoning skill, but the exam usually anchors it in a concrete biological system.

{md_table(["Knowledge subtopic", "Pillar", "Primary questions", "Experimental/control questions", "Share"], experiment_topic_rows)}

Interpretation:

- Experimental reasoning is strongest in molecular/cell biology, microbiology/pathogens, development, physiology, plant mechanisms, and lab-method contexts.
- BioBloom should generate experimental questions by choosing a knowledge target first, then adding variables, controls, mutants, expected results, and distractors.

## Subtopics Rising In The Late Stage

These knowledge subtopics are more prominent in 2014-2018 than in 2003-2008.

{md_table(["Subtopic", "Pillar", "Early", "Middle", "Late", "Late-minus-early", "Late share"], late_rows)}

Interpretation:

- Modern difficulty comes from combinations: molecular mechanisms plus experiments, genetics plus technology, physiology plus signaling, and plants plus molecular/developmental logic.
- Late-rising subtopics should anchor advanced practice sets and final-stage diagnostics.

## Early-Weighted Or Declining Subtopics

These knowledge subtopics appear more in early exams than late exams. They are useful for breadth, but they should not dominate a modern-practice plan.

{md_table(["Subtopic", "Pillar", "Early", "Middle", "Late", "Early-minus-late", "Years"], early_rows)}

Interpretation:

- Early-weighted does not mean obsolete. It means later exams are less likely to test the topic as a direct recognition item.
- For modern practice, convert early-weighted topics into mechanism, data, or experiment variants rather than repeating simple recall.

## Stage-Only Subtopics

Late-only knowledge subtopics in this heuristic pass:

{md_table(["Subtopic", "Pillar", "Late hits", "Years", "Avg difficulty"], late_only_rows or [["-", "-", "-", "-", "-"]])}

Early-only knowledge subtopics in this heuristic pass:

{md_table(["Subtopic", "Pillar", "Early hits", "Years", "Avg difficulty"], early_only_rows or [["-", "-", "-", "-", "-"]])}

Caution: stage-only classification is sensitive to keyword rules and the available 2003-2018 window. Use this as a manual-review prompt, not as a reason to delete a topic.

## Format And Reasoning Tags By Stage

These are not knowledge subtopics, but they strongly affect difficulty and should become separate BioBloom metadata fields.

{md_table(["Reasoning / format tag", "Questions", "Early", "Middle", "Late", "Share of corpus"], tag_rows)}

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

{md_table(["Subtopic", "Pillar", "Hits", "Early", "Middle", "Late", "Stage breadth", "Year breadth", "Years", "Avg diff", "Priority"], appendix_rows)}
"""
    REPORT_PATH.write_text(content)


def main() -> None:
    questions = parse_questions()
    subtopic_rows = aggregate_subtopics(questions)
    reasoning_rows = aggregate_reasoning_by_topic(questions)
    export_data(questions, subtopic_rows, reasoning_rows)
    plot_paths = render_plots(subtopic_rows, reasoning_rows)
    render_report(questions, subtopic_rows, reasoning_rows, plot_paths)
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {QUESTION_TAGS_JSONL}")
    print(f"Wrote {SUBTOPIC_SUMMARY_CSV}")
    print(f"Wrote {REASONING_TOPIC_CSV}")
    print(f"Wrote {DATA_JSON}")
    for path in plot_paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
