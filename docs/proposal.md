# BioBloom / Adaptive USABO Trainer — Proposal

## 1. Purpose

Build a private learning system to help Cindy prepare for the USABO Open Exam while studying *Campbell Biology, 12th Edition*.

BioBloom should help her move from textbook understanding to olympiad-style reasoning through high-quality multiple-choice practice, layered hints, explanations, wrong-answer review, and targeted follow-up practice.

This document is intentionally a proposal, not a detailed design. Detailed implementation choices should be handled later in `design.md`.

---

## 2. Product Vision

BioBloom should feel like a supportive biology training companion, not an exam machine.

Core experience:

```text
Cindy studies a Campbell chapter
  → practices related questions
  → gets hints when stuck
  → reviews explanations
  → sees why wrong choices are wrong
  → revisits weak concepts
  → receives targeted repair practice
```

Strong framing:

> An AI-assisted USABO calibration and question-quality pipeline plus an adaptive practice system.

Weak framing to avoid:

> A generic AI chatbot that randomly generates biology quizzes.

---

## 3. Key Context and Constraints

### USABO past exams are the calibration foundation

The project should start by importing and parsing available official USABO Open Exam materials for private study and calibration.

Purpose of the USABO calibration bank:

- understand real Open Exam difficulty
- map topic distribution
- identify recurring reasoning patterns
- identify common traps and distractor styles
- connect USABO-style questions back to Campbell chapters and concepts
- evaluate whether generated questions are too easy, too vague, or too unlike USABO

This component is foundational. Without it, generated questions will likely drift toward generic AP Biology difficulty instead of real USABO style.

Important constraint: official USABO materials are proprietary. They should be used privately and carefully. BioBloom should generate original questions that imitate reasoning patterns, not copy official wording or create near-duplicates.

### Campbell is the knowledge foundation

Campbell Biology is the primary learning source. The system should convert each chapter into original, structured learning material:

- concept summaries
- concept cards
- figure notes
- common misconceptions
- USABO reasoning angles
- question blueprints

The system should avoid publicly redistributing Campbell text or page images. Private local processing is acceptable for development and personal study, but the public repo should contain code and synthetic/sample content only.

### Question quality is the main risk

The web app is straightforward. The hard part is creating questions that are:

- biologically correct
- unambiguous
- useful for learning
- close to USABO style
- supported by source concepts
- equipped with good distractors and explanations

AI can produce many questions quickly, but raw outputs will often be too easy, repetitive, ambiguous, or subtly wrong. The project should optimize for quality before scale.

### Runtime API cost should be avoided at first

The preferred path is not to make direct paid API calls from the BioBloom app.

Instead, use local AI coding/agent tools during development and content production:

- Codex CLI
- Claude Code
- Gemini CLI

These tools can help parse, label, author, critique, validate, and organize content. BioBloom itself should initially work without requiring paid AI API calls at runtime.

Recommended principle:

> AI-assisted content production, not AI-dependent runtime.

---

## 4. High-Level Strategy

BioBloom should be built as an offline-first adaptive quiz system with an AI-assisted authoring, calibration, and validation pipeline.

High-level flow:

```text
USABO past exams
  → private calibration bank
  → style, topic, difficulty, and reasoning-pattern guidance

Campbell chapter PDFs
  → source-preserving Markdown extraction
  → LLM-maintained chapter wiki
  → concept cards and figure notes
  → question blueprints
  → original candidate questions
  → multi-model critique and validation
  → reviewed question bank
  → student practice and adaptive review
```

The most important separation:

```text
Campbell-derived wiki = truth and concept grounding
USABO calibration bank = style and difficulty calibration
Student attempt history = personalization
```

---

## 5. Phase 0: USABO Calibration Bank

Before generating many new questions, build a private calibration bank from available past USABO Open Exams.

This bank should store metadata, not only raw questions.

Useful labels:

- year
- question number
- answer key
- USABO topic area
- Campbell chapter mapping
- concept and subskill
- reasoning type
- difficulty estimate
- trap or misconception tested
- question type: recall, application, data interpretation, calculation, cross-topic reasoning
- notes about why the question feels USABO-like

This phase should answer:

```text
What does a real USABO Open question look like?
Which Campbell chapters are most represented?
What reasoning patterns appear repeatedly?
How hard should a generated question be to count as USABO-style?
```

