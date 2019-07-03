/* Blog Side Menu - On an entry page, lower opacity when scrolling down */

if (document.body.classList.contains("entry")) {
    var header = document.getElementById("header");
    var sidebar = document.getElementById("sidebar");
    window.addEventListener("scroll", function() {
        if (sidebar.contains(document.activeElement) ||
            header.contains(document.activeElement)) {
        // keep full opacity when tab-navigating the sidebar or top menu
            sidebar.classList.remove("semihidden");
        } else {
            if (window.scrollY == 0) {
                sidebar.classList.remove("semihidden");
            } else {
                sidebar.classList.add("semihidden");
            }
        }
    });
}


/* Blog Archive Widget - Expand/Collapse entries */

var widgetArchives = document.getElementById("widget-archives");

function addToggleListener(toggle) {
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

toggles = widgetArchives.getElementsByClassName("toggle");
[].forEach.call(toggles, addToggleListener);


/* Blog Comment */

var widthTriggerBlogSidebar = 1512;
var commentForm = document.getElementById("comment_form_custom");
if (commentForm) {

    /* Blog Comment - Reveal comment form */

    var commentFormTrigger = document.getElementById("comment-form-trigger");
    var commentFormTriggerImg = commentFormTrigger.getElementsByTagName("img")[0];
    commentFormTrigger.addEventListener("mouseover", function (e) {
        commentFormTriggerImg.setAttribute("src", "/static/blog/icon_comment_link_hover.png");
    });
    commentFormTrigger.addEventListener("mouseout", function (e) {
        commentFormTriggerImg.setAttribute("src", "/static/blog/icon_comment_link.png");
    });

    var duration;
    var delay = 20;
    function scrollToBottomWhileHeightChanges() {
        if (duration > 0) {
            window.scrollTo(0, document.body.scrollHeight);
            duration = duration - delay;
            setTimeout(scrollToBottomWhileHeightChanges, delay);
        }
    }

    /* Using a hardcoded time seems better than parsing CSS multi-transitionDuration */
    var commentFormTransitionTime = 600;
    commentForm.classList.add("collapsed");
    commentFormTrigger.addEventListener("click", function (e) {
        e.preventDefault();
        if (commentForm.classList.contains("expanded")) {
            commentForm.classList.add("collapsed");
            commentForm.classList.remove("expanded");
        } else {
            commentForm.classList.add("expanded");
            commentForm.classList.remove("collapsed");
            if (window.innerWidth > widthTriggerBlogSidebar) {
                /* Stick the viewport to the bottom of the document */
                duration = commentFormTransitionTime;
                scrollToBottomWhileHeightChanges();
            }
        }
    });

    /* Blog Comment - Warn IE10 users (loader won't appear) */

    submitButton = commentForm.getElementsByClassName("submit-post")[0];
    if (isIE10) {
        submitButton.value = "envoyer (le message sera en attente de modération)";
    }

    /* Blog Comment - Auto-scroll to the bottom of the window

    /* There is no textarea resize event, hence we need this hackish part
     * to auto-scroll when resizing the text area (horizontal layout only). */

    function scrollToBottom(e) {
        if ((window.innerHeight - event.clientY) < 50) {
            window.scrollTo(0, document.body.scrollHeight);
        }
    }

    var commentFormTextarea = commentForm.getElementsByTagName("textarea")[0];
    var posInfo = commentFormTextarea.getBoundingClientRect()
    commentFormTextarea.addEventListener("mousedown", function (e) {
        if (window.innerWidth >= widthTriggerBlogSidebar) {
            if (((posInfo.height - (e.pageY - this.offsetTop)) < 17) &&
                ((posInfo.width - (e.pageX - this.offsetLeft)) < 17)) {
                document.body.addEventListener("mousemove", scrollToBottom);
            }
        }
    });
    document.body.addEventListener("mouseup", function (e) {
        document.body.removeEventListener("mousemove", scrollToBottom);
    });

    /* Blog Comment - AJAX request */

    var currentlySubmitting = false;
    var commentFormWrap = document.getElementById("comment-form-wrap");
    var commentFormMain = document.getElementById("comment-form-main");
    var commentPostLoader = document.getElementById("comment-post-loader");
    var commentPostResult = document.getElementById("comment-post-result");
    var commentPostResultText = commentPostResult.getElementsByTagName("p")[0];
    var timeoutCleanForm;

    commentFormWrap.addEventListener("click", function (e) {
        if (!currentlySubmitting) {
            clearTimeout(timeoutCleanForm);
            commentFormMain.classList.remove("waiting");
            commentPostResult.style.display = "none";
        }
    });

    function commentFormSubmitHandler(e) {
        e.preventDefault();
        commentFormMain.classList.add("waiting");
        commentPostLoader.style.display = "block";

        if (!currentlySubmitting) {
            currentlySubmitting = true;
            var request = new XMLHttpRequest();
            request.open("POST", "/blog/comments/post/", true);
            request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");

            function cleanCommentFormSuccess() {
                commentPostResult.style.display = "none";
                commentForm.classList.add("collapsed");
                commentForm.classList.remove("expanded");
                setTimeout(function () { commentFormMain.classList.remove("waiting"); }, 500);
            }

            request.onreadystatechange = function() {
                /* allow to remove waiting screen after some time */
                setTimeout(function() { currentlySubmitting = false; }, 2000);
                commentPostLoader.style.display = "none";
                if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
                    res = JSON.parse(request.responseText);
                    var postCommentSuccess = res["post_comment_success"];
                    if (postCommentSuccess) {
                        if (userIsSuperuser) {
                            window.location.reload(false);
                        } else {
                        commentPostResultText.innerHTML = "Merci ! Votre commentaire sera publié après modération.";
                        timeoutCleanForm = setTimeout(cleanCommentFormSuccess, 6000);
                        }
                    } else {
                        commentPostResultText.innerHTML = "Une erreur est survenue. Merci de réessayer plus tard.<br/>(et désolée pour le dérangement)";
                    }
                } else {
                    commentPostResultText.innerHTML = "Une erreur est survenue. Merci de réessayer plus tard.<br/>(et désolée pour le dérangement)";
                }
                commentPostResult.style.display = "flex";
            }

            // ?? I can't find a way to build the x-www-form-urlencoded string
            // from the form data. And we can't use FormData because it would mess
            // with django's post_comment method. I guess I shall do it myself,
            // except it may break if the form changes...
            var urlEncodedData = "";
            var urlEncodedDataPairs = [];
            var inputs = commentForm.getElementsByTagName("input");
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
            var commentInput = commentForm.getElementsByTagName("textarea")[0];
            urlEncodedDataPairs.push(encodeURIComponent(commentInput.getAttribute('name'))
                + '=' + encodeURIComponent(commentInput.value));
            urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

            request.send(urlEncodedData);
        }
    }

    commentForm.addEventListener("submit", commentFormSubmitHandler);
}


/* Forms - Validate form inputs */

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
