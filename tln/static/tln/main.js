var isIE10 = 'behavior' in document.documentElement.style && '-ms-user-select' in document.documentElement.style;
var isIE11 = '-ms-scroll-limit' in document.documentElement.style && '-ms-ime-align' in document.documentElement.style;
function isTouchDevice() { return "ontouchstart" in window || navigator.maxTouchPoints; }


/* Login - Show login prompt on appropriate URLs */

var hash = window.location.hash.substr(1);
var loginForm = document.getElementById("login_form");

if (hash == "login" && !userIsAuthenticated) {
    loginForm.parentElement.classList.add("revealed");
    focusOn(loginForm.parentElement, "id_username");
    activeCode = "login";
}


/* Logout - Provide a utility method for a POST logout */

function logout() {
    fetch("/logout", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
    }).then(response => {
        if (response.ok) {
            location.reload()
            // reloading a protected page will trigger the login view
        }
    });
}


/* Todo Link - Modify object on touch devices */

var todoLinkNav = document.getElementById("todo-logo-nav");
if ((isTouchDevice()) && (todoLinkNav)) {
    todoLinkNav.classList.add("todo-logo-nav-mobile");
    todoLinkNav.href = "#";
    todoLinkNav.addEventListener("click", (e) => {
        if (todoLinkNav.getAttribute("href") == "#") {
            e.preventDefault();
            todoLinkNav.classList.add("mobile-hover");
            todoLinkNav.href = "/now";
        }
    });
    todoLinkNav.addEventListener("blur", (e) => {
        todoLinkNav.href = "#";
        todoLinkNav.classList.remove("mobile-hover");
    });
    window.addEventListener("scroll", (e) => {
        todoLinkNav.href = "#";
        todoLinkNav.classList.remove("mobile-hover");
    });
}


/* Sidebar - Display inset shadow for overflowing content */

var sidebar = document.getElementById("sidebar");
if (sidebar) {
    function displaySidebarShadows() {
        if (window.innerWidth <= 1512) {
            sidebar.classList.remove("shadow-top");
            sidebar.classList.remove("shadow-bottom");
            return;
        }

        if (sidebar.scrollTop != 0) {
            sidebar.classList.add("shadow-top");
        } else {
            sidebar.classList.remove("shadow-top");
        }

        // both top and bottom borders are 1px-wide
        if (sidebar.scrollTop + (sidebar.offsetHeight - 2) < sidebar.scrollHeight) {
            sidebar.classList.add("shadow-bottom");
        } else {
            sidebar.classList.remove("shadow-bottom");
        }
    }

    displaySidebarShadows();
    sidebar.addEventListener("scroll", displaySidebarShadows);
    sidebar.addEventListener("click", displaySidebarShadows);
    window.addEventListener("scroll", displaySidebarShadows);
    window.addEventListener("resize", displaySidebarShadows);
}


/* Overlays - Reveal appropriate overlay through keyboard inputs */

function getSearchInput() {
    return null;

}
function focusOn(overlay) {
    focusField = overlay.querySelector(".focus-on-reveal");
    $(overlay).one("transitionend",
        function() { focusField.focus(); });
}

var codes = {"login": loginForm,
             "logout": true,
             "admin": true }

var activeCode = "";
var cachedCode = "";

function activateOverlayIf(e) {
    var possibleCode = false;
    var codeFound = false;
    for (var key in codes) {
        if (codes.hasOwnProperty(key)) {
            if (key.startsWith(cachedCode)) {
                if ((cachedCode === key) && (codes[key])) {
                    if (!(key == "s") || ((key == "s") && !(possibleCode))) {
                        activeCode = key;
                        codeFound = true;
                    }
                }
                possibleCode = true;
            }
        }
    }
    if (!possibleCode) {
        var latestChar = cachedCode.slice(-1);
        var firstChars = Object.keys(codes).map(c => c.charAt(0));
        if (firstChars.includes(latestChar)) {
            cachedCode = latestChar;
            return activateOverlayIf(e);
        } else {
            cachedCode = "";
            return false;
        }
    } else if (codeFound) {
        cachedCode = "";
        var input = getSearchInput();
        if (activeCode == "s") {
            activeCode = "";
            if (input != null) {
                var searchFocusAfterEsc = ((document.activeElement == input) &&
                                           (!input.parentElement.parentElement.parentElement.classList.contains("expanded")));
                if ((document.activeElement != input) | searchFocusAfterEsc) {
                    e.preventDefault();
                    if (searchFocusAfterEsc) { input.blur(); }
                    input.focus();
                }
            }
        } else {
            if ((input != null) &&
                (document.activeElement == input) &&
                (input.parentElement.parentElement.parentElement.classList.contains("expanded"))) { return }
            if (activeCode == "logout") {
                activeCode = "";
                if (userIsAuthenticated) { logout(); }
            } else if (activeCode == "admin") {
                activeCode = "";
                if (userIsSuperuser) { window.location.href = "/admin"; }
            } else {
                var overlay = codes[activeCode].parentElement;
                overlay.classList.add("revealed");
                e.preventDefault();
                focusOn(overlay);
            }
        }
        return true;
    }
    return false;
}

