FROM python:3.9.23-slim-trixie
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY . .
EXPOSE 8080
CMD ["opentelemetry-instrument", "python", "app_metrics.py"]