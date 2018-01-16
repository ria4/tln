/* Errance Bar - Double height in small windows */

var window_width_trigger = 1200;
var errance_bar_trigger = document.getElementById("errance-bar-trigger");
var errance_bar = document.getElementById("errance-bar");

errance_bar_trigger.addEventListener("click", function(e) {
    e.preventDefault();
    if (errance_bar.classList.contains("expanded")) { 
        errance_bar.classList.remove("expanded");
    } else {
        errance_bar.classList.add("expanded");
    }

    if (window.innerWidth < window_width_trigger) {
        errance_bar.setAttribute("expanded_size", "double");
    } else {
        errance_bar.setAttribute("expanded_size", "simple");
    }
});

window.addEventListener("resize", function(e) {
    if (window.innerWidth < window_width_trigger) {
        errance_bar.setAttribute("expanded_size", "double");
    } else {
        errance_bar.setAttribute("expanded_size", "simple");
    }
});


/* Media Bar - Highlight selectec media type */

var media_bar = document.getElementById("media-bar");
if (media_bar) {
    var hrefs = window.location.href.split('/');
    var mtype = hrefs[hrefs.length - 1];
    if (!isNaN(parseInt(mtype.charAt(0)))) {
        mtype = hrefs[hrefs.length - 2];
    }
    links = media_bar.getElementsByTagName("li");
    for (var i=0; i<links.length; i++) {
        link = links[i].getElementsByTagName("a")[0]
        if (link.getAttribute("desc") == mtype) {
            link.classList.add("selected");
        }
    }
}


/* Collection - Display oeuvres by chunks */

var txt_decoder = document.createElement("textarea");
function decodeHtml(html) {
    txt_decoder.innerHTML = html;
    return txt_decoder.value;
}

var chunk_size = 25;
var collection = document.getElementById("collection");
if (collection) {
    for (i=0; i<oeuvres.length/chunk_size; i++) {
        var ul = document.createElement("ul");
        collection.appendChild(ul);
        for (j=0; j<chunk_size; j++) {
            if (oeuvres[chunk_size*i+j]) {
                var a = document.createElement("a");
                var text = decodeHtml(oeuvres[chunk_size*i+j][0]);
                var textNode = document.createTextNode(text);
                a.href = oeuvres[chunk_size*i+j][1];
                a.appendChild(textNode);
                var li = document.createElement("li");
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
    }
}


/* Seances - Displays seances by chunks */

var seances_display = document.getElementById("seances");
if (seances_display) {
    for (i=0; i<seances.length/chunk_size; i++) {
        var ul = document.createElement("ul");
        seances_display.appendChild(ul);
        for (j=0; j<chunk_size; j++) {
            if (seances[chunk_size*i+j]) {
                var li = document.createElement("li");
                var text = decodeHtml(seances[chunk_size*i+j]);
                var textNode = document.createTextNode(text);
                li.appendChild(textNode);
                ul.appendChild(li);
            }
        }
    }
}


/* Cinemas - Displays cinemas by chunks */

chunk_size = 23;
var cinemas = document.getElementById("cinemas");
if (cinemas) {
    for (i=0; i<cines.length/chunk_size; i++) {
        var ul = document.createElement("ul");
        cinemas.appendChild(ul);
        for (j=0; j<chunk_size; j++) {
            if (cines[chunk_size*i+j]) {
                var a = document.createElement("a");
                var text = decodeHtml(cines[chunk_size*i+j][0]);
                var textNode = document.createTextNode(text);
                a.href = cines[chunk_size*i+j][1];
                a.appendChild(textNode);
                var li = document.createElement("li");
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
    }
}


/* Oeuvre - Update an oeuvre from a django form */
/* TODO CSS styling! */

var oeuvre_form = document.getElementById("oeuvre_form");
if (oeuvre_form) {

    /* Validate inputs */

    function validation_mark(e, test) {
        if (test) {
            e.target.classList.add("bad_input");
        } else {
            e.target.classList.remove("bad_input");
        }
    }

    title_vf = document.getElementById("id_title_vf");
    title_vo = document.getElementById("id_title_vo");
    title_alt = document.getElementById("id_title_alt");
    artists = document.getElementById("id_artists");
    year = document.getElementById("id_year");
    imdb_id = document.getElementById("id_imdb_id");
    validated_elements = [title_vf, title_vo, title_alt, artists, year, imdb_id]

    title_vf.addEventListener("blur", function (e) {
        validation_mark(e, e.target.value.length > 1000);});
    title_vo.addEventListener("blur", function (e) {
        validation_mark(e, e.target.value.length > 1000);});
    title_alt.addEventListener("blur", function (e) {
        validation_mark(e, e.target.value.length > 1000);});
    artists.addEventListener("blur", function (e) {
        validation_mark(e, e.target.value.length > 1000);});
    year.addEventListener("blur", function (e) {
        validation_mark(e, e.target.value > 2100);});
    imdb_id.addEventListener("blur", function (e) {
        validation_mark(e, !e.target.value.match(/^tt\d{7}$/))});

    oeuvre_form.addEventListener("submit", function (e) {
        var data_ok = true;
        for (i=0; i<validated_elements.length; i++) {
            if (validated_elements[i].classList.contains("bad_input")) {
                data_ok = false;
            }
        };
        if (!data_ok) {
            e.preventDefault();
        }
    });
}

