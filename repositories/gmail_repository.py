from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
import base64
from googleapiclient.errors import HttpError
from email import message_from_bytes

#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

class ConexaoError(Exception):
  pass



class AutenticacaoGmail:

  @staticmethod
  def obter_credenciais():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = None

    try:
      if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)

      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
          with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    except:
      raise ConexaoError("Não foi possivel obter as credenciais, verifique se seu credentials.json existe")
    return creds
  
  def autenticacao(self): 
    creds = self.obter_credenciais()
    service = build('gmail', 'v1', credentials=creds)

    return service
      
class GmailInfra:
  def __init__(self):
    repo_autenticacao = AutenticacaoGmail()
    self.service = repo_autenticacao.autenticacao()

  def listar_gmails_ids(self) -> list:
    try:
      response = self.service.users().messages().list(userId = 'me',q="-in:trash",labelIds=['INBOX'],maxResults = 10).execute()
    except HttpError as e:
      raise ConexaoError("Não foi possivel conectar com a api do Gmail") from e
    messages = response.get('messages')
    list_ids = []
    for message in messages:
      list_ids.append(message.get('id'))

    return list_ids   

  def pegar_corpo_gmail(self,gmail_id) -> str:
    try:
      response = self.service.users().messages().get(userId = 'me',id = gmail_id,format = 'raw').execute()
    except HttpError as e:
      raise ConexaoError("Não foi possivel conectar com a api do Gmail") from e
    raw = response['raw']
    msg = message_from_bytes(base64.urlsafe_b64decode(raw))

    html = None

    for parte in msg.walk():
      tipo = parte.get_content_type()

      if tipo == "text/plain":
        return parte.get_payload(decode=True).decode("utf-8", errors="ignore")

      elif tipo == "text/html":
        html = parte.get_payload(decode=True).decode("utf-8", errors="ignore")

    return html 
  
  def alterar_label(self,id_mensagem,label_id) -> list:
    try:
      response = self.service.users().messages().modify(
        userId = 'me',
        id = id_mensagem,
        body={
          "addLabelIds": [label_id]
        }
      ).execute()
    except HttpError as e:
      raise ConexaoError("Não foi possivel conectar com a api do Gmail") from e

    return response

  def listar_labels(self) -> list:
    try:
      response = self.service.users().labels().list(userId='me').execute()
    except HttpError as e:
      raise ConexaoError("Não foi possivel conectar com a api do Gmail") from e
    labels = response.get('labels')
    name_labels = {}
    for label in labels:
      nome_label = label['name']
      id_label = label['id']
      name_labels[nome_label] = id_label
        
    return name_labels


