/* Homepage - Smooth scroll to info anchor */

$('a[href^="#info"]').click( function (event) {
    event.preventDefault();
    var href = $.attr(this, 'href');
    $('html, body').animate({
        scrollTop: $(href).offset().top
    }, 500, function () { window.location.hash = href; });
});


/* Start blurring animation when info appears in viewport */

if (!isTouchDevice()) {
    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (rect.top <= window.innerHeight);
    }

    var infoContent = document.getElementById("info-content");
    var infoSeparator = document.getElementById("info-separator");

    function infoHandler() {
        if (!infoContent.classList.contains("anim-blur")) {
            var visible = isElementInViewport(infoSeparator);
            if (visible) {
                infoContent.classList.add("anim-blur");
            }
        }
    }

    window.addEventListener('load', infoHandler, false);
    window.addEventListener('scroll', infoHandler, false);
    window.addEventListener('resize', infoHandler, false);
} else {
    var infoClones = document.getElementsByClassName("onhover-display");
    while(infoClones.length > 0) {
        infoClones[0].parentNode.removeChild(infoClones[0]);
    }
}
