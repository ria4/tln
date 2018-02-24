/* Layout - Toggle between horizontal and vertical style */

function setLayout(element, widthTrigger) {
    function setElementLayout() {
        if (window.innerWidth < widthTrigger) {
            element.setAttribute("layout", "v");
        } else {
            element.setAttribute("layout", "h");
        }
    }
    return setElementLayout;
}


/* Top Navigation - Navigation bar layout depends on window width */

var widthTriggerTopNavLayout = 900;
var topNavBar = document.getElementById("top-nav");
if (topNavBar) {
    var setTopNavLayout = setLayout(topNavBar, widthTriggerTopNavLayout);
    setTopNavLayout();
    window.addEventListener("resize", setTopNavLayout);
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
        }
    });
}


/* Overlays - Reveal appropriate overlay through keyboard inputs */

var loginForm = document.getElementById("login_form");
var codes = {"login": loginForm,
             "logout": true}

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

if (websiteApp == "critique") {


    /* Main Navigation Bars - Hide/reveal and resize bars */

    var mainNavBar = document.getElementById("main-nav");
    var subNavBar = document.getElementById("sub-nav");
    var mainNavLinksH = document.getElementById("main-nav-links-h");
    var mainNavLinksV = document.getElementById("main-nav-links-v");
    var subNavLinksH = document.getElementById("sub-nav-links-h");
    var subNavLinksV = document.getElementById("sub-nav-links-v");

    /* Reveal the topNavBar on clicking the utmost left link */
    var topNavTrigger = document.getElementById("top-nav-trigger");
    topNavTrigger.addEventListener("click", function(e) {
        e.preventDefault();
        topNavBar.classList.toggle("expanded");
    });

    /* Reveal the subNavBar on clicking the utmost right link */
    var subNavBarTrigger = document.getElementById("sub-nav-trigger");
    subNavBarTrigger.addEventListener("click", function(e) {
        e.preventDefault();
        subNavBar.classList.toggle("expanded");
    });

    /* Tag and show/extend the right boxes according to the window width */
    var critiqueNavBar = document.getElementById("critique-header");
    var widthTriggerCritiqueNavLayout = 960;
    var setCritiqueNavLayout = setLayout(critiqueNavBar, widthTriggerCritiqueNavLayout);
    var widthTriggerSubNavLayout = 1104;
    var setSubNavHLayout = setLayout(subNavLinksH, widthTriggerSubNavLayout);
    setCritiqueNavLayout(); setSubNavHLayout();
    window.addEventListener("resize", function(e) {
        setCritiqueNavLayout(); setSubNavHLayout();
    });

    /* Hide menus after scrolling down */
    var lastKnownScrollPosition = 0;
    var ticking = false;
    window.addEventListener("scroll", function() {
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

    /* Hide menus after clicking outside the menus */
    var content = document.getElementById("content");
    content.addEventListener("click", function () {
        topNavBar.classList.remove("expanded");
        subNavBar.classList.remove("expanded");
    });

    /* Hide menus after clicking on the transparent part of the subNavBar */
    subNavLinksV.addEventListener("click", function (e) {
        e.stopPropagation();
    });
    subNavBar.addEventListener("click", function () {
        if (subNavBar.classList.contains("v")) {
            topNavBar.classList.remove("expanded");
            subNavBar.classList.remove("expanded");
        }
    });


    /* Filter Bar - Highlight selected media type or year */

    var filterBar = document.getElementById("media-bar");
    if (filterBar) {
        var hrefs = window.location.href.split('/');
        var mtype = hrefs[hrefs.length - 1];
        if (!isNaN(parseInt(mtype.charAt(0)))) {
            mtype = hrefs[hrefs.length - 2];
        }
        links = filterBar.getElementsByTagName("li");
        for (var i=0; i<links.length; i++) {
            link = links[i].getElementsByTagName("a")[0]
            if (link.getAttribute("desc") == mtype) {
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

    var chunkSizeCollection = 25;
    var collection = document.getElementById("collection");
    if (collection) {
        for (i=0; i<oeuvres.length/chunkSizeCollection; i++) {
            var ul = document.createElement("ul");
            collection.appendChild(ul);
            for (j=0; j<chunkSizeCollection; j++) {
                if (oeuvres[chunkSizeCollection*i+j]) {
                    var a = document.createElement("a");
                    var text = decodeHtml(oeuvres[chunkSizeCollection*i+j][0]);
                    var textNode = document.createTextNode(text);
                    a.href = oeuvres[chunkSizeCollection*i+j][1];
                    a.appendChild(textNode);
                    var li = document.createElement("li");
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            }
        }
    }

    var chunkSizeSeances = 25;
    var seancesDisplay = document.getElementById("seances");
    if (seancesDisplay) {
        for (i=0; i<seances.length/chunkSizeSeances; i++) {
            var ul = document.createElement("ul");
            seancesDisplay.appendChild(ul);
            for (j=0; j<chunkSizeSeances; j++) {
                if (seances[chunkSizeSeances*i+j]) {
                    var li = document.createElement("li");
                    var text = decodeHtml(seances[chunkSizeSeances*i+j]);
                    li.innerHTML = text;
                    ul.appendChild(li);
                }
            }
        }
    }

    var chunkSizeCinemas = 21;
    var cinemas = document.getElementById("cinemas");
    if (cinemas) {
        for (i=0; i<cines.length/chunkSizeCinemas; i++) {
            var ul = document.createElement("ul");
            cinemas.appendChild(ul);
            for (j=0; j<chunkSizeCinemas; j++) {
                if (cines[chunkSizeCinemas*i+j]) {
                    var a = document.createElement("a");
                    var text = decodeHtml(cines[chunkSizeCinemas*i+j][0]);
                    var textNode = document.createTextNode(text);
                    a.href = cines[chunkSizeCinemas*i+j][1];
                    a.appendChild(textNode);
                    var li = document.createElement("li");
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            }
        }
    }


    /* Critique Update - Forms validation */

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
            [imdbId, x => !x.match(/^tt\d{7}$|^$/)]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(oeuvreFormEmpty, validatedElements);
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
            [imdbId, x => !x.match(/^tt\d{7}$|^$/)]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(oeuvreForm, validatedElements);
    }

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

    var cinemaForm = document.getElementById("cinema_form");
    if (cinemaForm) {
        nameInput = document.getElementById("id_name");
        comment = document.getElementById("id_comment");
        visited = document.getElementById("id_visited");
        validatedElements = [
            [nameInput, x => (x == "")],
            [comment, x => (x == "")],
            [visited, x => (x == "")]
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
            [cinema, x => ((x.length > 1000) || (x == ""))],
            [date, x => (x == "")],
            [hour, x => ((x.length != 5) || (x.charAt(2) != ":") || (parseInt(x.charAt(0), 10) > 2) || (parseInt(x.charAt(3), 10) > 5))],
        ];
        addInputsListener(validatedElements, true);

        /* exactly one of these must be filled */
        filmSlug = document.getElementById("id_empty_seance_film_slug");
        seanceTitle = document.getElementById("id_empty_seance_seance_title");

        validatedElementsComplete = validatedElements.slice()
        validatedElementsComplete.push([filmSlug, null]);
        validatedElementsComplete.push([seanceTitle, null]);
        addSubmitListener(seanceFormEmpty, validatedElementsComplete);

        warningOnElementIf(filmSlug, true);
        warningOnElementIf(seanceTitle, true);
        filmSlug.addEventListener("blur", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
        seanceTitle.addEventListener("blur", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
        filmSlug.addEventListener("input", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
        seanceTitle.addEventListener("input", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
    }

    codes["edito"] = oeuvreForm;
    codes["addo"] = oeuvreFormEmpty;
    codes["editc"] = commentForm;
    codes["addc"] = commentFormEmpty;
    codes["editi"] = cinemaForm;
    codes["adds"] = seanceFormEmpty;


} else if (websiteApp == "blog") {


    /* Blog Layout - Sidebar position depends on window width */

    var widthTriggerBlogSidebar = 1600;
    var body = document.getElementsByTagName("body")[0];
    var setBlogLayout = setLayout(body, widthTriggerBlogSidebar);
    setBlogLayout();
    window.addEventListener("resize", setBlogLayout);


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

        commentForm.classList.add("collapsed");
        commentFormTrigger.addEventListener("click", function (e) {
            e.preventDefault();
            if (commentForm.classList.contains("expanded")) {
                commentForm.classList.add("collapsed");
                commentForm.classList.remove("expanded");
            } else {
                commentForm.classList.add("expanded");
                commentForm.classList.remove("collapsed");
            }
        });

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

        /* Blog Comment - Form validation */

        username = document.getElementById("id_name");
        email = document.getElementById("id_email");
        comment = document.getElementById("id_comment");
        validatedElements = [
            [username, x => (x == "")],
            [comment, x => (x == "")]
        ];
        addInputsListener(validatedElements, false);
        addSubmitListener(commentForm, validatedElements);

        function validateEmail(x) {
            return ((x.length > 0) &&
                    ((x[x.length-2] == ".") || (x.indexOf(".") == -1) || (x.indexOf("@") == -1)))
        }
        var triedEmail = false;
        email.addEventListener("blur", function (e) {
            warningOnElementIf(e.target, validateEmail(e.target.value));
            if (e.target.value.length > 0) {triedEmail = true;}});
        email.addEventListener("input", function (e) {
            if (triedEmail) {
                warningOnElementIf(e.target, validateEmail(e.target.value));
            }
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


    var hseparators = document.getElementsByClassName("hseparator");

    function setHseparatorOverflow(item) {
        var container = item.parentNode;
        var maxWiw = parseInt(window.getComputedStyle(container).width, 10)
                        - parseInt(window.getComputedStyle(item).marginLeft, 10)
                        - parseInt(window.getComputedStyle(item).marginRight, 10);
        if (window.innerWidth < maxWiw) {
            container.style.overflow = "hidden";
        } else {
            container.style.overflow = "inherit";
        }
    }

    function addResizeListener(item) {
        window.addEventListener("resize", function () { setHseparatorOverflow(item); });
    }

    for (var i=0; i<hseparators.length; i++) {
        setHseparatorOverflow(hseparators[i]);
        addResizeListener(hseparators[i]);
    }


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
        if (photo.complete && (photo.naturalWidth !== 0)) {
            /* the image has already been loaded so onload event won't be fired */
            setPhotoSize(photo);
        }
        addPhotoResizeListener(photo);
    }
}


/* Global Forms - Define reset listeners once all codes have been registered */

for (var key in codes) {
    if (codes.hasOwnProperty(key)) {
        if ((key != "logout") && (codes[key])) {
            codes[key].addEventListener("reset", function (e) {
                e.target.parentElement.classList.remove("revealed");
                activeCode = "";
            });
        }
    }
}
