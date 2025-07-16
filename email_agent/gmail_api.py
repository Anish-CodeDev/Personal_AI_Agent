import os
import base64
import email
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.header import decode_header
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json",'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail','v1',credentials=creds)
        return service
    except HttpError as e:
        print(f"An error occured",str(e))
        return None
def list_messages(service,target_label,user_id='me',query=''):
    try:
        response = service.users().messages().list(userId=user_id,q=f'label:{target_label}').execute()
        messages = []
        if "messages" in response:
            messages.extend(response['messages'])
        
        while "nextPageToken" in response:
            page_token = response['nextPageToken']
            response = (service.users().messages().list(userId=user_id,q=f'label:{target_label}',pageToken=page_token).execute())

            if "messages" in response:
                messages.extend(response['messages'])
            
        return messages
    
    except HttpError as e:
        print("An error occurred: ",str(e))
        return []

def get_subject(service,msg_id,user_id='me'):
    try:
        message = service.users().messages().get(userId=user_id,id=msg_id,format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_message = email.message_from_bytes(msg_raw)

        headers = {header.lower():value for header,value in mime_message.items()}
        subject = headers.get('subject','No Subject')

        return subject
    
    except:
        print("An error occurred")
        return None

def move_email_to_spam(service,msg_id,folder,user_id='me'):
    labels_response = service.users().labels().list(userId=user_id).execute()
    labels = labels_response.get('labels',[])
    inbox_email_id = None
    spam_email_id = None

    for label in labels:
        if label['name'] == folder.upper():
            inbox_email_id = label['id']
        
        elif label['name'] == "SPAM":
            spam_email_id = label['id']
    
    if not inbox_email_id:
        print("An error occured")
    elif not spam_email_id:
        print("An error occured")
    
    body = {
        "removeLabelIds":[inbox_email_id],
        "addLabelIds":[spam_email_id]
    }

    try:
        message = service.users().messages().modify(userId='me',id=msg_id,body=body).execute()
        print("The inbox label was removed from the message")
    
    except:
        print("An error occured")

def read_subjects(service,folder):
    messages = list_messages(service,query='',target_label=folder)
    subjects = []
    if not messages:
        return "Your inbox is empty"
    
    else:
        for msg in messages[:5]:
            sub = get_subject(service,msg['id'])
            subjects.append(sub)
        return subjects

def get_senders_addy(service,msg_id):
    message = service.users().messages().get(userId='me',id=msg_id,format='full').execute()
    payload = message['payload']
    headers = payload['headers']
    sender_email = None
    sender_name = None
    for header in headers:
        if header['name'] == "From":

            sender_value = header['value']
            match  = re.match(r'^(.*?) <.*>$',sender_value)

            if match:
                sender_name = match.group(1).strip()
            
            else:
                sender_name = sender_value
            decoded_header = decode_header(sender_value)
            
            for value,charset in decoded_header:
                if isinstance(value,bytes):
                    value = value.decode(charset if charset else 'utf-8')
                
                if '<' in value and '>' in value:
                    start = value.find('<')
                    end = value.find('>')
                    sender_email = value[start:end]
                
                elif '@' in value:
                    sender_email = value
                
                if sender_email:
                    break
            
        if sender_email:
            break
    
    return sender_email,sender_name
        
