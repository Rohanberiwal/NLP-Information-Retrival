from fhirpy import SyncFHIRClient
import json
import random

patients = [
    {
        'name': "Rahul Sharma",
        'gender': "male",
        'birthDate': "1980-01-01",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 75,
        'observation_unit': "kg",
        'care_plan_code': "12345-6",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Priya Verma",
        'gender': "female",
        'birthDate': "1985-05-15",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
                'observation_value': 68,
        'observation_unit': "kg",
        'care_plan_code': "12346-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Anil Gupta",
        'gender': "male",
        'birthDate': "1975-08-22",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 80,
        'observation_unit': "kg",
        'care_plan_code': "12347-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Sneha Iyer",
        'gender': "female",
        'birthDate': "1990-02-20",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 55,
        'observation_unit': "kg",
        'care_plan_code': "12348-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Vikram Singh",
        'gender': "male",
        'birthDate': "1988-11-11",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 90,
        'observation_unit': "kg",
        'care_plan_code': "12349-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Deepika Rao",
        'gender': "female",
        'birthDate': "1979-06-30",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 50,
        'observation_unit': "kg",
        'care_plan_code': "12350-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Amit Patel",
        'gender': "male",
        'birthDate': "1983-03-05",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 70,
        'observation_unit': "kg",
        'care_plan_code': "12351-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Neha Kumari",
        'gender': "female",
        'birthDate': "1992-12-20",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 62,
        'observation_unit': "kg",
        'care_plan_code': "12352-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Suresh Nair",
        'gender': "male",
        'birthDate': "1985-07-15",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 85,
        'observation_unit': "kg",
        'care_plan_code': "12353-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Anjali Mehta",
        'gender': "female",
        'birthDate': "1994-03-10",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 58,
        'observation_unit': "kg",
        'care_plan_code': "12354-7",
        'care_plan_display': "Oncology Care Plan"
    },
    {
        'name': "Raghu the great",
        'gender': "male",
        'birthDate': "1983-03-05",
        'observation_code': "29463-7",
        'observation_display': "Body weight",
        'observation_value': 70,
        'observation_unit': "kg",
        'care_plan_code': "12351-7",
        'care_plan_display': "Oncology Care Plan"
    }
]



client = SyncFHIRClient('http://hapi.fhir.org/baseR4')
registered_patient_list = []
observation_list = []
care_plan_list = []
diagnostic_list = []
progress_notes_list = []

def search_patient_by_name(name, surname):
    try:
        results = client.resources('Patient').search(given=name, family=surname).fetch()
        if results:
            print(f"Patient '{name} {surname}' found with ID: {results[0]['id']}")
            return results[0]['id']  
        else:
            print(f"Patient '{name} {surname}' not found.")
            return None
    except Exception as e:
        print(f"Error during patient search: {e}")
        return None

def make_patient(patient_data):
    surname = patient_data['name'].split()[1]  
    name = patient_data['name'].split()[0] 
    patient_id = search_patient_by_name(name, surname)
    if patient_id:
        return patient_id 
    else :
      print("Registering the patient as he is not yet regsitted")
      new_patient = client.resource(
          'Patient',
          name=[{'family': surname, 'given': [name]}],
          gender=patient_data['gender'],
          birthDate=patient_data['birthDate']
      )
      new_patient.create()
      registered_patient_list.append(new_patient.id)
      print(f"Patient with ID {new_patient.id} registered")
    return new_patient.id

def create_observation(patient_id, patient_data):
    observation_data = {
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": patient_data['observation_code'],
                "display": patient_data['observation_display']
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "valueQuantity": {
            "value": patient_data['observation_value'],
            "unit": patient_data['observation_unit']
        }
    }
    observation = client.resource('Observation', **observation_data)
    observation.create()
    observation_list.append(observation.id)
    print(f"Observation with ID {observation.id} registered")
    return observation.id

