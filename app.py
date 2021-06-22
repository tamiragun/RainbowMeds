from flask import Flask, request, jsonify
from fda_client import get_field_for_drug
from translate_client import translate_text
import requests

app = Flask(__name__)

language='en'
_translate_text = lambda text: translate_text("zu", text)
HACKY=True
posted_drug = None

@app.route('/translate', methods=["GET", "POST"])
def translate():
    print(request.values)
    output = request.values.get('message')
    return _translate_text(output)

@app.route('/set_drug', methods=["GET", "POST"])
def set_drug():
    print(request.values)
    drug = request.values.get('drug')
    print(f"[INFO] drug: {drug}")
    global posted_drug
    posted_drug = drug
    output = f"What would you like to know about {drug}?"
    return output if language=='en' else _translate_text(output)

@app.route('/set_field', methods=["GET", "POST"])
def set_field():
    print(request.values)
    field = request.values.get('field') or request.values.get('description')
    og_field = field
    field = field.lower().strip().replace(" ", "_").replace("-", "_")
    if "dosage" in field or "isilinganiso" in field:
        field = "dosage_and_administration"
    if field == "side_effects":
        field = "adverse_reactions"
    if "side" in field and "effect" in field:
        field = "adverse_reactions"
    if "desc" in field:
        field = "adverse_reactions"
    print(f"[INFO] field: {field}")
    if not posted_drug:
        output = f"You need to provide a drug name first. Please tell me which drug you'd like to get the {field} for?"
    else:
        output = get_field_for_drug(drug, field)
    return output if language=='en' else _translate_text(output)

@app.route('/get_info', methods=["GET", "POST"])
def fetch_field_for_drug_in_language():
    #drug = request.args.get('drug')
    print(request.values)
    drug = request.values.get('drug')
    print(f"[INFO] drug: {drug}")
    drug = posted_drug or 'paracetamol'
    print(request.values)
    field = request.values.get('field') or request.values.get('description')
    field = field.lower().strip().replace(" ", "_").replace("-", "_")
    if "dosage" in field:
        field = "dosage_and_administration"
    if field == "side_effects":
        field = "adverse_reactions"
    if "side" in field and "effect" in field:
        field = "adverse_reactions"
    if "desc" in field:
        field = "adverse_reactions"
    print(f"[INFO] field: {field}")
    if not posted_drug:
        output = f"You need to provide a drug name first. Please tell me which drug you'd like to get the {field} for?"
    else:
        output = get_field_for_drug(drug, field)
    return output if language=='en' else _translate_text(output)
    print(f"[INFO] field: {field}")
    output = get_field_for_drug(drug, field)
    return output if language=='en' else _translate_text(output)

@app.route('/set_language', methods=["POST"])
def set_language():
    if HACKY:
        print(request.values)
        drug = request.values.get('drug')
        field = request.values.get('field') or request.values.get('description')
        if drug and field:
            print(f"[INFO] drug: {drug}")
            drug = 'paracetamol'
            field = request.values.get('field') or request.values.get('description')
            if field == "dosage":
                field = "dosage_and_administration"
            print(f"[INFO] field: {field}")
            output = get_field_for_drug(drug, field)
            return output if language=='en' else _translate_text(output)
    language_val = request.values.get('set_language') or request.values.get('language')
    language_val = language_val.lower()
    language = 'en' if 'en' in language_val else 'zu'
    language = 'zu' if 'zu' in language_val else 'en'
    print(f"[INFO] Setting language to {language}")
    update_whatsapp_proxy_language(language)

    output = "What medicine would you like to enquire about?"
    return output if language=='en' else _translate_text(output)

def update_whatsapp_proxy_language(language):
    proxy_url = "https://installing-data-tigers-direction.trycloudflare.com/set_active_bot"
    payload = {
        'language': language.lower()
    }
    headers={}
    response = requests.request("POST", proxy_url, headers=headers, data=payload)
    if response.content != "OK!":
        print(response)
        # raise Exception("Could not change whatsapp language")
