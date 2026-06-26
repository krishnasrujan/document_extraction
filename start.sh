#!/bin/bash

set -e

MODEL="qwen2.5vl:7b"
OLLAMA_CONTAINER="ollama"
APP_CONTAINER="app"

echo "================================="
echo "Starting Document Extraction App"
echo "================================="

echo ""
echo "Stopping existing containers..."
docker compose down


echo ""
echo "Building containers..."
docker compose build


echo ""
echo "Starting services..."
docker compose up -d


echo ""
echo "Waiting for Ollama service..."

until docker exec $OLLAMA_CONTAINER ollama list > /dev/null 2>&1
do
    echo "Ollama not ready yet..."
    sleep 3
done


echo ""
echo "Ollama is ready"


echo ""
echo "Checking model: $MODEL"


if docker exec $OLLAMA_CONTAINER ollama list | grep -q "$MODEL"
then
    echo "Model already available"
else
    echo "Downloading model..."
    docker exec $OLLAMA_CONTAINER ollama pull $MODEL
fi


echo ""
echo "Restarting application container..."
docker compose restart $APP_CONTAINER


echo ""
echo "================================="
echo "Application started successfully"
echo "================================="

echo ""
echo "Streamlit UI:"
echo "http://localhost:8501"

echo ""
echo "Logs:"
echo "docker compose logs -f app"