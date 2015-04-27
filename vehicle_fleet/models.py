from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _
from decimal import Decimal
from base import fields


class Brands(models.Model):
    """
    Create Brands for vehicles, example: Kia, VMW, etc...
    """

    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        ordering = {'name', }

    def __unicode__(self):
        """
        Gets the unicode object representation
        :return: String
        """
        return _('Name: %s') % self.name


class Model(models.Model):
    """
    Create the vehicle model, example: SW4324
    """

    name = models.CharField(_('Name'), max_length=255)
    brand = models.ForeignKey('Brands', verbose_name=_('Brand'))

    class Meta:
        ordering = {'name', }

    def __unicode__(self):
        """
        Gets the unicode object representation
        :return: String
        """
        return _('Brand: %s, Model: %s') % (self.brand.name if self.brand.name else 'None', self.name)


class VehicleType(models.Model):
    """
    Create the vehicle type, example: truck, van, bus, etc...
    """

    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        ordering = {'name', }

    def __unicode__(self):
        """
        Gets the unicode object representation
        :return: String
        """
        return _('Name: %s') % self.name


class Vehicles(models.Model):
    """
    Create a vehicle
    """

    TRANSMISSION_TYPE_AUTO = 0
    TRANSMISSION_TYPE_MANUAL = 1

    TRANSMISSION_TYPE = (
        (TRANSMISSION_TYPE_AUTO, _('Automatic')),
        (TRANSMISSION_TYPE_MANUAL, _('Manual')),
    )

    FUEL_TYPE_DIESEL = 0
    FUEL_TYPE_GASOLINE = 1
    FUEL_TYPE_ELECTRICAL = 2
    FUEL_TYPE_HYBRID = 3

    FUEL_TYPE = (
        (FUEL_TYPE_DIESEL, _('Diesel')),
        (FUEL_TYPE_GASOLINE, _('Gasoline')),
        (FUEL_TYPE_ELECTRICAL, _('Electrical')),
        (FUEL_TYPE_HYBRID, _('Hybrid')),
    )

    OWNERSHIP_TYPE_RENTED = 0
    OWNERSHIP_TYPE_OWNED = 1

    OWNERSHIP_TYPE = (
        (OWNERSHIP_TYPE_RENTED, _('Rented')),
        (OWNERSHIP_TYPE_OWNED, _('Owned')),
    )

    USAGE_TYPE_CHARGE = 0

    USAGE_TYPE = (
        (USAGE_TYPE_CHARGE, _('Charge')),
    )

    plate_number = models.CharField(_('Plate number'), max_length=20)
    chassis_number = models.CharField(_('Chassis number'), max_length=100)
    brand = models.ForeignKey('Brands', verbose_name='Brand')
    model = models.ForeignKey('Model', verbose_name='Model')

    # Created year
    year = models.PositiveIntegerField(_('Model year'))

    driver_name = models.CharField(_('Driver Name'), max_length=255)
    color = fields.ColorField(_('Color'))
    transmission = models.SmallIntegerField(_('Transmission type'), choices=TRANSMISSION_TYPE,
                                            default=TRANSMISSION_TYPE_AUTO)

    fuel = models.SmallIntegerField(_('Fuel type'), choices=FUEL_TYPE,
                                    default=FUEL_TYPE_DIESEL)

    # TODO: For electrical types only?
    power = models.PositiveIntegerField(_('Power'), help_text=_('Battery power in Kw'))

    co2 = models.FloatField(_('CO2 emission of the vehicle'), default=Decimal('0.00'))

    ownership = models.SmallIntegerField(_('Ownership'), choices=OWNERSHIP_TYPE,
                                         default=OWNERSHIP_TYPE_OWNED)

    vehicle_usage = models.SmallIntegerField(_('Usage'), choices=USAGE_TYPE,
                                             default=USAGE_TYPE_CHARGE)

    vehicle_type = models.ForeignKey('VehicleType', verbose_name=_('Vehicle type'))

    # Cars have at lease two doors, except hoist right?
    doors = models.PositiveSmallIntegerField(_('Doors count'), default=2)

    # At lease the driver
    people_capacity = models.PositiveSmallIntegerField(_('Number of passengers'), default=1)

    class Meta:
        ordering = {'plate_number'}

    def __unicode__(self):
        """
        Gets the unicode object representation
        :return: String
        """
        return _('Car: %s, Model: ,Plate number:') % (self.brand.name, self.model.name, str(self.plate_number))

