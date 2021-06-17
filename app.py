from flask import Flask, request, jsonify
from fda_client import get_field_for_drug
from translate_client import translate_text

app = Flask(__name__)

_translate_text = lambda text: translate_text("zu", text)

@app.route('/')
def fetch_field_for_drug_in_language():
    drug = request.args.get('drug')
    field = request.args.get('field')
    return {'response': _translate_text(
                          get_field_for_drug(drug, field))
            }
