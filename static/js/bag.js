// Get one 'Bag Total' value and (potentially 2) 'Grand Total' element(s)
const bagTotalElement = document.querySelector('.bag-total-number');
let bagTotal = bagTotalElement ? Number(bagTotalElement.textContent) : 0;
const grandTotalElements = document.querySelectorAll('.grand-total-number')

// Get all the radio buttons with the name "shipping_option"
// There are potentially 2 sets of buttons if the shopping bag page is also open
// in the background as well as the small shopping bag on the side.
const pickups = document.querySelectorAll('input[type="radio"][value="pickup"]');
const posts = document.querySelectorAll('input[type="radio"][value="post"]');
const radioButtons = document.querySelectorAll('input[type="radio"][name="shipping_option"]')

// Check localstorage for shipping preference
let shippingPreference = window.localStorage.getItem('shipping')
console.log(shippingPreference)

// if shippingPreference is in localStorage, set the corresponding button to checked,
// otherwise set the 'pickup' option to checked
if (shippingPreference === 'post') {
    posts.forEach(post => post.checked = true);
    grandTotalElements.forEach(el=>el.textContent = (bagTotal + 3.5).toFixed(2))
} else {
    pickups.forEach(pickup => pickup.checked = true);
    grandTotalElements.forEach((el) => (el.textContent = bagTotal));
}

// handle state changes such that all elements get updated on both pages.
pickups.forEach(pickup => pickup.addEventListener('change', function() {
    if (this.checked) {
        grandTotalElements.forEach(el => el.textContent = bagTotal);
        pickups.forEach((pickup) => (pickup.checked = true));
    }
    else {
        grandTotalElements.forEach(el => el.textContent = (bagTotal + 3.5).toFixed(2));
        posts.forEach((post) => (post.checked = true));
    }
}))

posts.forEach(post=>post.addEventListener('change', function() {
    if (this.checked) {
        grandTotalElements.forEach(el => (el.textContent = (bagTotal + 3.5).toFixed(2)));
        posts.forEach((post) => (post.checked = true));
    }
    else {
        grandTotalElements.forEach(el => (el.textContent = bagTotal));
        pickups.forEach((pickup) => (pickup.checked = true));
    }
}))

// Add event listeners to all buttons to change localStorage['shipping'] whenever the 'checked'
// attribute changes.
radioButtons.forEach(function (radio) {
	radio.addEventListener('change', function () {
		if (this.checked) {
			// Store the selected value in localStorage
			localStorage.setItem('shipping', this.value);
		}
	});
});


const bagLink = document.getElementById('bag-link');
const bagElement = document.getElementById('quick-bag');
const closeQuickBagBtn = document.getElementById('quick-bag-close-button');
let overlayEl;

const closeQuickBag = () => {
    if (bagElement.classList.contains('quick-bag-open')) {
        bagElement.classList.remove('quick-bag-open');
    }
    if (overlayEl) {
        overlayEl.remove()
    }
    // release scrolling ban
    document.body.style.position = 'static';
} 

/** Opens the quick bag window */
const openQuickBag = () => {
	overlayEl = document.createElement('div');
	document.body.appendChild(overlayEl);
	overlayEl.classList.add('overlay');
	bagElement.classList.add('quick-bag-open');
    // prevent the background to scroll
    document.body.style.position = 'fixed';
	closeQuickBagBtn.addEventListener('click', () => {
		closeQuickBag()
	});
	overlayEl.addEventListener('click', () => {
		closeQuickBag()
	});
}

bagLink.addEventListener('click', openQuickBag);

