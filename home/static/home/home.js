/* Homepage - Smooth scroll to info anchor */

$('a[href^="#info"]').click( function (event) {
    event.preventDefault();
    var href = $.attr(this, 'href');
    $('html, body').animate({
        scrollTop: $(href).offset().top
    }, 500, function () { window.location.hash = href; });
});


/* Night Sky - Position animation on nightsky anchor */

let nightSky = document.getElementById("night-sky");
let nightSkyAnchor = document.getElementById("nightsky-anchor");
let content = document.getElementById("content");

function setNightSkyOrigin() {
    let anchorRect = nightSkyAnchor.getBoundingClientRect();
    let contentRect = content.getBoundingClientRect();
    let x = Math.floor((anchorRect.left + anchorRect.right) / 2) + 1 + "px";
    let y = Math.floor(anchorRect.top * .3 + anchorRect.bottom * .7) - contentRect.top + "px";

    nightSky.style.clipPath = "circle(calc(var(--ns-radius) + min(var(--ns-radius), var(--ns-max-feather))) at " + x + " " + y +")";
    nightSky.style.maskImage = "radial-gradient(circle at " + x + " " + y + ", black, black var(--ns-radius), transparent calc(var(--ns-radius) + min(var(--ns-radius), var(--ns-max-feather))), transparent)";
}

setNightSkyOrigin();
nightSky.style.display = "initial";
window.addEventListener("resize", setNightSkyOrigin);


/* Night Sky - Start animation only when anchor is visible */

const startNightSky = (entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            nightSky.style.animationPlayState = "running, paused";
        }
    });
}

const observer = new IntersectionObserver(startNightSky, { threshold: 1.0 });
observer.observe(nightSkyAnchor);
