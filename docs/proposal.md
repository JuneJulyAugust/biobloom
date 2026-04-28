# BioBloom / Adaptive USABO Trainer — Proposal

## 1. Purpose

Build a private web-based learning system to help Cindy prepare for the USABO Open Exam while studying *Campbell Biology, 12th Edition*.

The product should help her move from textbook understanding to olympiad-style reasoning by giving her high-quality multiple-choice practice, useful hints, clear explanations, wrong-answer review, and targeted follow-up questions based on her weaknesses.

This proposal captures the project direction and core thinking. Detailed implementation choices should be handled later in a separate `design.md`.

---

## 2. Core Idea

The project is not simply an AI quiz generator.

The better framing is:

> An AI-assisted question-quality pipeline plus an adaptive practice system.

The system should eventually support this loop:

```text
Campbell study progress
  → concept understanding
  → USABO-style practice questions
  → Cindy answers questions
  → system diagnoses mistakes
  → system suggests review and generates targeted repair questions
  → spaced review strengthens retention
```

The key challenge is not building the web app. The key challenge is making the questions **correct, unambiguous, useful, and close to USABO style**.

---

## 3. Student and Learning Context

Cindy is preparing for the USABO Open Exam. She is reading Campbell Biology and needs practice after each chapter.

For each chapter, the desired system should generate or provide roughly **60–80 questions**, with a flexible mix such as:

- about 20 core-understanding questions
- application and reasoning questions
- data, graph, or experiment interpretation questions
- quantitative questions when appropriate
- misconception-targeted questions

The exact split should vary by chapter. For example, genetics may need more calculation and data interpretation, while ecology may need more scenario reasoning.

---

## 4. Product Vision

The system should feel like a supportive biology training companion, not an exam machine.

Core user experiences:

- Cindy selects a Campbell chapter or weak topic
- she answers multiple-choice questions
- she can request hints in layers
- after answering, she sees the correct reasoning
- if she is wrong, the system explains the likely misconception
- wrong questions are saved for review
- the system tracks weak concepts and generates targeted follow-up practice

A strong version of the product is:

```text
AI-powered USABO reasoning practice with misconception diagnosis and adaptive repair
```

A weak version to avoid is:

```text
Generic biology chatbot that generates random quizzes
```

---

## 5. Important Constraints

### Question quality is the main risk

AI can easily generate many questions, but many will be too easy, ambiguous, repetitive, or subtly wrong. The project should optimize for question quality before scale.

### Campbell and USABO copyright must be respected

Campbell Biology and official USABO exams should not be copied into a public product or redistributed without permission.

Safe usage direction:

- use personal notes, summaries, concept cards, and page references
- use official past USABO exams privately for practice and calibration
- use past exams to understand style, topic distribution, difficulty, and reasoning patterns
- generate original questions rather than copying official questions

### Campbell is necessary but may not be sufficient long term

Campbell is a strong foundation for the Open Exam, especially early on. If Cindy later targets Semifinals or very high performance, the system may need additional source summaries for plant physiology, animal physiology, biochemistry, ecology, and other advanced topics.

---

## 6. Consensus From Brainstorming

Across GPT, Claude, and Gemini responses, the main agreements were:

1. The project is feasible.
2. The hard part is question quality, not web development.
3. Do not simply prompt: “generate 80 questions for this chapter.”
4. Generate from structured concepts or blueprints instead.
5. Use past USABO exams as calibration, not copied content.
6. Use multiple AI models to review and criticize generated questions.
7. Distractors should represent real misconceptions.
8. Each question needs metadata: chapter, concept, skill, difficulty, reasoning type, and misconception tags.
9. Hints should be layered so they guide without giving away the answer.
10. Human review and flagging should exist, especially for high-confidence or mock-exam questions.

---

## 7. Proposed Content Pipeline

A good generation pipeline should be concept-first:

