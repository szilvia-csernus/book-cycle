// Grab the current URL and put the query parameters into variables.
const currentUrl = new URL(window.location);
const searchValue = currentUrl.searchParams.get('search');
const subjectValue = currentUrl.searchParams.get('subject');
const sortValue = currentUrl.searchParams.get('sort');
const yearGroupValue = currentUrl.searchParams.get('year_group');

// Grab all search and filter elements
const allBooksBtn = document.getElementById('all-books')
const year7to9Btn = document.getElementById('year7-9')
const gcseBtn = document.getElementById('gcse')
const aLevelBtn = document.getElementById('a-level')
const moreOptionsBtn = document.getElementById('more-options')
const filterSortBox = document.getElementById('filter-sort-search-box')

const searchTermElement = document.getElementById('search-input-nr2');
const searchButton = document.getElementById('search-button-nr2');
const filterSubject = document.getElementById('filter-subject');
const filterYearGroup = document.getElementById('filter-yeargroup');
const sortBy = document.getElementById('sort');

// Put the search term which was entered through the side menu
// into the search input field
searchTermElement.value = searchValue;

// Mark the More Options button active if any of its fields are filled in.
// Otherwise, mark the clicked yeargroup's button active
if (searchValue || subjectValue || sortValue) {
    moreOptionsBtn.classList.add('active');
    filterSortBox.classList.add('active');
    allBooksBtn.classList.remove('active');
}
else {
    if (yearGroupValue) {
        allBooksBtn.classList.remove('active');
        if (yearGroupValue === 'year7-9') {
            year7to9Btn.classList.add('active')
            }
        else if (yearGroupValue === 'gcse') {
                gcseBtn.classList.add('active');
            }
        else if (yearGroupValue === 'a-level') {
                aLevelBtn.classList.add('active');
            }
    }
}

// Put the clicked yeargroup in the query parameter and reload a page. 
// This will initiate filtering.

year7to9Btn.addEventListener('click', () => {
    currentUrl.search = '';
    currentUrl.searchParams.set('year_group', 'year7-9')
    window.location.replace(currentUrl);
})

gcseBtn.addEventListener('click', () => {
    currentUrl.search = '';
	currentUrl.searchParams.set('year_group', 'gcse');
	window.location.replace(currentUrl);
});

aLevelBtn.addEventListener('click', () => {
    currentUrl.search = '';
	currentUrl.searchParams.set('year_group', 'a-level');
	window.location.replace(currentUrl);
});

allBooksBtn.addEventListener('click', () => {
	currentUrl.search = '';
	window.location.replace(currentUrl);
});

/** Toggles an element by applying/removing the 'active' css class. */
function toggleActive(element) {
    if (element.classList.contains('active')) {
        element.classList.remove('active')
        window.location.replace(currentUrl);
    } else {
        element.classList.add('active')
    }
}

/** Removes the 'active' css class from the element. */
function removeActive(element) {
    if (element.classList.contains('active')) {
        element.classList.remove('active')
    }
}

/** If More Options button is clicked, remove the active status of all the
 * other buttons.
 */
moreOptionsBtn.addEventListener('click', () => {
    removeActive(allBooksBtn);
    removeActive(year7to9Btn);
    removeActive(gcseBtn);
    removeActive(aLevelBtn);

    toggleActive(moreOptionsBtn);
    toggleActive(filterSortBox);
})

/** separate the 'subject_asc' etc. sort input format into sort= and direction= 
 * and set them as params in the current url.
*/
const resolveSortInput = () => {
    const sort = sortBy.value.split('_')[0];
    const direction = sortBy.value.split('_')[1];
    currentUrl.searchParams.set('sort', sort);
    currentUrl.searchParams.set('direction', direction);
}

// If Enter is clicked after entering a search term, set all the search/filter
// query parameters and reload the window.
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

// If magnifying glass icon was clicked, set the search query parameter and
// reload the window.
searchButton.addEventListener('click', event => {
    event.preventDefault()
    resolveSortInput()
    currentUrl.searchParams.set('search', searchTermElement.value);
	window.location.replace(currentUrl);
})


// Update the filter/sort query parameters whenever the user changes the 
// select options.

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


// Scroll back to top if user clicks the 'back to top' button.
const backToTopBtn = document.querySelector('.back-to-top');
backToTopBtn.addEventListener('click', () => {
	window.scrollTo(0, 0);
});