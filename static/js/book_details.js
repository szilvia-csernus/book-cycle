const buttonNew = document.getElementById("add-button-new");
const buttonGood = document.getElementById("add-button-good");
const buttonFair = document.getElementById("add-button-fair");

const stock = {
	new: buttonNew?.dataset.stockQuantity,
	good: buttonGood?.dataset.stockQuantity,
	fair: buttonFair?.dataset.stockQuantity,
};

function addMoreBookToBag(id, key) {
    const counter = document.getElementById(`counter-${id}`);
    const stockElement = document.getElementById(`stock-${id}`);
    const plusButton = document.getElementById(`plus-${id}`);
    counter.textContent = Number(counter.textContent) + 1;
    stock[key]--;
    if (stock[key] > 0) {
        if (Number(counter.textContent) > 10) {
            stockElement.textContent = '10+ in stock';
        } else {
            stockElement.textContent = `${stock[key]} more in stock`;
        }
        plusButton.disabled = false;
    }
    else {
        stockElement.textContent = `no more left in stock`;
        
        plusButton.disabled = true;
    }
}

// function recreteAddButton(id, key) {
//     const button = document.createElement('button');
//     button.id = `button-${key}`;
//     button.dataset.stockId = id;
//     button.dataset.stockQuantity = stock[key];
//     button.classList.add('stockline-button');
//     button.textContent = 'Add';
    
//     stockElement.textContent = `\u2713 in stock`;
//     button.addEventListener('click', () => {
//         const replaceElement = replaceButtons(id, key);
//         button.replaceWith(replaceElement);
//         const stockElement = document.getElementById(`stock-${id}`);
//         stockElement.textContent = `${stock[key]} more in stock`;
//     });

//     return button
// }

function removeBookFromBag(id, key) {
	const counter = document.getElementById(`counter-${id}`);
	const stockElement = document.getElementById(`stock-${id}`);
    const minusButton = document.getElementById(`minus-${id}`);
    const plusButton = document.getElementById(`plus-${id}`);
    plusButton.disabled = false;
	counter.textContent = Number(counter.textContent) - 1;
	stock[key]++;
	if (counter.textContent === "0") {
        const replaceElement = key === "new" ? buttonNew :
            key === "good" ? buttonGood : buttonFair
        replaceElement.style.display = "block";
        stockElement.textContent = `\u2713 in stock`;
        minusButton.remove();
        counter.remove();
        plusButton.remove();
		
	} else {
        if (Number(counter.textContent) > 10) {
                stockElement.textContent = '10+ in stock';
            } else {
                stockElement.textContent = `${stock[key]} more in stock`;
            }
	}
}

function createPlusButton(id, key) {
    const plusButton = document.createElement('button');
    plusButton.classList.add('stockline-button');
    plusButton.textContent = '+';
    plusButton.id = `plus-${id}`;
    plusButton.addEventListener('click', () => addMoreBookToBag(id, key))
    return plusButton
}

function createMinusButton(id, key) {
    const minusButton = document.createElement('button')
    minusButton.classList.add("stockline-button");
    minusButton.textContent = "-"
    minusButton.id = `minus-${id}`;
    minusButton.addEventListener('click', () => removeBookFromBag(id, key))
    return minusButton
}

function createCounter(id, key) {
    const counter = document.createElement('strong');
    counter.classList.add('stockline-counter');
    counter.textContent = "1";
    counter.id = `counter-${id}`;
    stock[key]--;
    return counter
}

function replaceButtons(id, key) {
    const replaceElement = document.createElement('div');
    replaceElement.classList.add("stockline-replace-element")
    const minus = createMinusButton(id, key);
    replaceElement.append(minus);
    const counter = createCounter(id, key);
    replaceElement.append(counter);
    const plus = createPlusButton(id, key);
    replaceElement.append(plus);
    return replaceElement
}


buttonNew?.addEventListener('click', event => {
    const id = buttonNew.dataset.stockId;
    const replaceElement = replaceButtons(id, "new")
    buttonNew.parentNode.append(replaceElement);
    buttonNew.style.display = "none"
    const stockElement = document.getElementById(`stock-${id}`);
    const counterElement = document.getElementById(`counter-${id}`);
    stockElement.textContent = `${stock.new} more in stock`
    const plusButton = document.getElementById(`plus-${id}`);
    if (stock.new > 0) {
			if (Number(counterElement.textContent) > 10) {
				stockElement.textContent = '10+ in stock';
			} else {
				stockElement.textContent = `${stock.new} more in stock`;
			}
			plusButton.disabled = false;
		} else {
			stockElement.textContent = `no more left in stock`;

			plusButton.disabled = true;
		}

})

buttonGood?.addEventListener('click', event => {
    const id = buttonGood.dataset.stockId;
    const replaceElement = replaceButtons(id, "good")
    buttonGood.parentNode.append(replaceElement);
    buttonGood.style.display = "none";
    const stockElement = document.getElementById(`stock-${id}`);
    const counterElement = document.getElementById(`counter-${id}`);
    stockElement.textContent = `${stock.good} more in stock`
    const plusButton = document.getElementById(`plus-${id}`);
    if (stock.good > 0) {
			if (Number(counterElement.textContent) > 10) {
				stockElement.textContent = '10+ in stock';
			} else {
				stockElement.textContent = `${stock.good} more in stock`;
			}
			plusButton.disabled = false;
		} else {
			stockElement.textContent = `no more left in stock`;

			plusButton.disabled = true;
		}
})

buttonFair?.addEventListener('click', event => {
    const id = buttonFair.dataset.stockId;
    const replaceElement = replaceButtons(id, "fair")
    buttonFair.parentNode.append(replaceElement)
    buttonFair.style.display = "none";
    const stockElement = document.getElementById(`stock-${id}`);
    const counterElement = document.getElementById(`counter-${id}`);
    stockElement.textContent = `${stock.fair} more in stock`;
    const plusButton = document.getElementById(`plus-${id}`);
    if (stock.fair > 0) {
			if (Number(counterElement.textContent) > 10) {
				stockElement.textContent = '10+ in stock';
			} else {
				stockElement.textContent = `${stock.fair} more in stock`;
			}
			plusButton.disabled = false;
		} else {
			stockElement.textContent = `no more left in stock`;

			plusButton.disabled = true;
		}
})