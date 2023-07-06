from langchain import LLMChain, PromptTemplate
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

class ChatGptPlugin():
  def __init__(self, model):
      self.model = ChatOpenAI(temperature=0.7, client=None)
  def get_lang_chain_tool(self):
    chain = LLMChain(llm=self.model, memory=ConversationBufferMemory())
    return [Tool(
          name="Chat GPT",
          description="All requests that starts with /chatgpt must use this tool",
          func=chain.run,
          return_direct=True
    )]
