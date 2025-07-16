# Few lines of code are commented out since we have already uploaded the embeddings of the nodes to our vector store
# If there is a change in the data comment out the lines commented
from llama_index.core import Settings,StorageContext,SimpleDirectoryReader,VectorStoreIndex,load_index_from_storage
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.gemini import GeminiEmbedding
from  llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
import os
from llama_index.postprocessor.cohere_rerank import CohereRerank
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCFJ3RwiHvLTy9QYMhraasRH1D3h7zZ2G0'
os.environ['ACTIVELOOP_TOKEN'] = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTc1MjQxNTM1MywiZXhwIjoxNzgzOTUxMzQ0fQ.eyJpZCI6ImFrYW5pc2g0NDciLCJvcmdfaWQiOiJha2FuaXNoNDQ3In0.0LvHB3MAmmx_zZoVkqEa_taqfdgU6LtqRUBSuzyIcW4jS-igRJtNaBmb1R4ttwgsWGLY8iAoAp_ENharKghDyw'
llm = GoogleGenAI(model='gemini-2.5-flash-lite-preview-06-17')
embed_model = GeminiEmbedding(models='model/embedding-001')
Settings.llm = llm
Settings.embed_model = embed_model
dataset_path = f"hub://akanish447/personal_agent/"
cohere_rerank = CohereRerank(api_key='UyZatwiADpPOFnEuws2nE7z5F3oP95JapKp2q6ER',top_n=10)

def load_write_data(write):
    if write:
        documents = SimpleDirectoryReader('text/').load_data()
        node_parser = SimpleNodeParser(chunk_size=512,chunk_overlap=64)
        nodes = node_parser.get_nodes_from_documents(documents)

        

        vector_store = DeepLakeVectorStore(dataset_path=dataset_path,overwrite=True)


        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        vector_index = VectorStoreIndex(nodes,storage_context=storage_context)
        query_engine = vector_index.as_query_engine(similarity_top_k=10,node_post_processors=[cohere_rerank])

    else:
        documents = SimpleDirectoryReader('text/').load_data()
        node_parser = SimpleNodeParser(chunk_size=512)
        nodes = node_parser.get_nodes_from_documents(documents)
        vector_store = DeepLakeVectorStore(dataset_path=dataset_path,overwrite=False)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        vector_index = VectorStoreIndex(nodes,storage_context=storage_context)
        query_engine = vector_index.as_query_engine(similarity_top_k=10,node_post_processors=[cohere_rerank])
    
    return query_engine

def load_write_csv(write):
    csv = SimpleDirectoryReader('csv/').load_data()
    node_parser = SimpleNodeParser(chunk_size=512)
    nodes = node_parser.get_nodes_from_documents(csv)
    cohere_rerank_csv = CohereRerank(api_key='UyZatwiADpPOFnEuws2nE7z5F3oP95JapKp2q6ER',top_n=2)
    
    if write:
        index = VectorStoreIndex(nodes=nodes)
        index.storage_context.persist(persist_dir='./local_vector_store/')
        query_engine = index.as_query_engine(similarity_top_k=5,node_post_processors=[cohere_rerank_csv])
        return query_engine
    
    storage_context = StorageContext.from_defaults(persist_dir='./local_vector_store/')
    index = load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine(similarity_top_k=5,node_post_processors=[cohere_rerank_csv])
    return query_engine
def query_doc(q,query_engine):
    return str(query_engine.query(q))