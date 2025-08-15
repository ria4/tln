import math
import random

from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seed = 0
        # skip the random computations is there's a cache key for this seed
        random.seed(seed)
        stars = []
        stars_subgroups_n = 10
        stars_per_group_max = 60
        for i in range(stars_subgroups_n):
            stars_subgroup = []
            stars_in_subgroup = random.randint(
                math.floor(stars_per_group_max * .6),
                stars_per_group_max,
            )
            for j in range(stars_in_subgroup):
                star_cx = random.randint(0, 1000) / 10
                star_cy = random.randint(0, 1000) / 10
                star_r = random.randint(5, 10) / 10;
                stars_subgroup.append([star_cx, star_cy, star_r])
            stars.append(stars_subgroup)
        context["stars"] = stars
        return context
