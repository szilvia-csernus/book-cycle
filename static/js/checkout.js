const shippingOptionForm = document.getElementById('shipping-option-form');

// submit the form again if user changes the shipping method.
shippingOptionForm.addEventListener('change', () => {
    shippingOptionForm.submit()
})
