# Birthday Reminder Application
A birthday reminder application using drchrono api which shows all contacts with recent/nearby birthdays, and allows you to greet them with auto generated/custom message.

Available on:
https://birthdayreminder-app.herokuapp.com

### Setup

`social_auth_drchrono/` contains a custom provider for [Python Social Auth](http://psa.matiasaguirre.net/) that handles OAUTH for drchrono. You will also need to set up mail credentials. To configure these, set these fields in your `drchrono/secret_config.py` file:

```
SOCIAL_AUTH_DRCHRONO_KEY
SOCIAL_AUTH_DRCHRONO_SECRET
SOCIAL_AUTH_DRCHRONO_SCOPE
LOGIN_REDIRECT_URL
EMAIL_USE_TLS
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_PORT
DEFAULT_EMAIL_ADDRESS
```

### Instructions

Make sure that: 

1. current directory is api-example-django.
2. python path is set.
3. configuration data is set.

Run following commands to build and run application on localhost and test.
``` bash
$ make build
$ make run
$ make test
```

### Features and Considerations

1. Once you login using your drchrno credentials, the app fetches all your patient information, and extracts useful data: first name, last name, birthdate, address, contact number, email and photo. 
2. Missing birthdate is replaced with random date. Missing email is replaced with default email address. Other missing data is kept as "Missing"
3. Patients are filtered with respect to birthdate. Only those patients are considered whose birthday was in past week or is in following month. These patients are displayed as a list on homepage with birthday duration info: 'x days ago' or 'in y days'
4. Patient details are displayed when you select a patient from the list.
5. The 'Greet' option is provided in both the list and the details panel:
  * From patient list, you can greet with an auto generated message. The auto generated message is created considering when the birthday falls - today, past week or upcoming month.
  * From details panel, you can modify the auto generated message and send a custom message to greet.
6. Regardless of how you greet, once greeted, the option will be disabled on both list and panel to prevent repeated greeting. This 'greeted' history is not stored in database- you will be presented with a fresh list everytime you refresh or login. (Alternatively, I could keep track and prevent duplication over sessions.)

