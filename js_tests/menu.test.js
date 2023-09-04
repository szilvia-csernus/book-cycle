import { add, openBrowse } from "../static/js/menu"

test('Addition function should return the correct sum', () => {
	expect(add(2, 3)).toBe(5);
});

describe("DOM tests", () => {
	test("header exists", () => {
		expect(document.getElementsByTagName("header").length).toBe(1);
	})
	// test("icons exists", () => {
	// 	expect(document.getElementsByTagName("img").length).toBe(3);
	// })
	test("header-left exists", () => {
		expect(document.querySelectorAll(".header-left").length).toBe(1);
	})
	test("header-right exists", () => {
		expect(document.querySelectorAll(".header-right").length).toBe(1);
	})
	test("browse menu items exists", () => {
		expect(document.querySelectorAll(".browse-category").length).toBe(3);
	})
})

