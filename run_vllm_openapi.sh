ps  -ef | grep python |grep fastchat.serve.controller | grep -v grep | awk '{print $2}' | xargs kill -9
ps  -ef | grep python |grep fastchat.serve.vllm_worker | grep -v grep | awk '{print $2}' | xargs kill -9
ps  -ef | grep python |grep fastchat.serve.openai_api_server | grep -v grep | awk '{print $2}' | xargs kill -9

#14B-4BIT 启动脚本
nohup /opt/anaconda3/envs/vllm_int4/bin/python3 -m fastchat.serve.controller >> ./vllm_api.log 2>&1 &
nohup /opt/anaconda3/envs/vllm_int4/bin/python3 -m fastchat.serve.vllm_worker --model-path /data/laitianan/Qwen-14B-Chat-Int4 --trust-remote-code >> ./vllm_api.log 2>&1 &
nohup /opt/anaconda3/envs/vllm_int4/bin/python3 -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8081 >> ./vllm_api.log 2>&1 &


# 7b 启动脚本
#nohup /opt/anaconda3/envs/py392/bin/python3 -m fastchat.serve.controller >> ./vllm_api.log 2>&1 &
#nohup /opt/anaconda3/envs/py392/bin/python3 -m fastchat.serve.vllm_worker --model-path /home/ubuntu/.cache/modelscope/hub/qwen/Qwen-7B-Chat >> ./vllm_api.log 2>&1 &
#nohup /opt/anaconda3/envs/py392/bin/python3 -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8081 >> ./vllm_api.log 2>&1 &