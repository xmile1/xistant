from tabnanny import verbose
from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from utils.output_parser import OutputParser


class MyAI:
    def __init__(self, model, plugins, alt_model=None):
        self.tools = []
        self.model = model
        self.plugins = []
        self.output_parsers_tools = []

        for plugin in plugins:
            plugin_instance = plugin(self.model)
            self.plugins.append(plugin_instance)

            if(hasattr(plugin_instance, 'get_lang_chain_tool')):
                tool = plugin_instance.get_lang_chain_tool()
                self.tools.extend(tool)

            if(hasattr(plugin_instance, 'get_output_parser_tool')):
                output_parser = plugin_instance.get_output_parser_tool()
                self.output_parsers_tools.append(output_parser)

        self.agent = self.create_agent(self.tools)
        self.output_parser = self.create_output_parser(self.output_parsers_tools)

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
                memory_key="chat_history", return_messages=True, k=5
            ),
        )

    def create_output_parser(self, output_parsers_tools):
        return OutputParser.from_llm(tools=output_parsers_tools, llm=self.model)


    def ask(self, input):
        return self.agent.run(input=input)

    def handle_request(self, request):
        request_string = str(request)
        response = self.ask(request_string)
        final_output = self.output_parser.parse_with_prompt(request_string, response)

        return final_output
