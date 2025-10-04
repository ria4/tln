/* Critique Skip-to-main Link - Avoid header covering content */

var skipLink = document.getElementById("skip-link");
skipLink.addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("content").focus();
    window.scrollTo(0, 0);
});


/* Critique Navigation Bars - Reveal and resize bars */

var topNavBar = document.getElementById("top-nav-h");
var topNavTrigger = document.getElementById("top-nav-trigger");
var mainNavBar = document.getElementById("main-nav");
var subNavTrigger = document.getElementById("sub-nav-trigger");
var subNavBar = document.getElementById("sub-nav");
var mainNavLinks = document.getElementById("main-nav-links");
var subNavLinks = document.getElementById("sub-nav-links");

/* Reveal the topNavBar on clicking the utmost left link */
topNavTrigger.addEventListener("click", function(e) {
    e.preventDefault();
    topNavBar.classList.toggle("expanded");
});

/* Reveal the subNavBar on clicking the utmost right link */
subNavTrigger.addEventListener("click", function (e) {
    e.preventDefault();
    subNavBar.classList.toggle("expanded");
});

/* Place the top texts link according to window width */
var widthTriggerTopTextesPosition = 950;
var topTextesMain = mainNavLinks.getElementsByClassName("navlink-shrinkable");
var topTextesSub = subNavLinks.getElementsByClassName("navlink-shrinkable");
function setTopTextesPosition() {
    let elem = null;
    if (window.innerWidth < widthTriggerTopTextesPosition) {
        for (elem of topTextesMain) { elem.style.display = "none"; }
        for (elem of topTextesSub) { elem.style.display = "list-item"; }
    } else {
        for (elem of topTextesMain) { elem.style.display = "list-item"; }
        for (elem of topTextesSub) { elem.style.display = "none"; }
    }
}
setTopTextesPosition();
window.addEventListener("resize", setTopTextesPosition);

/* Hide menus when scrolling down */
var lastKnownScrollPosition = 0;
var ticking = false;
window.addEventListener("scroll", function () {
    if (!ticking) {
        window.requestAnimationFrame(function () {
            if (window.scrollY > lastKnownScrollPosition) {
                topNavBar.classList.remove("expanded");
                subNavBar.classList.remove("expanded");
            }
            lastKnownScrollPosition = window.scrollY;
            ticking = false;
        });
        ticking = true;
    }
});

/* Hide menus when clicking outside the menus */
var contentWrap = document.getElementById("content-wrap");
contentWrap.addEventListener("click", function () {
    topNavBar.classList.remove("expanded");
    subNavBar.classList.remove("expanded");
});

/* Hide menus when clicking on the transparent part of the subNavBar */
subNavLinks.addEventListener("click", function (e) {
    e.stopPropagation();
});
subNavBar.addEventListener("click", function () {
    if (subNavBar.classList.contains("v")) {
        topNavBar.classList.remove("expanded");
        subNavBar.classList.remove("expanded");
    }
});


/* Critique Search Bar - Reveal search bar */

var critiqueSearch = document.getElementById("critique-search");
var critiqueSearchButton = document.getElementById("critique-search-button");
var critiqueSearchEndButton = document.getElementById("critique-searchend-button");
var critiqueSearchM = document.getElementById("critique-search-m");
var critiqueSearchEndButtonM = document.getElementById("critique-searchend-button-m");

var searchInput = document.getElementById("critique-search-input");
var searchInputM = document.getElementById("critique-search-input-m");
var searchPlaceholderPrev = document.getElementById("critique-search-placeholder-prev");
var searchPlaceholderNext = document.getElementById("critique-search-placeholder-next");
var searchResultsList = document.getElementById("critique-search-results-list");
var searchResultsListM = document.getElementById("critique-search-results-list-m");
var critiqueSearchX; var searchInputX; var searchResultsListX;   /* agnostic versions */

