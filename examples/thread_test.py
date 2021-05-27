from threading import Thread
from queue import Queue
import time


def worker():
    while True:
        item = q.get()
        print(item)
        time.sleep(5)
        q.task_done()


q = Queue()
for i in range(3):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in ['1', '2', '3', '4']:
    q.put(item)


q.join()
