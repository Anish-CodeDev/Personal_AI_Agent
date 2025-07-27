# 📬 AI Inbox & Document Assistant
## Overview
This AI Agent is designed to manage your email inbox efficiently and intelligently respond to queries related to large, unstructured documents. It combines natural language understanding with retrieval-augmented generation to automate workflows and surface relevant information with minimal manual input.

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

### Unified Interface
- Both the email agent and the document(RAG) agent are integrated into a single unified ReAct agent.
- The agent can be accessed by a CLI interface, by running a python file, which gives access to the ReAct agent.

## 🛠️ Technology Stack
| Layer            | Tech                                      |
|------------------|-------------------------------------------|
| Language Model   | Gemini 2.5 Flash-Lite Preview             |
| Agentic Framework| LangGraph                                 |
| Document Indexing| LlamaIndex                                |
| Vector Store     | DeepLake                                  |
| Email Integration| Gmail API(SMTP is used for sending emails)|
 
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
