ps  -ef | grep python |grep openai_api.py| grep -v grep | awk '{print $2}' | xargs kill -9
nohup python openai_api.py >> ./openai_api.log 2>&1 &
