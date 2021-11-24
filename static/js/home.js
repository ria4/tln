/* Homepage - Smooth scroll to info anchor */

$('a[href^="#"]').click( function (event) {
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

    function infoHandler() {
        if (!infoContent.classList.contains("anim-blur")) {
            var visible = isElementInViewport(infoContent);
            if (visible) {
                infoContent.classList.add("anim-blur");
            }
        }
    }

    window.addEventListener('load', infoHandler, false);
    window.addEventListener('scroll', infoHandler, false);
    window.addEventListener('resize', infoHandler, false);
}
