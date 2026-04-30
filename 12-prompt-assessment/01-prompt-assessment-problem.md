# Prompt Engineering Assessment (Production-Grade)

## Context
You are building a healthcare AI assistant similar to Practo.

## Task
Design a production-grade prompt for a Medical QA system using RAG.

## Input

### User Query
What are the symptoms and treatment options for hypertension?

### Context
Hypertension (high blood pressure) is a chronic condition.

Common symptoms:
- Headache
- Dizziness
- Nosebleeds (rare)

Treatment:
- Lifestyle changes (diet, exercise)
- Medications (ACE inhibitors, beta-blockers)

## Constraints
- No hallucination
- Use only provided context
- No diagnosis
- Structured JSON output

## Output Format
{
  "condition": "",
  "symptoms": [],
  "treatment": [],
  "confidence": "",
  "notes": ""
}

## Requirements
- Role definition
- Task clarity
- Constraints
- Output schema
- Safety

## Evaluation Criteria
- Structure
- Grounding
- Safety
- Schema correctness
- Edge cases

## Deliverables
- Final prompt
- Explanation
- Example output
