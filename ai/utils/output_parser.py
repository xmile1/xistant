import re
from tabnanny import verbose
from typing import Any, Union

from langchain.agents.agent import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish, OutputParserException, PromptValue
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

PREFIX = """You are an output formatter. you can transform the data structure of the response to one of the following formats depending on the prompt:

FORMATS:
---------

"""

GENERIC_FORMAT = """

tool_name: default_format
description: This tool is used when no other tool is used to format the response.
format: {{response}}
"""

FORMAT_INSTRUCTIONS = """When there is a response and it does not contain some of the information that is needed to format the response, generate the missing information.

Do not summarize or edit the information in the response.

You must respond with the toolname and formatted response using the pattern below:
<The Name of the format that was used>
<the formatted response>
"""
THE_INPUT_FORMAT = """
The input is as follows:
prompt: {prompt}
response:
"""

class OutputParser(AgentOutputParser):
    ai_prefix: str = "AI"
    retry_chain: LLMChain
    tools: Any

    @classmethod
    def from_llm(cls, llm, tools):
        prompt = OutputParser.create_prompt(tools)

        llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
        tools_dict = {tool.name: tool for tool in tools}
        return cls(retry_chain=llm_chain, tools=tools_dict)

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS
    
    @classmethod
    def create_prompt(cls, tools) -> str:
        tool_strings = "\n".join(
            [f"format_name: {tool.name}\ndescription: {tool.description}.\nformat: {tool.format}\n" for tool in tools]
        )

        template = "\n\n".join([PREFIX + tool_strings + GENERIC_FORMAT, FORMAT_INSTRUCTIONS, THE_INPUT_FORMAT])

        input_variables = ["prompt"]
        return PromptTemplate(template=template, input_variables=input_variables)
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        return text

    def parse_with_prompt(self, prompt: PromptValue, completion: str) -> Any:

        response = self.retry_chain.run(prompt=prompt, max_iterations=1)
        toolname, formatted_response = response.split("\n", 1)
        
        if not self.tools.get(toolname):
            return completion

        if(self.tools.get(toolname) and self.tools[toolname].parse):
            return self.tools[toolname].parse(formatted_response, prompt, completion)
        
        return formatted_response
