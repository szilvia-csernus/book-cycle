# Automated Testing

I followed the Test Driven Development (TDD) Principle, writing test cases before and alongside the code itself. To run the automated test cases, run:

`python manage.py test`

To check the 'Coverage' of all code tested, run:

`coverage run --source=inventory manage.py test`
`coverage report`

To view the report in the browser, run:

`coverage html`
`python -m http.server`

Follow the link and click on `htmlcov`