import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

router = APIRouter()

model_cache = None
tokenizer_cache = None

def load_model():
    """AI 모델과 Tokenizer 로드"""
    global model_cache, tokenizer_cache

    if model_cache and tokenizer_cache:
        return pipeline("text-generation", model=model_cache, tokenizer=tokenizer_cache)

    model_name = os.environ.get("HF_MODEL_NAME", "Ashikan/dut-recipe-generator")
    cache_dir = os.environ.get('HF_CACHE_DIR', None)

    tokenizer_cache = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    model_cache = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)

    return pipeline("text-generation", model=model_cache, tokenizer=tokenizer_cache)

class IngredientsInput(BaseModel):
    ingredients: List[str]

@router.post("/generate-recipe")
async def generate_recipe(input_data: IngredientsInput):
    try:
        pipe = load_model()
        input_text = '{"prompt": ' + json.dumps(input_data.ingredients)

        output = pipe(
            input_text,
            max_length=1024,
            temperature=.2,
            do_sample=True
        )[0]["generated_text"]

        return json.loads(output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"레시피 생성 오류 {str(e)}")

if __name__ == "__main__":
    import asyncio

    async def test():
        test_ingredients = [
            "mushrooms",
            "cabbage",
            "soy sauce",
            "sesame seeds",
        ]
        input_data = IngredientsInput(ingredients=test_ingredients)
        print('여긴 통과?')
        result = await generate_recipe(input_data)
        print(json.dumps(result, indent=2))

    asyncio.run(test())
