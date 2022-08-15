# Login form error messages

LOGIN_FAILED_WRONG_CREDENTIALS = "wrong_credentials"
MISSING_PERM_TO_PHOTO_GALLERY = "no_perm_photo_gallery"
MISSING_PERM_TO_BLOG_ENTRY = "no_perm_blog_entry"

LOGIN_FORM_ERROR_CODES = [
    (LOGIN_FAILED_WRONG_CREDENTIALS, "Identifiant inconnu, ou mot de passe invalide."),
    (MISSING_PERM_TO_PHOTO_GALLERY, "Identifiant invalide pour cette galerie."),
    (MISSING_PERM_TO_BLOG_ENTRY, "Identifiant invalide pour cet article de blog."),
]
LOGIN_FORM_ERROR_CODES_MAP = dict(LOGIN_FORM_ERROR_CODES)
