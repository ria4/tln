from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import redirect

from critique.forms import OeuvreSpanForm
from critique.models import OeuvreSpan
from critique.utils import strftime_local


# OeuvreSpan

@permission_required('critique.all_rights')
def add_oeuvrespan(req):
    form = OeuvreSpanForm(req.POST)
    oeuvre_span = OeuvreSpan()
    if form.is_valid():
        update_oeuvrespan(req, oeuvre_span, form)
        return redirect('detail_oeuvre', slug=oeuvre_span.oeuvre.slug)

@permission_required('critique.all_rights')
def update_oeuvrespan(req, oeuvre_span, form):
    oeuvre_span.date_start = form.cleaned_data.get('date_start')
    oeuvre_span.date_start_du = form.cleaned_data.get('date_start_du', False)
    oeuvre_span.date_end = form.cleaned_data.get('date_end')
    oeuvre_span.date_end_du = form.cleaned_data.get('date_end_du', False)
    oeuvre_span.oeuvre = form.cleaned_data.get('oeuvre')
    oeuvre_span.ongoing = form.cleaned_data.get('ongoing', False)
    oeuvre_span.save()

def update_oeuvrespan_with_form(oeuvrespan, form):
    oeuvrespan.oeuvre = form.cleaned_data['oeuvre']
    oeuvrespan.date_start = form.cleaned_data['date_start']
    oeuvrespan.date_start_du = form.cleaned_data['date_start_du']
    oeuvrespan.date_end = form.cleaned_data['date_end']
    oeuvrespan.date_end_du = form.cleaned_data['date_end_du']
    oeuvrespan.ongoing = form.cleaned_data['ongoing']
    oeuvrespan.save()

@permission_required('critique.all_rights')
def update_latest_oeuvrespan(req, slug):
    oeuvrespan_form = OeuvreSpanForm(req.POST)
    if req.POST and oeuvrespan_form.is_valid():
        span = OeuvreSpan.objects.filter(oeuvre__slug=slug).order_by('-id').first()
        update_oeuvrespan_with_form(span, oeuvrespan_form)
    return redirect('detail_oeuvre', slug=slug)

@permission_required('critique.all_rights')
def delete_latest_oeuvrespan(req, slug):
    oeuvrespans = OeuvreSpan.objects.filter(oeuvre__slug=slug).order_by('-id')
    if not oeuvrespans.exists():
        raise Http404
    oeuvrespan = oeuvrespans.first()
    slug = oeuvrespan.oeuvre.slug
    oeuvrespan.delete()
    return redirect('detail_oeuvre', slug=slug)

def get_oeuvrespan_form_data(oeuvrespan):
    form_data = {}
    if hasattr(oeuvrespan, 'oeuvre'):
        form_data['oeuvre'] = oeuvrespan.oeuvre;
    form_data['date_start'] = strftime_local(oeuvrespan.date_start)
    form_data['date_start_du'] = oeuvrespan.date_start_du
    form_data['date_end'] = strftime_local(oeuvrespan.date_end)
    form_data['date_end_du'] = oeuvrespan.date_end_du
    form_data['ongoing'] = oeuvrespan.ongoing
    return form_data
