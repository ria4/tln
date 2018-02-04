
/* Errance Bar - Double height in small windows */

var errance_bar = document.getElementById("errance-bar");
if (errance_bar) {
    var width_trigger_errance = 1200;
    var errance_bar_trigger = document.getElementById("errance-bar-trigger");
    errance_bar_trigger.addEventListener("click", function(e) {
        e.preventDefault();
        if (errance_bar.classList.contains("expanded")) {
            errance_bar.classList.remove("expanded");
        } else {
            errance_bar.classList.add("expanded");
        }

        if (window.innerWidth < width_trigger_errance) {
            errance_bar.setAttribute("expanded_size", "double");
        } else {
            errance_bar.setAttribute("expanded_size", "simple");
        }
    });

    window.addEventListener("resize", function(e) {
        if (window.innerWidth < width_trigger_errance) {
            errance_bar.setAttribute("expanded_size", "double");
        } else {
            errance_bar.setAttribute("expanded_size", "simple");
        }
    });
}


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

function add_input_listener(validated_elements, at_init, n) {
    if (at_init) {
        validation_mark(validated_elements[n][0],
                        validated_elements[n][1](validated_elements[n][0].value));
    }
    validated_elements[n][0].addEventListener("blur", function (e) {
        validation_mark(e.target, validated_elements[n][1](e.target.value));});
    validated_elements[n][0].addEventListener("input", function (e) {
        validation_mark(e.target, validated_elements[n][1](e.target.value));});
}

function add_inputs_listener(validated_elements, at_init) {
    for (i=0; i<validated_elements.length; i++) {
        /* we need an auxiliary function to copy i */
        add_input_listener(validated_elements, at_init, i);
    }
}

