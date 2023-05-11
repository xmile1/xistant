from typing import Any, Mapping, Optional, List
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.llms.base import LLM

from langchain.chat_models import ChatOpenAI
from fastapi import FastAPI, Request
from langchain.agents import AgentType
import requests
from plugins.devotionals import DevotionalsPlugin
from plugins.german_teacher import GermanTeacherPlugin
from plugins.my_movie_preference import MyMoviePreferencePlugin
from plugins.internet_search import InternetSearchPlugin
from plugins.my_coding_projects import MyCodingProjectsPlugin
from langchain.llms import GPT4All
from fastapi.middleware.cors import CORSMiddleware
from gpt4free import Provider, Completion, you, forefront, quora
from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed, wait_random_exponential
 
class CustomLLM(LLM):
        
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    @retry(wait=wait_fixed(20), stop=stop_after_attempt(1))
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: any = None
    ) -> str:
            result = Completion.create(provider=Provider.Theb, prompt=prompt)

            if(result.startswith("Unable to fetch the response, Please try again.")):
                print("failed")
                raise Exception("Unable to fetch the response, Please try again.")
            return result    


class MyAI:
    def __init__(self, model, plugins, alt_model=None):
        self.tools = []
        self.model = model
        self.alt_model = alt_model
        self.plugins = []

        for plugin in plugins:
            plugin_instance = plugin(self.model)
            self.plugins.append(plugin_instance)
            
            tool = plugin_instance.get_lang_chain_tool()
            self.tools.extend(tool)

        self.agent = self.create_agent(self.tools)

    def create_agent(self, tools):
        agent = initialize_agent(
            tools,
            llm=self.model,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            ),
        )
        return agent
    
    def parse_response(self, response):
        for plugin in self.plugins:
            response = plugin.parse_response(response)

    def ask(self, input):
        return self.agent.run(input=input)

    def handle_request(self, request):
        try:
            request_string = str(request)
            response = self.ask(request_string)
        except Exception as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output:"):
                raise e
            response = response.removeprefix(
                "Could not parse LLM output: `"
            ).removesuffix("`")

        # TODO: add a plugin system for this
        if request_string.startswith("{'handler': {'name':"):
            url = "https://hooks.nabu.casa/gAAAAABkWTTNI-pAckU0gC2GeJYxnOFyJyVI81WSwOHD1KSa_Mv8G4UutufXnodtLR7XhN8tbRnygnIDaNcMLK4BKH5G1IKakIfJISul8XePr33EGW-vYGraSNYkwZE9qvrN5KREey53TgTO2_clXzEUdVngYey0V8wBrbHb-TlHftdg4U1eVJc="
            headers = {"Content-Type": "application/json"}
            requests.post(url, headers=headers, json={"text": response})

        if  request_string.startswith("{'query': 'give me a new german word"):
            url = "https://hooks.nabu.casa/gAAAAABkWTTt6eCMzxHXt8zgAP0XuM2MoYHy1kB2MTHA6Y35EnLXm_HotGl0zn-eo4oGmYZIblZ6lh0txubidSH2zwrqca8lFBkFEJ8LeVlXAMYE7-UnDejmOQApB6AGqApH394_9rUeoNgaPWuMnlWhrEYGMFMDYyezv4Z2PEZclP6yvHd_Oxg="
            headers = {"Content-Type": "application/json"}
            requests.post(url, headers=headers, json={"text": f"Hi there, This is your german teacher, get ready for your new word. {response}"})

        return response


def start():
    model = ChatOpenAI(
        temperature=0.3,
        openai_api_key="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",
        max_tokens=512,
    )

    # model = CustomLLM()

    # alt_model = GPT4All(
    #     model="/Users/xmile/Documents/projects/my-ai/ai/models/ggml-model-q4_1.bin",
    #     verbose=True,
    # )

    ai = MyAI(
        model,
        [InternetSearchPlugin, MyMoviePreferencePlugin, GermanTeacherPlugin, DevotionalsPlugin],
        alt_model=model,
    )
    return ai


ai = start()
app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def root(request: Request):
    body = await request.json()
    response = ai.handle_request(body)

    return response
