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
		fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
		fontSmoothing: 'antialiased',
		fontSize: '16px',
		'::placeholder': {
			color: '#aab7c4',
		},
	},
	invalid: {
		color: '#dc3545',
		iconColor: '#dc3545',
	},
};

// const appearance = {
// 	theme: 'stripe',

// 	variables: {
// 		colorPrimary: '#0570de',
// 		colorBackground: '#ffffff',
// 		colorText: '#30313d',
// 		colorDanger: '#df1b41',
// 		fontFamily: '"Montserrat", system-ui, sans-serif',
// 		spacingUnit: '2px',
// 		borderRadius: '.2rem',
// 	},
// };


const card = elements.create(
	'card',
	// appearance,
	{ 
		style: style,
	    // hidePostalCode: true
	}
	);

card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
	const errorDiv = document.getElementById('card-errors');
	if (event.error) {
		const html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
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

// Function to fade in an element
function fadeIn(element) {
	element.style.display = 'block';
	element.classList.add('fade-in');
	element.classList.remove('fade-out');
}

// Function to make a POST request using fetch
async function post(url, data) {
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
    },
    body: JSON.stringify(data),
  })
  .then(function(response) {
    if (!response.ok) {
      throw new Error('There was an error while waiting for network response.');
    }
    return response.text();
  });
}

// Function to handle the result of the card payment confirmation
function handlePaymentResult(result) {
	console.log(result)
  if (result.error) {
    const errorDiv = document.getElementById('card-errors');
    const html = `
      <span class="icon" role="alert">
      <i class="fas fa-times"></i>
      </span>
      <span>${result.error.message}</span>`;
    errorDiv.innerHTML = html;

	loadingOverlay.classList.remove('overlay');
	toggleElement(loadingOverlay)

    // Enable card and submit button
    card.update({ disabled: false });
    submitButton.disabled = false;
  } else {
    if (result.paymentIntent.status === 'succeeded') {
      paymentForm.submit();
    }
  }
}


paymentForm.addEventListener('submit', event => {
	event.preventDefault();
	card.update({ disabled: true });
	submitButton.disabled = true;
	loadingOverlay.classList.add('overlay');
	toggleElement(loadingOverlay);
	paymentForm.style.display = 'none';

	const saveInfoElement = document.getElementById('save-info');
	let saveInfo = Boolean(saveInfoElement.checked);
	console.log('save-info: ', saveInfo);
	// Form using {% csrf_token %} in the form
	const csrfToken = document
		.querySelector('input[name="csrfmiddlewaretoken"]')
		.value;

	const postData = {
		csrfmiddlewaretoken: csrfToken,
		client_secret: clientSecret,
		save_info: saveInfo,
	};
	const url = '/orders/checkout/';

	// $.post(url, postData)
	// 	.done(function () {
	// 		stripe
	// 			.confirmCardPayment(clientSecret, {
	// 				payment_method: {
	// 					card: card,
	// 					billing_details: {
	// 						name: $.trim(form.full_name.value),
	// 						phone: $.trim(form.phone_number.value),
	// 						email: $.trim(form.email.value),
	// 						// there is no postal code in the form because it's coming from the billing address
	// 						// which is coming from the stripe payment and stripe would overwrite it anyway
	// 						// if we tried to add it
	// 						address: {
	// 							line1: $.trim(form.street_address1.value),
	// 							line2: $.trim(form.street_address2.value),
	// 							city: $.trim(form.town_or_city.value),
	// 							country: $.trim(form.country.value),
	// 							state: $.trim(form.county.value),
	// 						},
	// 					},
	// 				},
	// 				shipping: {
	// 					name: $.trim(form.full_name.value),
	// 					phone: $.trim(form.phone_number.value),
	// 					address: {
	// 						line1: $.trim(form.street_address1.value),
	// 						line2: $.trim(form.street_address2.value),
	// 						city: $.trim(form.town_or_city.value),
	// 						country: $.trim(form.country.value),
	// 						postal_code: $.trim(form.postcode.value),
	// 						state: $.trim(form.county.value),
	// 					},
	// 				},
	// 			})
	// 			.then(function (result) {
	// 				if (result.error) {
	// 					var errorDiv = document.getElementById('card-errors');
	// 					var html = `
	// 						<span class="icon" role="alert">
	// 						<i class="fas fa-times"></i>
	// 						</span>
	// 						<span>${result.error.message}</span>`;
	// 					$(errorDiv).html(html);
	// 					$('#payment-form').fadeToggle(100);
	// 					$('#loading-overlay').fadeToggle(100);
	// 					card.update({ disabled: false });
	// 					$('#submit-button').attr('disabled', false);
	// 				} else {
	// 					if (result.paymentIntent.status === 'succeeded') {
	// 						form.submit();
	// 					}
	// 				}
	// 			});
	// 	})
	// 	.fail(function () {
	// 		// just reload the page, the error will be in django messages
	// 		location.reload();
	// 	});

	// Make the POST request and handle the card payment
	// post(url, postData)
	// 	.then( () => {
	// 		return stripe.confirmCardPayment(clientSecret, {
		stripe.confirmCardPayment(clientSecret, {
				payment_method: {
					card: card,
					billing_details: {
						name: paymentForm.full_name.value.trim(),
						phone: paymentForm.phone_number.value.trim(),
						email: paymentForm.email.value.trim(),

					},
				},
				shipping: {
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
				},
			})
		// })
		.then(result => {
			console.log(result)
			handlePaymentResult(result);
		})
		// .catch(() => {
		// 	// Reload the page on failure
		// 	location.reload();
		// });
});

