import datetime
import random

from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.timezone import localtime

from critique.models import OEUVRE_MTYPES
from critique.models import OeuvreSpan


OEUVRE_MTYPES_INDEXES = {
    mtype[0]: i
    for i, mtype in enumerate(OEUVRE_MTYPES)
    if mtype[0] != "album"
}

def get_formatted_span_start(span):
    date_start = localtime(span.date_start)
    if span.date_start_du:
        # floor the date to the first day of the current month
        date_start = date_start.replace(day=1)
    return date_start.strftime("%Y-%m-%d")

def get_formatted_span_end(span):
    if span.ongoing:
        date_end = datetime.datetime.now() + datetime.timedelta(days=1)
    elif span.date_end_du:
        # ceil the date to the first day of the following month
        date_end = localtime(span.date_end).replace(day=1)
        date_end = datetime.datetime(
            date_end.year + int(date_end.month / 12),
            (date_end.month % 12) + 1,
            1,
        )
    else:
        date_end = localtime(span.date_end) + datetime.timedelta(days=1)
    return date_end.strftime("%Y-%m-%d")

    
# Chronologie

def get_chronologie(req):
    # define one group for each media type
    chrono_groups = [
        {"id": i, "content": mtype[1], "className": f"vis-group-{mtype[0]}"}
        for i, mtype in enumerate(OEUVRE_MTYPES)
        if mtype[0] != "album"
    ]

    # define the spans queryset
    spans_start = datetime.datetime(2022, 5, 1)
    # there are earlier spans, but they're related to seances
    # we don't want to show them here, because they would be isolated
    spans = (
        OeuvreSpan.objects.filter(date_start__gte=spans_start)
        .exclude(oeuvre__mtype="album")
        .select_related("oeuvre", "seance")
        .prefetch_related("oeuvre__tags")
    )

    # format the spans
    chrono_items = []
    for i, span in enumerate(spans):
        class_name = f"vis-item-{i} vis-item-animated-{random.randint(0, 10)}"
        group = ""
        h2 = ""
        img_url = ""
        if hasattr(span, "seance"):
            class_name += " vis-item-seance"
            group = OEUVRE_MTYPES_INDEXES.get("film")
            if span.seance.seance_title:
                h2 = span.seance.seance_title
        if span.oeuvre:
            if not group:
                group = OEUVRE_MTYPES_INDEXES.get(span.oeuvre.mtype)
            if not h2:
                h2 = f"{span.oeuvre.title_vf} ({span.oeuvre.year})"
            if span.oeuvre.image:
                img_url = span.oeuvre.image.url
            for tag in span.oeuvre.tags.all():
                class_name += f" vis-item-tag-{tag.slug}"
        chrono_items.append(
            {
                "id": i,
                "className": class_name,
                "group": group,
                "start": get_formatted_span_start(span),
                "end": get_formatted_span_end(span),
                "content": render_to_string(
                    "critique/chronologie_items.html",
                    {
                        "linkable": span.oeuvre is not None,
                        "span_h2": h2,
                        "span_img_url": img_url,
                        "span": span,
                    },
                ),
            }
        )

    return render(
        req,
        'critique/chronologie.html',
        {"chrono_groups": chrono_groups, "chrono_items": chrono_items},
    )
