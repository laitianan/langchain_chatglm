ps  -ef | grep python |grep chat_api.py| grep -v grep | awk '{print $2}' | xargs kill -9
ps  -ef | grep python |grep multiprocessing| grep -v grep | awk '{print $2}' | xargs kill -9
nohup /opt/anaconda3/envs/py39/bin/python chat_api.py >> ./chat_api.log 2>&1 &
