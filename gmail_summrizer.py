import os
import base64
from openai import OpenAI
import email
from gtts import gTTS
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
from datetime import datetime, timezone
import logging
import requests

import base64
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


#  Gmail Scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# def get_unread_emails():
#     service = authenticate_gmail()
#     today = datetime.now(timezone.utc).date()
#     querya = f"after:{today.strftime('%Y/%m/%d')}"
#     #result = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=5).execute()
#     result = service.users().messages().list(userId='me', q=querya,maxResults=5).execute()
#     messages = result.get('messages', [])
#     email_texts = []

#     for msg in messages:
#         msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
#         payload = msg_data.get('payload', {})
#         parts = payload.get('parts', [])
#         body = ''
#         if 'data' in payload.get('body', {}):
#             body = payload['body']['data']
#         elif parts:
#             for part in parts:
#                 if part['mimeType'] == 'text/plain':
#                     body = part['body']['data']
#                     break
#         if body:
#             decoded_body = base64.urlsafe_b64decode(body).decode('utf-8')
#             email_texts.append(decoded_body.strip())
#     return email_texts




def get_unread_emails():
    service = authenticate_gmail()
    query = "is:unread newer_than:5d category:primary"
    result = service.users().messages().list(userId='me', q=query, maxResults=20).execute()
    messages = result.get('messages', [])
    logging.info(f"Gamil messages ----->  {len(messages)}")
    email_data = []

    def extract_text_plain(payload):
        if payload.get('mimeType') == 'text/plain' and 'data' in payload.get('body', {}):
            text = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore').strip()
            return clean_text(text)
        elif 'parts' in payload:
            for part in payload['parts']:
                text = extract_text_plain(part)
                if text:
                    return clean_text(text)
        return None

    def clean_text(text):
        text = re.sub(r'http\S+', '', text)                # Remove URLs
        text = re.sub(r'\n+', '\n', text).strip()          # Collapse newlines
        text = re.sub(r'\s{2,}', ' ', text)                # Remove extra spaces
        return text[:500] + '...' if len(text) > 500 else text

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        clean_body = extract_text_plain(payload)

        if clean_body:
            email_data.append({'subject': subject, 'message': clean_body})
        else:
            logging.warning(f"Skipped message ID {msg['id']} with subject '{subject}' — no plain text found")    

    logging.info(len(email_data))
    return email_data




# def summarize_emails(emails):
#     client = OpenAI(api_key=api_key)
#     if not emails:
#         return "No unread emails."
    
#     combined = "\n\n".join(emails)

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Summarize these emails in bullet points for a quick spoken summary."},
#             {"role": "user", "content": combined}
#         ]
#     )

#     return response.choices[0].message.content.strip()

def summarize_emails_ollama(emails):

    email_texts = [f"Subject: {e['subject']}\nMessage: {e['message']}" for e in emails]
    prompt1 = "Summarize these emails in bullet points:\n\n" + "\n".join(email_texts)
    prompt = (
    "Please summarize these email messages as clear, concise bullet points.\n"
    "Each bullet should reflect the main idea of each email:\n\n"
    + "\n\n".join(email_texts)
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()

        data = response.json()
        if 'response' in data:
            return data['response']
        else:
            logging.info("'response' key not found. Full JSON:")
            logging.info(data)
            return None

    except requests.exceptions.RequestException as e:
        logging.info(f"HTTP error: {e}")
        return None
    except ValueError:
        logging.info("Failed to parse JSON.")
        logging.info(" Raw text:", response.text)
        return None



def speak_text(texts):
      # If texts is a list, join into a single string
    if isinstance(texts, list):
        text = " ".join(texts)  # join with spaces (or "\n" if you want)
    else:
        text = texts
    cleaned_text = text.replace('\r\n', ' ').replace('\n', ' ').strip()

    max_len = 5000
    if len(cleaned_text) > max_len:
        cleaned_text = cleaned_text[:max_len] + "..."


    tts = gTTS(text=cleaned_text, lang='en')
    tts.save("static/summary.mp3")  # use 'afplay' for Mac, 'mpg123' for Linux

import platform
import subprocess

def play_audio(file_path="static/summary.mp3"):
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["afplay", file_path])
    elif system == "Linux":
        subprocess.run(["mpg123", file_path])
    elif system == "Windows":
        os.startfile(file_path)
    else:
        print("Cannot play audio automatically on this OS.")

def save_summary_text(summary_text):
    with open("static/last_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text.strip())

if __name__ == "__main__":
    emails = get_unread_emails()
    import json
    logging.info("Emails:\n%s", json.dumps(emails, indent=3))
    summary = summarize_emails_ollama(emails)
    logging.info(f"Summary:{summary}")
    speak_text(summary)
    play_audio()
