#!/usr/bin/env python3

import requests
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

# Configuration
FLASK_URL = 'http://127.0.0.1:5000'
FASTAPI_URL = 'http://127.0.0.1:8000'

# Define payloads
string_payload = {"message": "Hello, World!"}
int_string_payload = {"id": 1, "message": "Hello, World!"}
mixed_payload = {"id": 1, "value": 3.14, "message": "Hello, World!", "flags": [True, False, True]}

# Define endpoints with their respective payloads
endpoints = {
    "GET": [('/get', None)],
    "POST": [
        ('/post/string', string_payload),
        ('/post/int_string', int_string_payload),
        ('/post/mixed', mixed_payload),
    ],
    "PUT": [
        ('/put/string', string_payload),
        ('/put/int_string', int_string_payload),
        ('/put/mixed', mixed_payload),
    ],
}

def send_request(session, method, url, payload):
    if method == 'GET':
        response = session.get(url)
    elif method == 'POST':
        response = session.post(url, json=payload)
    elif method == 'PUT':
        response = session.put(url, json=payload)
    return response

def benchmark_individual(server_name, base_url, method, endpoint, payload, num_samples):
    print(f"Benchmarking {server_name} - {method} {endpoint}...")
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            futures = [
                executor.submit(send_request, session, method, base_url + endpoint, payload)
                for _ in range(num_samples)
            ]
            for future in futures:
                future.result()
    end_time = time.time()
    total_time = end_time - start_time
    req_per_sec = num_samples / total_time
    print(f"{server_name} handled {req_per_sec:.2f} requests per second for {method} {endpoint}.\n")
    return req_per_sec

def main():
    parser = argparse.ArgumentParser(description="Benchmark Flask vs FastAPI")
    parser.add_argument('--samples', type=int, default=1000, help='Number of samples per endpoint')
    args = parser.parse_args()

    num_samples = args.samples

    results = {
        "Flask": {},
        "FastAPI": {}
    }

    # Benchmark each endpoint individually for Flask and FastAPI
    for server_name, base_url in [("Flask", FLASK_URL), ("FastAPI", FASTAPI_URL)]:
        for method, endpoints_list in endpoints.items():
            for endpoint, payload in endpoints_list:
                if payload:
                    rps = benchmark_individual(server_name, base_url, method, endpoint, payload, num_samples)
                else:
                    # For GET requests without payload
                    rps = benchmark_individual(server_name, base_url, method, endpoint, None, num_samples)
                results[server_name][f"{method} {endpoint}"] = rps

    # Display the results in a tabular format with comparison
    print("Benchmark Results (Requests per second):\n")
    flask_wins = 0
    fastapi_wins = 0
    for endpoint in results["Flask"].keys():
        flask_rps = results["Flask"][endpoint]
        fastapi_rps = results["FastAPI"][endpoint]
        print(f"{endpoint}:")
        print(f"  Flask:   {flask_rps:.2f} RPS")
        print(f"  FastAPI: {fastapi_rps:.2f} RPS")
        if flask_rps > fastapi_rps:
            print("  Faster: Flask")
            flask_wins += 1
        elif fastapi_rps > flask_rps:
            print("  Faster: FastAPI")
            fastapi_wins += 1
        else:
            print("  Tie")
        print()

    # Overall comparison
    print("Overall Comparison:")
    if flask_wins > fastapi_wins:
        print(f"Flask was faster in {flask_wins} out of {flask_wins + fastapi_wins} tests.")
        print("Flask is overall faster in this benchmark.")
    elif fastapi_wins > flask_wins:
        print(f"FastAPI was faster in {fastapi_wins} out of {flask_wins + fastapi_wins} tests.")
        print("FastAPI is overall faster in this benchmark.")
    else:
        print(f"Flask and FastAPI tied with {flask_wins} wins each.")
        print("Neither framework is clearly faster overall in this benchmark.")

if __name__ == "__main__":
    main()
