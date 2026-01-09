import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render

from critique.forms import SeanceForm
from critique.models import OeuvreSpan, Seance


# Séances

@permission_required('critique.all_rights')
def update_seance(req, seance, data):
    if not (data.get('film') or data.get('seance_title')):
        return

    if data.get('film'):
        oeuvre = data.get('film')
    else:
        oeuvre = None
        seance.seance_title = data['seance_title']

    date = data['date']
    dtime = datetime.time(int(data['hour'][:2]), int(data['hour'][3:5]))
    date_start = datetime.datetime.combine(date, dtime)

    span = OeuvreSpan(
        oeuvre=oeuvre,
        date_start=date_start,
        date_start_du=data.get('no_day', False),
        date_start_mu=data.get('no_month', False),
        date_end=date_start,
        date_end_du=data.get('no_day', False),
        date_end_mu=data.get('no_month', False),
    )
    span.save()

    seance.oeuvre_span = span
    seance.cinema = data['cinema']
    seance.save()

@permission_required('critique.all_rights')
def add_seance(req):
    form = SeanceForm(req.POST)
    seance = Seance()
    if form.is_valid():
        update_seance(req, seance, form.cleaned_data)
        return redirect('list_seances', year=seance.oeuvre_span.date_start.year)

def list_seances(req, year=None):
    form = SeanceForm(req.POST)
    if req.POST and form.is_valid():
        update_seances(req, form)

    current_year = datetime.datetime.now().year
    if year is None:
        year = current_year
    elif year > current_year:
        return redirect('list_seances')

    if year > 2011:
        start = datetime.datetime(year, 1, 1)
        end = datetime.datetime(year + 1, 1, 1)
    else:
        year = 2011
        start = datetime.datetime(1998, 1, 1)
        end = datetime.datetime(2012, 1, 1)
    seances = (
        Seance.objects.filter(
            oeuvre_span__date_start__gte=start,
            oeuvre_span__date_start__lt=end,
        ).select_related(
            'cinema',
            'oeuvre_span',
        ).order_by('oeuvre_span__date_start')
    )

    # assemble the attributes used when creating the links to each seance year
    links_attrs = []
    mod = (current_year - 2011) % 3
    links_attrs_first = [[2011, "avant 2012"]]
    for i in range(mod):
        link_year = 2011 + i + 1
        links_attrs_first.append([link_year, str(link_year)])
    links_attrs.append(links_attrs_first)
    link_year_offset = 2011 + mod + 1
    while link_year_offset <= current_year:
        link_year_group = []
        for i in range(3):
            link_year_group.append([link_year_offset + i, str(link_year_offset + i)])
        links_attrs.append(link_year_group)
        link_year_offset += 3

    return render(
        req,
        'critique/seances.html',
        {'year': year, 'seances': seances, 'current_year': current_year, 'links_attrs': links_attrs},
    )
