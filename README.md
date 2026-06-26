# Document Extraction & Confidence Scoring System

## Objective

Build a generic Intelligent Document Processing (IDP) pipeline that extracts structured information from documents such as invoices, PAN cards, and other business/identity documents while providing:

- Field-level confidence scores
- Overall document confidence score
- Explainable confidence signals for every extracted entity

The system is designed to support multiple document types without changing the core extraction and confidence scoring framework.


## Methodology

The pipeline follows a hybrid OCR + Vision Language Model (VLM) approach.


### 1. Document Understanding

Documents are converted into page images and processed using:

- Tesseract OCR
  - Extracts text tokens
  - Captures bounding box information
  - Provides OCR confidence scores

- Qwen2.5-VL (running locally through Ollama)
  - Processes document images
  - Extracts structured entities based on the required schema


Example:

OCR Output:

INV 12345


VLM Output:

{
  "invoice_number": "INV12345"
}


---

### 2. Confidence Scoring

Each extracted field confidence is calculated by combining multiple signals:


Field Confidence =

(OCR Alignment * 0.6)

+

(VLM Extraction * 0.4)


### OCR Alignment (60%)

Validates whether the value extracted by the Vision Model is supported by OCR evidence.

The system:

- Matches extracted values against OCR tokens
- Uses text similarity matching
- Considers OCR confidence scores
- Uses token positions and bounding boxes for accurate alignment

This helps reduce incorrect extractions and hallucinations from the VLM.


### VLM Extraction (40%)

Measures whether the Vision Language Model successfully extracted the required entity.

A successfully extracted value contributes positively to the confidence score, while missing values reduce confidence.


---

### 3. Document Confidence

The overall document confidence is calculated by aggregating individual field confidence scores:


Document Confidence =

Average(Field Confidence Scores)


This provides a single reliability score for the complete document extraction.
