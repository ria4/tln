var errance_bar_trigger = document.getElementById("errance-bar-trigger");
var errance_bar = document.getElementById("errance-bar");
errance_bar_trigger.addEventListener("click", function(e) {
    e.preventDefault();
    if (errance_bar.classList.contains("expanded")) { 
        errance_bar.classList.remove("expanded");
        /* $(".topic-bar-trigger").removeClass("active"); */
    } else {
        errance_bar.classList.add("expanded");
        /* $(".topic-bar-trigger").addClass("active"); */
    }
});
