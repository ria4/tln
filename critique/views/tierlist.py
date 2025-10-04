import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from critique.forms import TierListForm
from critique.models import TierList


@permission_required('critique.all_rights')
def update_tierlist(req, tierlist, data):
    if not data.get('name'):
        return
    tierlist.name = data['name']
    tierlist.save()

@permission_required('critique.all_rights')
def add_tierlist(req):
    form = TierListForm(req.POST)
    tierlist = TierList()
    if form.is_valid():
        update_tierlist(req, tierlist, form.cleaned_data)
        return redirect('detail_tierlist', slug=tierlist.slug)

def detail_tierlist(req, slug):
    tierlist = get_object_or_404(TierList, slug=slug)
    #     Oeuvre.objects.prefetch_related(
    #         'comments',
    #         'spans__seance__cinema',
    #         'tags',
    #     ),
    #     slug=slug,
    # )
    tierlist_form = TierListForm(req.POST or {'name': tierlist.name})
    tierlist_form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    if req.POST and tierlist_form.is_valid():
        update_tierlist(req, tierlist, tierlist_form.cleaned_data)
        return redirect('detail_tierlist', slug=tierlist.slug)
    return render(req, 'critique/tierlist.html', locals())

@permission_required('critique.all_rights')
def delete_tierlist(req, slug):
    tierlist = get_object_or_404(TierList, slug=slug)
    tierlist.delete()
    return redirect('list_tags')
