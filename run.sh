#!/bin/bash

# Load environment variables
source .env

# Choose between Docker and Podman
RUNTIME=${RUNTIME:-podman}

# Build the Docker or Podman image
$RUNTIME build -t slm_bench .

# Set the Hugging Face token flag if provided
if [ -n "$HUGGING_FACE_ACCESS_TOKEN" ]; then
  TOKEN_FLAG="-e HUGGING_FACE_ACCESS_TOKEN=$HUGGING_FACE_ACCESS_TOKEN"
else
  TOKEN_FLAG=""
fi

# Split model paths into an array
IFS=',' read -ra MODELS <<< "$MODEL_PATHS"

# Run each model in a separate container
for model_path in "${MODELS[@]}"; do
    echo "Running model: $model_path"

    # Run the container for each model
    $RUNTIME run --rm \
    -v "$(pwd):/app" \
    -e MODEL_PATH="$model_path" \
    --env-file .env \
    $TOKEN_FLAG \
    slm_bench
done

echo "All models tested. Results saved to output.csv."
