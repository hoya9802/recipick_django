import os
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


def load_model():
    """AI 모델과 토크나이저를 로드"""
    model_name = os.environ.get('HF_MODEL_NAME')
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)


def generate_recipe(ingredients):
    """레시피 생성 함수"""
    pipe = load_model()
    input_text = '{"prompt": ' + json.dumps(ingredients)

    output = pipe(
        input_text,
        max_length=1024,
        temperature=0.7,
        do_sample=True,
        # truncation=True
    )[0]["generated_text"]

    return json.loads(output)


if __name__ == "__main__":
    # 직접 실행시 테스트
    test_ingredients = [
        "mushrooms",
        "cabbage",
        "soy sauce",
        "sesame seeds",
    ]
    result = generate_recipe(test_ingredients)
    print(json.dumps(result, indent=2))
