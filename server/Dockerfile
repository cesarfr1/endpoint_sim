FROM python:3.9.23-slim-trixie
WORKDIR /code
COPY ./server/requirements.txt .
COPY ./server/app_server.py .
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY . .
EXPOSE 8080
CMD ["opentelemetry-instrument", "python", "app_server.py"]