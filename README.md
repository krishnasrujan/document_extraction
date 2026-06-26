# Document Extraction & Confidence Scoring System

## Objective

Build a generic Intelligent Document Processing (IDP) pipeline that extracts structured information from documents such as invoices, identity documents, and business forms while providing:

- Field-level confidence scores
- Overall document confidence score
- Explainable confidence signals for every extracted entity
- Automated routing decision based on confidence

The system is designed to support multiple document types without changing the core extraction and confidence scoring framework.

## Architecture Overview

The pipeline follows a hybrid OCR + Vision Language Model (VLM) architecture.

Document
    |
    |
Document Loader
    |
    |
Page Image Conversion
    |
    +----------------+
    |                |
    |                |
Tesseract OCR     Qwen2.5-VL
    |                |
OCR Tokens        Extracted Entities
(BBox +           (Structured JSON)
Confidence)
    |
    |
Confidence Engine
    |
    |
Field Confidence
    |
    |
Document Confidence
    |
    |
Routing Decision
(Approve / Review)


## Methodology

## 1. Document Processing

Documents are converted into page images before extraction.

Supported formats:

- PDF
- PNG
- JPG
- JPEG

Each page is processed independently and stored as an image artifact.


## 2. OCR Extraction

The OCR layer uses Tesseract OCR.

Responsibilities:

- Extract text tokens
- Capture token bounding boxes
- Capture OCR confidence scores
- Preserve document layout information

Example:

OCR Output:

Invoice
No.
INV12345


The OCR output is represented as tokens:

{
  "text": "INV12345",
  "confidence": 92,
  "bounding_box": {}
}


## 3. Vision Language Model Extraction

The extraction layer uses Qwen2.5-VL running locally through Ollama.

The VLM processes document images and extracts structured entities.

Example:

Input:

Invoice
No: INV12345
Total: $150.00


Output:

{
  "invoice_number": "INV12345",
  "total": "$150.00"
}


Extraction rules:

- Extract only visible information
- Do not hallucinate missing values
- Preserve original document text
- Return structured JSON output


# Confidence Scoring

Each extracted field receives a confidence score calculated using multiple explainable signals.


## Field Confidence

Field Confidence =

(OCR Alignment × 0.5)

+

(VLM Extraction × 0.5)


## OCR Alignment Signal

Purpose:

Validate whether the extracted value is supported by OCR evidence.

The system:

- Matches extracted values against OCR tokens
- Uses fuzzy text similarity matching
- Handles OCR formatting issues
- Uses bounding box information
- Considers OCR confidence scores


Example:

VLM:

Subtotal: $150.00


OCR:

Subtotal
$150.00


The alignment score increases because OCR evidence supports the extracted value.


## VLM Extraction Signal

Purpose:

Measure whether the Vision Model successfully extracted the entity.

Rules:

- Extracted value exists → high confidence
- Missing value → lower confidence


Example:

{
  "total": "$157.50"
}


Extraction Score = 1.0


# Document Confidence

Overall document confidence is calculated by averaging all field confidence scores.


Document Confidence =

Average(Field Confidence Scores)


Example:

Invoice Number    0.95
Total             0.92
Date              0.70


Document Confidence = 0.85


This provides a single reliability score for the complete extraction.


# Routing Decision

Based on document confidence, the system determines the next action.

Example:

High Confidence
        |
        |
    Approved


Low Confidence
        |
        |
 Manual Review


The UI displays:

- Overall confidence score
- Routing decision
- Reason for decision


# Explainability

Every field confidence score includes individual signals.

Example:

{
  "field": "total",
  "confidence": 0.91,
  "signals": [
    {
      "name": "ocr_alignment",
      "score": 0.92,
      "reason": "OCR value aligned"
    },
    {
      "name": "extraction",
      "score": 1.0,
      "reason": "value extracted"
    }
  ]
}


This allows users to understand why a document was accepted or sent for review.


# Running the Application

## Requirements

- Docker
- Docker Compose


## Start Application

chmod +x start.sh

./start.sh


The script:

- Builds containers
- Starts Ollama
- Downloads Qwen2.5-VL model if required
- Starts Streamlit application


Application:

http://localhost:8501


# Technology Stack

## Backend

- Python
- Tesseract OCR
- Ollama
- Qwen2.5-VL


## Frontend

- Streamlit


## Deployment

- Docker
- Docker Compose


# Project Capabilities

Current capabilities:

- Multi-page document processing
- OCR token extraction with confidence
- Vision-based structured extraction
- Generic document support
- Field-level confidence scoring
- Document-level confidence aggregation
- Review routing decision


# Future Improvements

Potential enhancements:
- Preprocess the images such as downsizing, better contrast
- Table extraction support