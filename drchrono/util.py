import requests
import random
import datetime
from datetime import date
from django.core.mail import EmailMessage, BadHeaderError
from django.contrib.staticfiles.templatetags.staticfiles import static
from drchrono.settings import DEFAULT_EMAIL_ADDRESS

def get_patient_data(access_token):
    """
    Fetch all patient data from server.

    :param access_token (str): access token to be used to fetch data

    :return list: list of patient objects with name, birthdate and other details 
    """

    headers = {'Authorization': 'Bearer {0}'.format(access_token)}

    patients = []
    patients_url = 'https://drchrono.com/api/patients'

    # since patient url works like iterator where next patient data is accessed with next
    # try fetching till a null record is faced. 
    while patients_url:
        response = requests.get(patients_url, headers=headers)
        json = requests.get(patients_url, headers=headers).json()
        results = json['results']

        # extract useful data from json. 
        # replace with default if null value. 
        for result in results:
            patient = dict([('last_name', result['last_name']),
                            ('first_name', result['first_name']),
                            ('contact', result['cell_phone']),
                            ('address', result['address']),
                            ('email', result['email']),
                            ('id', result['id']),
                            ('profile_pic', result['patient_photo'])])

            # assign random birthdate if not available.  
            if result['date_of_birth']:
                date_of_birth = datetime.datetime.strptime(result['date_of_birth'], "%Y-%m-%d").date()
            else:
                rand_ordinal = random.randint(date.today().replace(day=1, month=1, year=1970).toordinal(),
                                              date.today().toordinal())
                date_of_birth = date.fromordinal(rand_ordinal)

            patient['date_of_birth'] = date_of_birth
            patient['date_of_birth_str'] = date_of_birth.strftime('%m/%d/%Y')

            # assign default email address if not available.
            if not result['email']:
                patient['email'] = DEFAULT_EMAIL_ADDRESS

            # assign default profile pic if not available.
            if not result['patient_photo']:
                patient['profile_pic'] = static('img/default-profile.png')
            patients.append(patient)

        patients_url = json['next'] # A JSON null on the last page

    return patients

def get_patients_with_recent_birthday(patient_list):
    """
    Filter patient data to get only recent birthdays  

    :param patient_list (list): list of patient objects

    :return (list): list of patients whose birthday is close with remaining days.
    """

    patients_with_daydiff = list()

    for patient in patient_list:
        diff = day_difference(patient['date_of_birth'], date.today())
        if diff > -7 and diff < 30:
            patients_with_daydiff.append([patient, diff])

    sorted_patients_with_daydiff = sorted(patients_with_daydiff, key=lambda x: x[1])

    return sorted_patients_with_daydiff

def day_difference(from_date, to_date):
    """
    Find difference between two dates with regards to day, ignoring year

    :param from_date (date): from date
    :param to_date (date): to date

    :return (int): difference between two dates
    """

    from_day = date(day=from_date.day, month=from_date.month, year=2000)
    to_day = date(day=to_date.day, month=to_date.month, year=2000)

    delta = from_day - to_day

    return delta.days

def send_email_util(mail_id, message):
    """
    send email using given mail id and message 

    :param mail_id (str): receipient's mail id
    :param message (str): message to be sent

    :return (bool): Success or failure message
    """

    subject = "Happy Birthday!"
    message = message.replace('\\n', '\r\n')
    email = EmailMessage(subject, message, to=[mail_id])

    try:
        email.send()
    except BadHeaderError:
        return False

    return True
