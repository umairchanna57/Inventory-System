import requests
from concurrent.futures import ThreadPoolExecutor

# Define the URL to which requests will be sent
URL = 'http://127.0.0.1:8000/api/products/5'

# Define the number of requests to send
NUM_REQUESTS = 5000
def send_request():
    try:
        response = requests.get(URL)
        print(f"Status Code: {response.status_code}")
      
    except Exception as e:
        print(f"Request failed: {e}")

def main():
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(send_request) for _ in range(NUM_REQUESTS)]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
