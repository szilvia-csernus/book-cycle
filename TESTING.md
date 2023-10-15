# TESTING - Community Transport project 


## Validation

### Python Validation

Validator: https://pep8ci.herokuapp.com/

| CI Python Linter Result | Passed |Warnings | 
| :--- | :---: | :--- | 
    

### JavaScript Validations

Validator: https://jshint.com/

| JSHint Result | Passed | Warnings |
| :--- | :---: | :--- | 

    

### HTML and CSS Validations

Validator: https://validator.w3.org/

> Please note that all the HTML validations' result looks the same, so I included only one screenshot under the `Home` Page.
> CSS Errors can be ignored as they are referring to new CSS properties (translate, scale, rotate) that are now widely supported.

| W3C Result | Passed |
| :--- | :---: | 
  

# Testing User Stories

Tests were carried out on Chrome 114.0.5735.133  
(macOS Catalina v10.15.7)

## Site Owner's Goals

| Passed | Site Owneer's Goals
| :--: | :-- |

## Shopper's Goals

| Passed | Site Owneer's Goals
| :--: | :-- |


## Staff member's Goals


| Passed | Member's Goals
| :--: | :-- |
|  |  **...be able to register and safely sign in.** |
| &check; | The user can sign up with either one of their Google accounts or with their email and a password. |


# Accessibility
  

* Images have `alt` labels. 
* Icons that have inferred meanings are marked with `aria` labels.
* Semantic HTML was used.
* All colours were tested for contrast in Chrome's Dev Tools.
* Chrome Dev Tools' Lighthouse score is 100% for accessibility for both mobile and desktop devices. (See below.)
* `WAVE` Accessibility checker was also used to check all the pages. 

 

# Automated Testing
 

To run the automated test cases, run:

`python manage.py test`

To check the 'Coverage' of all code tested, run:

`coverage run --source=inventory manage.py test`
`coverage report`

To view the report in the browser, run:

`coverage html`
`python -m http.server`

Follow the link and click on `htmlcov`


 # Manual Testing

Tests were carried out on Chrome 114.0.5735.133  
(macOS Catalina v10.15.7)

For detailed manual testing, please refer to this document:  

[Manual Test Cases](testing-images/manual-test-cases.pdf)

  

# Responsiveness Testing

Responsiveness was tested using [Google Dev Tools](https://developer.chrome.com/docs/devtools/)  
Browser & Version: Chrome 114.0.5735.133 (on Desktop, macOS Catalina version 10.15.7)
    

# Lighthouse tests

Performance, Accessibility, Best Practices and SEO tests were carried out with [Google Dev Tools](https://developer.chrome.com/docs/devtools/)' **Lighthouse** tool in `Incognito` mode.

| Page | Device  | Result | Note |
| :--: | :-----: | :----: | :--- |

---

# Resolved bugs - discovered during Testing

* On the `Edit Book` page, if the user checked the 'Remove image' box and at the same time selected a new image,
the form was not accepted as valid. To resolve this, I wrote a JS script which makes sure that only one of these
fields can be set.
* The image upload field on both `Add Book` and `Edit Book` pages allowed more file formats than django's ImageField
accepted as valid. If user attempted to upload an invalid image, it resulted in an invalid form error. To improve user experience, I restricted the file formats in the `custom_clerable_file_input.html` file, so the user can not accidentally
select invalid file formats.
* Automated testing revealed that uploading an image with no EXIF data would result in error. I corrected the inventory/signals.py file to handle such cases.

# Remaining Bugs


##

Chrome warning about Same-Site Cookies flags up Stripe's cookies:
https://support.stripe.com/questions/chrome-80-samesite-cookie-change?locale=en-GB

Stripe's Fraud Detection Scheme for which it is recommended to include its script in every page:
https://stripe.com/docs/disputes/prevention/advanced-fraud-detection