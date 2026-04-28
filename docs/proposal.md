# BioBloom — Proposal

## 1. Purpose

BioBloom is a private learning system to help Cindy prepare for the USABO Open Exam while studying *Campbell Biology, 12th Edition*.

The goal is to help her move from textbook understanding to olympiad-style reasoning through high-quality multiple-choice practice, hints, explanations, wrong-answer review, and targeted follow-up practice.

This document is intentionally a proposal, not a detailed design. Implementation details should live later in `design.md`.

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

The strong framing is:

> An AI-assisted USABO calibration and question-quality pipeline plus an adaptive practice system.

The weak framing to avoid is:

> A generic AI chatbot that randomly generates biology quizzes.

---

## 3. Key Context and Constraints

### USABO past exams are the calibration foundation

The project should start by importing and parsing the available official USABO Open Exam materials for private study and calibration.

The official USABO Training Resource Center states that past Open Exams and answer keys are available for 2003–2018 and are useful for understanding the breadth and depth of USABO content. It also states that the exams are proprietary property of the Center for Excellence in Education and may not be distributed or stored electronically without permission.

Therefore, BioBloom should use these materials carefully:

- Use them privately for Cindy’s practice if permitted by the source terms.
- Use them as the main calibration set for topic distribution, difficulty, style, and reasoning patterns.
- Do not copy official questions into a public product.
- Do not generate near-duplicates of official questions.
- Generate original questions that imitate reasoning patterns, not wording.

This calibration bank is not optional. Without it, generated questions will likely drift toward generic AP Biology difficulty instead of real USABO style.

### Question quality is the main risk

The web app is straightforward. The hard part is creating questions that are correct, unambiguous, useful, and close to USABO style.

AI can produce many questions quickly, but many raw outputs will be too easy, repetitive, ambiguous, or subtly wrong. The project should optimize for quality before scale.

### Runtime API cost should be avoided at first

The preferred path is not to make direct paid API calls from the BioBloom app.

Instead, use local AI coding/agent tools such as:

- Codex CLI
- Claude Code
- Gemini CLI

These tools can help parse, label, author, critique, validate, and organize question content during development. BioBloom itself should initially work without requiring paid AI API calls at runtime.

### Copyright must be respected

Campbell Biology and official USABO exams should not be copied into a public product or redistributed without permission.

Safe usage direction:

- use original notes, summaries, concept cards, and page references
- use official past USABO exams privately for practice and calibration
- use past exams to understand style, topic distribution, difficulty, and reasoning patterns
- generate original questions rather than copying official questions

---

## 4. Core Strategy

BioBloom should be built as an **offline-first adaptive quiz system** with an **AI-assisted authoring and calibration pipeline**.

That means:

```text
Past USABO exams calibrate style and difficulty.
Campbell concepts provide the knowledge foundation.
AI helps create and validate original content before use.
The app serves reviewed content during practice.
```

This avoids the cost and reliability issues of live question generation while still benefiting from AI.

Recommended principle:

> AI-assisted content production, not AI-dependent runtime.

---

## 5. Phase 0: USABO Calibration Bank

Before generating many new questions, BioBloom should build a private calibration bank from available past USABO Open Exams.

Purpose:

- understand real USABO difficulty
- map topic distribution
- identify recurring reasoning patterns
- identify common traps and distractors
- connect official-style questions back to Campbell chapters
- provide benchmark examples for evaluating generated questions

The calibration bank should store metadata, not just raw questions.

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
- whether it is recall, application, data interpretation, calculation, or cross-topic reasoning

Example metadata shape:

```json
{
  "source": "USABO Open Exam",
  "year": 2018,
  "question_number": 17,
  "topic_area": "Genetics and Evolution",
  "campbell_chapters": ["Meiosis", "Mendelian Genetics"],
  "skill": "linkage_mapping",
  "reasoning_type": "quantitative_inference",
  "difficulty": 4,
  "trap": "confuses recombinant and parental classes",
  "usage": "private_calibration"
}
```

This phase should produce a calibration dataset that can answer:

```text
What does a real USABO Open question look like?
Which Campbell chapters are most represented?
What reasoning patterns appear repeatedly?
How hard should a generated question be to count as USABO-style?
```

---

## 6. Campbell Content Pipeline

After the calibration bank exists, build chapter-level content from Campbell.

A good content pipeline should be concept-first:

```text
Campbell chapter
  → concept cards
  → question blueprints
  → candidate original questions
  → AI critique and validation
  → reviewed question bank
  → practice and review
```

### Concept cards

A concept card is a concise, original summary of a teachable biological idea.

It may include:

- core idea
- must-know facts
- common misconceptions
- related concepts
- possible USABO-style reasoning patterns

### Question blueprints

A blueprint defines what a question should test before the final wording is generated.

It may include:

- target concept
- skill being tested
- reasoning pattern
- difficulty target
- misconception trap
- expected reasoning steps
- question type, such as experiment interpretation or mechanism prediction

This prevents shallow prompts like:

```text
Generate 80 USABO questions for Chapter 7.
```

A better approach is:

