
api_base = "http://192.168.0.11:8081/v1"
# llm_model="Qwen-7B-Chat"
llm_model="Qwen-14B-Chat-Int4"

# llm_model="Qwen-7B-Chat"
# api_base = "http://192.168.0.11:8082/v1"
saveinterfacepath="./data/interface_template_dict.pkl"
topp_=0.8
def read_api_keys():
    with open("./data/api_keys.txt","r",encoding="utf-8") as f:
        api_keys=[]
        for key in f:
            api_keys.append(key.strip())
    return api_keys

api_keys=read_api_keys()
check_api_key=True
