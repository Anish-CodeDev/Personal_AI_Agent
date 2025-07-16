from flask import Flask,request
from agent import query
from markupsafe import escape
from werkzeug.utils import secure_filename
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
import os
from rag import load_write_data,load_write_csv
from image_rag import get_query_engine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core import Settings
from  llama_index.llms.google_genai import GoogleGenAI
import re
query_engine = None
Settings.llm = GoogleGenAI(model='gemini-2.5-flash-lite-preview-06-17')
app = Flask(__name__)
llm = GoogleGenAI(model='gemini-2.5-flash-lite-preview-06-17')
def write_status(status:str):
    with open("status/status.txt",'w') as f:
        f.write(f"{status}")
        f.close()
def get_retriever_query_engine():
        query_engine = load_write_data(True)
        csv_query_engine = load_write_csv(True)
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
        return router_query_engine
def read_status():
    status = None
    with open('status/status.txt','r') as f:
        status = f.read()
    
    if status == "True":
        
        query_engine = load_write_data(True)
        csv_query_engine = load_write_csv(True)
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
        return router_query_engine


@app.route("/query/<input>",methods=['GET'])
def agent(input):
    user_inp = escape(input)
    if query_engine:
        write_status('False')
    return query(str(user_inp),query_engine)

@app.route('/upload/',methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = filename.rsplit('.',1)[1].lower()
    global query_engine
    if extension == "csv":
        file.save(os.path.join('./csv/',filename))
        #write_status("True")
        
        query_engine = get_retriever_query_engine()
        return "Success"
    elif extension == "txt":

        file.save(os.path.join('./text/',filename))
        #write_status("True")
        query_engine = get_retriever_query_engine()
        return "Success"
    elif extension == "png" or extension == "jpg" or extension == "jpeg":
        img_len = len(os.listdir('./img'))//2
        file.save(os.path.join('./img/',f'img_{img_len+1}.jpg'))
        messages = [
            ChatMessage(
                role='user',
                blocks=[
                    ImageBlock(path=os.path.join('./img/',f"img_{img_len+1}.jpg")),
                    TextBlock(text='Generate a suitable caption for the uploaded image')
                ]
            )
        ]
        r = llm.chat(messages)
        r = re.sub("assistant:",'',str(r))
        
        with open(f'./img/img_{img_len+1}.txt','w') as f:
            f.write(str(r))
            f.close()
        #write_status("True")
        query_engine = get_retriever_query_engine()
        return "Success"
    return "Failure"