build:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test drchrono
