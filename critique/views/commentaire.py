import datetime

from django.contrib.auth.decorators import permission_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models.functions import Length
from django.shortcuts import get_object_or_404, redirect, render

from critique.forms import CommentaireForm
from critique.models import Commentaire, Oeuvre
from critique.utils import strftime_local


def get_comment_form_data(comment):
    form_data = {}
    form_data['title'] = comment.title
    form_data['date'] = strftime_local(comment.date)
    if hasattr(comment, 'date_mu'):
        form_data['no_month'] = comment.date_mu
    if hasattr(comment, 'date_du'):
        form_data['no_day'] = comment.date_du
    form_data['content'] = comment.content
    return form_data

@permission_required('critique.all_rights')
def update_latest_comment(req, slug):
    comment_form = CommentaireForm(req.POST)
    if req.POST and comment_form.is_valid():
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
        comments = sorted(oeuvre.comments.all(), key=lambda p: p.date, reverse=True)
        update_comment_with_form(comments[0], comment_form)
    return redirect('detail_oeuvre', slug=slug)

def update_comment_with_form(comment, form):
    comment.title = form.cleaned_data['title']
    dt = datetime.datetime.combine(
        form.cleaned_data['date'],
        datetime.datetime.now().time(),
    )
    comment.date = dt.replace(microsecond=0)
    comment.date_mu = form.cleaned_data['no_month']
    comment.date_du = form.cleaned_data['no_day']
    comment.content = form.cleaned_data['content']
    comment.save()

@permission_required('critique.all_rights')
def add_comment(req, slug):
    form = CommentaireForm(req.POST)
    if form.is_valid():
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
        comment = Commentaire(oeuvre=oeuvre)
        update_comment_with_form(comment, form)
        oeuvre.comments.add(comment)
    return redirect('detail_oeuvre', slug=slug)

@permission_required('critique.all_rights')
def delete_latest_comment(req, slug):
    oeuvre = get_object_or_404(
        Oeuvre.objects.prefetch_related('comments').order_by('-comment__date'),
        slug=slug,
    )
    if oeuvre.comments.exists():
        oeuvre.comments.first().delete()
    return redirect('detail_oeuvre', slug=slug)

def list_notes(req, mtype="all", page=1):
    if mtype == "all":
        notes_full = Commentaire.objects.annotate(content_len=Length('content')) \
                                        .filter(content_len__gt=400)
    else:
        notes_full = Commentaire.objects.filter(oeuvre__mtype=mtype) \
                                        .annotate(content_len=Length('content')) \
                                        .filter(content_len__gt=400)
    notes_full = notes_full.order_by('-date')
    paginator = Paginator(notes_full, 20)
    try:
        notes = paginator.page(page)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    context = {'notes': notes, 'mtype': mtype}
    return render(req, 'critique/notes.html', context)