```text
Generate question blueprints for membrane transport.
Use the USABO calibration bank to match style and difficulty.
Then generate original MCQs from those blueprints.
```

---

## 7. Local AI Pipeline

Because paid runtime API calls are not desired, local agent tools should be used as the content production and review environment.

Possible workflow:

```text
1. Parse available USABO Open Exam PDFs into structured private calibration files.
2. Use local AI tools to label each official question by topic, skill, difficulty, and reasoning pattern.
3. Prepare Campbell chapter notes or concept cards.
4. Generate question blueprints using both Campbell concept cards and USABO calibration patterns.
5. Generate original candidate MCQs from the blueprints.
6. Use another model/tool to solve the questions without seeing the answer key.
7. Use another model/tool to critique ambiguity, factual grounding, and distractor quality.
8. Save accepted questions as JSON or Markdown.
9. Import reviewed questions into BioBloom.
```

The models should not simply vote. They should play different roles:

```text
Parser / Labeler      → extracts and tags calibration questions
Generator             → creates original candidate questions
Independent Solver    → answers without seeing the key
Skeptic               → looks for ambiguity or multiple correct answers
Fact Auditor          → checks whether biology claims are grounded
USABO Calibrator      → checks whether difficulty/style match real Open Exam patterns
Pedagogy Auditor      → improves hints, explanations, and misconception diagnosis
Rewriter              → improves wording and clarity
```

This makes the AI pipeline useful even without a paid API backend.

---

## 8. Question Quality Requirements

A high-quality generated question should have:

- one clearly correct answer
- plausible distractors
- explanation of the correct answer
- explanation of why each wrong answer is wrong
- misconception tag for each wrong answer
- difficulty level
- chapter and concept tags
- reasoning type
- hint ladder
- source basis from notes or concept cards
- calibration reference to a USABO-style reasoning pattern, without copying the official question

Reject or rewrite questions if:

- more than one answer could be correct
- the answer depends on an unstated assumption
- the explanation contradicts the answer
- the question relies on unsupported facts
- distractors are silly or non-diagnostic
- difficulty comes from confusing wording rather than real reasoning
- it is too similar to an official or existing question
- it is AP-level recall while labeled as USABO-style

---

## 9. Adaptive Learning Direction

BioBloom should track more than right or wrong.

Useful signals include:

- selected answer
- wrong-answer misconception tag
- time spent
- hint level used
- confidence level, if Cindy enters it
- repeated mistakes across related concepts

The adaptive logic can start simple and does not require live AI:

```text
If Cindy repeatedly misses questions tagged `membrane_transport`, show more membrane transport questions.

If she repeatedly chooses distractors tagged `protein_transport_always_active`, show review material and targeted questions for that misconception.
```

Later, AI can help generate new repair sets, but the MVP should work from the reviewed question bank.

---

## 10. MVP Scope

The first useful version should be small and practical.

Recommended MVP:

- private web app
- USABO calibration import/labeling workflow
- chapter selection
- multiple-choice practice
- stored hints
- stored explanations
- wrong-answer review
- skill and misconception tags
- basic progress dashboard
- import questions from JSON or Markdown
- simple admin/review workflow

Start with two parallel tracks:

### Track A: Calibration

Import and label available USABO Open Exam questions enough to understand style, difficulty, and topic distribution.

### Track B: Campbell practice

Start with a few high-yield Campbell areas:

- cells and membranes
- cellular respiration
- photosynthesis
- cell communication
- cell cycle
- meiosis
- Mendelian genetics

For each chapter, aim for a reviewed set of roughly 60–80 original questions over time, not necessarily all at once.

---

## 11. Future Enhancements

Possible later improvements:

- timed USABO-style practice mode
- mock Open Exam mode
- spaced repetition scheduling
- stronger mastery model
- local AI-assisted admin tools
- optional Gemini API free-tier automation
- automated question validation reports
- personalized repair-question generation
- support for advanced sources beyond Campbell
- deeper analysis of official exam trends by year and topic

These should not block the MVP.

---

## 12. Development Philosophy

Build the system in layers:

```text
1. USABO calibration bank
2. Reviewed static original question bank
3. Practice UI
4. Wrong-answer review
5. Tag-based adaptation
6. AI-assisted authoring workflow
7. Optional runtime AI features
```

Avoid over-designing early. Keep the system flexible enough that `design.md` can later decide the exact stack, schema, storage format, and AI orchestration details.

The first milestone should be simple:

> Cindy can select a chapter, answer reviewed MCQs, see hints and explanations, and review her mistakes.

But the first project foundation should be:

> BioBloom understands what real USABO Open questions look like through a private calibration bank.

---

## 13. Summary

BioBloom is feasible and valuable, especially if the project focuses on quality-controlled practice rather than live AI generation.

The best near-term path is:

```text
Import and label available USABO Open Exam materials for private calibration.
Use local AI tools to produce and critique original content.
Store reviewed content in the app.
Use deterministic app logic for practice, review, and adaptation.
Add optional AI automation only after the core system works.
```

This keeps cost low, avoids runtime API dependency, respects copyright boundaries, and makes the project immediately useful for Cindy.
