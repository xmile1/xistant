from langchain import LLMChain, PromptTemplate
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

class ChatGptPlugin():
  def __init__(self, model):
      self.model = ChatOpenAI(temperature=0.7, client=None)
  def get_lang_chain_tool(self):

    template = """
    {history}
    Human: {human_input}
    Assistant:"""

    prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

    chain = LLMChain(llm=self.model, prompt=prompt, memory=ConversationBufferWindowMemory(k=2))
    return [Tool(
          name="Chat GPT",
          description="you MUST use this tool when the query contains /chatgpt, ",
          func=lambda input: chain.predict(human_input=input),
          return_direct=True
    )]
