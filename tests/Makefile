tests:
	@PYTHONPATH=..:${PYTHONPATH} python runtests.py --liveserver="127.0.0.1:8000"

coveralls:
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py --liveserver="127.0.0.1:8000"
	@coveralls -y coveralls.yaml -d .coverage

coverage-report: coverage
	@coverage report -m

coverage:
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py --liveserver="127.0.0.1:8000"
