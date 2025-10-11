import datetime

from dal.autocomplete import Select2QuerySetView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from critique.forms import TierForm, TierListForm
from critique.models import Tier, TierList


def get_tier_form_data(tier):
    return {
        "tier_list": tier.tier_list,
        "name": tier.name,
        "position": tier.position,
        "oeuvres": tier.oeuvres.all(),
    }


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
    tierlist = get_object_or_404(
        TierList.objects.prefetch_related("tiers__oeuvres"),
        slug=slug,
    )
    tierlist_form = TierListForm(req.POST or {'name': tierlist.name})
    tierlist_form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    if req.POST and tierlist_form.is_valid():
        update_tierlist(req, tierlist, tierlist_form.cleaned_data)
        return redirect('detail_tierlist', slug=tierlist.slug)
    tier_forms = []
    for tier in tierlist.tiers.all():
        tier_form = TierForm(
            get_tier_form_data(tier),
            auto_id=f"id_tier_%s_{tier.position}",
        )
        tier_form.fields["oeuvres"].widget.attrs.update({"class": "focus-on-reveal"})
        tier_forms.append((tier.position, tier_form))
    return render(req, 'critique/tierlist.html', locals())

@permission_required('critique.all_rights')
def delete_tierlist(req, slug):
    tierlist = get_object_or_404(TierList, slug=slug)
    tierlist.delete()
    return redirect('list_tags')


@permission_required('critique.all_rights')
def update_tier(req, tier, data):
    tier.tier_list = data['tier_list']
    tier.name = data['name']
    tier.position = data['position']
    tier.save()
    tier.oeuvres.set(data['oeuvres'])

@permission_required('critique.all_rights')
def add_tier(req):
    form = TierForm(req.POST)
    tier = Tier()
    if form.is_valid():
        update_tier(req, tier, form.cleaned_data)
        return redirect('detail_tierlist', slug=tier.tier_list.slug)

def detail_tier(req, slug, position):
    tier = get_object_or_404(Tier, tier_list__slug=slug, position=position)
    if req.POST:
        tier_form = TierForm(req.POST)
    else:
        tier_form = TierForm(get_tier_form_data(tier))
    tier_form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    if req.POST and tier_form.is_valid():
        update_tier(req, tier, tier_form.cleaned_data)
    return redirect('detail_tierlist', slug=slug)

@permission_required('critique.all_rights')
def delete_tier(req, slug, position):
    tier = get_object_or_404(Tier, tier_list__slug=slug, position=position)
    tier.delete()
    return redirect('detail_tierlist', slug=slug)


class TierListAutocomplete(PermissionRequiredMixin, Select2QuerySetView):
    permission_required = 'critique.all_rights'
    paginate_by = 30  # equivalent to pagination off

    def get_queryset(self):
        qs = TierList.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