def care_plan_function(patient_id, patient_data):
    care_plan_data = {
        "resourceType": "CarePlan",
        "status": "active",
        "intent": "plan",
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "activity": [{
            "detail": {
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": patient_data['care_plan_code'],
                        "display": patient_data['care_plan_display']
                    }]
                },
                "status": "in-progress"
            }
        }]
    }
    care_plan = client.resource('CarePlan', **care_plan_data)
    care_plan.create()
    care_plan_list.append(care_plan.id)
    return care_plan.id



def register_diagnostic_test(patient_id, patient_data):
    test_result = random.choice(["positive", "negative", "inconclusive"])

    diagnostic_data = {
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "33747-8",
                "display": "Lung Cancer Diagnostic Test"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "valueString": test_result
    }
    diagnostic_test = client.resource('Observation', **diagnostic_data)
    diagnostic_test.create()
    diagnostic_list.append(diagnostic_test.id)
    print("Daignosis test  ",diagnostic_test.id," registered")
    return diagnostic_test.id, test_result

def register_imaging_tests(patient_id):
    chest_xray_result = random.choice(["normal", "abnormal"])
    ct_scan_result = random.choice(["normal", "suspicious", "malignant"])
    chest_xray_data = {
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "30746-0",
                "display": "Chest X-ray"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "valueString": chest_xray_result
    }
    chest_xray = client.resource('Observation', **chest_xray_data)
    chest_xray.create()
    ct_scan_data = {
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "24606-6",
                "display": "CT Scan"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "valueString": ct_scan_result
    }
    ct_scan = client.resource('Observation', **ct_scan_data)
    ct_scan.create()

    return chest_xray.id, chest_xray_result, ct_scan.id, ct_scan_result


def register_progress_notes(patient_id):
    notes = [
        "Patient responding well to treatment.",
        "Patient experienced mild side effects from medication.",
        "Patient showing no signs of disease progression.",
        "Patient requires further tests to assess condition."
    ]
    selected_note = random.choice(notes)

    progress_note_data = {
        "status": "completed",
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "371531000",
                "display": "Progress note"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "performedString": selected_note
    }
    progress_note = client.resource('Procedure', **progress_note_data)
    progress_note.create()
    progress_notes_list.append(progress_note.id)
    print("Progress notes ",progress_note.id," regsitered ")
    return progress_note.id, selected_note


def register_patient(patient_data, combined_data):
    try:
        patient_id = make_patient(patient_data)
        observation_id = create_observation(patient_id, patient_data)
        care_plan_id = care_plan_function(patient_id, patient_data)
        diagnostic_id, test_result = register_diagnostic_test(patient_id, patient_data)

        chest_xray_id, chest_xray_result, ct_scan_id, ct_scan_result = register_imaging_tests(patient_id)
        progress_note_id, progress_note = register_progress_notes(patient_id)

        combined_entry = {
            "patient": {
                "id": patient_id,
                "name": patient_data['name'],
                "gender": patient_data['gender'],
                "birthDate": patient_data['birthDate']
            },
            "observation": {
                "id": observation_id,
                "code": patient_data['observation_code'],
                "display": patient_data['observation_display'],
                "value": patient_data['observation_value'],
                "unit": patient_data['observation_unit']
            },
            "carePlan": {
                "id": care_plan_id,
                "code": patient_data['care_plan_code'],
                "display": patient_data['care_plan_display']
            },
            "diagnosticTest": {
                "id": diagnostic_id,
                "code": "33747-8",
                "display": "Lung Cancer Diagnostic Test",
                "result": test_result
            },
            "imagingTests": {
                "chestXray": {
                    "id": chest_xray_id,
                    "result": chest_xray_result
                },
                "ctScan": {
                    "id": ct_scan_id,
                    "result": ct_scan_result
                }
            },
            "progressNotes": {
                "id": progress_note_id,
                "note": progress_note
            }
        }
        combined_data.append(combined_entry)

    except Exception as e:
        print(f"Error processing patient {patient_data['name']}: {e}")

def main():
    combined_patient_data = []
    for patient_data in patients:
        register_patient(patient_data, combined_patient_data)

    with open('combined_patient_data.json', 'w') as f:
        json.dump(combined_patient_data, f, indent=2)

    print("\nCombined Patient Data:")
    print(json.dumps(combined_patient_data, indent=2))

main()
