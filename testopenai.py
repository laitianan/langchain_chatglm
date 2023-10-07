import openai
if __name__ == "__main__":
    openai.api_base = "http://192.168.0.11:8081/v1/"
    openai.api_key = "none"
    for chunk in openai.ChatCompletion.create(
        model="internlm-chat-7b",
        messages=[
            {"role": "user", "content": "你好"}
        ],
        max_tokens=8000,
        temperature=0.9,
    ):

        if hasattr(chunk.choices[0].delta, "content"):
            print(chunk.choices[0].delta.content, end="", flush=True)


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