var widthTriggerMobileSearch = 700;
getSearchInput = function() {
    return ((window.innerWidth > widthTriggerMobileSearch)? searchInput : searchInputM ) }
function updateAgnosticSearchElements() {
    searchInputX = getSearchInput();
    critiqueSearchX = ((searchInputX === searchInput)? critiqueSearch : critiqueSearchM);
    searchResultsListX = ((searchInputX === searchInput)? searchResultsList : searchResultsListM);
}


function hideSearchInput(prev) {
    updateAgnosticSearchElements();
    if (!critiqueSearchX.classList.contains("expanded")) { return }

    document.activeElement.blur();
    searchResultsListX.replaceChildren();
    searchInputX.value = "";
    critiqueSearchX.classList.remove("expanded");
    if (searchInputX == searchInput) {
        subNavTrigger.classList.remove("reduced");
    } else {
        searchInputM.setAttribute("tabindex", "-1");
        if (prev) {
            searchPlaceholderPrev.focus();
        } else {
            searchPlaceholderNext.focus();
        }
    }
}

critiqueSearchButton.addEventListener("click", function () {
    getSearchInput().focus();
});
critiqueSearchEndButton.addEventListener("click", hideSearchInput);
critiqueSearchEndButtonM.addEventListener("click", hideSearchInput);

searchInput.addEventListener("focus", function () {
    if (getSearchInput() == searchInputM) {
        searchInputM.focus();
    } else {
        subNavTrigger.classList.add("reduced");
        critiqueSearch.classList.add("expanded");
        searchResultsList.parentElement.classList.add("expanded");
        searchResultsList.classList.add("highlight-ok");
    }
});
searchInputM.addEventListener("focus", function () {
    topNavBar.classList.remove("expanded");
    subNavBar.classList.remove("expanded");
    critiqueSearchM.classList.add("expanded");
    searchInputM.setAttribute("tabindex", "0");
});

searchInputM.addEventListener("keydown", function (e) {
    if (e.keyCode == 9) {
        updateAgnosticSearchElements();
        if (e.shiftKey) {
            hideSearchInput(true);
        } else if (searchResultsListX.children.length == 0) {
            hideSearchInput(false);
        }
    }
});
document.addEventListener("click", function () {
    updateAgnosticSearchElements();
    if (!critiqueSearchX.contains(document.activeElement)) {
        if (critiqueSearchX == critiqueSearch) {
            searchResultsList.parentElement.classList.remove("expanded");
        } else {
            hideSearchInput();
        }
    }
});

searchResultsList.addEventListener("mouseleave", function () {
    searchResultsList.classList.remove("highlight-ok"); });
searchResultsListM.addEventListener("mouseleave", function () {
    searchResultsListM.classList.remove("highlight-ok"); });


/* Critique Search Bar - Navigate with arrow keys and ESC */

var activeElementSearch;
document.addEventListener("keydown", function (e) {
    if (e.keyCode == 27) { hideSearchInput(); return }

    activeElementSearch = document.activeElement;
    updateAgnosticSearchElements();
    if (critiqueSearchX.contains(activeElementSearch)) {
        if (e.keyCode == 38) {
            e.preventDefault();
            if (activeElementSearch != searchInputX) {
                if (activeElementSearch == searchResultsListX.firstChild.firstChild) {
                    searchInputX.focus();
                } else {
                    activeElementSearch.parentElement.previousSibling.firstChild.focus();
                }
            }
        } else if (e.keyCode == 40) {
            e.preventDefault();
            if (activeElementSearch == searchInputX) {
                if (!searchResultsListX.firstChild.classList.contains("empty")) {
                    searchResultsListX.firstChild.firstChild.focus();
                }
            } else {
                if (activeElementSearch != searchResultsListX.lastChild.firstChild) {
                    activeElementSearch.parentElement.nextSibling.firstChild.focus();
                }
            }
        }
    }
});


