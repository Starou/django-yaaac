tests:
	@python runtests.py

runserver:
	@cd django_test_project ; PYTHONPATH=../..:${PYTHONPATH} python manage.py runserver;

coveralls:
	@coverage run --rcfile=coveragerc runtests.py
	@coveralls -y coveralls.yaml -d .coverage

coverage:
	@coverage run --rcfile=coveragerc runtests.py
	@coverage report -m
