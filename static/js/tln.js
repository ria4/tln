/* Critique Navigation Bars - Hide/Reveal and Resize bars */

var widthTriggerTopNav = 900;
var topNavigation = document.getElementById("top-navigation");
var topNavigationTrigger = document.getElementById("top-navigation-trigger");
if (topNavigationTrigger) {
    var erranceBarTrigger = document.getElementById("errance-bar-trigger");
    var erranceBar = document.getElementById("errance-bar");

    topNavigationTrigger.addEventListener("click", function(e) {
        e.preventDefault();
        if (topNavigation.classList.contains("expanded")) {
            topNavigation.classList.remove("expanded");
        } else {
            topNavigation.classList.add("expanded");
        }

        if (window.innerWidth < widthTriggerTopNav) {
            topNavigation.setAttribute("expanded-size", "double");
        } else {
            topNavigation.setAttribute("expanded-size", "simple");
        }
    });

    var widthTriggerErrance = 1104;
    erranceBarTrigger.addEventListener("click", function(e) {
        e.preventDefault();
        if (erranceBar.classList.contains("expanded")) {
            erranceBar.classList.remove("expanded");
        } else {
            erranceBar.classList.add("expanded");
        }

        if (window.innerWidth < widthTriggerErrance) {
            erranceBar.setAttribute("expanded-size", "double");
        } else {
            erranceBar.setAttribute("expanded-size", "simple");
        }
    });

    window.addEventListener("resize", function(e) {
        if (window.innerWidth < widthTriggerTopNav) {
            topNavigation.setAttribute("expanded-size", "double");
        } else {
            topNavigation.setAttribute("expanded-size", "simple");
        }
        if (window.innerWidth < widthTriggerErrance) {
            erranceBar.setAttribute("expanded-size", "double");
        } else {
            erranceBar.setAttribute("expanded-size", "simple");
        }
    });
}


/* Sub Bar - Highlight selected media type or year */

var mediaBar = document.getElementById("media-bar");
if (mediaBar) {
    var hrefs = window.location.href.split('/');
    var mtype = hrefs[hrefs.length - 1];
    if (!isNaN(parseInt(mtype.charAt(0)))) {
        mtype = hrefs[hrefs.length - 2];
    }
    links = mediaBar.getElementsByTagName("li");
    for (var i=0; i<links.length; i++) {
        link = links[i].getElementsByTagName("a")[0]
        if (link.getAttribute("desc") == mtype) {
            link.classList.add("selected");
        }
    }
}


/* Collection - Display oeuvres by chunks */

var textDecoder = document.createElement("textarea");
function decodeHtml(html) {
    textDecoder.innerHTML = html;
    return textDecoder.value;
}

