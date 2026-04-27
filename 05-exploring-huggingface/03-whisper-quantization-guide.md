# Whisper Quantization & Optimization Guide

## Overview

`openai/whisper-large-v3` is a very large model (\~1.5B parameters),
which makes it slow to load and memory intensive.

Quantization helps reduce: - Model size - Memory usage - Load time

------------------------------------------------------------------------

## Option 1 --- 8-bit Quantization (Recommended)

``` python
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
import torch

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    load_in_8bit=True,
    device_map="auto"
)

processor = AutoProcessor.from_pretrained(model_id)

transcriber = pipeline(
    task="automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
)

result = transcriber(
    "https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac"
)

print(result)
```

------------------------------------------------------------------------

## Option 2 --- 4-bit Quantization (Faster, lighter)

``` python
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor, BitsAndBytesConfig
import torch

model_id = "openai/whisper-large-v3"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)

processor = AutoProcessor.from_pretrained(model_id)

transcriber = pipeline(
    task="automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
)

result = transcriber(
    "https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac"
)

print(result)
```

------------------------------------------------------------------------

## Option 3 --- Use Smaller Models

``` python
pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)
```

------------------------------------------------------------------------

## Requirements

``` bash
pip install transformers accelerate bitsandbytes
```

------------------------------------------------------------------------

## Performance Comparison

  Approach         Load Time   Memory   Accuracy
  ---------------- ----------- -------- -------------
  Full precision   Slow        High     Best
  8-bit            Faster      Lower    Very good
  4-bit            Fastest     Lowest   Slight drop
  Smaller model    Fast        Low      Depends

------------------------------------------------------------------------

# Advanced Optimization: ONNX & TensorRT

## What is ONNX?

ONNX (Open Neural Network Exchange) is a format for representing machine
learning models that allows interoperability across frameworks.

### Benefits:

-   Faster inference
-   Hardware optimization
-   Cross-platform deployment

### Why use ONNX?

-   Converts PyTorch models into optimized graph execution
-   Enables inference engines like ONNX Runtime

------------------------------------------------------------------------

## What is TensorRT?

TensorRT is NVIDIA's high-performance inference engine designed for
GPUs.

### Benefits:

-   Kernel fusion
-   Layer optimization
-   FP16 / INT8 acceleration
-   Extremely low latency

------------------------------------------------------------------------

## Why ONNX + TensorRT?

Typical pipeline: 1. Convert PyTorch → ONNX 2. Optimize ONNX → TensorRT
engine

### Advantages:

-   5--20x faster inference
-   Lower latency (critical for real-time ASR)
-   Better GPU utilization
-   Production-grade deployment

------------------------------------------------------------------------

## When to Use Them?

Use ONNX/TensorRT when: - You need real-time transcription - Deploying
at scale - Running on NVIDIA GPUs - Optimizing latency-critical systems

------------------------------------------------------------------------

## Summary

-   Quantization → easiest win
-   Smaller models → practical improvement
-   ONNX/TensorRT → maximum performance (production)
