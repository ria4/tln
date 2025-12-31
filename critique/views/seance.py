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

def list_seances(req, year=2025):
    form = SeanceForm(req.POST)
    if req.POST and form.is_valid():
        update_seances(req, form)

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

    return render(req, 'critique/seances.html', {'year': year, 'seances': seances})
