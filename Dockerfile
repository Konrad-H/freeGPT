FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY ChatAssistant.py .
COPY discord.token .
COPY openai.token .

CMD ["python", "app.py"]