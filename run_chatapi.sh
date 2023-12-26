ps  -ef | grep python |grep chat_api| grep -v grep | awk '{print $2}' | xargs kill -9
ps  -ef | grep python |grep multiprocessing| grep -v grep | awk '{print $2}' | xargs kill -9
#nohup /opt/anaconda3/envs/py39/bin/python chat_api.py >> ./chat_api.log 2>&1 &
nohup /opt/anaconda3/envs/py39/bin/uvicorn chat_api:app --host 0.0.0.0 --port 8084 --workers 16 >> ./chat_api.log 2>&1 &
