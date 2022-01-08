if (document.body.classList.contains("gallery-list")) {


/* Gallery Title Display - Show & animate titles on touch devices */

if (isTouchDevice()) {
    var galleries = document.getElementById("gallery-list");
    var galleryLinks = galleries.getElementsByTagName("a");
    var galN = galleryLinks.length;

    function displayGalleryTitleSmallScreen(e) {
        for (i=0; i<galN; i++) {
            var rect = galleryLinks[i].getBoundingClientRect();
            var y = rect.top + rect.height/2;
            var highestY = window.innerHeight*3/10;
            var lowestY = window.innerHeight*(10-3)/10;
            if ((highestY < y) && (y < lowestY)) {
                galleryLinks[i].classList.add("display-title");
            } else {
                galleryLinks[i].classList.remove("display-title");
            }
        }
    }

    function displayGalleryTitleLargeScreen() {
        galleryLinks[(counter+1) % galN].classList.add("display-title");
        if (counter >= 0) {
            galleryLinks[counter].classList.remove("display-title");
        }
        counter = (counter+1) % galN;
    }

    var first = true;
    var isSmallScreen;
    var counter = -1;
    var interval;
    var isScrolling;
    function scrollHandler() {
        window.clearTimeout(isScrolling);
        isScrolling = setTimeout(displayGalleryTitleSmallScreen, 100);
    }

    function setTitleHandlers() {
        if (parseInt(window.getComputedStyle(galleries)["height"], 10) > window.innerHeight*1.5) {
            if (first || !isSmallScreen) {
                // remove any previous handlers
                for (i=0; i<galN; i++) { galleryLinks[i].classList.remove("display-title", "slow-transition"); }
                if (interval) { clearInterval(interval); }
                // titles appear when the link is approx. vertically centered
                displayGalleryTitleSmallScreen();
                document.addEventListener("touchmove", displayGalleryTitleSmallScreen);
                window.addEventListener("scroll", scrollHandler);
            }
            isSmallScreen = true;
        } else {
            if (first || isSmallScreen) {
                // remove any previous handlers
                for (i=0; i<galN; i++) { galleryLinks[i].classList.remove("display-title"); }
                document.removeEventListener("touchmove", displayGalleryTitleSmallScreen);
                window.removeEventListener("scroll", scrollHandler);
                // titles appear for two seconds every six seconds
                for (i=0; i<galN; i++) { galleryLinks[i].classList.add("slow-transition"); }
                displayGalleryTitleLargeScreen();
                if (interval) { clearInterval(interval); }
                interval = setInterval(displayGalleryTitleLargeScreen, 3000);
            }
            isSmallScreen = false;
        }
        first = false;
    }

    setTimeout(setTitleHandlers, 500);
    var isResizing;
    window.addEventListener("resize", function() {
        window.clearTimeout(isResizing);
        isResizing = setTimeout(setTitleHandlers, 200)
    });
}


} else if (document.body.classList.contains("gallery")) {


/* Gallery Display - Shrink-wrap container */

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


/* Slides Loading - Lazy-loading helpers for high-res pictures */

var gallerySlider = document.getElementById("gallery-slider");
var slider;
var animationSpeed = 600;

var overlaySlider = gallerySlider.parentNode;
var photoLinks = document.getElementsByClassName("photo-link");
var slides = gallerySlider.getElementsByClassName("slide");
var photosHTMLCollection = gallerySlider.getElementsByTagName("img");
var photos = Array.prototype.slice.call(photosHTMLCollection);
var photosN = photos.length;

/* Ugly profiling hack, see below */
var isFirefox = typeof InstallTrigger !== 'undefined';


function loadPhoto(idx) {
    function loadPhotoIdx(loadNeighbours) {
        var placeholder = photos[idx];
        if (placeholder.hasAttribute("data-src")) {
            var photo = document.createElement("img");
            photo.setAttribute("src", placeholder.getAttribute("data-src"));
            photo.setAttribute("slug", placeholder.getAttribute("slug"));
            photo.setAttribute("alt", placeholder.getAttribute("alt"));
            photo.setAttribute("draggable", "false");
            /* There's an issue with Firefox's WebRender which breaks the lazy-loading for jpg pictures:
             * they're loaded over a white background, which would cover the placeholder altogether...
             * See: https://bugzilla.mozilla.org/show_bug.cgi?id=1556156
             * In order not to see this white background, we'll load the picture behind the placeholder
             * for Firefox browsers (identified with a dirty hack), except if they're png pictures. */
            var placement = "afterend";
            if (isFirefox && placeholder.getAttribute("data-src").slice(-3) != "png") {
                placement = "beforebegin";
            }
            placeholder.insertAdjacentElement(placement, photo);
            photo.addEventListener("load", function() {
                placeholder.remove();
                photos[idx] = photo;
                if (loadNeighbours) { loadPhotoNext(idx)(false); loadPhotoPrev(idx)(false); }
            });
        } else if (loadNeighbours) {
            loadPhotoNext(idx)(false); loadPhotoPrev(idx)(false);
        }
    }
    return loadPhotoIdx;
}

Number.prototype.mod = function(n) { return ((this%n)+n)%n; };
function loadPhotoPPrev(idx) { var pprevIdx = idx-2; return loadPhoto(pprevIdx.mod(photosN)); }
function loadPhotoPrev(idx) { var prevIdx = idx-1; return loadPhoto(prevIdx.mod(photosN)); }
function loadPhotoNext(idx) { return loadPhoto((idx+1) % photosN); }
function loadPhotoNNext(idx) { return loadPhoto((idx+2) % photosN); }
function loadPhotoPrevNext(idx) { return function() { loadPhotoNext(idx)(); loadPhotoPrev(idx)(); }}


/* Slider Display - Launch slider from clicked or anchored image */

var photoSlugs = [];
for (var i=0; i<photosN; i++) {
    photoSlugs.push(photos[i].getAttribute("slug"));
}

function addSliderStartListener(item) {
    item.addEventListener("click", function (e) {
        e.preventDefault();
        slider.vars.animationSpeed = 0;

        var photoIdx = parseInt(item.getAttribute("data-onclick"), 10);
        loadPhoto(photoIdx)(true);

        slider.flexAnimate(photoIdx);
        slider.vars.animationSpeed = animationSpeed;
        if (isTouchDevice()) { window.location.hash = "display"; }
        overlaySlider.classList.add("revealed");
    });
}

for (var i=0; i<photoLinks.length; i++) {
    addSliderStartListener(photoLinks[i]);
}

$(document).ready(function() {
    $("#gallery-slider").flexslider({
        slideshow: false,
        animationSpeed: 0,
        controlNav: false,
        directionNav: false,
        touch: false,
    });

    slider = $("#gallery-slider").data("flexslider");

    // display the slider when loading from an anchored link
    photoIdx = photoSlugs.indexOf(hash);
    if (photoIdx != -1) {
        slider.vars.animationSpeed = 0;
        loadPhoto(photoIdx)(true);
        slider.flexAnimate(photoIdx);
        overlaySlider.classList.add("revealed");
    } else {
        if (photosN > 0) { loadPhoto(0)(false); }
    }

    slider.vars.animationSpeed = animationSpeed;
});


/* Slider Display - Hide slider with either ESC or click outside the image */

document.addEventListener("keydown", function(e) {
    if (e.keyCode == 27) {
        overlaySlider.classList.remove("revealed");
    }
});

overlaySlider.addEventListener("click", function() {
    overlaySlider.classList.remove("revealed");
    if (isTouchDevice()) { window.location.hash = ""; }
});
for (var i=0; i<slides.length; i++) {
    slides[i].addEventListener("click", function(e) {
        e.stopPropagation();
    });
}


/* Slider Display - On mobile, hide slider by hitting 'return' */

if (isTouchDevice()) {
    window.onhashchange = function() {
        if (window.location.hash == "") {
            overlaySlider.classList.remove("revealed");
        }
    }
}


/* Slider Navigation - Update slides according to click or keyboard arrows */

/* Chrome stays focused on the link after a click, which provokes autoslide.
 * That's why we use manual control for this action. */

$(".flex-nav-prev").on("click", function() {
    $("#gallery-slider").flexslider("prev");
    loadPhotoPPrev(slider.currentSlide)(false);
    return false;
});
$(".flex-nav-next").on("click", function() {
    $("#gallery-slider").flexslider("next");
    loadPhotoNNext(slider.currentSlide)(false);
    return false;
});

document.addEventListener("keydown", function(e) {
    if (e.keyCode == 37) { loadPhotoPPrev(slider.currentSlide)(false); }
    else if (e.keyCode == 39) { loadPhotoNNext(slider.currentSlide)(false); }
});


/* Slider Navigation - On mobile, allow swipe while retaining zoom */

if (isTouchDevice()) {
    var swipeXStart = swipeXEnd = 0;
    var swipeXStartPage;
    var swipeTStart; var swipeTEnd;
    var swipeXDelta = 20;
    var swipeXVelocity = 0.3;

    gallerySlider.addEventListener("touchstart", function(e) {
        if (e.touches.length == 1) {
            swipeXStart = swipeXEnd = e.touches[0].screenX;
            swipeXStartPage = e.touches[0].pageX;
            swipeTStart = Date.now();
            swipeTEnd = Date.now(); }
    });

    gallerySlider.addEventListener("touchmove", function(e) {
        if (e.touches.length == 1) {
            swipeXEnd = e.touches[0].screenX;
            swipeTEnd = Date.now(); }
    });

    gallerySlider.addEventListener("touchend", function(e) {
        if ((e.touches.length == 0) && (swipeXStart == swipeXStartPage)) {
            if ((Math.abs(swipeXEnd - swipeXStart) > swipeXDelta) &&
                (swipeTEnd > swipeTStart) &&
                (Math.abs(swipeXEnd - swipeXStart) / (swipeTEnd - swipeTStart) > swipeXVelocity)) {
                if (swipeXEnd > swipeXStart) {
                    $("#gallery-slider").flexslider("prev");
                    loadPhotoPPrev(slider.currentSlide)();
                } else {
                    $("#gallery-slider").flexslider("next");
                    loadPhotoNNext(slider.currentSlide)();
                }
            }
            swipeXStart = swipeXEnd = 0;
        }
    });
}


/* Slide Sizing - Compute slide sizes by comparing client & photo sizes */

/* We need to set the height for the img container explicitly.
 * Indeed we cannot rely on max-width or object-fit tools, because we want the image
 * to fill as much height/width as possible depending on its ratio, yet preparing
 * the image container with a maximal height repels the caption at the bottom... */

var maxSlideWidth = gallerySlider.clientWidth;
var slidesInfoHeight = document.getElementsByClassName("slide-info")[0].clientHeight;
var maxSlideHeight = gallerySlider.clientHeight - slidesInfoHeight;
var ratioRef = 1.0 * maxSlideWidth / maxSlideHeight;

function setPhotoSize(photo) {
    var ratioReal = 1.0 * photo.naturalWidth / photo.naturalHeight;
    var slideWidth;
    if (ratioReal > ratioRef) {
        slideWidth = Math.min(maxSlideWidth, photo.naturalWidth);
    } else {
        slideWidth = Math.min(maxSlideHeight, photo.naturalHeight) * ratioReal;
    }
    photo.closest(".slide").style.width = slideWidth + "px";
}

/* this is supposed to be fired before the listeners from addPhotoResizeListener */
window.addEventListener("resize", function() {
    maxSlideWidth = parseInt(window.getComputedStyle(gallerySlider).width, 10);
    maxSlideHeight = parseInt(window.getComputedStyle(gallerySlider).height, 10) - slidesInfoHeight;
    ratioRef = 1.0 * maxSlideWidth / maxSlideHeight;
    for (var i=0; i<photosN; i++) {
        setPhotoSize(photos[i]);
    }
});

for (var i=0; i<photosN; i++) {
    var placeholder = photos[i];
    placeholder.addEventListener("load", function() { setPhotoSize(this); });
    if ((placeholder.complete && (placeholder.naturalWidth !== 0)) || isIE10) {
        /* the image has already been loaded so onload event won't be fired */
        setPhotoSize(placeholder);
    }
}


}
