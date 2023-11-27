from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from MyOpenAI import myOpenAi
from intentAgent_model import IntentAgent
from langchain.agents import AgentExecutor
from prompt_helper import init_all_fun_prompt
from tool_model import Model_Tool, Unknown_Intention_Model_Tool
from utils import load_interface_template


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ChatConfig(metaclass=Singleton):
    def __init__(self):
        # 初始化全局变量
        self.agent_exec, self.toos_dict, self.llm, self.initparam, self.search=None,None,None,None,None
        self.saveinterfacepath = "./data/"
        self.init_run()
        print("333333333333333333333333333333333333")

    def get_init(self):
        return self.agent_exec,self.toos_dict,self.llm,self.initparam,self.search

    def init_run(self):

        self.initparam = load_interface_template(self.saveinterfacepath)
        if not self.initparam:
            return
        from search_intention import  Doc,Query_Search
        self.search = Query_Search()
        self.llm = myOpenAi(temperature=0.8,max_tokens=2000)
        toos_dict = {}
        docs=[]
        prompt_dict=init_all_fun_prompt(self.initparam)
        for param in self.initparam.params  :
            if param.usableFlag:
                toos_dict[param.id]=Model_Tool(name=param.name,description=param.functionDesc,id=param.id,llm=self.llm,prompt_dict=prompt_dict)
                docs.append(Doc(funtion_id=param.id, name=param.name))
        self.search.load(docs)
        tools=list(toos_dict.values())
        unknowntool=Unknown_Intention_Model_Tool(llm=self.llm)
        tools.append(unknowntool)
        # # 选择工具
        agent = IntentAgent(tools=tools, llm=self.llm,default_intent_name=unknowntool.name)
        self.agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,  tools=tools, verbose=False,max_iterations=1)
        return self.agent_exec,self.toos_dict,self.llm,self.initparam,self.search



# class OpenAPI_Config(metaclass=Singleton):
class OpenAPI_Config():
    def __init__(self):
        # 初始化全局变量
        self.llm_checkpoint_path="/data/laitianan/qwen-14b-4bit"
        self.emb_path="/data/laitianan/Langchain-Chatchat-master/text2vec-large-chinese"
        self.model, self.tokenizer, self.t2v_model=None,None,None
        self.init_run()


    def get_init(self):
        return self.model,self.tokenizer,self.t2v_model

    def init_run(self):

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.llm_checkpoint_path,
            trust_remote_code=True,
            resume_download=True,
        )

        device_map = "auto"

        self.model = AutoModelForCausalLM.from_pretrained(
            self.llm_checkpoint_path,
            device_map=device_map,
            trust_remote_code=True,
            resume_download=True,
        ).eval()

        self.model.generation_config = GenerationConfig.from_pretrained(
            self.llm_checkpoint_path,
            trust_remote_code=True,
            resume_download=True,
        )
        # from text2vec import SentenceModel
        # self.t2v_model = SentenceModel(self.emb_path)

if __name__ == "__main__":
    config=ChatConfig()
    # print(config.initparam)
    config=ChatConfig()
    print(config.initparam)