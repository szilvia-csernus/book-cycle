const searchedTermBox = document.querySelector(".searched-term-box");
const searchedTermCloseBtn = document.querySelector(".searched-term-close");
searchedTermCloseBtn.addEventListener('click', () => {
    searchedTermBox.classList.remove('active');
    // clear search term and submit the form again
})