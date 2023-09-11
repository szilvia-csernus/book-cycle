const currentUrl = new URL(window.location);
const searchValue = currentUrl.searchParams.get('search');

const searchTermElement = document.getElementById('search-input-nr2');
searchTermElement.value = searchValue
const searchButton = document.getElementById('search-button-nr2');
const filterSubject = document.getElementById('filter-subject');
const filterYearGroup = document.getElementById('filter-yeargroup');
const sortBy = document.getElementById('sort');
console.log(sortBy.value)

/** separate the 'subject_asc' etc. sort input format into sort= and direction= 
 * and set them as params in the current url.
*/
const resolveSortInput = () => {
    const sort = sortBy.value.split('_')[0];
    const direction = sortBy.value.split('_')[1];
    currentUrl.searchParams.set('sort', sort);
    currentUrl.searchParams.set('direction', direction);
}

searchTermElement.addEventListener('keydown', (event) => {
	
    resolveSortInput()

	if (event.key === 'Enter') {
        event.preventDefault()
		
        currentUrl.searchParams.set('search', event.target.value);
        currentUrl.searchParams.set('subject', filterSubject.value);
        currentUrl.searchParams.set('year_group', filterYearGroup.value);
        window.location.replace(currentUrl);
		
	}
});

searchButton.addEventListener('click', event => {
    event.preventDefault()
    resolveSortInput()
    currentUrl.searchParams.set('search', searchTermElement.value);
	window.location.replace(currentUrl);
})


// Update the selected attribute based on user interaction

filterSubject.addEventListener('change', (event) => {
	const selectedValue = event.currentTarget.value;

	currentUrl.searchParams.set('subject', selectedValue);
    currentUrl.searchParams.set('search', searchTermElement.value);
	window.location.replace(currentUrl);
});

filterYearGroup.addEventListener('change', (event) => {
	const selectedValue = event.currentTarget.value;

	currentUrl.searchParams.set('year_group', selectedValue);
    currentUrl.searchParams.set('search', searchTermElement.value);
	window.location.replace(currentUrl);
});


sortBy.addEventListener('change', (event) => {

    resolveSortInput()

    currentUrl.searchParams.set('search', searchTermElement.value);
	window.location.replace(currentUrl);
});

const backToTopBtn = document.querySelector('.back-to-top');
backToTopBtn.addEventListener('click', () => {
	window.scrollTo(0, 0);
});