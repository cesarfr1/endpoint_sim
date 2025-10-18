import requests
import time
while True:
    x = requests.get('http://server:8080/health')
    time.sleep(5)
