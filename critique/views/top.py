from datetime import datetime

from django.shortcuts import redirect
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

    def get(self, req, year=None, **kwargs):
        if year is not None:
            if year < 2012:
                return redirect("top_films")
            endyear = max(
                [
                    int(s[-4:])
                    for s in OeuvreTag.objects.filter(
                        name__startswith="top.ciné."
                    ).values_list("name", flat=True)
                ]
            )
            if year > endyear:
                return redirect("top_films", year=endyear)
        return super().get(req, year, **kwargs)

    def get_queryset(self):
        year = self.kwargs.get("year")
        top_name = "top.ciné" if year is None else f"top.ciné.{year}"
        return OeuvreTag.objects.get(name=top_name).oeuvres.order_by("?")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if year := self.kwargs.get("year"):
            context["year"] = year

        # assemble the attributes used when creating the links to each top ciné year
        endyear = max(
            [
                int(s[-4:])
                for s in OeuvreTag.objects.filter(
                    name__startswith="top.ciné."
                ).values_list("name", flat=True)
            ]
        )
        links_attrs = []
        mod = (endyear - 2011) % 3
        links_attrs_first = [[2011, f"189x-{endyear}"]]
        for i in range(mod):
            link_year = 2011 + i + 1
            links_attrs_first.append([link_year, str(link_year)])
        links_attrs.append(links_attrs_first)
        link_year_offset = 2011 + mod + 1
        while link_year_offset <= endyear:
            link_year_group = []
            for i in range(3):
                link_year_group.append([link_year_offset + i, str(link_year_offset + i)])
            links_attrs.append(link_year_group)
            link_year_offset += 3
        context["links_attrs"] = links_attrs

        return context


# Top Jeux

class TopJeuxView(ListView):
    queryset = OeuvreTag.objects.get(name="top.jeux").oeuvres.order_by("?")
    template_name = "critique/top_jeux.html"
    context_object_name = "oeuvres"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["endyear"] = datetime.now().year - 1
        return context
