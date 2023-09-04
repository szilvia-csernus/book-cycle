const browseLink = document.querySelector(".browse-link");
console.log(browseLink)
const browse = document.querySelector(".browse");

export function add(a, b) {
	return a + b;
}

export function openBrowse() {
    const overlay = document.createElement('div');
    overlay.classList.add('overlay');
    browse.classList.add("browse-open");
    overlay.addEventListener('click', () => {
        browse.classList.remove("browse-open")
        overlay.remove();
    })
}



browseLink.addEventListener('click', openBrowse)

