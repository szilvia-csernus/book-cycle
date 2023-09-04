import { add, openBrowse } from "../static/js/menu"

test('Addition function should return the correct sum', () => {
	expect(add(2, 3)).toBe(5);
});

test('Test DOM interaction', () => {
	// Access DOM elements and perform interactions as needed
	const myElement = document.querySelector('.test');
	expect(myElement.textContent).toBe('TestDiv');
});

describe("DOM tests", () => {
	test("header exists", () => {
		expect(document.getElementsByTagName("header").length).toBe(1);
	})
	test("main exists", () => {
		expect(document.getElementsByTagName("main").length).toBe(1);
	})
})

