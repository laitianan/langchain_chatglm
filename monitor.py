import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
import os

class MyHandler(FileSystemEventHandler):
   def on_modified(self, event):

        print("*************************************************\n***************************************************\n*************************************")
        # s1="ps  -ef |grep chat_api.py| grep -v grep | awk '{print $2}' | xargs kill -9 "
        # s3="nohup /opt/anaconda3/envs/py39/bin/python chat_api.py >> ./chat_api.log 2>&1 &"
        time.sleep(5)
        s4="sh ./run_chatapi.sh"
        for cmd in [s4]:
           output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
           print(output)

           if output.returncode == 0:
               print(f"----------------执行命令成功{cmd}-----------------------------")
           else:
               print(f"----------------执行命令失败{cmd}-----------------------------")

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