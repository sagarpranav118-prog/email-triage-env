FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir openai pydantic

CMD ["sh", "-c", "python inference.py && tail -f /dev/null"]