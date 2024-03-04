/* Autofocus on input field, desktop-only */
/* (the html 'autofocus' attribute works on desktop but not on mobile) */

if (!isTouchDevice()) {
    const inputFieldTodoItem = document.getElementById("id_content");
    const inputFieldTodoList = document.getElementById("id_title");
    let inputField = null;
    if (inputFieldTodoItem) { inputField = inputFieldTodoItem; }
    else if (inputFieldTodoList) { inputField = inputFieldTodoList; }
    if (inputField) { inputField.focus(); }
}
