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
var photos = gallerySlider.getElementsByTagName("img");

function loadPhoto(idx) {
    function loadPhotoIdx() {
        photo = photos[idx];
        if (photo.hasAttribute("data-src")) {
            photo.setAttribute("src", photo.getAttribute("data-src"));
            photo.removeAttribute("data-src");
        }
    }
    return loadPhotoIdx;
}

Number.prototype.mod = function(n) { return ((this%n)+n)%n; };
function loadPhotoPPrev() { var prevIdx = slider.currentSlide-2; loadPhoto(prevIdx.mod(photos.length))(); }
function loadPhotoPrev() { var prevIdx = slider.currentSlide-1; loadPhoto(prevIdx.mod(photos.length))(); }
function loadPhotoNext() { loadPhoto((slider.currentSlide+1) % photos.length)(); }
function loadPhotoNNext() { loadPhoto((slider.currentSlide+2) % photos.length)(); }
function loadPhotoPrevNext() { loadPhotoNext(); loadPhotoPrev(); }


/* Slider Display - Launch slider from clicked or anchored image */

var photoSlugs = [];
for (var i=0; i<photos.length; i++) {
    photoSlugs.push(photos[i].getAttribute("slug"));
}

function addSliderStartListener(item) {
    item.addEventListener("click", function (e) {
        e.preventDefault();
        slider.vars.animationSpeed = 0;

        var photoIdx = parseInt(item.getAttribute("data-onclick"), 10);
        if (photoIdx == 0) {
            loadPhotoPrevNext();
        } else {
            photos[photoIdx].onload = loadPhotoPrevNext;
            loadPhoto(photoIdx)();
        }

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
        photos[photoIdx].onload = loadPhotoPrevNext;
        loadPhoto(photoIdx)();
        slider.flexAnimate(photoIdx);
        overlaySlider.classList.add("revealed");
    } else {
        if (photos.length > 0) { loadPhoto(0)(); }
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
for (var i=0; i<photos.length; i++) {
    photos[i].addEventListener("click", function(e) {
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
    loadPhotoPPrev();
    return false;
});
$(".flex-nav-next").on("click", function() {
    $("#gallery-slider").flexslider("next");
    loadPhotoNNext();
    return false;
});

document.addEventListener("keydown", function(e) {
    if (e.keyCode == 37) { loadPhotoPPrev(); }
    else if (e.keyCode == 39) { loadPhotoNNext(); }
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
                    loadPhotoPPrev();
                } else {
                    $("#gallery-slider").flexslider("next");
                    loadPhotoNNext();
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

/* this is supposed to be fired before the listeners from addPhotoResizeListener */
window.addEventListener("resize", function() {
    maxSlideWidth = parseInt(window.getComputedStyle(gallerySlider).width, 10);
    maxSlideHeight = parseInt(window.getComputedStyle(gallerySlider).height, 10) - slidesInfoHeight;
    ratioRef = 1.0 * maxSlideWidth / maxSlideHeight;
});

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
