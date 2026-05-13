# Agent Evaluation Handout (Agentic AI Systems)

## 1. Why Agent Evaluation is Hard

Evaluating agentic systems is fundamentally more complex than evaluating
traditional ML models or standalone LLM outputs.

**Key Challenges:** - Non-determinism: Same input → different outputs -
Multi-step reasoning - Tool interaction complexity - Open-ended
outputs - Context dependency - Emergent behavior

------------------------------------------------------------------------

## 2. Evaluation Dimensions (Core Metrics)

-   **Task Success**: Did the agent achieve the goal?
-   **Correctness**: Accuracy and logic
-   **Coherence**: Logical flow
-   **Coverage**: Completeness
-   **Latency**: Time taken
-   **Cost**: Token/API usage
-   **Robustness**: Stability across inputs

------------------------------------------------------------------------

## 3. Logging and Tracing Basics

**Log:** - Inputs - Intermediate steps - Tool calls - Outputs - Errors

**Purpose:** - Debugging - Observability

------------------------------------------------------------------------

## 4. Manual vs Automated Evaluation

### Manual

-   Accurate but slow

### Automated

-   Scalable but imperfect

**Best Practice:** Hybrid approach

------------------------------------------------------------------------

## 5. LLM-as-a-Judge

Use an LLM to evaluate outputs.

**Pros:** - Scalable

**Cons:** - Bias

**Mitigation:** - Multiple judges - Pairwise comparisons

------------------------------------------------------------------------

## 6. Human Evaluation Loops

-   Annotation
-   Approval (HITL)
-   Feedback loops

Used in high-stakes domains.

------------------------------------------------------------------------

## 7. Benchmark Datasets

-   QA datasets
-   Reasoning datasets
-   Tool-use benchmarks

**Limitation:** Static, may not reflect real-world

------------------------------------------------------------------------

## 8. Hallucination Detection

-   Retrieval verification
-   Self-consistency
-   Tool validation
-   LLM critique
-   Rule-based checks

------------------------------------------------------------------------

## 9. Guardrail Testing

-   Input validation
-   Output filtering
-   Adversarial testing
-   Boundary testing

------------------------------------------------------------------------

## 10. Failure Modes

-   Tool misuse
-   Infinite loops
-   Hallucinated tool calls
-   Context overflow
-   Cascading failures

------------------------------------------------------------------------

## 11. Additional Topics

-   Memory evaluation
-   Multi-agent coordination
-   Continuous evaluation
-   A/B testing

------------------------------------------------------------------------

## 12. Evaluation Pipeline

1.  Define task
2.  Create dataset
3.  Run agent with tracing
4.  Automated evaluation
5.  LLM judge
6.  Human review
7.  Iterate

------------------------------------------------------------------------

## 13. Best Practices

-   Combine metrics
-   Log everything
-   Test real scenarios
-   Monitor cost
-   Include human feedback

------------------------------------------------------------------------

## 14. Summary

Agent evaluation focuses on behavior, reasoning, and reliability---not
just correctness.
