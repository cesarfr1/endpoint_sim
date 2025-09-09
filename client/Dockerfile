FROM python:3.9.23-trixie
WORKDIR /code
COPY ./client/requirements.txt .
COPY ./client/app_client.py .
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY . .
# EXPOSE 8080
CMD ["opentelemetry-instrument", "python", "app_client.py"]
# CMD ["/bin/bash"]