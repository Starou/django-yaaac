tests:
ifeq (${USER},vagrant)
	@PATH=${PATH}:/usr/lib/chromium/ DISPLAY=:99 PYTHONPATH=..:${PYTHONPATH} xvfb-run -n 99 python runtests.py
else
	@PYTHONPATH=..:${PYTHONPATH} python runtests.py
endif

coverage-report: coverage
	@coverage report -m

coverage-report-html: coverage
	@coverage html

coverage:
ifeq (${USER},vagrant)
	@PATH=${PATH}:/usr/lib/chromium/ DISPLAY=:99 PYTHONPATH=..:${PYTHONPATH} xvfb-run -n 99 coverage run --rcfile=coveragerc runtests.py
else
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py
endif
