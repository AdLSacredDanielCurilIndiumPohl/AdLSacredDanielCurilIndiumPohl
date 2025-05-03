FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY cli_simple.py .

ENTRYPOINT ["python", "cli_simple.py"]