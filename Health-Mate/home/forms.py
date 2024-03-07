# forms.py
from django import forms





    
class SymptomForm(forms.Form):
    ALL_SYMPTOMS = [
        'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
        'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
        'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings',
        'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever',
        'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin',
        'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
        'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
        'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
        'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
        'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
        'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
        'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremities',
        'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
        'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness',
        'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell',
        'bladder_discomfort', 'foul_smell_of_urine', 'continuous_feel_of_urine', 'passage_of_gases',
        'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
        'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes',
        'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
        'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
        'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum',
        'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurrying',
        'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
        'red_sore_around_nose', 'yellow_crust_ooze',
    ]

  
    SYMPTOM_CHOICES_INITIAL = [('None', 'None')] + [
        (symptom, symptom.replace('_', ' ').title()) for symptom in ALL_SYMPTOMS
    ]

    symptom1 = forms.ChoiceField(choices=SYMPTOM_CHOICES_INITIAL, label='Symptom 1')
    symptom2 = forms.ChoiceField(choices=SYMPTOM_CHOICES_INITIAL, label='Symptom 2')
    symptom3 = forms.ChoiceField(choices=SYMPTOM_CHOICES_INITIAL, label='Symptom 3')
    symptom4 = forms.ChoiceField(choices=SYMPTOM_CHOICES_INITIAL, label='Symptom 4')

def __init__(self, *args, **kwargs):
    super(SymptomForm, self).__init__(*args, **kwargs)

    # Initialize choices for Symptom 2
    self.fields['symptom2'].choices = self.get_filtered_choices('symptom1')

    # Initialize choices for Symptom 3
    self.fields['symptom3'].choices = self.get_filtered_choices('symptom2')

    # Initialize choices for Symptom 4
    self.fields['symptom4'].choices = self.get_filtered_choices('symptom3')

def get_filtered_choices(self, previous_symptom):
    cleaned_data = getattr(self, 'cleaned_data', None)
    selected_symptoms = [cleaned_data.get(field) for field in ['symptom1', 'symptom2', 'symptom3', 'symptom4'] if cleaned_data and cleaned_data.get(field)]

    return [('None', 'None')] + [
        (symptom, symptom.replace('_', ' ').title())
        for symptom in self.ALL_SYMPTOMS
        if symptom not in selected_symptoms and (cleaned_data and cleaned_data.get(previous_symptom) != symptom)
    ]

def clean(self):
        cleaned_data = super(SymptomForm, self).clean()
        selected_symptoms = [cleaned_data.get(field) for field in ['symptom1', 'symptom2', 'symptom3', 'symptom4'] if cleaned_data.get(field) and cleaned_data.get(field) != 'None']

        if len(selected_symptoms) < 2:
            raise forms.ValidationError("Please provide at least two symptoms.")

        return cleaned_data


