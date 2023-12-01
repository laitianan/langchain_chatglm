ps  -ef | grep python |grep openai_api_qwen.py|grep multiprocessing.spawn| grep -v grep | awk '{print $2}' | xargs kill -9
nohup /opt/anaconda3/envs/py39/bin/python openai_api_qwen.py >> ./openai_api.log 2>&1 &

