# Invoice confidence-scoring app — single image running the Streamlit UI,
# which imports the backend pipeline. Stock Docker Hub base + public PyPI.
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
 PYTHONUNBUFFERED=1 \
 PIP_NO_CACHE_DIR=1 \
 HOME=/home/appuser

WORKDIR /app

# System dependencies: Tesseract (OCR), Poppler (pdf2image backend), curl (healthcheck).
RUN apt-get update && apt-get install -y --no-install-recommends \
 tesseract-ocr \
 poppler-utils \
 curl \
 && rm -rf /var/lib/apt/lists/*

# Python dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code.
COPY backend ./backend
COPY ui ./ui

# Writable dirs (also bind-mounted via docker-compose) + non-root user.
RUN mkdir -p samples labels artifacts \
 && useradd --create-home appuser \
 && chown -R appuser:appuser /app /home/appuser
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
 CMD curl -fs http://localhost:8501/_stcore/health || exit 1

ENV PYTHONPATH=/app

CMD ["streamlit", "run", "ui/streamlit_app.py", \
 "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

