import os
import json
import runpod
import torch
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Global model cache
model_cache = None
tokenizer_cache = None

def load_model():
    """AI 모델과 Tokenizer 로드"""
    global model_cache, tokenizer_cache

    if model_cache and tokenizer_cache:
        # 이미 로드된 모델이 있으면 재사용
        print("Reuse the model if it's already loaded")
        device = 0 if torch.cuda.is_available() else -1
        return pipeline("text-generation", model=model_cache, tokenizer=tokenizer_cache, device=device)

    model_name = os.environ.get("HF_MODEL_NAME", "Ashikan/dut-recipe-generator")
    cache_dir = os.environ.get('HF_CACHE_DIR', "/runpod-volume/cache")

    # 캐시 디렉토리 확인 및 생성
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        print(f"Created cache directory: {cache_dir}")

    # GPU 사용 가능 여부 확인
    device = 0 if torch.cuda.is_available() else -1
    device_str = "GPU" if device == 0 else "CPU"
    print(f"Loading model: {model_name} from cache: {cache_dir} on {device_str}")

    try:
        tokenizer_cache = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            local_files_only=True
        )
        model_cache = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            local_files_only=True
        )
        print("Successfully loaded model from local cache")
    except Exception as e:
        print(f"Could not load model from cache: {str(e)}")
        print("Downloading model from Hugging Face Hub")
        tokenizer_cache = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model_cache = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)

    # GPU 장치 지정하여 pipeline 생성
    return pipeline("text-generation", model=model_cache, tokenizer=tokenizer_cache, device=device)

def handler(event):
    """
    RunPod Serverless handler function that processes incoming requests

    Args:
        event (dict): Contains the input data and request metadata

    Returns:
        dict: The recipe generation result
    """
    try:
        print("Worker starting...")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU device count: {torch.cuda.device_count()}")
            print(f"GPU device name: {torch.cuda.get_device_name(0)}")

        input_data = event["input"]

        if not input_data or "ingredients" not in input_data:
            return {
                "error": "Missing required field: ingredients"
            }

        ingredients = input_data["ingredients"]

        # Validate ingredients
        if not isinstance(ingredients, list):
            return {
                "error": "Ingredients must be a list of strings"
            }

        print(f"Generating recipe for ingredients: {ingredients}")

        # Load model and generate recipe
        pipe = load_model()
        input_text = '{"prompt": ' + json.dumps(ingredients)

        output = pipe(
            input_text,
            max_length=1024,
            temperature=0.5,
            do_sample=True
        )[0]["generated_text"]

        # Parse the model output
        try:
            result = json.loads(output)
            return result
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse model output",
                "raw_output": output
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "error": f"Recipe generation error: {str(e)}"
        }

# Start the serverless function
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})