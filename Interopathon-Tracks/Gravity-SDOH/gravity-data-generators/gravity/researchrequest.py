from flask import Blueprint, abort, jsonify, request
from datetime import datetime
import uuid, random, json

researchRequestGenerator = Blueprint('researchRequestGenerator', __name__)

@researchRequestGenerator.route('/researchRequest', methods=['GET'])
def get_research_request():
    response = generate_research_request_bundle()
    return jsonify(response)

def generate_research_request_bundle():
    communicationRequest = generate_communication_request()
    bundle = {
        'resourceType': 'Bundle',
        'type': 'transaction',
        'entry': [
            communicationRequest
        ]
    }
    return bundle;

def generate_communication_request():
    patient = select_screening_patient()
    return {
        "resource": {
            "resourceType": "CommunicationRequest",
            "status": "active",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http:\/\/hl7.org\/fhir\/us\/sdoh-cc\/CodeSystem\/sdohcc-temporary-codes",
                            "code": "sdohcc-hl7t-request-data",
                            "display": "Reqeust Data"
                        }
                    ],
                    "text": "Please return the requested data"
                }
            ],
            "subject": convert_patient_to_subject(patient),
            "reasonCode": [
                {
                    "coding": [
                        {
                            "system": "http:\/\/terminology.hl7.org\/CodeSystem\/v3-ActReason",
                            "code": "CAREMGT"
                        }
                    ]
                }
            ],
            "payload": [
                {
                    "extension": [
                        {
                            "url": "http:\/\/hl7.org\/fhir\/us\/davinci-cdex\/StructureDefinition\/cdex-payload-query-string",
                            "valueString": "QuestionnaireResponse"
                        }
                    ],
                    "contentString": "What are the Screening Responses for this patient?"
                }
            ],
            "text": {
                "status": "generated",
                "div": "CommunicationRequest: Please return the requested data"
            },
        },
        "request": {
            "method": "POST",
            "url": "CommunicationRequest"
        }
    }
    
def convert_patient_to_subject(patient):
    family_name = patient['resource']['name'][0]['family']
    given_name = patient['resource']['name'][0]['given'][0]
    birth_date = patient['resource']['birthDate']
    postal_code = patient['resource']['address'][0]['postalCode']
    return {
        'reference': 'Patient?given=' + given_name + '&family=' + family_name + '&birthdate=' + birth_date + '&address-postalcode=' + postal_code,
    }
    
def select_screening_patient():
    return select_sample_from_json_file('patients.json', 1)[0]

def select_sample_from_json_file(filename, sample_size):
    json_file = open(filename)
    all_candidates = json.load(json_file)
    selected_candidates = random.sample(all_candidates, sample_size)
    json_file.close()
    return selected_candidates
    
    
    
    