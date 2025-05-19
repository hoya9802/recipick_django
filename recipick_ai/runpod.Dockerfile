FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.runpod.txt .
RUN pip install --no-cache-dir -r requirements.runpod.txt && \
    pip install --no-cache-dir runpod

# Copy handler file
COPY handler.py .
COPY test_input.json .

# Create volume directory for persistent storage
RUN mkdir -p /runpod-volume/cache

# Set environment variables
ENV HF_MODEL_NAME="Ashikan/dut-recipe-generator"
ENV HF_CACHE_DIR="/runpod-volume/cache"

# Pre-download model during build
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    model_name='${HF_MODEL_NAME}'; \
    print(f'Downloading model: {model_name}'); \
    AutoTokenizer.from_pretrained(model_name, cache_dir='${HF_CACHE_DIR}'); \
    AutoModelForCausalLM.from_pretrained(model_name, cache_dir='${HF_CACHE_DIR}')"

# Start the container
CMD ["python", "-u", "handler.py"]