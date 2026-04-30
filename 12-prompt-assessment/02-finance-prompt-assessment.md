
# Prompt Engineering Assessment #2 (Finance – Production Grade)

## Context
You are building an AI-powered financial assistant for a platform similar to Zerodha or Groww.

The assistant must:
- Analyze stock-related queries
- Use structured financial data (RAG-style input)
- Avoid speculation and hallucination
- Provide safe, non-advisory responses
- Output structured data

---

## Problem Statement

### Task
Design a production-grade prompt for a:

Stock Analysis Assistant (RAG-based + risk-aware + structured output)

---

## Inputs

### User Query
Should I invest in Infosys right now?

### Context
Company: Infosys Ltd.

Recent Performance:
- Revenue growth: 6% YoY
- Net profit growth: 4% YoY

Market Sentiment:
- Analyst consensus: Neutral
- Recent news: Stable outlook, cautious IT spending

Valuation:
- P/E ratio: 28
- Sector average P/E: 25

Risks:
- Slowdown in global IT demand
- Currency fluctuations

---

## Constraints

- No financial advice (no Buy/Sell)
- No prediction of prices
- Use only provided context
- No hallucination
- If insufficient → say "Insufficient data"
- Structured output required

---

## Output Format

{
  "company": "",
  "summary": "",
  "positives": [],
  "risks": [],
  "valuation_comment": "",
  "recommendation": "",
  "confidence": ""
}

---

## Requirements

### Prompt must include:
- Role definition
- Task clarity
- Context usage rules
- Constraints
- Output schema

---

## Behavior Requirements

### Safety
- Avoid direct financial advice

### RAG Grounding
- Use only provided context

### Uncertainty Handling
- Explicit fallback

### Determinism
- Consistent outputs

---

## Evaluation Criteria

- Structure & clarity
- Grounding
- Safety
- Schema correctness
- Risk-awareness
- Advanced techniques

---

## Deliverables

- Final prompt
- Explanation
- Example output

---

## Common Mistakes

- Giving Buy/Sell advice
- Adding external knowledge
- Missing structure
- Ignoring risks

---

End of Assessment
