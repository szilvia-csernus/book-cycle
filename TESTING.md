# Automated Testing

I wrote automated test cases before and alongside writing the code itself, so it
helped identifying bugs early during the development process. 

To run the automated test cases, run:

`python manage.py test`

To check the 'Coverage' of all code tested, run:

`coverage run --source=inventory manage.py test`
`coverage report`

To view the report in the browser, run:

`coverage html`
`python -m http.server`

Follow the link and click on `htmlcov`