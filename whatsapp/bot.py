from flask import Flask, jsonify, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
import botlhale_client

LANGUAGES = ["english", "zulu"]
current_lang = "en"


EN_BOT_ID = 'BBYBOPNZFRNGGRPP'
ZU_BOT_ID = 'ZYXPYXMAQRZZIRYR'
zu_bot_client = botlhale_client.BotlhaleClient(ZU_BOT_ID, "Zulu")
en_bot_client = botlhale_client.BotlhaleClient(EN_BOT_ID, "English")
active_bot = None
app = Flask(__name__)

def init_bot(bot):
    bot.startConversation()
    return bot

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World!"})

@app.route('/set_active_bot', methods=["POST"])
def set_active_bot():
    language = request.values.get('language')
    print(f"[INFO] Language set to {language}")
    active_bot = en_bot_client if language=="en" else zu_bot_client
    return "OK!"

@app.route('/bot-status', methods=['POST'])
def bot_status():
    incoming_msg = request.values.get('Body', '')
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    return str(resp)

@app.route('/bot-receiver', methods=['POST'])
def bot_receiver():
    bot = init_bot(en_bot_client)
    incoming_msg = request.values.get('Body', '')
    responded = False
    resp = MessagingResponse()
    msg = resp.message()
    if incoming_msg.lower() in LANGUAGES:
        update_katjie(incoming_msg[:2])
        outgoing_msg = "Please provide the medicine you need information for"
    else:
        bot_response = json.loads(bot.sendMessage(incoming_msg))
        print("Bot resonse:")
        print(bot_response)
        bot_msg = bot_response['TextResponse']
        outgoing_msg = bot_msg[0] if len(bot_msg) == 1 else bot_msg[1]
    outgoing_msg = outgoing_msg.replace(f'</div>','').replace(f'<div>','')
    outgoing_msg = translate(outgoing_msg)
    try:
        msg.body(outgoing_msg)
        responded = True
    except:
        msg.body('Sorry, Can\'t help with that!')
    return str(resp)

known_drugs = ["panado", "dispirin", "grandpa"]

@app.route('/bot-receiver-v2', methods=['POST'])
def bot_receiver_v2():
    bot = init_bot(en_bot_client)
    incoming_msg = request.values.get('Body', '')
    responded = False
    resp = MessagingResponse()
    msg = resp.message()
    global current_lang
    if incoming_msg.lower() in LANGUAGES:
        current_lang = incoming_msg[:2]
        update_katjie(current_lang)
        outgoing_msg = "Please provide the medicine you need information for"
    elif incoming_msg.lower() in known_drugs:
        outgoing_msg = f"What do you need to know about {incoming_msg}"
        set_drug(incoming_msg.lower())
    else:
        bot_response = json.loads(bot.sendMessage(incoming_msg))
        print("Bot resonse:")
        print(bot_response)
        bot_msg = bot_response['TextResponse']
        outgoing_msg = bot_msg[0] if len(bot_msg) == 1 else bot_msg[1]
    outgoing_msg = outgoing_msg.replace(f'</div>',' ').replace(f'<div>',' ')
    outgoing_msg = translate(outgoing_msg) if current_lang.lower() != "en" else outgoing_msg
    try:
        msg.body(outgoing_msg)
        responded = True
    except:
        msg.body('Sorry, Can\'t help with that!')
    return str(resp)

def update_katjie(language):
    proxy_url = "https://dololo.online/set_language"
    payload = {
        'language': language.lower()
    }
    headers={}
    response = requests.request("POST", proxy_url, headers=headers, data=payload)
    print(response)

def translate(message):
    proxy_url = "https://dololo.online/translate"
    payload = {
        'message': message
    }
    headers={}
    response = requests.request("POST", proxy_url, headers=headers, data=payload)
    return str(bytes.decode(response.content))

def set_drug(drug):
    proxy_url = "https://dololo.online/set_drug"
    payload = {
        'drug': drug
    }
    headers={}
    response = requests.request("POST", proxy_url, headers=headers, data=payload)
    return str(bytes.decode(response.content))


if __name__ == '__main__':
 app.run()
