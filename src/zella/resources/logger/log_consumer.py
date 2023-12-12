import threading
import logging
from queue import Queue
from time import sleep


class LogConsumer(threading.Thread):
    def __init__(self, client, batch_size=10, process_interval_seconds=1, max_retries=3):
        super().__init__()
        self.log = logging.getLogger("zella_ai")
        self.queue = Queue()
        self.batch_size = batch_size
        self.process_interval_seconds = process_interval_seconds
        self.stop_thread = False
        self.start()
        self.client = client
        self.max_retries = max_retries

    def consume(self, item):
        self.queue.put(item)

    def run(self):
        while True:
            if self.stop_thread and self.queue.empty():
                return

            batch_data = []
            while not self.queue.empty() and len(batch_data) < self.batch_size:
                batch_data.append(self.queue.get())

            if batch_data:
                self.process_batch(batch_data)

            sleep(self.process_interval_seconds)

    def process_batch(self, batch_data):
        attempt = 0

        while attempt < self.max_retries:
            try:
                self.client.post(self.client.base_url + "/log/batch", batch_data)
                break
            except Exception as e:
                self.log.exception("Attempt %d - Upload to Zella failed: %s", attempt + 1, e)
                attempt += 1
                sleep(1)

        if attempt == self.max_retries:
            self.log.error("All retry attempts failed for batch upload.")

        for _ in batch_data:
            self.queue.task_done()

    def stop_processing(self):
        self.stop_thread = True
        self.queue.join()
        self.join()

    def __del__(self):
        self.stop_processing()
