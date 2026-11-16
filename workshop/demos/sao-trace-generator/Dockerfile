FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY generate_traces.py input.csv /app/

RUN useradd --create-home --uid 1000 --shell /bin/bash app && chown -R app:app /app
USER 1000

CMD ["python", "generate_traces.py"]
