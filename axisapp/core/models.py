from django.db import models


class NameBase(models.Model):
    """
    Abstract model for small tables that have name field
    """
    name = models.CharField(_('Name'), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
