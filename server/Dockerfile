FROM python:3.9.23-slim-trixie
WORKDIR /code
COPY ./server/requirements.txt .
COPY ./server/app_server.py .
COPY ./server/templates /code/templates 
RUN pip install  -r requirements.txt
RUN opentelemetry-bootstrap -a install
# HEALTHCHECK --interval=1m30s --timeout=10s --retries=3 --start-period=40s --start-period=5s
#   CMD ["curl", "-f", "http://localhost:8080/health"]
#COPY . .
EXPOSE 8080
CMD ["opentelemetry-instrument", "python", "app_server.py"]
