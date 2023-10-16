// Grab the form element containing the shipping option radio buttons.
const shippingOptionForm = document.getElementById('shipping-option-form');

// Submit the form again if user changes the shipping method. This will re-
// calculate the Grand Total.
shippingOptionForm.addEventListener('change', () => {
    shippingOptionForm.submit();
});
