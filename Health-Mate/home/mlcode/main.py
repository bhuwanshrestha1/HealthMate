import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def predict_disease_and_specialist(symptom1, symptom2, symptom3, symptom4):
    # Importing the dataset
    test = pd.read_csv("home\mlcode\Testing.csv")
    train = pd.read_csv("home/mlcode/Training.csv")

        # Drop duplicates
    train = train.drop_duplicates()
    test = test.drop_duplicates()

        # Drop rows with missing values
    train = train.dropna()
    test = test.dropna()

    x_test = test.iloc[:, 0:-1].values
    y_test = test.iloc[:, -1].values
    x_train = train.iloc[:, 0:-1].values
    y_train = train.iloc[:, -1].values

    symptom_names = list(test.columns)[:-1]

    # Encode categorical data
    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_test = le.transform(y_test)

    # Seed the random number generator for reproducibility
    np.random.seed(42)

    # Train the model
    dtc = RandomForestClassifier(n_estimators=10)
    dtc.fit(x_train, y_train)

    # Prediction and accuracy test
    y_predict = dtc.predict(x_test)

    # Get user input for symptoms
    user_symptoms = [symptom.lower() for symptom in [symptom1, symptom2, symptom3, symptom4]]

    # Ensemble averaging for more stable predictions
    num_predictions = 100
    predictions = [dtc.predict(np.array([1 if symptom in user_symptoms else 0 for symptom in symptom_names]).reshape(1, -1))[0] for _ in range(num_predictions)]
    final_prediction = max(set(predictions), key=predictions.count)
    final_prediction_in_string = le.inverse_transform([final_prediction])[0]
    print("Final Predicted Disease:", final_prediction_in_string)

    # Categories of 15 specialties
    specialty_categories = {
    'Dermatology': ['Fungal infection', 'Acne', 'Psoriasis', 'Impetigo'],
    'Allergy/Immunology': ['Allergy'],
    'Gastroenterology': ['GERD', 'Peptic ulcer disease', 'Dimorphic hemmorhoids(piles)'],
    'Hepatology': ['Chronic cholestasis', 'Jaundice', 'Hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis'],
    'Infectious Disease': ['AIDS', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid'],
    'Endocrinology': ['Diabetes', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia'],
    'Pulmonology': ['Bronchial Asthma', 'Tuberculosis', 'Pneumonia'],
    'Cardiology': ['Hypertension', 'Heart attack'],
    'Neurology': ['Migraine', 'Paralysis (brain hemorrhage)', '(Vertigo) Paroxysmal Positional Vertigo'],
    'Orthopedics': ['Cervical spondylosis', 'Osteoarthristis', 'Arthritis'],
    'General Practice': ['Drug Reaction', 'Common Cold'],
    'Urology': ['Urinary tract infection'],
    'Vascular Surgery': ['Varicose veins'],
    'Rheumatology': ['Osteoarthritis', 'Arthritis'],
    'ENT Specialist': ['(Vertigo) Paroxysmal Positional Vertigo']
}

    # Map final predicted disease to doctor specialist
    category_of_final_prediction = None
    for category, diseases in specialty_categories.items():
        if final_prediction_in_string.strip().lower() in [disease.strip().lower() for disease in diseases]:
            category_of_final_prediction = category
            break



    # Define doctor specialists for each category
    doctor_specialists = {
        'Dermatology': 'Dermatologist',
        'Allergy/Immunology': 'Allergist',
        'Gastroenterology': 'Gastroenterologist',
        'Hepatology': 'Hepatologist',
        'Infectious Disease': 'Infectious Disease Specialist',
        'Endocrinology': 'Endocrinologist',
        'Pulmonology': 'Pulmonologist',
        'Cardiology': 'Cardiologist',
        'Neurology': 'Neurologist',
        'Orthopedics': 'Orthopedic Surgeon',
        'General Practice': 'General Practitioner',
        'Urology': 'Urologist',
        'Vascular Surgery': 'Vascular Surgeon',
        'Rheumatology': 'Rheumatologist',
        'ENT Specialist': 'ENT Specialist'
    }

    # Print final predicted category and associated doctor specialist
    if category_of_final_prediction:
        print(f'Final Predicted Category: {category_of_final_prediction}')
        print(f'Associated Doctor Specialist: {doctor_specialists.get(category_of_final_prediction, "Specialist not found")}')
    else:
        print('Category not found for the final prediction.')

    return final_prediction_in_string, doctor_specialists.get(category_of_final_prediction, 'Specialist not found')

# For testing the function
# symptom1 = input('Enter symptom 1: ')
# symptom2 = input('Enter symptom 2: ')
# symptom3 = input('Enter symptom 3: ')
# symptom4 = input('Enter symptom 4: ')
# predict_disease_and_specialist(symptom1, symptom2, symptom3, symptom4)
