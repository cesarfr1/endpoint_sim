Readme
Create a .env file using the .env_sample as example.
Bring up the container with `docker compose up` command
There are a couple of endpoint available, refer to the python code.
The POST payload can be simulated by using `curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:8082/submit`
You can validate the signals being created by APM by enabling the variable OTEL_LOG_LEVEL on the compose.yaml file 