/* Critique Search Bar - AJAX Search */

var emptyElementSearchResult = document.createElement("li");
emptyElementSearchResult.classList.add("empty");
emptyElementSearchResult.innerHTML = "Aucun résultat";

function createElementSearchResult() {
    var li = document.createElement("li");
    var a = document.createElement("a"); li.appendChild(a);
    var p0 = document.createElement("p"); a.appendChild(p0);
    var div = document.createElement("div"); a.appendChild(div);
    var p1 = document.createElement("p"); div.appendChild(p1);
    var p2 = document.createElement("p"); div.appendChild(p2);
    return li
}

function setElementSearchResult(li, res) {
    var a = li.firstChild;
    a.setAttribute("href", "/critique/oeuvre/" + res.slug);
    var p0 = a.firstChild;
    p0.innerHTML = res.vf;
    var div = a.lastChild; var p1 = div.firstChild; var p2 = div.lastChild;
    if (res.vo) {
        p1.innerHTML = res.vo;
    } else {
        p1.innerHTML = "";
    }
    p2.innerHTML = "(" + res.year + ")";

    a.addEventListener("mouseenter", function (e) {
        searchResultsList.classList.add("highlight-ok");
        if (document.activeElement != searchInput) {
            document.activeElement.blur();
        }
    });
    a.addEventListener("focus", function (e) {
        searchResultsListX.classList.add("highlight-ok");
    });
}

var currentSearchRequest = new XMLHttpRequest();
function displaySearchResults(e) {
    updateAgnosticSearchElements();

    if (e.target.value.length > 2) {

        currentSearchRequest.abort();
        var request = new XMLHttpRequest();
        request.open("GET", "/critique/search/" + e.target.value, true);
        request.setRequestHeader("X-Requested-With", "XMLHttpRequest");

        request.onreadystatechange = function() {
            if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
                var response = JSON.parse(request.responseText);

                if (response.length == 0) {

                    if ((!searchResultsListX.firstChild) ||
                        ((searchResultsListX.firstChild) &&
                         (!searchResultsListX.firstChild.classList.contains("empty")))) {
                        while (searchResultsListX.lastChild) {
                            searchResultsListX.removeChild(searchResultsListX.lastChild);
                        }
                        searchResultsListX.appendChild(emptyElementSearchResult);
                    }

                } else {

                    if ((searchResultsListX.firstChild) &&
                        (searchResultsListX.firstChild.classList.contains("empty"))) {
                        searchResultsListX.removeChild(searchResultsListX.firstChild);
                    }

                    var diff = response.length - searchResultsListX.children.length;
                    if (diff > 0) {
                        for (var i=0; i<diff; i++) {
                            searchResultsListX.appendChild(createElementSearchResult());
                        }
                        if (searchResultsListX == searchResultsListM) {
                            var lastLink = searchResultsListX.lastChild.firstChild;
                            lastLink.addEventListener("keydown", function (e) {
                                if (!e.shiftKey && (e.keyCode == 9)) {
                                    hideSearchInput();
                                }
                            });
                        }
                    } else if (diff < 0) {
                        for (var i=diff; i<0; i++) {
                            searchResultsListX.removeChild(searchResultsListX.firstChild);
                        }
                    }

                    for (var i=0; i<response.length; i++) {
                        var li = searchResultsListX.children[i];
                        setElementSearchResult(li, response[i]);
                    }
                }
            }
        }

        currentSearchRequest = request;
        request.send();

    } else {
        while (searchResultsListX.lastChild) {
            searchResultsListX.removeChild(searchResultsListX.lastChild);
        }
    }
}

searchInput.addEventListener("input", displaySearchResults);
searchInputM.addEventListener("input", displaySearchResults);


/* Filter Bar - Highlight selected media type or year */

