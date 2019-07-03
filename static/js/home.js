/* Homepage - Smooth scroll to info anchor */

$('a[href^="#"]').click( function (event) {
    event.preventDefault();
    var href = $.attr(this, 'href');
    $('html, body').animate({
        scrollTop: $(href).offset().top
    }, 500, function () { window.location.hash = href; });
});
