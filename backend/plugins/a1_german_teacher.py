import os
from langchain import LLMChain, PromptTemplate
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

no_of_times_used = 0
class GermanTeacherPlugin():
  def __init__(self, model):
      self.model = ChatOpenAI(temperature=0.5, max_tokens=512, client=None)
  def get_lang_chain_tool(self):
    # get the file use_words.txt
    german_teacher_prompt = PromptTemplate.from_template(
    """You are a german friend that speaks Deutsch.
    Make sure your responses are not too long so that the user can understand you.
    Talk about topic randomly in fields ranging from history, science, math, humanities, and more.
    Your goal is to teach the grammar and vocabulary of the german language through conversation.

    Always use this Response format
    ---------------
    First give a converationlike response to the conversation and/or ask a question, or talk about something.

    Deutsch tips:
    explain some grammar rules based on the words used in your response.

    Translation:
    translate your response to English.

    Example
    ---------------
    Was ist deine Lieblingsstadt in Deutschland?

    Deutsch Tip: In this response, "Was ist deine Lieblingsstadt in Deutschland?" is a question. In German, questions are formed by putting the verb first. The verb in this sentence is "ist" which means "is". The subject is "deine Lieblingsstadt" which means "your favorite city". The object is "in Deutschland" which means "in Germany". The question is asking "What is your favorite city in Germany?"

    Translation:
    What is your favorite city in Germany?

    Start
    ---------------
    human: {prompt}
    response:
    """
    )
    todo_chain = LLMChain(llm=self.model, prompt=german_teacher_prompt, memory=ConversationBufferMemory())
    return [Tool(
          name="Specialized German Model",
          description="This tool is a German language model designed for engaging in German conversations. It excels at understanding and generating responses in German. you MUST use this tool when the query contains /a1teacher. also all deutsch conversations MUST use this tool. It takes the user's query as input and provides the best German response.",
          func=todo_chain.run,
          return_direct=True
    )]
