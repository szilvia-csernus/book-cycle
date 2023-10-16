o# TESTING - Book-Cycle project 


## Validation

### Python Validation

In VSCode, I used the `autopep8` and `Flake8` extensions to help keep my code free of linting issues.

The validation of the final versions of my files were carried out with CI's Python validator: https://pep8ci.herokuapp.com/

| CI Python Linter Result | Passed |
| :--- | :---: |
| [book_cycle/settings.py file CI Linter Result](testing_files/book_cycle-settings-py.jpeg) | &check; |
| [book_cycle/urls.py file CI Linter Result](testing_files/book_cycle-urls-py.jpeg) | &check; |  
| [book_cycle/wsgi.py file CI Linter Result](testing_files/book_cycle-wsgi-py.jpeg) | &check; |
| [home/urls.py file CI Linter Result](testing_files/home-urls-py.jpeg) | &check; |
| [home/views.py file CI Linter Result](testing_files/home-views-py.jpeg) | &check; |  
| [inventory/admin.py file CI Linter Result](testing_files/inventory-admin-py.jpeg) | &check; |
| [inventory/context.py file CI Linter Result](testing_files/inventory-context-py.jpeg) | &check; |  
| [inventory/forms.py file CI Linter Result](testing_files/inventory-forms-py.jpeg) | &check; |
| [inventory/models.py file CI Linter Result](testing_files/inventory-models-py.jpeg) | &check; |  
| [inventory/signals.py file CI Linter Result](testing_files/inventory-signals-py.jpeg) | &check; |
| [inventory/urls.py file CI Linter Result](testing_files/inventory-urls-py.jpeg) | &check; |  
| [inventory/views.py file CI Linter Result](testing_files/inventory-views-py.jpeg) | &check; |
| [inventory/widgets.py file CI Linter Result](testing_files/inventory-widgets-py.jpeg) | &check; |
| [orders/admin.py file CI Linter Result](testing_files/orders-admin-py.jpeg) | &check; |
| [orders/context.py file CI Linter Result](testing_files/orders-context-py.jpeg) | &check; |  
| [orders/forms.py file CI Linter Result](testing_files/orders-forms-py.jpeg) | &check; |
| [orders/models.py file CI Linter Result](testing_files/orders-models-py.jpeg) | &check; |  
| [orders/signals.py file CI Linter Result](testing_files/orders-signals-py.jpeg) | &check; |
| [orders/urls.py file CI Linter Result](testing_files/orders-urls-py.jpeg) | &check; |  
| [orders/views.py file CI Linter Result](testing_files/orders-views-py.jpeg) | &check; |
| [orders/webhook-handler.py file CI Linter Result](testing_files/orders-webhook-handler-py.jpeg) | &check; | 
| [orders/webhooks.py file CI Linter Result](testing_files/orders-webhooks-py.jpeg) | &check; |
| [profiles/forms.py file CI Linter Result](testing_files/profiles-forms-py.jpeg) | &check; |
| [profiles/models.py file CI Linter Result](testing_files/profiles-models-py.jpeg) | &check; |  
| [profiles/urls.py file CI Linter Result](testing_files/profiles-urls-py.jpeg) | &check; |  
| [profiles/views.py file CI Linter Result](testing_files/profiles-views-py.jpeg) | &check; |
| [shopping_bag/context.py file CI Linter Result](testing_files/shopping_bag-context-py.jpeg) | &check; |  
| [shopping_bag/urls.py file CI Linter Result](testing_files/shopping_bag-urls-py.jpeg) | &check; |  
| [shopping_bag/views.py file CI Linter Result](testing_files/shopping_bag-views-py.jpeg) | &check; |

### JavaScript Validations

Validator: https://jshint.com/

| JSHint Result | Passed | Warnings |
| :--- | :---: | :--- | 
| [bag.js file JSHint Result](testing_files/bag-js.jpeg)| &check; | ES11 features were flagged due to JSHint testing code against ES6.|
| [book_management.js file JSHint Result](testing_files/book_management-js.jpeg)| &check; | ES11 features were flagged due to JSHint testing code against ES6.|
| [books.js file JSHint Result](testing_files/books-js.jpeg)| &check; | |
| [checkout.js file JSHint Result](testing_files/checkout-js.jpeg)| &check; | |
| [menu.js file JSHint Result](testing_files/menu-js.jpeg)| &check; | |
| [modal.js file JSHint Result](testing_files/modal-js.jpeg)| &check; | ES11 features were flagged due to JSHint testing code against ES6.|
| [stripe-elements.js file JSHint Result](testing_files/stripe-elements-js.jpeg)| &check; | `Stripe` object is flagged as undefined due to it being imported in the template script.|
| [toast.js file JSHint Result](testing_files/toast-js.jpeg)| &check; | ES11 features were flagged due to JSHint testing code against ES6.|
    

### HTML and CSS Validations

Validator: https://validator.w3.org/

> Please note that all the HTML validations' result looks the same, so I included only one screenshot under the `Home` Page.
> CSS Errors can be ignored as they are referring to new CSS properties (translate, scale, rotate) that are now widely supported.

| W3C Result | Passed |
| :--- | :---: |
| [`Home`](testing-images/ww3c-home.jpeg) Page | &check; |
  

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
* Manual testing revealed that the specified stock data remained blocked (reserved) after session (shopping bag) data got cleared. To rectify this, I wrote a signal to un-reserve the stock after a session is destroyed. I also configured the session to expire after 1 hour of inactivity so that items won't be reserved after this period.
* On `books` page, the Subject choices under `More Options` were all `None` on the deployed site, which did not occure in development. The issue was caused by a linebreak in front of the `</option>` tag.

# Remaining Bugs


##

Chrome warning about Same-Site Cookies flags up Stripe's cookies:
https://support.stripe.com/questions/chrome-80-samesite-cookie-change?locale=en-GB

Stripe's Fraud Detection Scheme for which it is recommended to include its script in every page:
https://stripe.com/docs/disputes/prevention/advanced-fraud-detection