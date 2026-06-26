#!/bin/bash

set -e

echo "Stopping existing containers..."
docker compose down

echo "Building Docker images..."
docker compose build

echo "Starting containers..."
docker compose up -d

echo "Waiting for Ollama container..."

until docker exec ollama ollama list > /dev/null 2>&1
do
    sleep 3
done

echo "Ollama is ready"

MODEL="qwen2.5vl:7b"

echo "Checking model: $MODEL"

if docker exec ollama ollama list | grep -q "$MODEL"
then
    echo "Model already exists"
else
    echo "Downloading model: $MODEL"
    docker exec ollama ollama pull $MODEL
fi

echo "Restarting application container..."
docker compose restart app

echo "Done!"
echo "Application running at:"
echo "http://localhost:8501"