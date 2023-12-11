# langchain_qwen-chat-7b  

#启动脚本

1.启动高并发API服务，执行脚本
sh ./run_vllm_openapi.sh

2.启动提示模板服务，chat_api.py，执行脚本
sh ./run_chatapi.sh

3.启动监听服务，用于函数模板更新之后重启脚本2.（多进程无法共享全局变量，需要重启服务）
sh ./run_monitor.sh

(以上脚本执行缺一不可)