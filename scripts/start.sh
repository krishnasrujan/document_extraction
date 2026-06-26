#!/bin/bash

set -e

echo "Starting Document Confidence Application"

streamlit run ui/streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0