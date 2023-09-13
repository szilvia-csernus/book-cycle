// Get the form element by its ID
const form = document.getElementById('shipping-option-form');

// Get all the radio buttons with the name "shipping_option"
const radioButtons = form.querySelectorAll(
	'input[type=radio][name=shipping_option]'
);

// Add event listeners to both buttons to submit the form whenever the 'checked'
// attribute changes.
radioButtons.forEach( radioButton => {
    radioButton.addEventListener('change', () => {
        form.submit();
    });
});

