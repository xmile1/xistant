from langchain import LLMChain, PromptTemplate
from langchain.agents.tools import Tool


class GermanTeacherPlugin():
  def __init__(self, model):
      self.model = model
  def get_lang_chain_tool(self):
    german_teacher_prompt = PromptTemplate.from_template(
    "You are a german teacher having a conversation with a human with A1 language proficency, You gradually and efficiently introduce new words and sometimes tell the user the english translation in a conversational manner \n human: {prompt}\n {{response}}"
    )
    todo_chain = LLMChain(llm=self.model, prompt=german_teacher_prompt)
    return [Tool(
          name="Specialized German Model",
          description="This tool is a German language model designed for engaging in German conversations. It excels at understanding and generating responses in German. All requests that starts with /a1teacher must use this tool. It takes the user's query as input and provides the best German response.",
          func=todo_chain.run,
          return_direct=True
    )]
