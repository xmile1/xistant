from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.agents.tools import Tool
from langchain.tools import BaseTool


class GermanTeacherPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
    german_teacher_prompt = PromptTemplate.from_template(
    "You are a german teacher having a conversation with a human with A1 language proficency, You gradually and efficiently introduce new words and sometimes tell me the english translation in a conversational manner \n human: {prompt}"
    )
    todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=german_teacher_prompt)
    return [Tool(
          name="Specialized German Model",
          func=todo_chain.run,
          description="A german language model that is very good at german conversations, Input is the users query and it will give the best german response",
          return_direct=True
      )]