```text
chapter notes
  → concept cards
  → question blueprints
  → candidate questions
  → validation
  → accepted question bank
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

A blueprint defines the question before wording is generated.

It may include:

- target concept
- skill being tested
- reasoning pattern
- difficulty target
- misconception trap
- expected reasoning steps
- question type, such as experiment interpretation or mechanism prediction

This prevents the AI from producing shallow recall questions.

### Candidate questions

For each chapter, generate more questions than needed, then reject weak ones.

A reasonable early expectation:

```text
Generate 100–150 candidates → keep the best 60–80
```

---

## 8. Multi-Model Critique Strategy

Yes, GPT, Claude Opus, and Gemini can be used to criticize each other. But they should not be used as simple majority voters.

Better approach:

```text
Model A: generate the question
Model B: solve it independently without seeing the answer
Model C: search for ambiguity or multiple correct answers
Model D: check factual grounding
Model E: improve explanation, hints, and misconception diagnosis
```

The goal is to make each model detect a different failure mode.

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
- source basis from concept notes

Example misconception-tagged distractors:

- confusing facilitated diffusion with active transport
- thinking dominant traits are always common
- assuming cholesterol always increases membrane fluidity
- confusing sister chromatids with homologous chromosomes
- thinking the Calvin cycle directly produces oxygen

This metadata is what enables useful wrong-answer diagnosis later.

---

## 10. Adaptive Learning Direction

The system should track more than correct or incorrect.

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

When Cindy misses a question, the system should give specific feedback, for example:

```text
You may be associating all protein-mediated transport with active transport.
But facilitated diffusion also uses proteins and does not require ATP when movement is down the gradient.
Next, practice questions comparing simple diffusion, facilitated diffusion, primary active transport, and secondary active transport.
```

---

## 11. Product Scope

### MVP goal

Start small and prove the quality loop.

Recommended MVP:

- private web app
- 3–5 high-yield Campbell chapters
- 200–400 validated questions
- chapter practice mode
- hints
- explanations
- wrong-question review
- basic weakness dashboard
- question flag/review workflow

Initial high-yield chapters may include:

- cell structure
- membranes
- cellular respiration
- photosynthesis
- cell communication
- cell cycle
- meiosis
- Mendelian genetics

Do not start by covering the entire Campbell book. First prove that the system can generate 50 genuinely good questions from one chapter.

---

## 12. Suggested Development Phases

### Phase 0 — Calibration and taxonomy

- collect official/public USABO past exams for private reference
- study topic distribution and reasoning patterns
- define initial topic, skill, difficulty, and misconception taxonomies
- label a small sample of historical questions for calibration

### Phase 1 — Concept cards

- create concept cards for a few high-yield Campbell chapters
- map each card to USABO topic areas and likely question types
- identify common misconceptions

### Phase 2 — Question generation and validation

- generate question blueprints
- generate candidate MCQs
- run multi-model critique
- reject, rewrite, or accept questions
- manually inspect early outputs

### Phase 3 — Practice web app

- chapter practice UI
- multiple-choice answering
- hint ladder
- explanation and wrong-answer feedback
- attempt history
- question flagging

### Phase 4 — Adaptive review

- track mastery by concept or skill
- detect repeated misconception patterns
- generate targeted repair questions
- schedule spaced review

### Phase 5 — Mock exam and gold bank

- human-review best questions
- mark trusted questions as Gold
- build timed Open Exam simulation
- generate performance reports by USABO topic area

---

## 13. Minimal Data Concepts

Detailed database design should go into `design.md`, but the system will likely need these core entities:

- Student
- Chapter
- ConceptCard
- QuestionBlueprint
- Question
- AnswerChoice
- Attempt
- MisconceptionTag
- SkillMastery
- ReviewFlag

A question should store enough metadata to support diagnosis and adaptive review, not just stem, choices, and answer.

---

## 14. Main Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Factual hallucination | source-grounded concept cards, factual audit, human review |
| Ambiguous questions | independent solver, skeptic model, review flagging |
| Too easy / AP-level questions | USABO calibration examples and difficulty rubric |
| Weak distractors | require misconception-linked distractors |
| Generic feedback | use selected wrong answer and misconception tag |
| Repetitive generated questions | track question type, concept, reasoning pattern, and similarity |
| Copyright issues | use private notes and original questions; avoid redistribution of protected content |

---

## 15. Success Criteria

The first milestone is not thousands of questions.

The first milestone is:

> Can the system produce 50 high-quality, validated, misconception-tagged questions from one Campbell chapter that Cindy finds useful?

If yes, the project can scale.

If no, generating more questions will only create a larger low-quality bank.

Early success indicators:

- Cindy enjoys using it
- explanations are actually helpful
- wrong-answer feedback feels specific, not generic
- questions are challenging but fair
- parent/admin can flag and improve weak questions
- the system identifies recurring blind spots correctly

---

## 16. Final Recommendation

Start with the question-quality pipeline, not the full product.

Recommended first sprint:

```text
1. Pick one Campbell chapter.
2. Create 10–20 concept cards.
3. Generate 50–100 candidate questions.
4. Use multi-model critique to filter them.
5. Manually review the best 30–50.
6. Build a simple practice UI.
7. Let Cindy try it and collect feedback.
```

The long-term product can become an adaptive USABO training system, but the project should earn that complexity gradually.

The guiding principle:

> Quality first, adaptation second, scale third.
