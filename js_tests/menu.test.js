// run "npx jest" in the js_tests folder

import { add, openBrowse } from "../static/js/menu"

describe("DOM tests", () => {
	test("header exists", () => {
		expect(document.getElementsByTagName("header").length).toBe(1);
	})
	test("all 6 icons are rendered", () => {
		expect(document.getElementsByTagName("img").length).toBe(6);
	})
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

