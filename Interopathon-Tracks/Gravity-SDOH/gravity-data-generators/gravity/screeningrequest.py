from flask import Blueprint, abort, jsonify, request
from datetime import datetime
import uuid, random, json

patientListGenerator = Blueprint('screeningRequestGenerator', __name__)

@patientListGenerator.route('/screeningRequest', methods=['GET'])
def get_screening_request():
    response = generate_screening_request_bundle()
    return jsonify(response)

def generate_screening_request_bundle():
    patientList = generate_screening_patient_list('working title')
    questionnaire = select_screening_questionnaire()
    bundle = {
        'resourceType': 'Bundle',
        'type': 'message',
        'entry': [
            patientList,
            questionnaire
        ]
    }
    return bundle;

def generate_screening_patient_list(list_title):
    list_id = 'id-list-' + str(uuid.uuid4())
    selected_patients = select_sample_from_json_file('patients.json', 3)
    return {
        'id': list_id,
        'fullUrl': 'urn:uuid:id-list-' + str(list_id),
        'resourceType': 'List',
        'status': 'current',
        'title': list_title,
        'entry': convert_patient_list_to_fhir_items(selected_patients)
    }
    
def convert_patient_list_to_fhir_items(patients):
    entries = []
    for patient in patients:
        entries.append(convert_patient_to_fhir_item(patient))
    return entries
    
def convert_patient_to_fhir_item(patient):
    family_name = patient['resource']['name'][0]['family']
    given_name = patient['resource']['name'][0]['given'][0]
    birth_date = patient['resource']['birthDate']
    postal_code = patient['resource']['address'][0]['postalCode']
    return {
        'item': {
            'reference': 'Patient?given=' + given_name + '&family=' + family_name + '&birthdate=' + birth_date + '&address-postalcode=' + postal_code,
            'type': 'Patient',
            'display': family_name + ', ' + given_name
        }
    }
    
def select_screening_questionnaire():
    return select_sample_from_json_file('questionnaires.json', 1)[0]

def select_sample_from_json_file(filename, sample_size):
    json_file = open(filename)
    all_candidates = json.load(json_file)
    selected_candidates = random.sample(all_candidates, sample_size)
    json_file.close()
    return selected_candidates
    
    
    
    