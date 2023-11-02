ps  -ef | grep python |grep chat_api.py| grep -v grep | awk '{print $2}' | xargs kill -9
nohup python chat_api.py >> ./chat_api.log 2>&1 &