if (isTouchDevice()) {

    var adminInput = document.getElementById("admin-codes");
    if (adminInput) {
        // wait 1s for critique.js to load with deployAdminInputLogic
        function deployAdminInputLogicDummy() { deployAdminInputLogic() };
        setTimeout(deployAdminInputLogicDummy, 1000);
    }

} else {

    document.addEventListener("keydown", function (e) {
        if (!activeCode) {
            var k = e.keyCode;
            var keyCode = (96 <= k && k <= 105)? k-48 : k;
            cachedCode += String.fromCharCode(keyCode).toLowerCase();
            activateOverlayIf(e);
        }
    });

}

document.addEventListener("keydown", function (e) {
    if (activeCode && (e.keyCode == 27)) {      // ESC keyCode
        codes[activeCode].parentElement.classList.remove("revealed");
        activeCode = "";
        document.activeElement.blur()
    }
});

if (loginForm) {
    loginForm.addEventListener("reset", function (e) {
        e.target.parentElement.classList.remove("revealed");
        activeCode = "";
        document.activeElement.blur()
    });
}


/* Forms - Validate form inputs */

function warningOnElementIf(elem, test) {
    if (test) {
        elem.classList.add("bad-input");
    } else {
        elem.classList.remove("bad-input");
    }
}

function addInputListener(element, atInit) {
    if (atInit) {
        warningOnElementIf(element[0],
                           element[1](element[0].value));
    }
    element[0].addEventListener("blur", function (e) {
        warningOnElementIf(e.target, element[1](e.target.value));});
    element[0].addEventListener("input", function (e) {
        warningOnElementIf(e.target, element[1](e.target.value));});
}

function addInputsListener(validatedElements, atInit) {
    for (i=0; i<validatedElements.length; i++) {
        addInputListener(validatedElements[i], atInit);
    }
}

function addSubmitListener(form, validatedElements) {
    form.addEventListener("submit", function (e) {
        var dataOk = true;
        for (i=0; i<validatedElements.length; i++) {
            if (validatedElements[i][0].classList.contains("bad-input")) {
                dataOk = false;
            }
        };
        if (!dataOk) {
            e.preventDefault();
            // stop the AJAX submit handler in tln.js
            e.stopImmediatePropagation();
        }
    });
}


/* Forms - Improve Select2 dropdowns */

var catchClosingSelect2 = true;     // prevent recursion loop
var catchOpenSelect2 = false;       // restore proper focus
// 1. on first focus, open the menu
$(document).on('focus', '.select2-selection.select2-selection--single', function (e) {
    if (!catchOpenSelect2) {
        $(this).closest(".select2-container").siblings('select:enabled').select2('open');
    }
});
// 2. focus on search field (bugfix for jQuery 3.6)
$(document).on('select2:open', () => {
    document.querySelector('.select2-container--open .select2-search__field').focus();
});
// 3. return focus to the right form input
$(document).on('select2:closing', function (e) {
    if (catchClosingSelect2) {
        e.preventDefault();
        catchClosingSelect2 = false; $(e.target).select2('close'); catchClosingSelect2 = true;
        catchOpenSelect2 = true; e.target.focus(); catchOpenSelect2 = false;
    }
});


/* Pagination - Navigate with arrow keys */

var pagination = document.getElementById("pagination");
if (pagination) {
    document.addEventListener("keydown", function (e) {
        if (getSearchInput() != document.activeElement) {
            if ((e.keyCode == 37) && prevPageUrl && !(activeCode)) {
                window.location.href = prevPageUrl;
            } else if ((e.keyCode == 39) && nextPageUrl && !(activeCode)) {
                window.location.href = nextPageUrl;
            }
        }
    });
}


/* Display zoomable pictures */

var zoomableContainers = document.getElementsByClassName("zoomable-container");
if (zoomableContainers.length > 0) {

    if (isTouchDevice()) {

        for (var i=0; i<zoomableContainers.length; i++) {
            zoomableContainers[i].removeChild(zoomableContainers[i].children[0]);
            zoomableContainers[i].children[0].style.display = "inline-block";
        }

    } else {

        for (var i=0; i<zoomableContainers.length; i++) {
            zoomableContainers[i].removeChild(zoomableContainers[i].children[1]);
        }

        var placeholders = [];

        for (var i=0; i<zoomableContainers.length; i++) {
            var child = zoomableContainers[i].children[0].children[0];
            // either we only display the img
            if (child.tagName == "IMG") { placeholders.push(child); }
            // or we embed it within an anchor element
            else if (child.tagName == "A") { placeholders.push(child.children[0]); }
        }

        function setPhotoPosition(i, coeff) {
            function setPhotoPos(e) {
                var posX = e.offsetX;
                var posY = e.offsetY;
                placeholders[i].style.left = -coeff*posX+"px";
                placeholders[i].style.top = -coeff*posY+"px";
            }
            return setPhotoPos;
        }

        $(document).ready(function() {
            for (i=0; i<placeholders.length; i++) {
                var placeholder = placeholders[i];
                placeholder.setAttribute("src", placeholder.getAttribute("data-src"));
                placeholder.removeAttribute("data-src");
                var coeff = 1;
                if (zoomableContainers[i].hasAttribute("data-zoom-coeff")) {
                    coeff = parseFloat(zoomableContainers[i].getAttribute("data-zoom-coeff"));
                }
                zoomableContainers[i].children[0].addEventListener("mousemove", setPhotoPosition(i, coeff));
            }
        });

    }

}
