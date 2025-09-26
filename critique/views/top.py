from django.views.generic.list import ListView

from critique.models import Commentaire, OeuvreTag


# Top Textes

class TopTextesView(ListView):
    queryset = Commentaire.objects.filter(starred=True).order_by('-date')
    template_name = 'critique/top_textes.html'


# Thinky Games database excerpts

class TgdbExcerptsView(ListView):
    queryset = Commentaire.objects.filter(tgdb=True).order_by('-date')
    template_name = 'critique/tgdb_excerpts.html'


# Top Films

class TopFilmsView(ListView):
    template_name = "critique/top_films.html"
    context_object_name = "oeuvres"

    def get_queryset(self):
        year = self.kwargs.get("year")
        top_name = "top.ciné" if year is None else f"top.ciné.{year}"
        return OeuvreTag.objects.get(name=top_name).oeuvres.order_by("?")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if year := self.kwargs.get("year"):
            context["year"] = year
        return context


# Top Jeux

class TopJeuxView(ListView):
    queryset = OeuvreTag.objects.get(name="top.jeux").oeuvres.order_by("?")
    template_name = "critique/top_jeux.html"
    context_object_name = "oeuvres"
