import json
import random

# These value are taken for the LLM 
names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Lee", "Emma Brown"]
genders = ["Male", "Female", "Other"]
conditions = ["Lung Cancer", "Heart Disease", "Diabetes", "Hypertension"]
treatment_plans = ["Chemotherapy", "Surgery", "Radiation", "Medication"]
medications = ["Aspirin", "Metformin", "Ibuprofen", "Cisplatin", "Paclitaxel"]
follow_up_care_options = ["Regular monitoring", "Post-surgery follow-up", "Medication adjustment"]
smoking_history_options = ["Yes", "No"]
persistent_cough_options = ["Yes", "No"]


def generator(options):
    return random.choice(options)

def collect_patient_data(name):
    patient_data = {
        "patient": {
            "name": name,
            "age": random.randint(20, 90), 
            "gender": generator(genders),
            "condition": generator(conditions)
        },
        "demographics reports": {
            "smoking_history": generator(smoking_history_options),
            "weight_loss": f"{random.randint(0, 30)} kg",  
            "persistent_cough":generator(persistent_cough_options)
        },
        "procedures plan": {
            "xray": f"Mass found in {random.choice(['left', 'right'])} lung",
            "ct_scan": random.choice(["Tumor detected", "No significant findings"]),
            "biopsy": random.choice(["Benign", "Malignant"])
        },
        "care_plan": {
            "treatment_plan": generator(treatment_plans),
            "medications": generator(medications),
            "follow_up_care": generator(follow_up_care_options)
        },
        "appointments scheduling ": []
    }
    
    add_random_appointments(patient_data)
    return patient_data

def add_random_appointments(patient_data):
    for _ in range(random.randint(1, 3)): 
        appointment_details = {
            "date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "purpose": random.choice(["Post-chemo checkup", "Routine follow-up", "Scan"])
        }
        patient_data["appointments"].append(appointment_details)

def main():
    for name in names: 
        patient_data = collect_patient_data(name)
        json_data = json.dumps(patient_data, indent=4)
        print(f"Patient Data for {name}:\n{json_data}\n" + "-"*80)

main()
