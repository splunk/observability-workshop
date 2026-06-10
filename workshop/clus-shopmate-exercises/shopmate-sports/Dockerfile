FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    SHOPMATE_HOST=0.0.0.0 \
    SHOPMATE_PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data ./shopmate-sports/data
COPY static ./shopmate-sports/static
COPY server.py ./shopmate-sports/server.py

EXPOSE 8080

CMD ["opentelemetry-instrument", "python", "shopmate-sports/server.py"]