var chunkSize = 25;
var collection = document.getElementById("collection");
if (collection) {
    for (i=0; i<oeuvres.length/chunkSize; i++) {
        var ul = document.createElement("ul");
        collection.appendChild(ul);
        for (j=0; j<chunkSize; j++) {
            if (oeuvres[chunkSize*i+j]) {
                var a = document.createElement("a");
                var text = decodeHtml(oeuvres[chunkSize*i+j][0]);
                var textNode = document.createTextNode(text);
                a.href = oeuvres[chunkSize*i+j][1];
                a.appendChild(textNode);
                var li = document.createElement("li");
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
    }
}


/* Seances - Displays seances by chunks */

var seancesDisplay = document.getElementById("seances");
if (seancesDisplay) {
    for (i=0; i<seances.length/chunkSize; i++) {
        var ul = document.createElement("ul");
        seancesDisplay.appendChild(ul);
        for (j=0; j<chunkSize; j++) {
            if (seances[chunkSize*i+j]) {
                var li = document.createElement("li");
                var text = decodeHtml(seances[chunkSize*i+j]);
                var textNode = document.createTextNode(text);
                li.appendChild(textNode);
                ul.appendChild(li);
            }
        }
    }
}


/* Cinemas - Displays cinemas by chunks */

chunkSize = 21;
var cinemas = document.getElementById("cinemas");
if (cinemas) {
    for (i=0; i<cines.length/chunkSize; i++) {
        var ul = document.createElement("ul");
        cinemas.appendChild(ul);
        for (j=0; j<chunkSize; j++) {
            if (cines[chunkSize*i+j]) {
                var a = document.createElement("a");
                var text = decodeHtml(cines[chunkSize*i+j][0]);
                var textNode = document.createTextNode(text);
                a.href = cines[chunkSize*i+j][1];
                a.appendChild(textNode);
                var li = document.createElement("li");
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
    }
}


/* Forms Validation */

function validationMark(elem, test) {
    if (test) {
        elem.classList.add("bad-input");
    } else {
        elem.classList.remove("bad-input");
    }
}

function addInputListener(element, atInit) {
    if (atInit) {
        validationMark(element[0],
                       element[1](element[0].value));
    }
    element[0].addEventListener("blur", function (e) {
        validationMark(e.target, element[1](e.target.value));});
    element[0].addEventListener("input", function (e) {
        validationMark(e.target, element[1](e.target.value));});
}

function addInputsListener(validatedElements, atInit) {
    for (i=0; i<validatedElements.length; i++) {
        /* we need an auxiliary function to copy i */
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

var commentFormEmpty = document.getElementById("comment_form_empty");
if (commentFormEmpty) {
    date = document.getElementById("id_empty_date");
    content = document.getElementById("id_empty_content");
    validatedElements = [
        [date, x => (x == "")],
        [content, x => (x == "")]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(commentFormEmpty, validatedElements);
}

var commentForm = document.getElementById("comment_form");
if (commentForm) {
    date = document.getElementById("id_date");
    content = document.getElementById("id_content");
    validatedElements = [
        [date, x => (x == "")],
        [content, x => (x == "")]
    ];
    addInputsListener(validatedElements, true);
    addSubmitListener(commentForm, validatedElements);
}

/* this is for the blog */
var commentFormCustom = document.getElementById("comment_form_custom");
if (commentFormCustom) {
    username = document.getElementById("id_name");
    email = document.getElementById("id_email");
    comment = document.getElementById("id_comment");
    validatedElements = [
        [username, x => (x == "")],
        [comment, x => (x == "")]
    ];
    addInputsListener(validatedElements, false);
    addSubmitListener(commentFormCustom, validatedElements);

    function validateEmail(x) {
        return ((x.length > 0) &&
                ((x[x.length-2] == ".") || (x.indexOf(".") == -1) || (x.indexOf("@") == -1)))
    }
    var triedEmail = false;
    email.addEventListener("blur", function (e) {
        validationMark(e.target, validateEmail(e.target.value));
        if (e.target.value.length > 0) {triedEmail = true;}});
    email.addEventListener("input", function (e) {
        if (triedEmail) {
            validationMark(e.target, validateEmail(e.target.value));
        }
    });
}


/* Global - Reveal login, edit... through keyboard inputs */

var loginForm = document.getElementById("login_form");

var codes = {"login": loginForm,
             "logout": true,
             "edito": oeuvreForm,
             "addo": oeuvreFormEmpty,
             "editc": commentForm,
             "addc": commentFormEmpty,
             "editi": cinemaForm};

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
                        function(e) { nameInput.focus(); });
                }
            }
        }
    }
});

/* there is no keypress event for ESC... */
document.addEventListener("keydown", function (e) {
    if (activeCode && (e.keyCode == 27)) {
        codes[activeCode].parentElement.classList.remove("revealed");
        activeCode = "";
    }
});

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


/* Blog - Menus positions depend on window width */

var widthTriggerBlogSidebar = 1600;
var topNavigation = document.getElementById("top-navigation");
var blogContentWrap = document.getElementById("blog-content-wrap");
if (blogContentWrap) {
    if (window.innerWidth < widthTriggerBlogSidebar) {
        blogContentWrap.setAttribute("layout", "vertical");
        topNavigation.style.paddingRight = "0px";
    } else {
        blogContentWrap.setAttribute("layout", "horizontal");
        topNavigation.style.paddingRight = "60px";
    }

    window.addEventListener("resize", function(e) {
        if (window.innerWidth < widthTriggerBlogSidebar) {
            blogContentWrap.setAttribute("layout", "vertical");
            topNavigation.style.paddingRight = "0px";
        } else {
            blogContentWrap.setAttribute("layout", "horizontal");
            topNavigation.style.paddingRight = "60px";
        }
    });
}

if (topNavigation) {
    if (window.innerWidth < widthTriggerTopNav) {
        topNavigation.setAttribute("layout", "vertical");
    } else {
        topNavigation.setAttribute("layout", "horizontal");
    }

    window.addEventListener("resize", function(e) {
        if (window.innerWidth < widthTriggerTopNav) {
            topNavigation.setAttribute("layout", "vertical");
        } else {
            topNavigation.setAttribute("layout", "horizontal");
        }
    });
}


/* Blog Archive Widget - Expand/Collapse entries */

var widgetArchives = document.getElementById("widget-archives");
if (widgetArchives) {

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
}


/* Blog Comment - Reveal comment form */

var commentForm = document.getElementById("comment_form_custom");
if (commentForm) {
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


    /* this hackish part auto-scrolls to the bottom of the window
     * when resizing the text area, for the horizontal layout
     * (there is no textarea resize event support) */
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


/* Photos Display - Shrink-wrap container */

var galleryPhotos = document.getElementById("gallery-photos");
if (galleryPhotos) {
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
}


/* Photos Display - Flexslider overlay */

var gallerySlider = document.getElementById("gallery-slider");
if (gallerySlider) {
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
