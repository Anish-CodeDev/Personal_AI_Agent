from  llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from PIL import Image
import os
from llama_index.core.indices import MultiModalVectorStoreIndex
llm = GoogleGenAI(model='gemini-2.5-flash-lite-preview-06-17')

def load_data(filepath):

    with open(filepath + '.txt','r') as f:
        text = f.read()
    
    image = Image.open(filepath + '.jpg')
    return Document(text=text,image=image)
def get_query_engine():
    documents = [load_data(f'img/img_{n}') for n in range(1,len(os.listdir('img/'))//2)]
    index = MultiModalVectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine(llm=llm)
    return query_engine