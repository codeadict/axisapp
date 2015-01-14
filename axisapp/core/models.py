# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.db import models


class IdentificationType(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Identification Type')
        verbose_name_plural = _('Identification Types')

    def short_name(self):
        return self.name[:3]


class Partner(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    lastname = models.CharField(_('Last Name'), max_length=200)
    shortname = models.CharField(_('Short Name'), max_length=100, blank=True)
    typeid = models.ForeignKey(IdentificationType)
    identification = models.CharField(_('Identification'), max_length=200)
    address = models.CharField(_('Street Address'), max_length=200)
    phone = models.CharField(_('Phone'), max_length=100, blank=True)
    cellphone = models.CharField(_('Cellphone'), max_length=100, blank=True)
    email = models.CharField(_('Email'), max_length=200, blank=True)
    fax = models.CharField(_('Fax'), max_length=100, blank=True)
    trade_name = models.CharField(_('Trade Name'), max_length=100, null=True, blank=True)
    special_contributor = models.BooleanField(_('Special Contributor'), False)
    is_provider = models.BooleanField(_('Is Provider'), False)
    is_customer = models.BooleanField(_('Is Customer'), False)


    @staticmethod
    def have_tradename(self):
        return self.tradename != ''

    def business_name(self):
        return self.name

    def __unicode__(self):
        return self.name

    def full_name(self):
        return self.fullname

    def name_identification(self):
        return "%s - %s" % (self.identification, self.name)

    class Meta:
        abstract = True
        ordering = ['name']

    def save(self, **kargs):
        super(Partner, self).save(kargs)
