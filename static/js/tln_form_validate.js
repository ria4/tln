/* Forms - Validate form inputs */

function warningOnElementIf(elem, test) {
    if (test) {
        elem.classList.add("bad-input");
    } else {
        elem.classList.remove("bad-input");
    }
}

function addInputListener(element, atInit) {
    if (atInit) {
        warningOnElementIf(element[0],
                           element[1](element[0].value));
    }
    element[0].addEventListener("blur", function (e) {
        warningOnElementIf(e.target, element[1](e.target.value));});
    element[0].addEventListener("input", function (e) {
        warningOnElementIf(e.target, element[1](e.target.value));});
}

function addInputsListener(validatedElements, atInit) {
    for (i=0; i<validatedElements.length; i++) {
        addInputListener(validatedElements[i], atInit);
    }
}

function addSubmitListener(form, validatedElements) {
    form.addEventListener("submit", function (e) {
        var dataOk = true;
        for (i=0; i<validatedElements.length; i++) {
            if (validatedElements[i][0].classList.contains("bad-input")) {
                dataOk = false;
            }
        };
        if (!dataOk) {
            e.preventDefault();
            // stop the AJAX submit handler in tln.js
            e.stopImmediatePropagation();
        }
    });
}



var websiteApp = location.pathname.split("/")[1];


