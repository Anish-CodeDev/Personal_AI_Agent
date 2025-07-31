# 📬 Personal AI Agent
## Overview
This AI Agent is designed to manage your email inbox efficiently and intelligently respond to queries related to large, unstructured documents. It combines natural language understanding with retrieval-augmented generation to automate workflows and surface relevant information with minimal manual input.

This AI Agent is also capable of conducting **deep research**, finding the **distance between two places** and offering **navigation between two places** with the help of `openrouteservice` API. 

This AI Agent also has the feature of **autonomously browsing the web** using the `playwright` framework and a `VLM(Vision Language Model)`.

## 🚀 Features
### Email Inbox Automation
- Summarizes email content and suggests quick replies from any folder/label.
- Can sort emails from any folder and move non-important emails to the spam folder.
- Given the topic the agent can send an email to any person if his email address is provided.

### Document Question Answering(Offers visual reasoning based on the images provided)

- Handles large documents using chunking and vector embeddings

- Supports plain text formats, CSV files(Any other spreasheet format) and also images(.jpg,.jpeg,.png)
- Answers natural language queries with contextual precision
- Uses semantic retrieval for accurate and scalable responses

### Deep Research

- With the help of this feature the user can get a complete research report, comprising of the meaning of the topic, its use cases, advantages and disadvantages.
- This feature first extracts the topic from the user's prompt.
- It then searches the web on the topic extracted
- Then all the information is converted into embedding vectors using an `embedding model` and the embedding vectors are stored in the vector store.
- Then we ask the `LLM` to generate a series of questions revolving around the topic asked by the user.
- Then we collect the answers to all these questions by utilizing the `RAG Query Engine`
- Then all the collected answers are compiled and the resultant is shown to the user.
- This is maintained using a dedicated `MCP (Model Context Protocol) Server`.

### Integration with GPS
- With the help of `openrouteservice` API, the agent can calculate the distance between two points and also offers navigation between the two places
- The LLM first captures the two places entered in the user's prompt and also figures out the task requested by the user.
- The task may be either **navigation** or the calculation of **distance** between two places.
- Using the `openrouteservice` API, the geo-coordinates of the places are retrieved using the names of the places mentioned by the user.
- Accordingly, the geo-coordinates are fed into the API and the distance/navigation between two places is shown to the user
- This is maintained using a dedicated `MCP (Model Context Protocol) Server`.
### Autonomous browsing
- This agent can perform various autonomous such as:
- Booking hotels(Choosing the best)
- Booking movie tickets
- Shopping for item(selects the best item based on the requirements of the user)
- Filling online forms
- Selecting specific elements
### Unified Interface
- Both the email agent and the document(RAG) agent,maps,deep research and autonomous browsing are integrated into a single unified ReAct agent.
- The agent can be accessed by a CLI interface, by running a python file, which gives access to the ReAct agent.

## 🛠️ Technology Stack
| Layer            | Tech                                      |
|------------------|-------------------------------------------|
| Language Model   | Gemini 2.5 Flash-Lite                     |
| Agentic Framework| LangGraph                                 |
| Document Indexing| LlamaIndex                                |
| Vector Store     | DeepLake                                  |
| Email Integration| Gmail API(SMTP is used for sending emails)|
|Autonomous browsing| Playwright                               | 
 
## 📁 Setup Instructions
1. Clone this repo
2. Install dependencies:
   `pip install -r requirements.txt`
3. Fill in all the api keys where ever required.
4. Running python files: You'll have to run two python files, one is the agent.py under the email_agent folder, thr other one is server.py under the rag_agent folder, the server.py holds the instructions of the `flask` server.
   Go to the email_agent folder and run the following command:
   `python agent.py`

   Then go to the rag_agent folder and run the following command:
   `flask --app server run`
