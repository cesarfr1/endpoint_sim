import requests
import time
import random

while True:
    random_value = random.randint(1, 100)  # Generate a random integer
    payload = {'id': random_value}
    response = requests.post('http://server:8080/submit', json=payload)
    sleep_time = random.uniform(1, 3)  # Sleep for a random time between 1 and 10 seconds
    time.sleep(sleep_time)
