from flask import Blueprint, abort, jsonify, request
from datetime import datetime
import uuid, random
from jinja2.compiler import generate

autoresponder = Blueprint('autoresponder', __name__)

@autoresponder.route('/response', methods=['POST'])
def respond_to_questionnaire():
    if not request.json or not 'title' in request.json:
        abort(400)
    response = generate_response_bundle()
    return jsonify(response)

def generate_response_bundle():
    response = generate_response_object()
    bundle = {
        'resourceType': 'Bundle',
        'type': 'message',
        'entry': [
            response
        ]
    }
    if (random.choice([True, False])):
        bundle['entry'].append(generate_consent(response))
    return bundle;

def generate_response_object():
    current_time = datetime.now()
    response_id = uuid.uuid4()
    author_id = uuid.uuid4()
    response = {
        'fullUrl': 'uun:uuid:' + str(response_id),
        'request': {
            'method': 'POST',
            'url': 'MessageHeader'
        },
        'resource': {
            'resourceType': 'QuestionnaireResponse',
            'id': str(response_id),
            'meta': {
                'versionId': '1',
                'lastUpdated': current_time.isoformat(),
                'profile': ['https://www.hl7.org/fhir/questionnaireresponse.html']
            },
            'questionnaire': request.json['id'],
            'status': 'completed',
            'authored': current_time.isoformat(),
            'author': {
                'reference': 'uun:uuid:' + str(author_id)
            },
            'item': generate_questionnaire_answers()
            
        }
    }
    return response;

def generate_questionnaire_answers():
    answers = []
    for question in request.json['item']:
        selected_option = random.choice(question['item'])
        answer = {
            'linkId': question['linkId'],
            'text': question['text'],
            'answer': {
                'valueCoding': selected_option['code']
            }
        }
        answers.append(answer)
    return answers
    
def generate_consent(response):
    consent_id = uuid.uuid4()
    current_time = datetime.now()
    return {
        'fullUrl': 'uun:uuid:' + str(consent_id),
        'resource': {
            'resourceType': 'Consent',
            'id': str(consent_id),
            'meta': {
                'versionId': '1',
                'lastUpdated': current_time.isoformat(),
                'profile': ['https://www.hl7.org/fhir/consent.html']
            },
            'status': 'active',
            'scope': {
                'coding': [
                    {
                        'system': 'http://terminology.hl7.org/CodeSystem/consentscope',
                        'code': 'patient-privacy',
                        'display': 'Privacy Consent'
                    }
                ]
            },
            'category': [
                {
                    'coding': [
                        {
                            'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode',
                            'code': 'ICOL',
                            'display': 'information collection'
                        }
                    ]
                }
            ],
            'dateTime': str(current_time),
            'sourceReference': {
                'reference': response['fullUrl']
            }    
        },
        'request': {
            'method': 'POST',
            'url': 'Consent'
        }
    }
