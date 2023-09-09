const buttonNew = document.getElementById("button-new");
const buttonGood = document.getElementById("button-good");
const buttonFair = document.getElementById("button-fair");

const stock = {
	new: buttonNew?.dataset.stockQuantity,
	good: buttonGood?.dataset.stockQuantity,
	fair: buttonFair?.dataset.stockQuantity,
};

function addMoreBookToBasket(id, key) {
    const counter = document.getElementById(`counter-${id}`);
    const stockElement = document.getElementById(`stock-${id}`);
    counter.textContent = counter.textContent ++;
    stock[key]--;
    if (stock[key] > 0) {
        counter.textContent = Number(counter.textContent) + 1;
        stockElement.textContent = `${stock[key]} more in stock`;
    }
    else {
        stockElement.textContent = `no more left in stock`;
        counter.textContent = Number(counter.textContent) + 1;
        const plusBtn = document.getElementById(`plus-${id}`)
        plusBtn.disabled = true;
    }
}

function createPlusButton(id, key) {
    const plusButton = document.createElement('button');
    plusButton.classList.add('stockline-button');
    plusButton.textContent = '+';
    plusButton.id = `plus-${id}`;
    plusButton.addEventListener('click', () => addMoreBookToBasket(id, key))
    return plusButton
}

function createMinusButton(id) {
    const minusButton = document.createElement('button')
    minusButton.classList.add("stockline-button");
    minusButton.textContent = "-"
    minusButton.id = `minus-${id}`;
    return minusButton
}

function createCounter(id) {
    const counter = document.createElement('strong');
    counter.textContent = "1";
    counter.id = `counter-${id}`;
    return counter
}

function replaceButtons(id, key) {
    const replaceElement = document.createElement('div');
    replaceElement.classList.add("replace-element")
    const minus = createMinusButton(id, key);
    replaceElement.append(minus);
    const counter = createCounter(id);
    replaceElement.append(counter);
    const plus = createPlusButton(id, key);
    replaceElement.append(plus);
    return replaceElement
}


buttonNew?.addEventListener('click', event => {
    const id = buttonNew.dataset.stockId;
    const replaceElement = replaceButtons(id, "new")
    buttonNew.replaceWith(replaceElement)
    const stockElement = document.getElementById(`stock-${id}`);
    stockElement.textContent = `${stock.new} more in stock`
})

buttonGood?.addEventListener('click', event => {
    const id = buttonGood.dataset.stockId;
    const replaceElement = replaceButtons(id, "good")
    buttonGood.replaceWith(replaceElement)
    const stockElement = document.getElementById(`stock-${id}`);
    stockElement.textContent = `${stock.good} more in stock`
})

buttonFair?.addEventListener('click', event => {
    const id = buttonFair.dataset.stockId;
    const replaceElement = replaceButtons(id, "fair")
    buttonFair.replaceWith(replaceElement)
    const stockElement = document.getElementById(`stock-${id}`);
    stockElement.textContent = `${stock.fair} more in stock`
})