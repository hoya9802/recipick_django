# Recipick AI - RunPod Serverless Deployment

이 문서는 Recipick AI 모델을 RunPod Serverless에 배포하는 방법을 설명합니다.

## 배포 단계

### 1. 로컬 테스트 (선택사항)

로컬에서 테스트하기 전에 Python 가상환경을 설정하고 필요한 패키지를 설치합니다:

```bash
python -m venv venv
source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
pip install -r requirements.txt
pip install runpod
```

테스트 실행:

```bash
python handler.py
```

### 2. Docker 이미지 빌드 및 푸시

RunPod에 배포하기 위해 Docker 이미지를 빌드하고 Docker Hub에 업로드합니다:

```bash
# Docker 이미지 빌드
docker build --platform linux/amd64 -f runpod.Dockerfile -t [YOUR_DOCKER_USERNAME]/recipick-ai-serverless:latest .

# Docker Hub에 이미지 푸시
docker push [YOUR_DOCKER_USERNAME]/recipick-ai-serverless:latest
```

### 3. RunPod에 배포

1. RunPod 계정에 로그인하고 Serverless 섹션으로 이동합니다.
2. "New Endpoint" 버튼을 클릭합니다.
3. "Custom Source"에서 "Docker Image"를 선택하고 "Next"를 클릭합니다.
4. "Container Image" 필드에 Docker 이미지 URL을 입력합니다: `docker.io/[YOUR_DOCKER_USERNAME]/recipick-ai-serverless:latest`
5. (선택사항) 엔드포인트의 이름을 지정하거나 자동 생성된 이름을 사용합니다.
6. "Worker Configuration"에서 필요한 GPU 타입을 선택합니다.
7. 만약 이미 Pods랑 연결되어 있는 Network Volume 이 있다면. 이를 연결하여 모델 캐싱합니다.
8. 나머지 설정은 기본값으로 둡니다.
9. "Create Endpoint"를 클릭합니다.

### 4. 엔드포인트 테스트

엔드포인트 상세 페이지에서 "Requests" 탭을 클릭하여 다음과 같은 요청을 테스트합니다:

```json
{
    "input": {
        "ingredients": [
            "mushrooms",
            "cabbage",
            "soy sauce",
            "sesame seeds"
        ]
    }
}
```

"Run" 버튼을 클릭하면 결과가 표시됩니다.

## API 호출 예시

엔드포인트가 배포되면 다음과 같이 API를 호출할 수 있습니다:

```python
import requests
import json

RUNPOD_API_KEY = "YOUR_RUNPOD_API_KEY"
ENDPOINT_ID = "YOUR_ENDPOINT_ID"

url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"

payload = {
    "input": {
        "ingredients": [
            "mushrooms",
            "cabbage",
            "soy sauce",
            "sesame seeds"
        ]
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {RUNPOD_API_KEY}"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())
```
