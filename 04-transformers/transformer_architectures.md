# Transformer Architectures: Encoder, Decoder, Encoder--Decoder

## 1. Encoder-Only Models

### Key Idea

-   Reads entire input at once (bidirectional)
-   Builds deep contextual understanding
-   Uses self-attention only (no cross-attention)

### Cross-Attention

-   Not used
-   No separate input-output sequences

### Applications

1.  Text classification (spam, sentiment)
2.  Named Entity Recognition (NER)
3.  Semantic search / embeddings
4.  Document similarity
5.  Extractive question answering
6.  RAG retrievers

### Models

-   BERT
-   RoBERTa
-   DistilBERT
-   ELECTRA
-   Sentence-BERT

------------------------------------------------------------------------

## 2. Decoder-Only Models

### Key Idea

-   Generates text token by token
-   Uses causal (masked) self-attention
-   Looks only at past tokens

### Cross-Attention

-   Not used
-   Input is part of the same sequence (prompt)

### Applications

1.  Chatbots
2.  Code generation
3.  Story generation
4.  Text completion
5.  Reasoning tasks
6.  Agent systems

### Models

-   GPT-4
-   GPT-3
-   LLaMA
-   Mistral
-   Gemini

------------------------------------------------------------------------

## 3. Encoder--Decoder Models

### Key Idea

-   Encoder processes input
-   Decoder generates output
-   Connected via cross-attention

### Cross-Attention (Core Concept)

-   Query → Decoder
-   Key/Value → Encoder

### Intuition

While generating each token, the decoder looks back at input.

### Example

Input: "Bonjour" Output: "Hello"

### Applications

1.  Machine translation
2.  Text summarization
3.  Generative QA
4.  Paraphrasing
5.  Speech-to-text
6.  Image captioning

### Models

-   T5
-   BART
-   MarianMT
-   FLAN-T5
-   mT5

------------------------------------------------------------------------

## Comparison

  Feature           Encoder         Decoder         Encoder--Decoder
  ----------------- --------------- --------------- ------------------
  Attention         Self            Masked Self     Self + Cross
  Direction         Bidirectional   Left-to-right   Both
  Cross-Attention   No              No              Yes
  Use Case          Understanding   Generation      Conversion

------------------------------------------------------------------------

## Final Intuition

-   Encoder-only → Understand text
-   Decoder-only → Generate text
-   Encoder--Decoder → Convert text

------------------------------------------------------------------------

## Key Insight

Cross-attention allows the decoder to refer to input while generating
output.

------------------------------------------------------------------------

## Pro Insight

Modern LLMs (GPT, LLaMA): - Do not use cross-attention - Still perform
tasks via prompting
