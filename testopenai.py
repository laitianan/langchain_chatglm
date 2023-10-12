import openai
if __name__ == "__main__":
    openai.api_base = "http://192.168.0.11:8081/v1"
    openai.api_key = "none"
    for chunk in openai.ChatCompletion.create(
        model="internlm-chat-7b",
        messages=[
            {"role": "system", "content": "你当前的角色是幸福西饼AI客服，主要负责对用户问答，，问答的方向为4方面，1.财务问答 2.订单详情咨询 3.销量统计，4.退货帮助 ，如果不在你职责范围内的请回答，我帮助不了你"
                                          +"并明确告诉他你可以回答四个方面"},
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "您好，我是幸福西饼的AI客服，有什么我可以帮助您的吗？"},
            {"role": "user", "content": "我想查询下员工问题"},
        ],
        temperature=0.9,
        stream=True
    ):

        if hasattr(chunk.choices[0].delta, "content"):
            print(chunk.choices[0].delta.content, end="", flush=True)

            # {"role": "assistant", "content": "怒发冲冠"},
            # {"role": "user", "content": "你可以使用这个成语造句吗"},

"""
curl -X POST \
        -H "Accept: text/event-stream"  \
  -H "Content-Type: application/json" \
 -d '{
    "model": "internlm-chat-7b",
    "messages": [{"role": "user", "content": "你好，请问你是什么模型"}],
    "stream": true
  }' \
  http://192.168.0.11:8081/v1/chat/completions

"""

#
# curl http://192.168.0.11:8081/v1/chat/completions \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "model": "internlm-chat-20b",
#   "messages": "我叫赖天俊",
#   "max_tokens": 8000,
#   "top_p": 10,
#   "temperature": 0.9,
#     "user": "lai"
# }'
#
# curl http://192.168.0.11:8081/v1/chat/completions \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "model": "internlm-chat-20b",
#   "messages": "我叫赖天俊",
#   "max_tokens": 8000,
#   "top_p": 10,
#   "temperature": 0.9,
#     "user": "jun"
# }'
#
# "model": ""chatglm2-6b"",
#   "messages": "string",
#   "temperature": 0.7,
#   "top_p": 1,
#   "n": 1,
#   "max_tokens": 512,
#   "stop": false,
#   "stream": false,
#   "presence_penalty": 0,
#   "frequency_penalty": 0,
#   "user": "string",
#   "repetition_penalty": 1,
#   "renew_session": false,
#   "ignore_eos": false

# curl http://192.168.0.11:8081/v1/embeddings \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "model": "chatglm2-6b",
#   "input": "你好"
# }'