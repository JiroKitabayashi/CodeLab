import requests
import concurrent.futures
import random
import logging
import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

current_time = datetime.now()
formatted_time = current_time.strftime("%y-%m-%d %H:%M:%S")


# Configure log format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s (in %(funcName)s at line %(lineno)d)",
    handlers=[
        logging.FileHandler(os.path.join(os.getcwd(), "log", f"{formatted_time}.log")),
        logging.StreamHandler(),
    ],
)


def generate_test_url(min_wait_time=0, max_wait_time=10):
    # Generate a random status code
    status_code = random.choice([200, 301, 400, 404, 500])

    # Generate a random delay time
    delay = random.randint(min_wait_time, max_wait_time)

    # Create a URL with the status code and delay time
    url = f"https://httpstat.us/{status_code}?sleep={delay*1000}"

    return url


def request_url(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    # Log the execution time
    logging.info(f"{url}: {response.status_code} ({end_time - start_time:.2f} seconds)")
    return response


# Parallel processing
def run_parallel(urls, threads_num):
    # Create a ThreadPoolExecutor and process URLs in parallel
    with ThreadPoolExecutor(max_workers=threads_num) as executor:
        results = executor.map(request_url, urls)


def ascon_separate(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(request_url, url) for url in urls]
        return as_completed(futures)


def get_responses(urls):
    """
    Function to get responses from multiple URLs
    """
    logging.info("function_start")
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Send asynchronous requests to each URL
        future_to_url = {executor.submit(requests.get, url): url for url in urls}
        logging.info("generator is created")
        # Get responses as requests are completed
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            logging.info(f"try to access url: {url}")
            try:
                response = future.result()
            except Exception as exc:
                logging.info(f"{url} generated an exception: {exc}")
            else:
                # logging.info(f'{url} returned status code {response.status_code}')
                return response.status_code


# Concurrent processing
async def run_concurrent(urls):
    # Send asynchronous requests to URLs
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(request_url_async(url)))

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


# Asynchronous request
async def request_url_async(url):
    start_time = time.time()
    response = await asyncio.to_thread(requests.get, url)
    end_time = time.time()

    logging.info(f"{url}: {response.status_code} ({end_time - start_time:.2f} seconds)")


# Compare parallel and concurrent processing
def compare_parallel_concurrent():
    # Create an array of 10 test URLs
    TEST_URLS = [generate_test_url() for _ in range(10)]
    # Run parallel processing
    logging.info("Parallel Execution")
    start_time = time.time()
    run_parallel(TEST_URLS, 10)
    end_time = time.time()
    logging.info(f"Total Execution Time: {end_time - start_time:.2f} seconds")


def concurrent_test():
    TEST_URLS = [generate_test_url() for _ in range(25)]
    futures = ascon_separate(TEST_URLS)
    start_time = time.time()
    logging.info("start")
    for i, future in enumerate(futures):
        result = future.result()
        logging.info({"result": result, "num": i})
    end_time = time.time()
    logging.info(f"Total Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    concurrent_test()
