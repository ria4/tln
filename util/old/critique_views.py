
#import base64
#from tempfile import NamedTemporaryFile
#from shutil import copyfileobj

#def detail_oeuvre_tmpfile(req, slug):
#    """
#    Version qui crée un fichier temporaire.
#    """
#    try:
#        oeuvre = get_object_or_404(Oeuvre, slug=slug)
#        tmpFileObj = NamedTemporaryFile(dir='critique/static/critique')
#        copyfileobj(oeuvre.info.image, tmpFileObj)
#        tmpFileObj.seek(0, 0)
#        tmpFileObjName = 'critique/' + os.path.basename(tmpFileObj.name)
#    except Oeuvre.MultipleObjectsReturned:
#        raise Http404
#    return render(req, 'critique/oeuvre.html', {'oeuvre': oeuvre, 'img_url': img_name})

#def detail_oeuvre_b64(req, slug):
#    """
#    Version qui transmet l'image en base64.
#    """
#    try:
#        oeuvre = get_object_or_404(Oeuvre, slug=slug)
#        img = oeuvre.info.image.read()
#        img_b64 = base64.encodebytes(img).decode('utf-8')
#    except Oeuvre.MultipleObjectsReturned:
#        raise Http404
#    return render(req, 'critique/oeuvre.html', {'oeuvre': oeuvre, 'img_b64': img_b64})

