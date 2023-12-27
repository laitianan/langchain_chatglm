# langchain_qwen-chat-7b  

#启动脚本

1.启动高并发大模型API服务，执行脚本
sh ./run_vllm_openapi.sh

2.启动提示模板服务，chat_api.py，执行脚本
sh ./run_chatapi.sh
(以上脚本执行缺一不可)


3.启动监听服务，用于函数模板更新之后更新接口初始化.（多进程无法共享全局变量，通过监听redis模板信息改变版本跟当前内存版本不一样
，重新加载变量,通过发送100一次请求，给每个worker提前加载变量）  该脚本不执行，只是影响函数模板更新后，用户存在可能需要等待加载变量（N 个worker的其中一个更新变量）
sh ./run_monitor.sh

