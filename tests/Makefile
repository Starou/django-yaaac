tests:
	@PYTHONPATH=..:${PYTHONPATH} python runtests.py

coveralls:
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py
	@coveralls -y coveralls.yaml -d .coverage

coverage-report: coverage
	@coverage report -m

coverage:
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py
