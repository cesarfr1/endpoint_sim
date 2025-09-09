import requests
import time
x = requests.get('http://server:8080/health')
time.sleep(600)


