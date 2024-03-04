/* Autofocus on input field, desktop-only */
/* (the html 'autofocus' attribute works on desktop but not on mobile) */

if (!isTouchDevice()) {
    var inputField = document.getElementById("id_content");
    inputField.focus();
}
