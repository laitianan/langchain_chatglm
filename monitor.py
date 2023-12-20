import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
import os
import  requests
class MyHandler(FileSystemEventHandler):
   def on_modified(self, event):

        print("*************************************************\n***************************************************\n*************************************")
        base_url = "127.0.0.1:8084"
        for i in range(100):
            t1 = time.time()
            r1 = requests.post(f"http://{base_url}/get_all_template/completions")
            # print(r1.content.decode("utf8"))
            content = r1.content.decode("utf8")
            print(content)
            t2 = time.time()
            print("总耗时(秒):", t2 - t1)

           # break




if __name__ == "__main__":
   event_handler = MyHandler()
   observer = Observer()
   observer.schedule(event_handler, path=config.saveinterfacepath, recursive=False)
   observer.start()
   try:
       while True:
           time.sleep(1)
   except KeyboardInterrupt:
       observer.stop()
   observer.join()