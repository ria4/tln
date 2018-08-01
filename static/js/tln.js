var isIE10 = 'behavior' in document.documentElement.style && '-ms-user-select' in document.documentElement.style;
var isIE11 = '-ms-scroll-limit' in document.documentElement.style && '-ms-ime-align' in document.documentElement.style;


/* Top Navigation - Deactivate hoverable photos link for touchscreens */

function isTouchDevice() {
    return "ontouchstart" in window || navigator.maxTouchPoints;
}

var topNavPhotoButton = document.getElementById("photos-dropdown-link");
topNavPhotoButton.addEventListener("click", function (e) {
    if (isTouchDevice()) {
        e.preventDefault();
    }
});


/* Top Navigation - Enable tab navigation with photos dropdown menu */

var photosDropdownMenu = document.getElementById("photos-dropdown-menu");

topNavPhotoButton.addEventListener("focus", function () {
    photosDropdownMenu.classList.add("expanded");
});

function collapseDropdownMenu () {
    if (!photosDropdownMenu.contains(document.activeElement)) {
        photosDropdownMenu.classList.remove("expanded");
    }
}

document.addEventListener("click", collapseDropdownMenu)
document.addEventListener("focusin", collapseDropdownMenu)


/* Overlays - Reveal appropriate overlay through keyboard inputs */

function getSearchInput() {
    return null;
}

var loginForm = document.getElementById("login_form");
var codes = {"login": loginForm,
             "logout": true,
             "s": true }

var activeCode = "";
var cachedCode = "";
document.addEventListener("keypress", function (e) {
    if (!activeCode) {
        cachedCode += String.fromCharCode(e.charCode);
        var possibleCode = false;
        var codeFound = false;
        for (var key in codes) {
            if (codes.hasOwnProperty(key)) {
                if (key.startsWith(cachedCode)) {
                    possibleCode = true;
                    if ((cachedCode === key) && (codes[key])) {
                        activeCode = key;
                        codeFound = true;
                    }
                }
            }
        }
        if (!possibleCode) {
            cachedCode = "";
        } else if (codeFound) {
            cachedCode = "";
            if (activeCode == "logout") {
                activeCode = "";
                if (userIsAuthenticated) { window.location.href = "/logout"; }
            } else if (activeCode == "s") {
                activeCode = "";
                if (document.activeElement != getSearchInput()) {
                    e.preventDefault();
                    var input = getSearchInput();
                    if (input != null) {
                        input.focus();
                    }
                }
            } else {
                var overlay = codes[activeCode].parentElement;
                overlay.classList.add("revealed");
                if (activeCode == "login") {
                    e.preventDefault();
                    nameInput = document.getElementById("id_username");
                    $(overlay).one("transitionend",
                        function() { nameInput.focus(); });
                } else if (activeCode == "adds") {
                    e.preventDefault();
                    cinemaInput = document.getElementById("id_empty_seance_cinema");
                    $(overlay).one("transitionend",
                        function() { cinemaInput.focus(); });
                }
            }
        }
    }
});

document.addEventListener("keydown", function (e) {
    /* there is no keypress event for ESC */
    if (activeCode && (e.keyCode == 27)) {
        codes[activeCode].parentElement.classList.remove("revealed");
        activeCode = "";
    }
});

if (loginForm) {
    loginForm.addEventListener("reset", function (e) {
        e.target.parentElement.classList.remove("revealed");
        activeCode = "";
    });
}

/* Pagination - Navigate with arrow keys */

var pagination = document.getElementById("pagination");
if (pagination) {
    document.addEventListener("keydown", function (e) {
        if ((e.keyCode == 37) && prevPageUrl && !(activeCode)) {
            window.location.href = prevPageUrl;
        } else if ((e.keyCode == 39) && nextPageUrl && !(activeCode)) {
            window.location.href = nextPageUrl;
        }
    });
}


/* Apps logic */

var websiteApp = location.pathname.split("/")[1];


if (websiteApp == "") {

    /* Homepage - Smooth scroll to info anchor */

    $('a[href^="#"]').click( function (event) {
        event.preventDefault();
        var href = $.attr(this, 'href');
        $('html, body').animate({
            scrollTop: $(href).offset().top
        }, 500, function () { window.location.hash = href; });
    });

}


