isPageOnTop = true;

function changeToResponsive() {
    var x = document.getElementById("nav-responsive");
    x.classList.toggle("nav-responsive");
}

// check if scrolled?
window.addEventListener("scroll", scrollFunction);

function scrollFunction() {
    const accentBar = document.getElementById("accent-bar");
    const spacer = document.getElementById("spacer");
    if (window.scrollY > 0) {
        accentBar.classList.add("small-bar");
        spacer.classList.add("small-bar");
    } else {
        accentBar.classList.remove("small-bar");
        spacer.classList.remove("small-bar");
    }
}

function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("show");
}