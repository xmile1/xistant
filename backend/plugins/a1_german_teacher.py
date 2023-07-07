from langchain import LLMChain, PromptTemplate
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

class GermanTeacherPlugin():
  def __init__(self, model):
      self.model = ChatOpenAI(temperature=0.5, max_tokens=512, client=None)
  def get_lang_chain_tool(self):
    german_teacher_prompt = PromptTemplate.from_template(
    """You are a german teacher having a conversation with a human with A1 language proficency, You gradually and efficiently introduce new words and sometimes tell the user the english translation in a conversational manner.
    Sometimes also explain the grammar rules but keep it interesting and conversational.

    Make sure your responses are not too long, and that you are not overwhelming the human with too much information.

    Your goal is to make the human gradually understand the grammar and vocabulary of the german language.

    human: {prompt}
    german teacher:
    """
    )
    todo_chain = LLMChain(llm=self.model, prompt=german_teacher_prompt, memory=ConversationBufferMemory())
    return [Tool(
          name="Specialized German Model",
          description="This tool is a German language model designed for engaging in German conversations. It excels at understanding and generating responses in German. you MUST use this tool when the query contains /a1teacher. also all deutsch conversations MUST use this tool. It takes the user's query as input and provides the best German response.",
          func=todo_chain.run,
          return_direct=True
    )]