if (websiteApp == "critique") {


    /* Critique Skip-to-main Link - Avoid header covering content */

    var skipLink = document.getElementById("skip-link");
    skipLink.addEventListener("click", function(e) {
        e.preventDefault();
        document.getElementById("content").focus();
        window.scrollTo(0, 0);
    });


    /* Critique Navigation Bars - Hide/reveal and resize bars */

    var topNavBar = document.getElementById("top-nav-h");
    var topNavTrigger = document.getElementById("top-nav-trigger");
    var mainNavBar = document.getElementById("main-nav");
    var subNavTrigger = document.getElementById("sub-nav-trigger");
    var subNavBar = document.getElementById("sub-nav");
    var mainNavLinksH = document.getElementById("main-nav-links-h");
    var mainNavLinksV = document.getElementById("main-nav-links-v");
    var subNavLinksV = document.getElementById("sub-nav-links-v");

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
    var widthTriggerCritiqueNavLayout = 1210;
    var widthTriggerTopTextesPosition = 880;
    var topTextesMain = mainNavLinksV.getElementsByClassName("top-textes")[0];
    var topTextesSub = subNavLinksV.getElementsByClassName("top-textes")[0];
    function setTopTextesPosition() {
        if (window.innerWidth < widthTriggerCritiqueNavLayout) {
            if (window.innerWidth < widthTriggerTopTextesPosition) {
                topTextesMain.style.display = "none";
                topTextesSub.style.display = "list-item";
            } else {
                topTextesMain.style.display = "list-item";
                topTextesSub.style.display = "none";
            }
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
    subNavLinksV.addEventListener("click", function (e) {
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
    var critiqueSearchImg = critiqueSearchButton.getElementsByTagName("img")[0];
    var critiqueSearchEndButton = document.getElementById("critique-searchend-button");
    var critiqueSearchEndImg = critiqueSearchEndButton.getElementsByTagName("img")[0];
    var critiqueSearchM = document.getElementById("critique-search-m");
    var critiqueSearchEndButtonM = document.getElementById("critique-searchend-button-m");
    var critiqueSearchEndImgM = critiqueSearchEndButtonM.getElementsByTagName("img")[0];

    var searchInput = document.getElementById("critique-search-input");
    var searchInputM = document.getElementById("critique-search-input-m");
    var searchResults = document.getElementById("critique-search-results");
    var searchResultsList = document.getElementById("critique-search-results-list");
    var widthTriggerMobileSearch = 700;
    getSearchInput = function() {
        if (window.innerWidth > widthTriggerMobileSearch) {
            return searchInput;
        } else {
            return searchInputM;
        }
    }

    function hideSearchInput() {
        subNavTrigger.classList.remove("reduced");
        searchInput.classList.remove("expanded");
        searchInput.value = "";
        while (searchResultsList.lastChild) {
            searchResultsList.removeChild(searchResultsList.lastChild);
        }
        critiqueSearchEndButton.style.zIndex = "-1";
        critiqueSearchEndImg.style.opacity = "0";
        critiqueSearchButton.style.zIndex = "1";
        critiqueSearchImg.style.opacity = "1";
    }

    critiqueSearchButton.addEventListener("click", function (e) {
        getSearchInput().focus();
    });
    critiqueSearchEndButton.addEventListener("click", function (e) {
        hideSearchInput();
    });
    critiqueSearchEndButtonM.addEventListener("click", function (e) {
        critiqueSearchM.classList.remove("expanded");
        critiqueSearchButton.style.zIndex = "1";
        critiqueSearchImg.style.opacity = "1";
    });

    var searchInputMBlurred = false;
    searchInput.addEventListener("focus", function (e) {
        if (getSearchInput() === searchInputM) {
            if (!searchInputMBlurred) {
                searchInputM.focus();
            } else {
                searchInputMBlurred = false;
            }
        } else {
            subNavTrigger.classList.add("reduced");
            searchInput.classList.add("expanded");
            critiqueSearchButton.style.zIndex = "-1";
            critiqueSearchImg.style.opacity = "0";
            critiqueSearchEndButton.style.zIndex = "1";
            critiqueSearchEndImg.style.opacity = "1";
            searchResults.style.display = "block";
        }
    });
    searchInputM.addEventListener("focus", function (e) {
        critiqueSearchM.classList.add("expanded");
        critiqueSearchButton.style.zIndex = "-1";
        critiqueSearchImg.style.opacity = "0";
    });
    searchInputM.addEventListener("blur", function (e) {
        critiqueSearchM.classList.remove("expanded");
        critiqueSearchButton.style.zIndex = "1";
        critiqueSearchImg.style.opacity = "1";
        searchInputMBlurred = true;
        searchInput.focus();
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth < widthTriggerMobileSearch) {
            hideSearchInput();
        }
    });
    document.addEventListener("click", function () {
        if (!critiqueSearch.contains(document.activeElement)) {
            searchResults.style.display = "none";
        }
    });


    /* Critique Search Bar - AJAX Search */

    function createElementSearchResult() {
        var li = document.createElement("li");
        var a = document.createElement("a"); li.appendChild(a);
        var p0 = document.createElement("p"); a.appendChild(p0);
        var div = document.createElement("div"); a.appendChild(div);
        var p1 = document.createElement("p"); div.appendChild(p1);
        var p2 = document.createElement("p"); div.appendChild(p2);
        return li
    }

    function setElementSearchResult(li, oeuvre) {
        var a = li.firstChild;
        a.setAttribute("href", "/critique/oeuvre/" + oeuvre.slug);
        var p0 = a.firstChild;
        p0.innerHTML = oeuvre.info.titles.vf;
        var div = a.lastChild; var p1 = div.firstChild; var p2 = div.lastChild;
        if (oeuvre.info.titles.vo) {
            p1.innerHTML = oeuvre.info.titles.vo;
        } else {
            p1.innerHTML = "";
        }
        p2.innerHTML = "(" + oeuvre.info.year + ")";

        a.addEventListener("mouseenter", function (e) {
            e.target.focus();
        });
    }

    var currentSearchRequest = new XMLHttpRequest();
    searchInput.addEventListener("input", function (e) {
        if (e.target.value.length > 2) {
            currentSearchRequest.abort();
            var request = new XMLHttpRequest();
            request.open("GET", "/critique/search/" + e.target.value, true);
            request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            request.onreadystatechange = function() {
                if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
                    var response = JSON.parse(request.responseText);

                    var diff = response.length - searchResultsList.children.length;
                    if (diff > 0) {
                        for (var i=0; i<diff; i++) {
                            searchResultsList.appendChild(createElementSearchResult());
                        }
                    } else if (diff < 0) {
                        for (var i=diff; i<0; i++) {
                            searchResultsList.removeChild(searchResultsList.lastChild);
                        }
                    }

                    for (var i=0; i<response.length; i++) {
                        var li = searchResultsList.children[i];
                        setElementSearchResult(li, response[i]);
                    }
                }
            }
            currentSearchRequest = request;
            request.send();
        } else {
            while (searchResultsList.lastChild) {
                searchResultsList.removeChild(searchResultsList.lastChild);
            }
        }
    });


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


    /* Critique Layout - Display objects by chunks */

    var textDecoder = document.createElement("textarea");
    function decodeHtml(html) {
        textDecoder.innerHTML = html;
        return textDecoder.value;
    }

    function fillChunksBy(container, collection, chunkSize, wholeLinks) {
        for (i=0; i<collection.length/chunkSize; i++) {
            var ul = document.createElement("ul");
            container.appendChild(ul);
            for (j=0; j<chunkSize; j++) {
                if (collection[chunkSize*i+j]) {
                    var li = document.createElement("li");
                    if (wholeLinks) {
                        var a = document.createElement("a");
                        var text = decodeHtml(collection[chunkSize*i+j][0]);
                        var textNode = document.createTextNode(text);
                        a.href = collection[chunkSize*i+j][1];
                        a.appendChild(textNode);
                        li.appendChild(a);
                    } else {
                        var text = decodeHtml(collection[chunkSize*i+j]);
                        li.innerHTML = text;
                    }
                    ul.appendChild(li);
                }
            }
        }
    }

    var collection = document.getElementById("collection");
    if (collection) { fillChunksBy(collection, oeuvres, 25, true); }
    var cinemas = document.getElementById("cinemas");
    if (cinemas) { fillChunksBy(cinemas, cines, 21, true); }
    var seancesDisplay = document.getElementById("seances");
    if (seancesDisplay) { fillChunksBy(seancesDisplay, seances, 25, false); }


} else if (websiteApp == "blog") {


    /* Blog Side Menu - On an entry page, lower opacity when scrolling down */

    if (document.body.classList.contains("entry")) {
        var header = document.getElementById("header");
        var sidebar = document.getElementById("sidebar");
        window.addEventListener("scroll", function() {
            if (sidebar.contains(document.activeElement) ||
                header.contains(document.activeElement)) {
            // keep full opacity when tab-navigating the sidebar or top menu
                sidebar.classList.remove("semihidden");
            } else {
                if (window.scrollY == 0) {
                    sidebar.classList.remove("semihidden");
                } else {
                    sidebar.classList.add("semihidden");
                }
            }
        });
    }


    /* Blog Archive Widget - Expand/Collapse entries */

    var widgetArchives = document.getElementById("widget-archives");

    function addToggleListener(toggle) {
        toggle.addEventListener("click", function(e) {
            e.preventDefault();
            if (toggle.classList.contains("expanded")) {
                toggle.classList.add("collapsed");
                toggle.classList.remove("expanded");
            } else {
                toggle.classList.add("expanded");
                toggle.classList.remove("collapsed");
            }
        });
    }

    toggles = widgetArchives.getElementsByClassName("toggle");
    [].forEach.call(toggles, addToggleListener);


    /* Blog Comment */

    var widthTriggerBlogSidebar = 1512;
    var commentForm = document.getElementById("comment_form_custom");
    if (commentForm) {

        /* Blog Comment - Reveal comment form */

        var commentFormTrigger = document.getElementById("comment-form-trigger");
        var commentFormTriggerImg = commentFormTrigger.getElementsByTagName("img")[0];
        commentFormTrigger.addEventListener("mouseover", function (e) {
            commentFormTriggerImg.setAttribute("src", "/static/blog/icon_comment_link_hover.png");
        });
        commentFormTrigger.addEventListener("mouseout", function (e) {
            commentFormTriggerImg.setAttribute("src", "/static/blog/icon_comment_link.png");
        });

        var duration;
        var delay = 20;
        function scrollToBottomWhileHeightChanges() {
            if (duration > 0) {
                window.scrollTo(0, document.body.scrollHeight);
                duration = duration - delay;
                setTimeout(scrollToBottomWhileHeightChanges, delay);
            }
        }

        /* Using a hardcoded time seems better than parsing CSS multi-transitionDuration */
        var commentFormTransitionTime = 600;
        commentForm.classList.add("collapsed");
        commentFormTrigger.addEventListener("click", function (e) {
            e.preventDefault();
            if (commentForm.classList.contains("expanded")) {
                commentForm.classList.add("collapsed");
                commentForm.classList.remove("expanded");
            } else {
                commentForm.classList.add("expanded");
                commentForm.classList.remove("collapsed");
                if (window.innerWidth > widthTriggerBlogSidebar) {
                    /* Stick the viewport to the bottom of the document */
                    duration = commentFormTransitionTime;
                    scrollToBottomWhileHeightChanges();
                }
            }
        });

        /* Blog Comment - Warn IE10 users (loader won't appear) */

        submitButton = commentForm.getElementsByClassName("submit-post")[0];
        if (isIE10) {
            submitButton.value = "envoyer (le message sera en attente de modération)";
        }

        /* Blog Comment - Auto-scroll to the bottom of the window

        /* There is no textarea resize event, hence we need this hackish part
         * to auto-scroll when resizing the text area (horizontal layout only). */

        function scrollToBottom(e) {
            if ((window.innerHeight - event.clientY) < 50) {
                window.scrollTo(0, document.body.scrollHeight);
            }
        }

        var commentFormTextarea = commentForm.getElementsByTagName("textarea")[0];
        var posInfo = commentFormTextarea.getBoundingClientRect()
        commentFormTextarea.addEventListener("mousedown", function (e) {
            if (window.innerWidth >= widthTriggerBlogSidebar) {
                if (((posInfo.height - (e.pageY - this.offsetTop)) < 17) &&
                    ((posInfo.width - (e.pageX - this.offsetLeft)) < 17)) {
                    document.body.addEventListener("mousemove", scrollToBottom);
                }
            }
        });
        document.body.addEventListener("mouseup", function (e) {
            document.body.removeEventListener("mousemove", scrollToBottom);
        });

        /* Blog Comment - AJAX request */

        var currentlySubmitting = false;
        var commentFormWrap = document.getElementById("comment-form-wrap");
        var commentFormMain = document.getElementById("comment-form-main");
        var commentPostLoader = document.getElementById("comment-post-loader");
        var commentPostResult = document.getElementById("comment-post-result");
        var commentPostResultText = commentPostResult.getElementsByTagName("p")[0];
        var timeoutCleanForm;

        commentFormWrap.addEventListener("click", function (e) {
            if (!currentlySubmitting) {
                clearTimeout(timeoutCleanForm);
                commentFormMain.classList.remove("waiting");
                commentPostResult.style.display = "none";
            }
        });

        commentForm.addEventListener("submit", function (e) {
            e.preventDefault();
            commentFormMain.classList.add("waiting");
            commentPostLoader.style.display = "block";

            if (!currentlySubmitting) {
                currentlySubmitting = true;
                var request = new XMLHttpRequest();
                request.open("POST", "/blog/comments/post/", true);
                request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");

                function cleanCommentFormSuccess() {
                    commentPostResult.style.display = "none";
                    commentForm.classList.add("collapsed");
                    commentForm.classList.remove("expanded");
                    setTimeout(function () { commentFormMain.classList.remove("waiting"); }, 500);
                }

                request.onreadystatechange = function() {
                    /* allow to remove waiting screen after some time */
                    setTimeout(function() { currentlySubmitting = false; }, 2000);
                    commentPostLoader.style.display = "none";
                    if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
                        res = JSON.parse(request.responseText);
                        var postCommentSuccess = res["post_comment_success"];
                        if (postCommentSuccess) {
                            if (userIsAuthenticated) {
                                window.location.reload(false);
                            } else {
                            commentPostResultText.innerHTML = "Merci ! Votre commentaire sera publié après modération.";
                            timeoutCleanForm = setTimeout(cleanCommentFormSuccess, 6000);
                            }
                        } else {
                            commentPostResultText.innerHTML = "Une erreur est survenue. Merci de réessayer plus tard.<br/>(et désolée pour le dérangement)";
                        }
                    } else {
                        commentPostResultText.innerHTML = "Une erreur est survenue. Merci de réessayer plus tard.<br/>(et désolée pour le dérangement)";
                    }
                    commentPostResult.style.display = "flex";
                }

                // ?? I can't find a way to build the x-www-form-urlencoded string
                // from the form data. And we can't use FormData because it would mess
                // with django's post_comment method. I guess I shall do it myself,
                // except it may break if the form changes...
                var urlEncodedData = "";
                var urlEncodedDataPairs = [];
                var inputs = commentForm.getElementsByTagName("input");
                for (var i=0; i<inputs.length; i++) {
                    var input = inputs[i];
                    name = input.getAttribute('name');
                    value = '';
                    if (name == "name") {
                        if (input.value != null) { value = input.value; }
                        else if (input.getAttribute('value') != null) {
                            /* authenticated user only */
                            value = input.getAttribute('value'); }
                    } else if ((name == "email") || (name == "honeypot")) {
                        if (input.value != null) { value = input.value; }
                    } else {
                        if (input.value != null) { value = input.getAttribute('value'); }
                    }
                    urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(value));
                }
                var commentInput = commentForm.getElementsByTagName("textarea")[0];
                urlEncodedDataPairs.push(encodeURIComponent(commentInput.getAttribute('name'))
                    + '=' + encodeURIComponent(commentInput.value));
                urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

                request.send(urlEncodedData);
            }
        });
    }


} else if (websiteApp == "photos") {


    /* Photos Display - Shrink-wrap container */

    var galleryPhotos = document.getElementById("gallery-photos");
    var deltaMargin = 2*parseInt(window.getComputedStyle(galleryPhotos).marginLeft, 10);
    var deltaPadding = 2*(1+parseInt(window.getComputedStyle(galleryPhotos).paddingLeft, 10));    // border should be 1px wide
    var photoDisplay = galleryPhotos.getElementsByClassName("photo-display")[0];
    var itemWidth = parseInt(window.getComputedStyle(photoDisplay).width, 10) + 2*parseInt(window.getComputedStyle(photoDisplay).marginLeft, 10);
    var contentMaxWidth = parseInt(window.getComputedStyle(document.getElementById("content")).maxWidth, 10);

    function setGalleryWidth() {
        var width = Math.min(contentMaxWidth, window.innerWidth - deltaMargin);
        var q = Math.floor((width - deltaMargin - deltaPadding)/itemWidth);     // number of photos on a single line
        galleryPhotos.style.width = q*itemWidth + deltaPadding + "px";
    }

    setGalleryWidth();
    window.addEventListener("resize", setGalleryWidth);


    /* Photos Display - Flexslider overlay */

    var gallerySlider = document.getElementById("gallery-slider");
    var slider;
    var animationSpeed;

    var overlaySlider = gallerySlider.parentNode;
    var photoLinks = document.getElementsByClassName("photo-link");
    var photos = gallerySlider.getElementsByTagName("img");

    function addSliderStartListener(item) {
        item.addEventListener("click", function (e) {
            e.preventDefault();
            slider.vars.animationSpeed = 0;
            slider.flexAnimate(parseInt(item.getAttribute("data-onclick"), 10));
            slider.vars.animationSpeed = animationSpeed;
            overlaySlider.classList.add("revealed");
        });
    }

    for (var i=0; i<photoLinks.length; i++) {
        addSliderStartListener(photoLinks[i]);
    }

    // hide overlaySlider if click outside photo & arrows
    document.addEventListener("keydown", function (e) {
        if (e.keyCode == 27) {
            overlaySlider.classList.remove("revealed");
        }
    });

    $(document).ready(function() {
        $('#gallery-slider').flexslider({
            slideshow: false,
            animationSpeed: 600,
            controlNav: false,
            directionNav: false,
        });
        slider = $("#gallery-slider").data("flexslider");
        animationSpeed = slider.vars.animationSpeed;
    });


    /* Click outside the image to hide the slider. */

    overlaySlider.addEventListener("click", function() {
        overlaySlider.classList.remove("revealed");
    });
    for (var i=0; i<photos.length; i++) {
        photos[i].addEventListener("click", function(e) {
            e.stopPropagation();
        });
    }


    /* Chrome stays focused on the link after a click, which provokes autoslide.
     * That's why we use manual control for this action. */

    $(".flex-nav-prev").on('click', function() {
        $("#gallery-slider").flexslider('prev');
        return false;
    });
    $(".flex-nav-next").on('click', function() {
        $("#gallery-slider").flexslider('next');
        return false;
    });


    /* We need to set the height for the img container explicitly.
     * Indeed we cannot rely on max-width or object-fit tools, because we want the image
     * to fill as much height/width as possible depending on its ratio, yet preparing
     * the image container with a maximal height repels the caption at the bottom... */

    var maxSlideWidth = gallerySlider.clientWidth;
    var slidesInfoHeight = document.getElementsByClassName("slide-info")[0].clientHeight;
    var maxSlideHeight = gallerySlider.clientHeight - slidesInfoHeight;
    var ratioRef = 1.0 * maxSlideWidth / maxSlideHeight;

    /* this is supposed to be fired before the listeners from addPhotoResizeListener */
    window.addEventListener("resize", function() {
        maxSlideWidth = parseInt(window.getComputedStyle(gallerySlider).width, 10);
        maxSlideHeight = parseInt(window.getComputedStyle(gallerySlider).height, 10) - slidesInfoHeight;
        ratioRef = 1.0 * maxSlideWidth / maxSlideHeight;
    });

    function setPhotoSize(photo) {
        var ratioReal = 1.0 * photo.naturalWidth / photo.naturalHeight;
        if (ratioReal > ratioRef) {
            photo.style.width = Math.min(maxSlideWidth, photo.naturalWidth) + "px";
            photo.style.height = "auto";
        } else {
            photo.style.height = Math.min(maxSlideHeight, photo.naturalHeight) + "px";
            photo.style.width = "auto";
        }
    }

    function addPhotoResizeListener(photo) {
        window.addEventListener("resize", function() {
            setPhotoSize(photo);
        });
    }

    for (var i=0; i<photos.length; i++) {
        var photo = photos[i];
        photo.onload = function() { setPhotoSize(this); }
        if ((photo.complete && (photo.naturalWidth !== 0)) || isIE10) {
            /* the image has already been loaded so onload event won't be fired */
            setPhotoSize(photo);
        }
        addPhotoResizeListener(photo);
    }

}
