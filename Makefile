run:
	python manage.py runserver

new_db:
	dropdb projetodb --if-exists
	createdb projetodb
	python manage.py makemigrations
	python manage.py migrate

deps:
	pip install -r requirements.txt

shell:
	python manage.py shell

clean:
	find . -name '*.pyc' -delete

migrations:
	python manage.py makemigrations
	python manage.py migrate

create_user:
	python manage.py createsuperuser
