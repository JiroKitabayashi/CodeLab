import requests
import concurrent.futures
import asyncio
import random
import time

def generate_test_url():
    # ランダムなステータスコードを生成
    status_code = random.choice([200, 301, 400, 404, 500])

    # ランダムな遅延時間を生成
    delay = random.randint(1, 10)

    # ステータスコードと遅延時間を組み合わせたURLを生成
    url = f"https://httpstat.us/{status_code}?sleep={delay*1000}"

    return url

def request_url(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    print(f"{url}: {response.status_code} ({end_time - start_time:.2f} seconds)")

# 並列処理
def run_parallel():
    # テスト用のURLを10個含む配列を生成
    test_urls = [generate_test_url() for i in range(10)]

    # ThreadPoolExecutorを作成して、URLを並列処理
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(request_url, test_urls)

# 並行処理
async def run_concurrent():
    # テスト用のURLを10個含む配列を生成
    test_urls = [generate_test_url() for i in range(10)]

    # URLを非同期にリクエスト
    tasks = []
    for url in test_urls:
        tasks.append(asyncio.create_task(request_url_async(url)))

    # 全てのタスクが完了するまで待機
    await asyncio.gather(*tasks)

# 非同期リクエスト
async def request_url_async(url):
    start_time = time.time()
    response = await asyncio.to_thread(requests.get, url)
    end_time = time.time()

    print(f"{url}: {response.status_code} ({end_time - start_time:.2f} seconds)")

# 並列処理を実行
print("Parallel Execution")
start_time = time.time()
run_parallel()
end_time = time.time()
print(f"Total Execution Time: {end_time - start_time:.2f} seconds")

# 並行処理を実行
print("Concurrent Execution")
start_time = time.time()
asyncio.run(run_concurrent())
end_time = time.time()
print(f"Total Execution Time: {end_time - start_time:.2f} seconds")