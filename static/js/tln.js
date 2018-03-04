var isIE10 = 'behavior' in document.documentElement.style && '-ms-user-select' in document.documentElement.style;


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


    /* Critique Navigation Bars - Hide/reveal and resize bars */

    var topNavBar = document.getElementById("top-nav-h");
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

    /* Place the top texts link according to window width */
    var widthTriggerCritiqueNavLayout = 960;
    var widthTriggerTopTextesPosition = 600;
    function setTopTextesPosition() {
        if (window.innerWidth < widthTriggerCritiqueNavLayout) {
            if (window.innerWidth < widthTriggerTopTextesPosition) {
                if (mainNavLinksV.children.length > 0) {
                    var topTextesLink = mainNavLinksV.children[0];
                    var oldTopTextesLink = mainNavLinksV.removeChild(topTextesLink);
                    subNavLinksV.insertBefore(oldTopTextesLink, subNavLinksV.children[1]);
                }
            } else {
                if (mainNavLinksV.children.length == 0) {
                    var topTextesLink = subNavLinksV.children[1];
                    var oldTopTextesLink = subNavLinksV.removeChild(topTextesLink);
                    mainNavLinksV.append(oldTopTextesLink);
                }
            }
        }
    }
    setTopTextesPosition();
    window.addEventListener("resize", setTopTextesPosition);

    /* Hide menus when scrolling down */
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
