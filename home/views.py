import random

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["textlines"] = [
            {
                "left": random.randrange(-60, 100),
                "top": random.randrange(-60, 100),
                "rotate": random.randrange(-80, 80),
                "font_size": random.randrange(4, 10),
            } for i in range(500)
        ]
        return context
