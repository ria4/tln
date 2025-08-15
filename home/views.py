import math
import random

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import render
from django.views.generic import TemplateView

NIGHTSKY_SEEDS = [0, 1, 2, 3, 4]
# poor seeds can be removed if needed


class HomeView(TemplateView):
    template_name = "home/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seed = random.choice(NIGHTSKY_SEEDS)
        context["nightsky_seed"] = seed
        stars = []
        sparks = []

        # skip the random computations is there's a cache key for this seed
        cache_key = make_template_fragment_key("nightsky", [seed])
        if cache.has_key(cache_key):
            context["stars"] = stars
            context["sparks"] = sparks
            return context

        # else, build the stars and the sparks based on the seed
        random.seed(seed)

        stars_subgroups_n = 10
        stars_per_group_max = 60
        for _ in range(stars_subgroups_n):
            stars_subgroup = []
            stars_in_subgroup = random.randint(
                math.floor(stars_per_group_max * .6),
                stars_per_group_max,
            )
            for _ in range(stars_in_subgroup):
                star_cx = random.randint(0, 1000) / 10
                star_cy = random.randint(0, 1000) / 10
                star_r = random.randint(5, 10) / 10;
                stars_subgroup.append([star_cx, star_cy, star_r])
            stars.append(stars_subgroup)
        context["stars"] = stars

        sparks_n = 10
        for _ in range(sparks_n):
            spark_cx = random.randint(0, 1000) / 10
            spark_cy = random.randint(0, 1000) / 10
            spark_scale = random.randint(15, 25) / 100;
            sparks.append([spark_cx, spark_cy, spark_scale])
        context["sparks"] = sparks

        return context