---

## 6. Campbell Content Pipeline

The Campbell pipeline should be concept-first, but it should preserve the original PDF page structure for traceability.

Recommended high-level flow:

```text
PDF chapter
  → page images + raw extracted text
  → cleaned page-level Markdown
  → LLM-maintained chapter wiki
  → concept cards
  → question blueprints
  → candidate questions
  → validation
  → reviewed question bank
```

### PDF parsing direction

PyMuPDF is a good fit and should be the first-choice parser for the initial pipeline.

Use PyMuPDF to extract:

- page text
- page numbers
- text blocks and approximate layout
- images or rendered page screenshots
- figure captions when detectable
- coordinates when useful for reconstructing layout

For Campbell chapters, raw text extraction alone is not enough because many pages contain important diagrams, figure labels, tables, microscopy images, and scientific-skills exercises. Therefore, each page should preserve both:

```text
1. extracted text
2. rendered page image
```

The rendered page image gives local AI agents visual context when text extraction loses layout or diagram meaning.

### Source-preserving Markdown

The first output should be page-level raw Markdown, not final study notes.

Example structure:

```text
raw/campbell_12e/ch06/
  source.pdf
  pages/
    page_093.png
    page_094.png
  extracted/
    page_093.raw.md
    page_094.raw.md
```

Each raw Markdown page should preserve:

- book page number
- PDF page number
- source file
- link to rendered page image
- extracted text
- detected headings
- detected figure captions
- notes about visual elements that need review

The raw extraction can be imperfect. It should not be treated as the final learning layer.

---

## 7. LLM Wiki Instead of Early Vector DB / RAG

For the early version, BioBloom should use an LLM Wiki approach rather than immediately building a vector database or complex RAG system.

Reasoning:

- the project scope is bounded by Campbell chapters and USABO preparation
- local AI agents can work effectively over Markdown files
- the wiki can accumulate curated knowledge over time
- source anchors can preserve traceability
- Markdown is easy to review, edit, diff, and version-control
- vector search can be added later if needed

The wiki is the compiled knowledge layer. It should contain original summaries and learning structures, not long copied textbook passages.

Suggested high-level structure:

```text
wiki/campbell_12e/ch06/
  index.md
  overview.md
  concepts/
    concept-6-1-microscopy.md
    concept-6-2-compartmentalization.md
    concept-6-3-nucleus-ribosomes.md
  figures/
    figure-6-7-surface-area-volume.md
    figure-6-8-eukaryotic-cells.md
  skills/
    scale-bar-volume-surface-area.md
  misconceptions.md
  usabo-angles.md
  log.md
```

Each concept page should include, at a high level:

- core idea
- must-know facts
- mechanisms
- important figures
- common misconceptions
- useful distractor ideas
- USABO reasoning angles
- source anchors back to raw pages

Each important figure should become a first-class learning object when it has question-generation value.

Examples of figure-level value:

- microscopy comparison figures can support method-selection questions
- surface-area-to-volume diagrams can support quantitative reasoning questions
- animal/plant cell diagrams can support organelle function and comparison questions
- scientific-skills exercises can support data interpretation and calculation questions

---

## 8. Local AI Authoring and Validation Pipeline

Use local AI tools as the orchestration and content-production layer, not as a runtime dependency for the student app.

Possible workflow:

```text
1. Parse USABO Open Exam PDFs into private calibration files.
2. Label official questions by topic, skill, difficulty, and reasoning pattern.
3. Parse Campbell chapter PDFs with PyMuPDF into page images and raw Markdown.
4. Use local AI agents to build and maintain the chapter wiki.
5. Generate concept cards from the wiki.
6. Generate question blueprints using both Campbell concepts and USABO calibration patterns.
7. Generate original candidate MCQs from the blueprints.
8. Use another model/tool to solve questions without seeing the answer key.
9. Use another model/tool to critique ambiguity, factual grounding, and distractor quality.
10. Save accepted questions as reviewed JSON or Markdown.
11. Import reviewed questions into BioBloom.
```

The models should not simply vote. They should play different roles:

