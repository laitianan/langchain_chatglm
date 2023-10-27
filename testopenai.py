import openai

# print(text)
if __name__ == "__main__":
    openai.api_base = "http://192.168.0.11:8081/v1"
    openai.api_key = "none"
    for chunk in openai.ChatCompletion.create(
        model="internlm-chat-7b",
        messages=[
            {"role": "user", "content": "什么是AI"},
        ],
        temperature=0.8,
        max_tokens=200,
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
    "stream": false
  }' \
  http://127.0.0.1:8081/v1/chat/completions

"""

# import requests
# r1 = requests.post("http://127.0.0.1:8081/v1/chat/completions",header, data=post_json)
# print(r1.content.decode("utf8"))