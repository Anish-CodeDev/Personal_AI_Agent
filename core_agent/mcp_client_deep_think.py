from typing import Optional
from contextlib import AsyncExitStack
import re
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
gemini = genai.Client(api_key='AIzaSyCFJ3RwiHvLTy9QYMhraasRH1D3h7zZ2G0')

def get_result(query,tools):
    tools_with_desc = {
         tool.name:tool.description
         for tool in tools
    }
    response = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""Given the {query}, decide the tool by the tool's name and description which are represented by triple backticks
            ```{tools_with_desc}```
            Choose the tool best suits the user's query, extract arguments,
            Return the best tool with the key 'tool'and the extracted arguments under the key 'args' in the form of json.
            Remove all the backticks like ``` at any cost.
            """,
    )
    return eval(str(re.sub('json','',response.text)))


class MCPClient:
    def __init__(self):
        self.session:Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    
    async def connect_to_maps_server(self,query):

            server_params = StdioServerParameters(
                command='python',
                args=['D:\Anish\ComputerScience\Computer science\Machine Learning\mcp\mcp_servers\maps\server.py'],
                env=None
            )
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.read,self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.read,self.write))

            await self.session.initialize()

            response = await self.session.list_tools()
            tools = response.tools
            result = get_result(query,tools)
            return result
    async def connect_to_research_server(self,query):
         server_params = StdioServerParameters(
              command=r'D:\Anish\ComputerScience\Computer science\Machine Learning\mcp\mcp_servers\deep_research\venv\Scripts\python.exe',
              args=['D:\Anish\ComputerScience\Computer science\Machine Learning\mcp\mcp_servers\deep_research\server.py'],
              env=None
         )
         stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
         self.read,self.write = stdio_transport
         self.session = await self.exit_stack.enter_async_context(ClientSession(self.read,self.write))
         await self.session.initialize()
         response = await self.session.list_tools()
         tools = response.tools
         result = get_result(query,tools)
         print(type(result))
         return result
client = MCPClient()
#user_inp = input("User: ")
async def deep_research(user_inp):
     print("This might take a while.")
     try:
            result = await client.connect_to_research_server(user_inp)
            print(result)
            tool_name = result['tool']
            args = result['args']
            print(args)
            response = await client.session.call_tool(tool_name,args)
            print(response.content[0].text)
            return "The deep research report is shown above"
     except:
          pass
     finally:
          await client.exit_stack.aclose()
#asyncio.run(deep_research(user_inp))