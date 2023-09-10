
const urlSearchParams = new URLSearchParams(window.location.search);
const searchValue = urlSearchParams.get('search');

const searchTerm = document.getElementById('search-input');
console.log(searchTerm)
if (!searchTerm.value === "") {
    searchTerm.value = ""
}

// Update the selected attribute based on user interaction
    document.getElementById("filter-subject").addEventListener("change", function() {
        var selectedValue = this.value;
        var options = this.querySelectorAll("option");
        options.forEach(function(option) {
            option.removeAttribute("selected");
            if (option.value === selectedValue) {
                option.setAttribute("selected", "selected");
            }
        });
    });

    document.getElementById("filter-yeargroup").addEventListener("change", function() {
        var selectedValue = this.value;
        var options = this.querySelectorAll("option");
        options.forEach(function(option) {
            option.removeAttribute("selected");
            if (option.value === selectedValue) {
                option.setAttribute("selected", "selected");
            }
        });
    });