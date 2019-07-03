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
var animationSpeed = 600;

var overlaySlider = gallerySlider.parentNode;
var photoLinks = document.getElementsByClassName("photo-link");
var photos = gallerySlider.getElementsByTagName("img");

var photoSlugs = [];
for (var i=0; i<photos.length; i++) {
    photoSlugs.push(photos[i].getAttribute("slug"));
}

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

// hide overlaySlider on hitting ESC
document.addEventListener("keydown", function (e) {
    if (e.keyCode == 27) {
        overlaySlider.classList.remove("revealed");
    }
});

$(document).ready(function() {
    $('#gallery-slider').flexslider({
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
        slider.flexAnimate(photoIdx);
        overlaySlider.classList.add("revealed");
    }

    slider.vars.animationSpeed = animationSpeed;
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