function add_submit_listener(form, validated_elements) {
    form.addEventListener("submit", function (e) {
        var data_ok = true;
        for (i=0; i<validated_elements.length; i++) {
            if (validated_elements[i][0].classList.contains("bad_input")) {
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
    validated_elements = [
        [title_vf, x => ((x.length > 1000) || (x == ""))],
        [title_vo, x => (x.length > 1000)],
        [title_alt, x => (x.length > 1000)],
        [artists, x => ((x.length > 1000) || (x == ""))],
        [year, x => ((x > 2100) || (x == ""))],
        [imdb_id, x => !x.match(/^tt\d{7}$|^$/)]
    ];
    add_inputs_listener(validated_elements, true);
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
    validated_elements = [
        [title_vf, x => ((x.length > 1000) || (x == ""))],
        [title_vo, x => (x.length > 1000)],
        [title_alt, x => (x.length > 1000)],
        [artists, x => ((x.length > 1000) || (x == ""))],
        [year, x => ((x > 2100) || (x == ""))],
        [imdb_id, x => !x.match(/^tt\d{7}$|^$/)]
    ];
    add_inputs_listener(validated_elements, true);
    add_submit_listener(oeuvre_form_empty, validated_elements);
}

var cinema_form = document.getElementById("cinema_form");
if (cinema_form) {
    name_input = document.getElementById("id_name");
    comment = document.getElementById("id_comment");
    visited = document.getElementById("id_visited");
    validated_elements = [
        [name_input, x => (x == "")],
        [comment, x => (x == "")],
        [visited, x => (x == "")]
    ];
    add_inputs_listener(validated_elements, true);
    add_submit_listener(cinema_form, validated_elements);
}

var comment_form_empty = document.getElementById("comment_form_empty");
if (comment_form_empty) {
    date = document.getElementById("id_empty_date");
    content = document.getElementById("id_empty_content");
    validated_elements = [
        [date, x => (x == "")],
        [content, x => (x == "")]
    ];
    add_inputs_listener(validated_elements, true);
    add_submit_listener(comment_form_empty, validated_elements);
}

var comment_form = document.getElementById("comment_form");
if (comment_form) {
    date = document.getElementById("id_date");
    content = document.getElementById("id_content");
    validated_elements = [
        [date, x => (x == "")],
        [content, x => (x == "")]
    ];
    add_inputs_listener(validated_elements, true);
    add_submit_listener(comment_form, validated_elements);
}

/* this is for the blog */
var comment_form_custom = document.getElementById("comment_form_custom");
if (comment_form_custom) {
    username = document.getElementById("id_name");
    email = document.getElementById("id_email");
    comment = document.getElementById("id_comment");
    validated_elements = [
        [username, x => (x == "")],
        [comment, x => (x == "")]
    ];
    add_inputs_listener(validated_elements, false);
    add_submit_listener(comment_form_custom, validated_elements);

    function validate_email(x) {
        return ((x.length > 0) &&
                ((x[x.length-2] == ".") || (x.indexOf(".") == -1) || (x.indexOf("@") == -1)))
    }
    email.addEventListener("blur", function (e) {
        validation_mark(e.target, validate_email(e.target.value));});
    email.addEventListener("input", function (e) {
        validation_mark(e.target, (e.target.value.length > 0));});
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
                if (user_is_authenticated) { window.location.href = "/logout"; }
            } else {
                codes[active_code].parentElement.classList.add("revealed");
                if (active_code == "login") {
                    e.preventDefault();
                    name_input = document.getElementById("id_username");
                    name_input.focus();
                }
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


/* Blog - Nav menu position depends on window width */

var width_trigger_blogdisplay = 1600;
var blog_content_wrap = document.getElementById("blog-content-wrap");
if (blog_content_wrap) {
    if (window.innerWidth < width_trigger_blogdisplay) {
        blog_content_wrap.setAttribute("layout", "vertical");
    } else {
        blog_content_wrap.setAttribute("layout", "horizontal");
    }

    window.addEventListener("resize", function(e) {
        if (window.innerWidth < width_trigger_blogdisplay) {
            blog_content_wrap.setAttribute("layout", "vertical");
        } else {
            blog_content_wrap.setAttribute("layout", "horizontal");
        }
    });
}


/* Blog Archive Widget - Expand/Collapse entries */

var widget_archives = document.getElementById("widget-archives");
if (widget_archives) {

    function add_toggle_listener(toggle) {
        toggle.addEventListener("click", function(e) {
            e.preventDefault();
            if (toggle.classList.contains("expanded")) {
                toggle.classList.add("collapsed");
                toggle.classList.remove("expanded");
            } else {
                toggle.classList.add("expanded");
                toggle.classList.remove("collapsed");
            }
        });
    }

    toggles = widget_archives.getElementsByClassName("toggle");
    [].forEach.call(toggles, add_toggle_listener);
}


/* Blog Comment - Reveal comment form */

var comment_form = document.getElementById("comment_form_custom");
if (comment_form) {
    var comment_form_trigger = document.getElementById("comment-form-trigger");
    var comment_form_trigger_img = comment_form_trigger.getElementsByTagName("img")[0];
    comment_form_trigger.addEventListener("mouseover", function (e) {
        comment_form_trigger_img.setAttribute("src", "/static/blog/icon_comment_link_hover.png");
    });
    comment_form_trigger.addEventListener("mouseout", function (e) {
        comment_form_trigger_img.setAttribute("src", "/static/blog/icon_comment_link.png");
    });

    comment_form.classList.add("collapsed");
    comment_form_trigger.addEventListener("click", function (e) {
        e.preventDefault();
        if (comment_form.classList.contains("expanded")) {
            comment_form.classList.add("collapsed");
            comment_form.classList.remove("expanded");
        } else {
            comment_form.classList.add("expanded");
            comment_form.classList.remove("collapsed");
        }
    });


    /* this hackish part auto-scrolls to the bottom of the window
     * when resizing the text area, for the horizontal layout
     * (there is no textarea resize event support) */
    function scroll_to_bottom(e) {
        if ((window.innerHeight - event.clientY) < 50) {
            window.scrollTo(0, document.body.scrollHeight);
        }
    }

    var comment_form_textarea = comment_form.getElementsByTagName("textarea")[0];
    var pos_info = comment_form_textarea.getBoundingClientRect()
    comment_form_textarea.addEventListener("mousedown", function (e) {
        if (window.innerWidth >= width_trigger_blogdisplay) {
            if (((pos_info.height - (e.pageY - this.offsetTop)) < 17) &&
                ((pos_info.width - (e.pageX - this.offsetLeft)) < 17)) {
                document.body.addEventListener("mousemove", scroll_to_bottom);
            }
        }
    });
    document.body.addEventListener("mouseup", function (e) {
        document.body.removeEventListener("mousemove", scroll_to_bottom);
    });


    var currently_submitting = false;
    var comment_form_wrap = document.getElementById("comment-form-wrap");
    var comment_form_main = document.getElementById("comment-form-main");
    var comment_post_loader = document.getElementById("comment-post-loader");
    var comment_post_result = document.getElementById("comment-post-result");
    var comment_post_result_text = comment_post_result.getElementsByTagName("p")[0];
    var timeout_clean_form;

    comment_form_wrap.addEventListener("click", function (e) {
        if (!currently_submitting) {
            clearTimeout(timeout_clean_form);
            comment_form_main.classList.remove("waiting");
            comment_post_result.style.display = "none";
        }
    });

    comment_form.addEventListener("submit", function (e) {
        e.preventDefault();
        comment_form_main.classList.add("waiting");
        comment_post_loader.style.display = "block";

        if (!currently_submitting) {
            currently_submitting = true;
            var request = new XMLHttpRequest();
            request.open("POST", "/blog/comments/post/", true);
            request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");

            function clean_comment_form_success() {
                comment_post_result.style.display = "none";
                comment_form.classList.add("collapsed");
                comment_form.classList.remove("expanded");
                setTimeout(function () { comment_form_main.classList.remove("waiting"); }, 500);
            }

            request.onreadystatechange = function() {
                /* allow to remove waiting screen after some time */
                setTimeout(function() { currently_submitting = false; }, 2000);
                comment_post_loader.style.display = "none";
                if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
                    res = JSON.parse(request.responseText);
                    var post_comment_success = res["post_comment_success"];
                    if (post_comment_success) {
                        if (user_is_authenticated) {
                            window.location.reload(false);
                        } else {
                        comment_post_result_text.innerHTML = "Merci ! Votre commentaire sera publié après modération.";
                        timeout_clean_form = setTimeout(clean_comment_form_success, 6000);
                        }
                    } else {
                        comment_post_result_text.innerHTML = "Une erreur est survenue. Merci de réessayer plus tard.<br/>(et désolée pour le dérangement)";
                    }
                } else {
                    comment_post_result_text.innerHTML = "Une erreur est survenue. Merci de réessayer plus tard.<br/>(et désolée pour le dérangement)";
                }
                comment_post_result.style.display = "flex";
            }

            // ?? I can't find a way to build the x-www-form-urlencoded string
            // from the form data. And we can't use FormData because it would mess
            // with django's post_comment method. I guess I shall do it myself,
            // except it may break if the form changes...
            var urlEncodedData = "";
            var urlEncodedDataPairs = [];
            var inputs = comment_form.getElementsByTagName("input");
            for (var i=0; i<inputs.length; i++) {
                var input = inputs[i];
                name = input.getAttribute('name');
                value = '';
                if (name == "name") {
                    if (input.value != null) { value = input.value; }
                    else if (input.getAttribute('value') != null) {
                        /* authenticated user only */
                        value = input.getAttribute('value'); }
                } else if ((name == "email") || (name == "honeypot")) {
                    if (input.value != null) { value = input.value; }
                } else {
                    if (input.value != null) { value = input.getAttribute('value'); }
                }
                urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(value));
            }
            var comment_input = comment_form.getElementsByTagName("textarea")[0];
            urlEncodedDataPairs.push(encodeURIComponent(comment_input.getAttribute('name'))
                + '=' + encodeURIComponent(comment_input.value));
            urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

            request.send(urlEncodedData);
        }
    });
}