if (websiteApp == "critique") {


    var oeuvreFormEmpty = document.getElementById("oeuvre_form_empty");
    if (oeuvreFormEmpty) {
        titleVf = document.getElementById("id_empty_title_vf");
        titleVo = document.getElementById("id_empty_title_vo");
        titleAlt = document.getElementById("id_empty_title_alt");
        artists = document.getElementById("id_empty_artists");
        year = document.getElementById("id_empty_year");
        imdbId = document.getElementById("id_empty_imdb_id");
        validatedElements = [
            [titleVf, x => ((x.length > 1000) || (x == ""))],
            [titleVo, x => (x.length > 1000)],
            [titleAlt, x => (x.length > 1000)],
            [artists, x => ((x.length > 1000) || (x == ""))],
            [year, x => ((x > 2100) || (x == ""))],
            [imdbId, x => !x.match(/^tt\d{7}$|^$/)]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(oeuvreFormEmpty, validatedElements);
    }

    var oeuvreForm = document.getElementById("oeuvre_form");
    if (oeuvreForm) {
        titleVf = document.getElementById("id_title_vf");
        titleVo = document.getElementById("id_title_vo");
        titleAlt = document.getElementById("id_title_alt");
        artists = document.getElementById("id_artists");
        year = document.getElementById("id_year");
        imdbId = document.getElementById("id_imdb_id");
        validatedElements = [
            [titleVf, x => ((x.length > 1000) || (x == ""))],
            [titleVo, x => (x.length > 1000)],
            [titleAlt, x => (x.length > 1000)],
            [artists, x => ((x.length > 1000) || (x == ""))],
            [year, x => ((x > 2100) || (x == ""))],
            [imdbId, x => !x.match(/^tt\d{7}$|^$/)]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(oeuvreForm, validatedElements);
    }

    var commentFormEmpty = document.getElementById("comment_form_empty");
    if (commentFormEmpty) {
        date = document.getElementById("id_empty_date");
        comment_content = document.getElementById("id_empty_content");
        validatedElements = [
            [date, x => (x == "")],
            [comment_content, x => (x == "")]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(commentFormEmpty, validatedElements);
    }

    var commentForm = document.getElementById("comment_form");
    if (commentForm) {
        date = document.getElementById("id_date");
        comment_content = document.getElementById("id_content");
        validatedElements = [
            [date, x => (x == "")],
            [comment_content, x => (x == "")]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(commentForm, validatedElements);
    }

    var cinemaForm = document.getElementById("cinema_form");
    if (cinemaForm) {
        nameInput = document.getElementById("id_name");
        comment = document.getElementById("id_comment");
        visited = document.getElementById("id_visited");
        validatedElements = [
            [nameInput, x => (x == "")],
            [comment, x => (x == "")],
            [visited, x => (x == "")]
        ];
        addInputsListener(validatedElements, true);
        addSubmitListener(cinemaForm, validatedElements);
    }

    var seanceFormEmpty = document.getElementById("seance_form_empty");
    if (seanceFormEmpty) {
        cinema = document.getElementById("id_empty_seance_cinema");
        date = document.getElementById("id_empty_seance_date");
        hour = document.getElementById("id_empty_seance_hour");
        validatedElements = [
            [cinema, x => ((x.length > 1000) || (x == ""))],
            [date, x => (x == "")],
            [hour, x => ((x.length != 5) || (x.charAt(2) != ":") || (parseInt(x.charAt(0), 10) > 2) || (parseInt(x.charAt(3), 10) > 5))],
        ];
        addInputsListener(validatedElements, true);

        /* exactly one of these must be filled */
        filmSlug = document.getElementById("id_empty_seance_film_slug");
        seanceTitle = document.getElementById("id_empty_seance_seance_title");

        validatedElementsComplete = validatedElements.slice()
        validatedElementsComplete.push([filmSlug, null]);
        validatedElementsComplete.push([seanceTitle, null]);
        addSubmitListener(seanceFormEmpty, validatedElementsComplete);

        warningOnElementIf(filmSlug, true);
        warningOnElementIf(seanceTitle, true);
        filmSlug.addEventListener("blur", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
        seanceTitle.addEventListener("blur", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
        filmSlug.addEventListener("input", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
        seanceTitle.addEventListener("input", function(e) {
            var seanceFormError = (((filmSlug.value == "") && (seanceTitle.value == "")) ||
                                   ((filmSlug.value != "") && (seanceTitle.value != "")))
            warningOnElementIf(filmSlug, seanceFormError);
            warningOnElementIf(seanceTitle, seanceFormError);
        });
    }

    codes["edito"] = oeuvreForm;
    codes["addo"] = oeuvreFormEmpty;
    codes["editc"] = commentForm;
    codes["addc"] = commentFormEmpty;
    codes["editi"] = cinemaForm;
    codes["adde"] = seanceFormEmpty;

    for (var key in codes) {
        if (codes.hasOwnProperty(key)) {
            if ((key != "login") && (key != "logout") && (key != "s") && (codes[key])) {
                codes[key].addEventListener("reset", function (e) {
                    e.preventDefault();
                    e.target.parentElement.classList.remove("revealed");
                    activeCode = "";
                });
            }
        }
    }


} else if (websiteApp == "blog") {


    var commentForm = document.getElementById("comment_form_custom");
    if (commentForm) {

        /* Blog Comment - Form validation */

        username = document.getElementById("id_name");
        email = document.getElementById("id_email");
        comment = document.getElementById("id_comment");
        validatedElements = [
            [username, x => (x == "")],
            [email, x => false],        // email format is checked below
            [comment, x => ((x == "") || (x.indexOf("http://") != -1) || (x.indexOf("https://") != -1))]
        ];
        addInputsListener(validatedElements, false);

        // awkward solution to enable this script to stop the AJAX submit handler
        commentForm.removeEventListener("submit", commentFormSubmitHandler);
        addSubmitListener(commentForm, validatedElements);
        commentForm.addEventListener("submit", commentFormSubmitHandler);

        function validateEmail(x) {
            return ((x.length > 0) &&
                    ((x[x.length-2] == ".") || (x.indexOf(".") == -1) || (x.indexOf("@") == -1)))
        }
        var triedEmail = false;
        email.addEventListener("blur", function (e) {
            warningOnElementIf(e.target, validateEmail(e.target.value));
            if (e.target.value.length > 0) {triedEmail = true;}});
        email.addEventListener("input", function (e) {
            if (triedEmail) {
                warningOnElementIf(e.target, validateEmail(e.target.value));
            }
        });

        comment.addEventListener("blur", function (e) {
            if ((e.target.value.indexOf("http://") != -1) || (e.target.value.indexOf("https://") != -1)) {
                alert("Merci de retirer tout lien de votre message, afin qu'il ne soit pas considéré comme du spam !");
            }
        });

    }


}
