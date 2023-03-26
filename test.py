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


# ログフォーマットの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s (in %(funcName)s at line %(lineno)d)',
    handlers=[
        logging.FileHandler(os.path.join(os.getcwd(), "log", f"{formatted_time}.log")),
        logging.StreamHandler()
    ]
)


def generate_test_url():
    # ランダムなステータスコードを生成
    status_code = random.choice([200, 301, 400, 404, 500])

    # ランダムな遅延時間を生成
    delay = random.randint(5, 5)

    # ステータスコードと遅延時間を組み合わせたURLを生成
    url = f"https://httpstat.us/{status_code}?sleep={delay*1000}"

    return url

def request_url(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    # ログに実行時間を出力
    logging.info(f"{url}: {response.status_code} ({end_time - start_time:.2f} seconds)")
    return response

# 並列処理
def run_parallel(urls, threads_num):
    # ThreadPoolExecutorを作成して、URLを並列処理
    with ThreadPoolExecutor(max_workers=threads_num) as executor:
        results = executor.map(request_url, urls)

def ascon_separate(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(request_url, url) for url in urls]
        return as_completed(futures)

def get_responses(urls):
    """
    複数のURLからレスポンスを取得する関数
    """
    logging.info('function_start')
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 各URLに対して非同期的にリクエストを送る
        future_to_url = {executor.submit(requests.get, url): url for url in urls}
        logging.info('generator is created')
        # リクエストが完了した順にレスポンスを取得する
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            logging.info(f'try to access url: {url}')
            try:
                response = future.result()
            except Exception as exc:
                logging.info(f'{url} generated an exception: {exc}')
            else:
                # logging.info(f'{url} returned status code {response.status_code}')
                return response.status_code

# 並行処理
async def run_concurrent(urls):
    # URLを非同期にリクエスト
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(request_url_async(url)))

    # 全てのタスクが完了するまで待機
    await asyncio.gather(*tasks)

# 非同期リクエスト
async def request_url_async(url):
    start_time = time.time()
    response = await asyncio.to_thread(requests.get, url)
    end_time = time.time()

    logging.info(f"{url}: {response.status_code} ({end_time - start_time:.2f} seconds)")


def compare_parallel_concurrent():
    # テスト用のURLを10個含む配列を生成
    TEST_URLS = [generate_test_url() for _ in range(10)]
    # 並列処理を実行
    logging.info("Parallel Execution")
    start_time = time.time()
    run_parallel(TEST_URLS,10)
    end_time = time.time()
    logging.info(f"Total Execution Time: {end_time - start_time:.2f} seconds")

    # 並行処理を実行
    logging.info("Concurrent Execution")
    start_time = time.time()
    asyncio.run(run_concurrent(TEST_URLS))
    end_time = time.time()
    logging.info(f"Total Execution Time: {end_time - start_time:.2f} seconds")

def concurrent_test():
    TEST_URLS = [generate_test_url() for _ in range(25)]
    futures = ascon_separate(TEST_URLS)
    start_time = time.time()
    logging.info("start")
    for i, future in enumerate(futures):
        result = future.result()
        logging.info(
            {"result": result,
             "num": i
             }
        )
    end_time = time.time()
    logging.info(f"Total Execution Time: {end_time - start_time:.2f} seconds")

concurrent_test()