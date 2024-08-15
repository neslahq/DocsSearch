from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from datetime import datetime
import os

SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                return creds
            except RefreshError:
                os.remove('token.json')
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_google_docs(start_date, end_date):
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    query = f"mimeType='application/vnd.google-apps.document' and modifiedTime >= '{start_date}' and modifiedTime <= '{end_date}'"
    results = service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
    items = results.get('files', [])
    
    docs = []
    for item in items:
        doc_service = build('docs', 'v1', credentials=creds)
        document = doc_service.documents().get(documentId=item['id']).execute()
        content = document.get('body').get('content')
        text = ''
        for elem in content:
            if 'paragraph' in elem:
                for run in elem['paragraph']['elements']:
                    if 'textRun' in run:
                        text += run['textRun']['content']
        
        docs.append({
            'id': item['id'],
            'name': item['name'],
            'link': item['webViewLink'],
            'content': text
        })
    
    return docs
