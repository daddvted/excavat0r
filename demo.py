import time
import queue
from queue import Empty
import threading

task_queue = queue.Queue()


class ProducerThread(threading.Thread):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def run(self):
        global task_queue

        # while True:
        for item in self.items:
            task_queue.put(item)
            print("Produced: {}".format(item))
            # time.sleep(1)
        print("Producer [exit]")


class ConsumerThread(threading.Thread):
    def run(self):
        global task_queue

        while True:
            print("Consumer running")
            try:
                num = task_queue.get(block=False)
            except Empty:
                time.sleep(5)
                if task_queue.empty():
                    print("{} [exit]".format(self.name))
                    break
                else:
                    continue

            print("{} consumed: {}".format(self.name, num))
            time.sleep(1)
            task_queue.task_done()


if __name__ == "__main__":
    print("[ main ] starting...")
    nums = range(10)
    ProducerThread(nums).start()

    for _ in range(1, 3):
        t = ConsumerThread()
        t.start()

    task_queue.join()

    print("[ main ] the end")
