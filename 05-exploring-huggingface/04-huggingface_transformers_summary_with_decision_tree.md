# Hugging Face Transformers — Clean Summary Guide (Extended)

## Overview
A structured and clean reference guide to Hugging Face Transformers, covering:
- Tasks
- Model classes
- Example models
- Real-world applications
- Decision tree for model selection

---

## NLP (Text)

| Task | Pipeline | Model Class | Example Models | Use Cases |
|------|----------|------------|----------------|----------|
| Text Classification | text-classification | AutoModelForSequenceClassification | BERT, RoBERTa | Sentiment analysis, spam detection |
| Token Classification | token-classification | AutoModelForTokenClassification | BERT-NER | Named Entity Recognition |
| Question Answering | question-answering | AutoModelForQuestionAnswering | BERT-QA | Chatbots, document QA |
| Text Generation | text-generation | AutoModelForCausalLM | GPT, LLaMA | Chat systems |
| Seq2Seq | text2text-generation | AutoModelForSeq2SeqLM | T5, BART | Translation, summarization |
| Fill Mask | fill-mask | AutoModelForMaskedLM | BERT | Autocomplete |
| Sentence Similarity | feature-extraction | AutoModel | Sentence-BERT | Semantic search |
| Summarization | summarization | AutoModelForSeq2SeqLM | BART, T5 | Article summarization |
| Translation | translation | AutoModelForSeq2SeqLM | MarianMT | Language translation |

---

## Speech / Audio

| Task | Pipeline | Model Class | Example Models | Use Cases |
|------|----------|------------|----------------|----------|
| Speech Recognition | automatic-speech-recognition | AutoModelForSpeechSeq2Seq / CTC | Whisper, Wav2Vec2 | Transcription |
| Audio Classification | audio-classification | AutoModelForAudioClassification | AST | Sound detection |
| Text-to-Speech | text-to-speech | AutoModelForTextToWaveform | Bark, VITS | Voice synthesis |
| Audio-to-Audio | audio-to-audio | Varies | Enhancement models | Noise reduction |

---

## Vision (Computer Vision)

| Task | Pipeline | Model Class | Example Models | Use Cases |
|------|----------|------------|----------------|----------|
| Image Classification | image-classification | AutoModelForImageClassification | ViT, ResNet | Object recognition |
| Object Detection | object-detection | AutoModelForObjectDetection | DETR, YOLO | Autonomous systems |
| Image Segmentation | image-segmentation | AutoModelForSemanticSegmentation | SegFormer | Medical imaging |
| Image Captioning | image-to-text | VisionEncoderDecoder | BLIP | Accessibility |

---

## Multimodal

| Task | Pipeline | Model Class | Example Models | Use Cases |
|------|----------|------------|----------------|----------|
| Visual QA | visual-question-answering | Vision+Text | BLIP, LLaVA | Image understanding |
| Document QA | document-question-answering | LayoutLM | LayoutLMv3 | Invoice parsing |
| Image + Text | image-to-text | VisionEncoderDecoder | Donut | OCR-free extraction |

---

## Tabular / Other

| Task | Pipeline | Model Class | Example Models | Use Cases |
|------|----------|------------|----------------|----------|
| Feature Extraction | feature-extraction | AutoModel | Any encoder | Embeddings |
| Reinforcement Learning | N/A | Custom | Decision Transformers | Robotics |

---

## Key Design Abstractions

| Component | Purpose |
|----------|--------|
| pipeline() | High-level API |
| AutoModel* | Task-specific loaders |
| AutoTokenizer | Text preprocessing |
| AutoProcessor | Multimodal preprocessing |
| Trainer | Training loop |
| Datasets | Data handling |

---

## How to Choose

- Classification → AutoModelForSequenceClassification  
- Generation → AutoModelForCausalLM  
- Translation/Summarization → AutoModelForSeq2SeqLM  
- Speech → AutoModelForSpeechSeq2Seq  
- Vision → AutoModelForImageClassification  

---

## Decision Tree

```
Start
 │
 ├── Text?
 │     ├── Classification → SequenceClassification (BERT)
 │     ├── Generation
 │     │     ├── Open-ended → CausalLM (GPT, LLaMA)
 │     │     └── Structured → Seq2SeqLM (T5, BART)
 │     ├── QA → QuestionAnswering
 │     └── Embeddings → AutoModel / Sentence-BERT
 │
 ├── Audio?
 │     ├── Speech-to-text → SpeechSeq2Seq (Whisper)
 │     ├── Classification → AudioClassification
 │     └── TTS → TextToWaveform
 │
 ├── Image?
 │     ├── Classification → ImageClassification
 │     ├── Detection → ObjectDetection
 │     ├── Segmentation → SemanticSegmentation
 │     └── Captioning → VisionEncoderDecoder
 │
 └── Multimodal?
       ├── Image + Text → VQA (BLIP, LLaVA)
       └── Documents → LayoutLM
```

---

## Production Insights

- Use pipelines for prototyping  
- Use model classes for fine control  
- Optimize using:
  - Quantization
  - ONNX
  - TensorRT  

---

## Mental Model

```
Task → Pipeline → Model Class → Pretrained Model → Deployment
```
