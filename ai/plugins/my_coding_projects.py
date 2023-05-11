import os
from llama_index import ComposableGraph, GPTListIndex, LLMPredictor, ServiceContext, SimpleDirectoryReader
from llama_index.langchain_helpers.agents import LlamaToolkit, GraphToolConfig, IndexToolConfig
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform
from langchain.llms import GPT4All, LlamaCpp

class MyCodingProjectsPlugin:
    def __init__(self, model):
        self.projects_file_names = ["flow"]
        self.name = "software_projects"
        self.description = f"useful for when you need to adapting coding answers from a language model to the following software projects: {'or '.join(self.projects_file_names)}"
        self.model = model
    
    def build_indices(self):
      llm_predictor = LLMPredictor(llm=self.model)
      service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

      indices = []

      for project in self.projects_file_names:
        documents = SimpleDirectoryReader(
           input_dir=f'/Users/xmile/Documents/projects/{project}/src', 
           recursive=True, 
           exclude=['**/'],
           file_extractor= {
             "vue": "UnstructuredReader",
             "ts": "UnstructuredReader",
             "js": "UnstructuredReader",
             "json": "UnstructuredReader",
             "py": "UnstructuredReader",
           }
        ).load_data()
        index = GPTListIndex.from_documents(documents, service_context=service_context)

        index.save_to_disk(f"graphs/{project}_code_base.json")
        indices.append({
          "index": index,
          "description": f"useful for when you need to adapt software code answers from a language model to {project}",
          "name": f"{project}_code_base"
        })

      return indices

    def get_lang_chain_tool(self):
      indices = self.build_indices()

      index_tool_config = IndexToolConfig(
        index=indices[0]['index'],
        name=indices[0]['name'],
        description=indices[0]['description'],
        # index_query_kwargs={"verbose": True},
        
      )

      toolkit = LlamaToolkit(
         index_configs=[index_tool_config],
      )
      return toolkit.get_tools()
      
      llm_predictor = LLMPredictor(llm=self.model)
      service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
      index_summaries = [index['description'] for index in indices]

      # if its in the disk, load it
      if os.path.exists(f"graphs/{self.name}_graph.json"):
        graph = ComposableGraph.load_from_disk(f"graphs/{self.name}_graph.json", service_context=service_context)
      else:
        graph = ComposableGraph.from_indices(
            GPTListIndex,
            [i['index'] for i in indices], 
            index_summaries=index_summaries,
            service_context=service_context,
          )
        graph.save_to_disk(f"graphs/{self.name}_graph.json")

      decompose_transform = DecomposeQueryTransform(
          llm_predictor, verbose=True
      )

      # define query configs for graph 
      query_configs = [
          {
              "index_struct_type": "simple_dict",
              "query_mode": "default",
              "query_transform": decompose_transform
          },
          {
              "index_struct_type": "list",
              "query_mode": "default",
              "query_kwargs": {
                  "response_mode": "tree_summarize",
                  "verbose": True
              }
          },
      ]

      # graph config
      graph_config = GraphToolConfig(
          graph=graph,
          name=self.name,
          description=self.description,
          query_configs=query_configs,
          tool_kwargs={"return_direct": True}
      )
      toolkit = LlamaToolkit(
        graph_configs=[graph_config]
      ) 
      return toolkit.get_tools()
