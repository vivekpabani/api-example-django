import requests
import random
import datetime
from datetime import date

def get_patient_data(access_token):

    headers = {'Authorization': 'Bearer {0}'.format(access_token)}

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        response = requests.get(patients_url, headers=headers)
        json = requests.get(patients_url, headers=headers).json()
        results = json['results']

        for result in results:
            patient = dict([('last_name', result['last_name']),
                            ('first_name', result['first_name']),
                            ('contact', result['cell_phone']),
                            ('address', result['address']),
                            ('email', result['email']),
                            ('id', result['id']),
                            ('profile_pic', result['patient_photo'])])

            if result['date_of_birth']:
                date_of_birth = datetime.datetime.strptime(result['date_of_birth'], "%Y-%m-%d").date()
            else:
                rand_ordinal = random.randint(date.today().replace(day=1, month=1, year=1970).toordinal(),
                                              date.today().toordinal())
                date_of_birth = date.fromordinal(rand_ordinal)

            patient['date_of_birth'] = date_of_birth
            patient['date_of_birth_str'] = date_of_birth.strftime('%m/%d/%Y')

            if not result['email']:
                patient['email'] = DEFAULT_EMAIL_ADDRESS

            if not result['patient_photo']:
                patient['profile_pic'] = DEFAULT_PROFILE_PHOTO
            patients.append(patient)

        patients_url = json['next'] # A JSON null on the last page

    return patients
