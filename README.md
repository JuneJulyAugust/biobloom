# BioBloom

BioBloom is a private, web-based learning system for Cindy's USABO Open Exam preparation while she studies *Campbell Biology, 12th Edition*.

The goal is not to generate random quizzes. The goal is to build an AI-assisted question pipeline and an adaptive practice system that can:

- generate high-quality multiple-choice practice
- provide layered hints and clear explanations
- diagnose wrong answers by misconception
- surface targeted follow-up questions
- support spaced review for weaker concepts

## Project Direction

The proposal frames the system as a loop:

```text
Campbell study progress
  -> concept understanding
  -> USABO-style practice questions
  -> answers and feedback
  -> misconception diagnosis
  -> targeted repair questions
  -> spaced review
```

The main risk is question quality. The system should optimize for correctness, clarity, and USABO-style reasoning before it scales to a large question bank.

## Learning Model

For each chapter, the system should support a mixed set of questions, usually around 60 to 80 total:

- core-understanding questions
- application and reasoning questions
- data, graph, or experiment interpretation
- quantitative questions where appropriate
- misconception-targeted questions

The mix should vary by topic. Genetics, for example, should lean harder on calculations and data interpretation than ecology.

## Content Pipeline

The intended content flow is:

```text
chapter notes
  -> concept cards
  -> question blueprints
  -> candidate questions
  -> validation
  -> accepted question bank
```

This project should generate structured, original content instead of copying official exams or textbook text.

## Quality Requirements

Each question should eventually carry metadata such as:

- chapter
- concept
- skill being tested
- difficulty
- reasoning type
- misconception tags
- hint ladder
- source basis

That metadata is what makes adaptive review and wrong-answer diagnosis useful.

## Repository Notes

- `docs/proposal.md` captures the product direction and constraints.
- Raw source documents such as PDF and Word files should be stored with Git LFS.
- The web app implementation has not started yet; this repository is being set up with the initial project scaffold.

## Next Steps

- define the technical design in `docs/design.md`
- choose the web stack
- model concepts, blueprints, and question metadata
- implement the practice flow and review loop