```text
Generator: creates original question candidates
Solver: solves independently without seeing the key
Skeptic: tries to find ambiguity or multiple correct answers
Fact checker: checks source grounding against the wiki
Teacher: improves explanations, hints, and misconception feedback
Calibrator: compares style and difficulty against USABO patterns
```

---

## 9. Question Quality Requirements

A high-quality question should have:

- one clearly correct answer
- plausible distractors
- explanation of the correct answer
- explanation of why each wrong answer is wrong
- misconception tag for each wrong answer
- difficulty level
- chapter and concept tags
- reasoning type
- hint ladder
- source basis from concept notes or figure notes
- calibration notes when it imitates a USABO-style reasoning pattern

Reject or rewrite a question if:

- more than one answer could be correct
- the correct answer depends on an unstated assumption
- the explanation contradicts the answer
- the question relies on unsupported biology facts
- distractors are silly or non-diagnostic
- difficulty comes from confusing wording rather than real reasoning
- it is too similar to an official or existing question
- it is AP-level recall while labeled as USABO-style

---

## 10. Adaptive Learning Direction

The student-facing system should track more than correct or incorrect.

Useful signals:

- selected answer
- wrong-answer misconception tag
- time spent
- hint level used
- confidence level
- repeated mistakes on similar concepts
- improvement or regression over time

The adaptive loop should distinguish between:

- missing a fact
- misunderstanding a mechanism
- misreading a graph
- making a calculation error
- falling for the same misconception repeatedly
- knowing the idea but being too slow or uncertain

Early adaptation can be deterministic and tag-based. It does not require runtime AI.

Example:

```text
If Cindy repeatedly misses questions tagged membrane_transport,
show more reviewed membrane_transport questions.

If she chooses distractors tagged protein_transport_always_active,
show a repair card and targeted questions comparing facilitated diffusion and active transport.
```

---

## 11. MVP Scope

The MVP should avoid overbuilding.

Minimum useful product:

- private web app
- chapter selection
- multiple-choice practice
- layered hints
- explanations
- wrong-answer review
- skill and misconception tags
- basic progress dashboard
- import reviewed questions from JSON or Markdown
- simple admin/review workflow

Start with a few high-yield Campbell areas:

- cells and membranes
- cellular respiration
- photosynthesis
- cell communication
- cell cycle
- meiosis
- Mendelian genetics

For each chapter, aim for a reviewed set of roughly 60–80 questions over time, not necessarily all at once.

---

## 12. Future Enhancements

Possible later improvements:

- timed USABO-style practice mode
- mock Open Exam mode
- spaced repetition scheduling
- stronger mastery model
- richer local AI-assisted admin tools
- optional free-tier Gemini API automation where appropriate
- automated question validation reports
- personalized repair-question generation
- support for advanced sources beyond Campbell
- vector search or RAG if the Markdown wiki becomes too large or difficult for local agents to navigate

These should not block the MVP.

---

## 13. Development Philosophy

Build the system in layers:

```text
1. USABO calibration bank
2. Campbell PDF-to-Markdown extraction
3. LLM-maintained chapter wiki
4. Reviewed static question bank
5. Practice UI
6. Wrong-answer review
7. Tag-based adaptation
8. Local AI-assisted authoring workflow
9. Optional runtime AI features
```

Avoid over-designing early. Keep the system flexible enough that `design.md` can later decide the exact stack, schema, storage format, and AI orchestration details.

The first meaningful milestone should be:

> Cindy can select a chapter, answer reviewed MCQs, see hints and explanations, and review her mistakes.

The first content milestone should be:

> One Campbell chapter is parsed with PyMuPDF, converted into a source-preserving Markdown/wiki structure, and used to produce a small reviewed set of original USABO-style questions.

---

## 14. Summary

BioBloom is feasible and valuable if it focuses on quality-controlled practice rather than live AI generation.

The best near-term path is:

```text
Use USABO past exams as private calibration.
Use PyMuPDF to parse Campbell chapters into text plus page images.
Use an LLM Wiki to maintain source-grounded concept knowledge.
Use local AI tools to produce and critique original questions.
Store reviewed content in the app.
Use deterministic app logic for practice, review, and adaptation.
Add optional AI automation only after the core system works.
```

This keeps cost low, avoids paid runtime API dependency, respects source constraints, and makes the project immediately useful for Cindy.
