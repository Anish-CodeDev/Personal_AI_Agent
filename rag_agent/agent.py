from rag import load_write_data,load_write_csv
from image_rag import get_query_engine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core import Settings
from  llama_index.llms.google_genai import GoogleGenAI
Settings.llm = GoogleGenAI(model='gemini-2.5-flash-lite-preview-06-17')
query_engine = load_write_data(False)
csv_query_engine = load_write_csv(False)
img_query_engine = get_query_engine()
query_doc_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    description=(
        "Useful when the user has questions about to know about text documents without any tables."
    )
)

query_csv_tool = QueryEngineTool.from_defaults(
    query_engine=csv_query_engine,
    description = (
        "This is used when the user has questions about the  csv or spreadsheet files that contain factual information"
    )
)
query_img_tool = QueryEngineTool.from_defaults(
    query_engine=img_query_engine,
    description=(
        "This is used when the user has uploaded images and has reasoning questions about thoses images"
    )
)
router_query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        query_doc_tool,
        query_csv_tool,
        query_img_tool
    ]
)

#user_inp = input("User: ")
def query(q:str,query_engine):
    if query_engine:

        response = query_engine.query(q)
        return str(response)
    else:
        response = router_query_engine.query(q)
        return str(response)
'''
while user_inp !='exit':
    response = router_query_engine.query(user_inp)
    print("AI: ",str(response))
    user_inp = input("User: ")'''