var filterBar = document.getElementsByClassName("filter-navbar")[0];
if (filterBar) {
    var filter = filterBar.classList[2];
    var links = filterBar.getElementsByTagName("li");
    for (var i=0; i<links.length; i++) {
        var link = links[i].getElementsByTagName("a")[0]
        if (link.getAttribute("desc") == filter) {
            link.classList.add("selected");
        }
    }
}


/* Forms - Validate form inputs */

var oeuvreFormEmpty = document.getElementById("oeuvre_form_empty");
if (oeuvreFormEmpty) {
    titleVf = document.getElementById("id_empty_title_vf");
    titleVo = document.getElementById("id_empty_title_vo");
    titleAlt = document.getElementById("id_empty_title_alt");
    artists = document.getElementById("id_empty_artists");
    year = document.getElementById("id_empty_year");
    imdbId = document.getElementById("id_empty_imdb_id");
    validatedElements = [
        [titleVf, x => ((x.length > 1000) || (x == ""))],
        [titleVo, x => (x.length > 1000)],
        [titleAlt, x => (x.length > 1000)],
        [artists, x => ((x.length > 1000) || (x == ""))],
        [year, x => ((x > 2100) || (x == ""))],
        [imdbId, x => !x.match(/^tt\d{7,8}$|^$/)]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(oeuvreFormEmpty, validatedElements);

    // identify each p-element in the form
    formInputsEmpty = oeuvreFormEmpty.querySelector(".form_inputs");
    for (let pInput of formInputsEmpty.getElementsByTagName("p")) {
        labelFor = pInput.querySelector("label").getAttribute("for");
        pInput.dataset.input = labelFor;
    };
    // assign a data-mtype to display only selected fields
    mtype = document.getElementById("id_empty_mtype");
    formInputsEmpty = oeuvreFormEmpty.querySelector(".form_inputs");
    mtype.addEventListener("change", function (e) {
        formInputsEmpty.dataset.mtype = this.value;
    });
}

var oeuvreForm = document.getElementById("oeuvre_form");
if (oeuvreForm) {
    titleVf = document.getElementById("id_title_vf");
    titleVo = document.getElementById("id_title_vo");
    titleAlt = document.getElementById("id_title_alt");
    artists = document.getElementById("id_artists");
    year = document.getElementById("id_year");
    imdbId = document.getElementById("id_imdb_id");
    validatedElements = [
        [titleVf, x => ((x.length > 1000) || (x == ""))],
        [titleVo, x => (x.length > 1000)],
        [titleAlt, x => (x.length > 1000)],
        [artists, x => ((x.length > 1000) || (x == ""))],
        [year, x => ((x > 2100) || (x == ""))],
        [imdbId, x => !x.match(/^tt\d{7,8}$|^$/)]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(oeuvreForm, validatedElements);

    // identify each p-elements in the form
    formInputs = oeuvreForm.querySelector(".form_inputs");
    for (let pInput of formInputs.getElementsByTagName("p")) {
        labelFor = pInput.querySelector("label").getAttribute("for");
        pInput.dataset.input = labelFor;
    };
    // assign a data-mtype to display only selected fields
    mtype = document.getElementById("id_mtype");
    mtype.addEventListener("change", function (e) {
        formInputs.dataset.mtype = this.value;
    });
}

var oeuvrespanFormEmpty = document.getElementById("oeuvrespan_form_empty");
var oeuvrespanForm = document.getElementById("oeuvrespan_form");

var commentFormEmpty = document.getElementById("comment_form_empty");
if (commentFormEmpty) {
    date = document.getElementById("id_empty_date");
    comment_content = document.getElementById("id_empty_content");
    validatedElements = [
        [date, x => (x == "")],
        [comment_content, x => (x == "")]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(commentFormEmpty, validatedElements);
}

var commentForm = document.getElementById("comment_form");
if (commentForm) {
    date = document.getElementById("id_date");
    comment_content = document.getElementById("id_content");
    validatedElements = [
        [date, x => (x == "")],
        [comment_content, x => (x == "")]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(commentForm, validatedElements);
}

var cinemaFormEmpty = document.getElementById("cinema_form_empty");
if (cinemaFormEmpty) {
    nameInput = document.getElementById("id_empty_cinema_name");
    nameLong = document.getElementById("id_empty_cinema_name_long");
    locationInput = document.getElementById("id_empty_cinema_location");
    validatedElements = [
        [nameInput, x => (x == "")],
        [nameLong, x => (x == "")],
        [locationInput, x => (x == "")]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(cinemaFormEmpty, validatedElements);
}

var cinemaForm = document.getElementById("cinema_form");
if (cinemaForm) {
    nameInput = document.getElementById("id_name");
    nameLong = document.getElementById("id_name_long");
    locationInput = document.getElementById("id_location");
    validatedElements = [
        [nameInput, x => (x == "")],
        [nameLong, x => (x == "")],
        [locationInput, x => (x == "")]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(cinemaForm, validatedElements);
}

var seanceFormEmpty = document.getElementById("seance_form_empty");
if (seanceFormEmpty) {
    cinema = document.getElementById("id_empty_seance_cinema");
    date = document.getElementById("id_empty_seance_date");
    hour = document.getElementById("id_empty_seance_hour");
    validatedElements = [
        [date, x => (x == "")],
        [hour, x => ((x.length != 5) || (x.charAt(2) != ":") || (parseInt(x.charAt(0), 10) > 2) || (parseInt(x.charAt(3), 10) > 5))],
    ];
    addInputsListener(validatedElements, true);

    // this cross-check does not work with the select2 used for film selection
    /* exactly one of these must be filled
    film = document.getElementById("id_empty_seance_film");
    seanceTitle = document.getElementById("id_empty_seance_seance_title");

    validatedElementsComplete = validatedElements.slice()
    validatedElementsComplete.push([film, null]);
    validatedElementsComplete.push([seanceTitle, null]);
    addSubmitListener(seanceFormEmpty, validatedElementsComplete);

    warningOnElementIf(film, true);
    warningOnElementIf(seanceTitle, true);
    film.addEventListener("blur", function(e) {
        var seanceFormError = (((film.value == "") && (seanceTitle.value == "")) ||
                               ((film.value != "") && (seanceTitle.value != "")))
        warningOnElementIf(film, seanceFormError);
        warningOnElementIf(seanceTitle, seanceFormError);
    });
    film.addEventListener("change", function(e) {
        var seanceFormError = (((film.value == "") && (seanceTitle.value == "")) ||
                               ((film.value != "") && (seanceTitle.value != "")))
        warningOnElementIf(film, seanceFormError);
        warningOnElementIf(seanceTitle, seanceFormError);
    });
    seanceTitle.addEventListener("blur", function(e) {
        var seanceFormError = (((film.value == "") && (seanceTitle.value == "")) ||
                               ((film.value != "") && (seanceTitle.value != "")))
        warningOnElementIf(film, seanceFormError);
        warningOnElementIf(seanceTitle, seanceFormError);
    });
    seanceTitle.addEventListener("input", function(e) {
        var seanceFormError = (((film.value == "") && (seanceTitle.value == "")) ||
                               ((film.value != "") && (seanceTitle.value != "")))
        warningOnElementIf(film, seanceFormError);
        warningOnElementIf(seanceTitle, seanceFormError);
    });
    */
}

var tierListFormEmpty = document.getElementById("tierlist_form_empty");
if (tierListFormEmpty) {
    nameInput = document.getElementById("id_empty_tierlist_name");
    validatedElements = [
        [nameInput, x => (x == "")],
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(tierListFormEmpty, validatedElements);
}

var tierListForm = document.getElementById("tierlist_form");
if (tierListForm) {
    nameInput = document.getElementById("id_name");
    validatedElements = [
        [nameInput, x => (x == "")],
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(tierListForm, validatedElements);
}

var tierFormEmpty = document.getElementById("tier_form_empty");
if (tierFormEmpty) {
    nameInput = document.getElementById("id_empty_tier_name");
    position = document.getElementById("id_empty_tier_position");
    validatedElements = [
        [nameInput, x => (x == "")],
        [position, x => ((x < 0) || (x > 100) || (x == ""))],
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(tierFormEmpty, validatedElements);
}

// no validation on existing tierForms because getting the input fields
// becomes messy when looping over multiple overlays


/* Forms - Autocomplete init values on appropriate pages */

if (oeuvrespanFormEmpty) {
    if (
        (typeof oeuvrespanDefaultOeuvreId !== "undefined")
        && (typeof oeuvrespanDefaultOeuvreTitle !== "undefined")) {
        var oeuvrespanEmptySelect = document.getElementById("id_empty_oeuvrespan_oeuvre");
        oeuvrespanEmptySelect.children[0].removeAttribute("selected");
        var optionOeuvreSpan = document.createElement("option");
        optionOeuvreSpan.setAttribute("value", oeuvrespanDefaultOeuvreId);
        optionOeuvreSpan.setAttribute("selected", "");
        optionOeuvreSpan.textContent = oeuvrespanDefaultOeuvreTitle;
        oeuvrespanEmptySelect.appendChild(optionOeuvreSpan);
    }
}


/* Critique Admin Codes - Register admin inputs */

function deployAdminInputLogic() {

    function displayAdminInput() {
        adminInput.style.display = "initial";
        adminInput.focus();
    }
    function hideAdminInput() {
        adminInput.style.display = "none";
        adminInput.value = "";
    }

    // display admin input after two short taps

    let adminTapCount = 0;
    let tapStartTime = 0;
    let noTapStartTime = 0;

    function handleTouchStart() {
        if (adminTapCount > 0) {
            var noTapDuration = new Date().getTime() - noTapStartTime;
            if (noTapDuration > 500) {
                // reset counter if too much time has passed
                adminTapCount = 0;
            }
        }
        tapStartTime = new Date().getTime();
    }

    function handleTouchEnd(e) {
        var tapDuration = new Date().getTime() - tapStartTime;
        if (tapDuration < 200) {
            adminTapCount++;
        }
        if (adminTapCount >= 2) {
            e.preventDefault();
            displayAdminInput();
            adminTapCount = 0;
        }
        noTapStartTime = new Date().getTime();
    }

    document.body.addEventListener("touchstart", handleTouchStart);
    document.body.addEventListener("touchend", handleTouchEnd);

    adminInput.addEventListener("input", function (e) {
        cachedCode = e.target.value;
        if (activateOverlayIf(e)) { hideAdminInput(); }
    });
}


codes["addo"] = oeuvreFormEmpty;
codes["edito"] = oeuvreForm;

codes["addsp"] = oeuvrespanFormEmpty;
codes["editsp"] = oeuvrespanForm;

codes["addco"] = commentFormEmpty;
codes["editco"] = commentForm;

codes["addci"] = cinemaFormEmpty;
codes["editci"] = cinemaForm;

codes["addse"] = seanceFormEmpty;

codes["addtl"] = tierListFormEmpty;
codes["edittl"] = tierListForm;

codes["addte"] = tierFormEmpty;
for (let i = 0; i < 10; i++) {
    var tierForm = document.getElementById(`tier_form_${i}`);
    if (tierForm) {
        codes[`editte${i}`] = tierForm;
    }
}

codes["s"] = true;

for (var key in codes) {
    if (codes.hasOwnProperty(key)) {
        if ((["s", "login", "logout", "admin"].indexOf(key) < 0) && (codes[key])) {
            codes[key].addEventListener("reset", function (e) {
                e.preventDefault();
                e.target.parentElement.classList.remove("revealed");
                activeCode = "";
            });
        }
    }
}
