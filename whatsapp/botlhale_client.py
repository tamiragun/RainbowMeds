import requests
import json
import os

generate_auth_token_url = "https://dev-botlhale.io/generateAuthToken"
connect_url = "https://dev-botlhale.io/startConversation"
send_message_url = "https://dev-botlhale.io/message"
session={}
message_type = 'text'
response_type = 'text'
refresh_token=os.environ['REFRESH_TOKEN']

class BotlhaleClient:
    generate_auth_token_url = "https://dev-botlhale.io/generateAuthToken"
    connect_url = "https://dev-botlhale.io/startConversation"
    send_message_url = "https://dev-botlhale.io/message"
    session={}
    message_type = 'text'
    response_type = 'text'

    def __init__(self, bot_id, language_code):
  # Chatbot Params
      self.bot_id = bot_id
      self.refresh_token = '<RefreshToken>'
      self.language_code = language_code


    def startConversation(self):
  # Generate IdToken for Bearer Auth on other endpoints.
      payload={
          'REFRESH_TOKEN': refresh_token,
      }
      IdToken = json.loads(requests.request("POST", generate_auth_token_url, data=payload).content)['AuthenticationResult']['IdToken']

      # Generate ConversationID.
      payload={
          'BotID': self.bot_id,
          'LanguageCode': self.language_code
      }
      headers = {"Authorization": "Bearer {}".format(IdToken)}
      ConversationID = json.loads(requests.request("POST", connect_url, headers=headers, data=payload).content)['ConversationID']

      # Store ConversationID & IdToken in the session for use in the sendMessage route.
      session['ConversationID'] = ConversationID
      session['IdToken'] = IdToken

      return {"ConversationID":ConversationID, "IdToken":IdToken}


    def sendMessage(self, message):
      # Get session variables
      ConversationID = session['ConversationID']
      IdToken = session['IdToken']

      # Get request parameters
      TextMsg = message

      # Send message to bot
      payload={
          'BotID': self.bot_id,
          'LanguageCode': self.language_code,
          'ConversationID': ConversationID,
          'MessageType': message_type,
          'ResponseType': response_type,
          'TextMsg': TextMsg
      }
      headers = {"Authorization": "Bearer {}".format(IdToken)}
      response = requests.request("POST", send_message_url, headers=headers, data=payload).text
      return response
