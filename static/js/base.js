
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


/* Sub Bar - Highlight selected media type or year */

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

chunk_size = 21;
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


/* Forms Validation */

function validation_mark(elem, test) {
    if (test) {
        elem.classList.add("bad_input");
    } else {
        elem.classList.remove("bad_input");
    }
}

function add_submit_listener(form, validated_elements) {
    form.addEventListener("submit", function (e) {
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

var oeuvre_form = document.getElementById("oeuvre_form");
if (oeuvre_form) {

    title_vf = document.getElementById("id_title_vf");
    title_vo = document.getElementById("id_title_vo");
    title_alt = document.getElementById("id_title_alt");
    artists = document.getElementById("id_artists");
    year = document.getElementById("id_year");
    imdb_id = document.getElementById("id_imdb_id");
    validated_elements = [title_vf, title_vo, title_alt, artists, year, imdb_id];

    validation_mark(title_vf, ((title_vf.value.length > 1000) || (title_vf.value == "")));
    validation_mark(title_vo, title_vo.value.length > 1000);
    validation_mark(title_alt, title_alt.value.length > 1000);
    validation_mark(artists, ((artists.value.length > 1000) || (artists.value == "")));
    validation_mark(year, ((year.value > 2100) || (year.value == "")));
    validation_mark(imdb_id, !imdb_id.value.match(/^tt\d{7}$|^$/));

    title_vf.addEventListener("blur", function (e) {
        validation_mark(e.target, ((e.target.value.length > 1000) || (e.target.value == "")));});
    title_vo.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value.length > 1000);});
    title_alt.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value.length > 1000);});
    artists.addEventListener("blur", function (e) {
        validation_mark(e.target, ((e.target.value.length > 1000) || (e.target.value == "")));});
    year.addEventListener("blur", function (e) {
        validation_mark(e.target, ((e.target.value > 2100) || (e.target.value == "")));});
    imdb_id.addEventListener("blur", function (e) {
        validation_mark(e.target, !e.target.value.match(/^tt\d{7}$|^$/))});

    add_submit_listener(oeuvre_form, validated_elements);
}

var oeuvre_form_empty = document.getElementById("oeuvre_form_empty");
if (oeuvre_form_empty) {

    title_vf = document.getElementById("id_empty_title_vf");
    title_vo = document.getElementById("id_empty_title_vo");
    title_alt = document.getElementById("id_empty_title_alt");
    artists = document.getElementById("id_empty_artists");
    year = document.getElementById("id_empty_year");
    imdb_id = document.getElementById("id_empty_imdb_id");
    validated_elements = [title_vf, title_vo, title_alt, artists, year, imdb_id];

    validation_mark(title_vf, ((title_vf.value.length > 1000) || (title_vf.value == "")));
    validation_mark(title_vo, title_vo.value.length > 1000);
    validation_mark(title_alt, title_alt.value.length > 1000);
    validation_mark(artists, ((artists.value.length > 1000) || (artists.value == "")));
    validation_mark(year, ((year.value > 2100) || (year.value == "")));
    validation_mark(imdb_id, !imdb_id.value.match(/^tt\d{7}$|^$/));

    title_vf.addEventListener("blur", function (e) {
        validation_mark(e.target, ((e.target.value.length > 1000) || (e.target.value == "")));});
    title_vo.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value.length > 1000);});
    title_alt.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value.length > 1000);});
    artists.addEventListener("blur", function (e) {
        validation_mark(e.target, ((e.target.value.length > 1000) || (e.target.value == "")));});
    year.addEventListener("blur", function (e) {
        validation_mark(e.target, ((e.target.value > 2100) || (e.target.value == "")));});
    imdb_id.addEventListener("blur", function (e) {
        validation_mark(e.target, !e.target.value.match(/^tt\d{7}$|^$/))});

    add_submit_listener(oeuvre_form_empty, validated_elements);
}

var cinema_form = document.getElementById("cinema_form");
if (cinema_form) {

    name_input = document.getElementById("id_name");
    comment = document.getElementById("id_comment");
    visited = document.getElementById("id_visited");
    validated_elements = [name, comment, visited];

    validation_mark(name_input, name_input.value == "");
    validation_mark(comment, comment.value == "");
    validation_mark(visited, visited.value == "");

    name_input.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});
    comment.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});
    visited.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});

    add_submit_listener(cinema_form, validated_elements);
}

var comment_form_empty = document.getElementById("comment_form_empty");
if (comment_form_empty) {

    date = document.getElementById("id_empty_date");
    content = document.getElementById("id_empty_content");
    validated_elements = [date, content];

    validation_mark(date, date.value == "");
    validation_mark(content, content.value == "");

    date.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});
    content.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});

    add_submit_listener(comment_form_empty, validated_elements);
}

var comment_form = document.getElementById("comment_form");
if (comment_form) {

    date = document.getElementById("id_date");
    content = document.getElementById("id_content");
    validated_elements = [date, content];

    validation_mark(date, date.value == "");
    validation_mark(content, content.value == "");

    date.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});
    content.addEventListener("blur", function (e) {
        validation_mark(e.target, e.target.value == "");});

    add_submit_listener(comment_form, validated_elements);
}


/* Global - Reveal login, edit... through keyboard inputs */

var login_form = document.getElementById("login_form");

var codes = {"login": login_form,
             "logout": true,
             "edito": oeuvre_form,
             "addo": oeuvre_form_empty,
             "editc": comment_form,
             "addc": comment_form_empty,
             "editi": cinema_form};

var active_code = "";
var cached_code = "";
document.addEventListener("keypress", function (e) {
    if (!active_code) {
        cached_code += String.fromCharCode(e.charCode);
        var possible_code = false;
        var code_found = false;
        for (var key in codes) {
            if (codes.hasOwnProperty(key)) {
                if (key.startsWith(cached_code)) {
                    possible_code = true;
                    if ((cached_code === key) && (codes[key])) {
                        active_code = key;
                        code_found = true;
                    }
                }
            }
        }
        if (!possible_code) {
            cached_code = "";
        } else if (code_found) {
            cached_code = "";
            if (active_code == "logout") {
                active_code = "";
                window.location.href = "/critique/logout";
            } else {
                codes[active_code].parentElement.classList.add("revealed");
            }
        }
    }
});

/* there is no keypress event for ESC... */
document.addEventListener("keydown", function (e) {
    if (active_code && (e.keyCode == 27)) {
        codes[active_code].parentElement.classList.remove("revealed");
        active_code = "";
    }
});

for (var key in codes) {
    if (codes.hasOwnProperty(key)) {
        if ((key != "logout") && (codes[key])) {
            codes[key].addEventListener("reset", function (e) {
                e.target.parentElement.classList.remove("revealed");
                active_code = "";
            });
        }
    }
}

/* Pagination - Navigate with arrow keys */

var pagination = document.getElementById("pagination");
if (pagination) {
    document.addEventListener("keydown", function (e) {
        if ((e.keyCode == 37) && previous_page_url && !(active_code)) {
            window.location.href = previous_page_url;
        } else if ((e.keyCode == 39) && next_page_url && !(active_code)) {
            window.location.href = next_page_url;
        }
    });
}
