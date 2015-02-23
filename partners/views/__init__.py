from base.models import Label, Partner
from clients import *


def role_set_label(request, pk):
    qs = Partner.objects.all()
    partner = get_object_or_404(qs, pk=pk)

    sys_role_name = partner.get_sys_partner_name()
    labels = Label.objects.available_for_obj(partner)
    label_pk = request.POST.get('label')
    print label_pk
    label = get_object_or_404(labels, pk=label_pk)
    if partner in label.partners.all():
        label.partners.remove(partner)
    else:
        label.partners.add(partner)
    label.save()
    return redirect(partner.get_absolute_url())
