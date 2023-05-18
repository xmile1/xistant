import re
from tabnanny import verbose
from typing import Any, Union

from langchain.agents.agent import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish, OutputParserException, PromptValue
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


GENERIC_TOOL = """
tool_name: general_format
description: For general responses that do not need to be formatted
format: response
"""

FORMAT_INSTRUCTIONS = """Depending on the prompt, select a format to use from the tools above, If the response does not contain relevant information to create the format, generate the relevant information and add it to the response:

Only return the toolname and formatted response without any additional information using the pattern below:

The Name of the tool that was used to format the response
the formatted response

"""

THE_INPUT_FORMAT = """The input format is:
prompt: {prompt}
response: {response}
"""

class OutputParser(AgentOutputParser):
    ai_prefix: str = "AI"
    retry_chain: LLMChain
    tools: Any

    @classmethod
    def from_llm(cls, llm, tools):
        prompt = OutputParser.create_prompt(tools)

        llm_chain = LLMChain(llm=llm, prompt=prompt)
        tools_dict = {tool.name: tool for tool in tools}
        return cls(retry_chain=llm_chain, tools=tools_dict)

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS
    
    @classmethod
    def create_prompt(cls, tools) -> str:
        tool_strings = "\n".join(
            [f"toolname: {tool.name}\ndescription: {tool.description}\nformat: {tool.format}" for tool in tools]
        )

        template = "\n\n".join(["TOOLS:\n" + tool_strings + GENERIC_TOOL, FORMAT_INSTRUCTIONS, THE_INPUT_FORMAT])

        input_variables = ["prompt", "response"]
        return PromptTemplate(template=template, input_variables=input_variables)
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        return text

    def parse_with_prompt(self, prompt: PromptValue, completion: str) -> Any:

        response = self.retry_chain.run(prompt=prompt, response=completion, verbose=True,max_iterations=1)
        toolname, formatted_response = response.split("\n", 1)

        if(self.tools.get(toolname) and self.tools[toolname].parse):
            return self.tools[toolname].parse(formatted_response, prompt)
        
        return formatted_response
