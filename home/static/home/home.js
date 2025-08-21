/* Homepage - Smooth scroll to info anchor */

$('a[href^="#info"]').click( function (event) {
    event.preventDefault();
    var href = $.attr(this, 'href');
    $('html, body').animate({
        scrollTop: $(href).offset().top
    }, 500, function () { window.location.hash = href; });
});


/* Night Sky animation */

let nightSky = document.getElementById("night-sky");
let nightSkyAnchor = document.getElementById("nightsky-anchor");
let content = document.getElementById("content");


/* Night Sky - Deactivate on iPhones */

// safari on iOS may crash-loop on the night sky animation, so I'll turn it off
// strangely enough, it works for firefox & chrome even if on iOS they're essentially reskins of safari (?)
// frankly, I don't care enough about crappy expensive iphones to spend more time trying to fix this
if (
    navigator.userAgent.includes("iPhone")
    && (!(
        (navigator.userAgent.includes("FxiOS"))
        || (navigator.userAgent.includes("CriOS"))
    ))) {
    nightSky.style.display = "none";
    nightSkyAnchor.style.display = "none";
} else {


/* Night Sky - Position animation on nightsky anchor */

// dirty heuristic to approximate mobile screen detection
let biggerClipPath = (screen.width < 1920) && (window.devicePixelRatio > 2.2);

function setNightSkyOrigin() {
    let anchorRect = nightSkyAnchor.getBoundingClientRect();
    let contentRect = content.getBoundingClientRect();
    let x = Math.floor((anchorRect.left + anchorRect.right) / 2) + 1 + "px";
    let y = Math.floor(anchorRect.top * .3 + anchorRect.bottom * .7) - contentRect.top + "px";

    let clipPathRadius = "var(--ns-radius) + min(var(--ns-radius), var(--ns-max-feather))"
    if (biggerClipPath) {
        clipPathRadius += " + 20px";
    }

    nightSky.style.clipPath = "circle(calc(" + clipPathRadius + ") at " + x + " " + y +")";
    nightSky.style.maskImage = "radial-gradient(circle at " + x + " " + y + ", black, black var(--ns-radius), transparent calc(var(--ns-radius) + min(var(--ns-radius), var(--ns-max-feather))), transparent)";
}

window.addEventListener("load", (e) => {
    setNightSkyOrigin();
    nightSky.style.display = "initial";
});
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


/* Night Sky - Toggle animations based on hover */

nightSky.addEventListener("mouseenter", (event) => {
    let style = window.getComputedStyle(nightSky);
    if (style.getPropertyValue("animation-play-state") == "running, paused") {
        nightSky.style.animationPlayState = "paused, running";
    }
});

nightSky.addEventListener("mouseleave", (event) => {
    let style = window.getComputedStyle(nightSky);
    if (style.getPropertyValue("animation-play-state") == "paused, running") {
        nightSky.style.animationPlayState = "running, paused";
    }
});

nightSky.addEventListener("animationend", (event) => {
    /* stop the remaining animation once either one completed */
    nightSky.style.animationPlayState = "paused, paused";
});

}
