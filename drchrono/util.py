import requests
import random
import datetime
from datetime import date
from django.core.mail import EmailMessage, BadHeaderError
from drchrono.settings import DEFAULT_EMAIL_ADDRESS, DEFAULT_PROFILE_PHOTO

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

def get_patients_with_recent_birthday(patient_list):

    patients_with_daydiff = list()

    for patient in patient_list:
        diff = day_difference(patient['date_of_birth'], date.today())
        if diff > -7 and diff < 30:
            patients_with_daydiff.append([patient, diff])

    sorted_patients_with_daydiff = sorted(patients_with_daydiff, key=lambda x: x[1])

    return sorted_patients_with_daydiff

def day_difference(from_date, to_date):

    from_day = date(day=from_date.day, month=from_date.month, year=2000)
    to_day = date(day=to_date.day, month=to_date.month, year=2000)

    delta = from_day - to_day

    return delta.days

def send_email_util(mail_id, message):

    subject = "Happy Birthday!"
    message = message.replace('\\n', '\r\n')
    email = EmailMessage(subject, message, to=[mail_id])

    try:
        email.send()
    except BadHeaderError:
        return False

    return True
