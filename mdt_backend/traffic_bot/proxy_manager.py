import threading
import queue
import requests
import random

class ProxyManager:
    def __init__(self, proxy_file_path):
        self.valid_proxies = []
        self.proxy_queue = queue.Queue()
        self._load_proxies(proxy_file_path)
        self._validate_proxies()

    def _load_proxies(self, path):
        with open(path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    self.proxy_queue.put(proxy)

    def _validate_proxy(self, proxy):
        try:
            response = requests.get(
                'http://ipinfo.io/json',
                proxies={'http': proxy, 'https': proxy},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def _worker(self):
        while not self.proxy_queue.empty():
            proxy = self.proxy_queue.get()
            if self._validate_proxy(proxy):
                self.valid_proxies.append(proxy)
            self.proxy_queue.task_done()

    def _validate_proxies(self):
        threads = []
        for _ in range(10):  # Number of concurrent threads
            t = threading.Thread(target=self._worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def get_proxy(self):
        if not self.valid_proxies:
            return None
        return random.choice(self.valid_proxies)
