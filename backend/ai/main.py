from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from ai.output_parser import OutputParser


class AI:
    def __init__(self, model, plugins):
        self.tools = []
        self.model = model
        self.plugins = []
        output_parsers_tools = []

        for plugin in plugins:
            plugin_ = plugin(self.model)
            self.plugins.append(plugin_)

            if(hasattr(plugin_, 'get_lang_chain_tool')):
                tool = plugin_.get_lang_chain_tool()
                self.tools.extend(tool)

            if(hasattr(plugin_, 'get_output_parser_tool')):
                output_parser = plugin_.get_output_parser_tool()
                output_parsers_tools.append(output_parser)

        self.agent = self.create_agent(self.tools)
        self.output_parser = self.create_output_parser(output_parsers_tools)

    def create_agent(self, tools):
        agent = ConversationalAgent.from_llm_and_tools(
            llm=self.model,
            tools=tools,
        )
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            memory=ConversationBufferWindowMemory(
                memory_key="chat_history", return_messages=True, k=8
            ),
        )

    def create_output_parser(self, output_parsers_tools):
        return OutputParser.from_llm(tools=output_parsers_tools, llm=self.model)

    def run(self, request):
        request_string = str(request)
        response = self.agent.run(input=request_string)
        final_output = self.output_parser.parse_with_prompt(request_string, response)

        return final_output
