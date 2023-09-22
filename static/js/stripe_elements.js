/**
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/js

    CSS from here: 
    https://stripe.com/docs/stripe-js
	https://stripe.com/docs/elements/appearance-api
*/

const stripePublicKeyEl = document.getElementById('id_stripe_public_key')
const stripePublicKey = stripePublicKeyEl.textContent.slice(1, -1);

const clientSecret = document
	.getElementById('id_client_secret')
	.textContent.slice(1, -1);

const stripe = Stripe(stripePublicKey);

const elements = stripe.elements();

var style = {
	base: {
		color: '#000',
		fontFamily: '"Montserrat", sans-serif',
		fontSmoothing: 'antialiased',
		fontSize: '17px',
		'::placeholder': {
			color: '#aab7c4',
		},
	},
	invalid: {
		color: '#dc3545',
		iconColor: '#dc3545',
	},
};

const card = elements.create(
	'card',
	{ 
		style: style,
	    hidePostalCode: true
	}
	);

card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
	const errorDiv = document.getElementById('card-errors');
	if (event.error) {
		const html = `
            <div>&cross;</div>
            <div>${event.error.message}</div>
        `;
		errorDiv.innerHTML = html;
	} else {
		errorDiv.textContent = '';
	}
});

// Toggle the visibility of the element with a fade effect
const toggleElement = element => {
	if (element.classList.contains('loading-overlay-active')) {
		element.classList.remove('loading-overlay-active')
	} else {
		element.classList.add('loading-overlay-active')
	}
}

// Handle form submit
const paymentForm = document.getElementById('payment-form');

const submitButton = document.getElementById('submit-button');
const loadingOverlay = document.getElementById('loading-overlay')
loadingOverlay.classList.add('loading-overlay');


// Function to handle the result of the card payment confirmation
function handlePaymentResult(result) {
  if (result.error) {
    const errorDiv = document.getElementById('card-errors');
    const html = `
	  <div>&cross;</div>
      <div> ${result.error.message}</div>`;
    errorDiv.innerHTML = html;

	toggleElement(loadingOverlay)
	loadingOverlay.classList.remove('overlay');
	paymentForm.style.display = 'block';

    // Enable card and submit button
    card.update({ disabled: false });
    submitButton.disabled = false;
  } else {
    if (result.paymentIntent.status === 'succeeded') {
    //   paymentForm.submit();
    }
  }
}

const shippingInfo = localStorage.getItem('shipping') === 'post' ? true : false

paymentForm.addEventListener('submit', event => {
	event.preventDefault();
	card.update({ disabled: true });
	submitButton.disabled = true;
	loadingOverlay.classList.add('overlay');
	toggleElement(loadingOverlay);
	paymentForm.style.display = 'none';

	const saveInfoElement = document.getElementById('save-info');
	const saveInfo = saveInfoElement ? Boolean(saveInfoElement.checked) : false;
	console.log('save-info: ', saveInfo);
	
	const csrfToken = document
		.querySelector('input[name="csrfmiddlewaretoken"]')
		.value;

	const postData = {
		csrfmiddlewaretoken: csrfToken,
		client_secret: clientSecret,
		save_info: saveInfo,
		shipping_option: shippingInfo
	};

	const url = '/orders/cache_checkout_data/';


	// Make the POST request and handle the card payment
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
		body: JSON.stringify(postData),
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error(
					'There was an error while waiting for network response.'
				);
			}
			let shipping = null;
			if (shippingInfo) {
				shipping = {
					name: paymentForm.full_name.value.trim(),
					phone: paymentForm.phone_number.value.trim(),
					address: {
						line1: paymentForm.street_address1.value.trim(),
						line2: paymentForm.street_address2.value.trim(),
						city: paymentForm.town_or_city.value.trim(),
						country: paymentForm.country.value.trim(),
						postal_code: paymentForm.postcode.value.trim(),
						state: paymentForm.county.value.trim(),
					},
				};
			}
			return stripe.confirmCardPayment(clientSecret, {
				payment_method: {
					card: card,
					billing_details: {
						name: paymentForm.full_name.value.trim(),
						phone: paymentForm.phone_number.value.trim(),
						email: paymentForm.email.value.trim(),
						// there is no postal code in the form because it's coming from stripe's card element
						// and stripe would overwrite it anyway if we tried to add it
					},
				},
				shipping: shipping,
			});
		})
		.then((result) => {
			console.log(result);
			handlePaymentResult(result);
		})
		.catch(() => {
			// Reload the page on failure
			location.reload();
		});
});

