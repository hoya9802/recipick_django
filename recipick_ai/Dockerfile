FROM python:3.11-slim

LABEL maintainer="recipick_ai"

COPY ./src/requirements.txt /app/requirements.txt
COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]