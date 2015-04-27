from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _
from decimal import Decimal
from mptt.models import MPTTModel, TreeForeignKey
from base.models import Partner


def date_default():
    """
    :return: timezone timedate
    """
    return timezone.now()


class IceTax(models.Model):
    """
    Class to handle the ICE taxes to the product
    """

    name = models.CharField(_("Name"), max_length=255)
    code = models.IntegerField(_("Code"), max_length=255)
    percent = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0))

    class Meta:
        ordering = ['name']
        verbose_name = _('I.C.E. tax')
        verbose_name_plural = _('I.C.E taxes')

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s' % (self.name, self.code)


class ProductsCategory(MPTTModel):
    """
    Products category, created as MTTP
    """

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    full_name = models.CharField(verbose_name=_("Full name"), max_length=255)
    description = models.CharField(verbose_name=_("Name"), max_length=2048, blank=True, null=True)
    parent = TreeForeignKey("self", verbose_name=_("Sub categories"),
                           blank=True, null=True, related_name="sub_categories")
    image = models.ImageField(_('Image'), upload_to='categories', blank=True,
                              null=True, max_length=255)

    #Defaults attributes belong to the category and can be used for the products
    default_attributes = models.ManyToManyField('products.ProductAttribute', verbose_name="Attributes",
                                                related_name='category_attributes', blank=True, null=True)

    date_created = models.DateField(_("Date Created"), default=date_default)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s %s %s' % (self.name, " with ", self.get_children().count(), " childs")

    class MPTTMeta:
        ordering = ['full_name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class ProductAttribute(models.Model):
    """
    Product attribute
    """
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')


class ProductAttributeValueUnitMeasure(models.Model):
    """
    Value unit of measure, representation of
    the unit measure (Kg, Lb, cm, Km, etc...)
    """

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    representation_sign = models.CharField(verbose_name=_("Representation sign"), max_length=5)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return self.name

    class Meta:
        ordering = ['name']


class ProductAttributeValue(models.Model):
    """
    Product Attribute value
    """

    attr = models.ForeignKey('products.ProductAttribute', related_name='value', verbose_name=_("Attribute"),
                             default=None)
    #TODO: Make a better attribute value to support all attribute types (string, int, float, bool)
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    unit_measure = models.ForeignKey('products.ProductAttributeValueUnitMeasure', verbose_name=_("Unit of measure"),
                                     related_name='unit_measure')
    value = models.FloatField(verbose_name=_("Value"), null=True, blank=True)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return "%s%s%s" % (self.name, ugettext(' in '), self.unit_measure.name)

    class Meta:
        ordering = ['name']


class ProductImage(models.Model):
    """
    Product images
    """

    identification = models.CharField(verbose_name=_("Image identification"), max_length=255,
                                      blank=True, null=True)
    display_order = models.IntegerField(verbose_name=_("Display order"))
    image = models.ImageField(_('Image'), upload_to='products', max_length=255)
    date_uploaded = models.DateField(verbose_name=_("Date added"), default=date_default)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return self.identification if self.identification else self.image.name

    class Meta:
        ordering = ['identification']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class SelleAbleItem(models.Model):
    """
    Abstract class for products and services
    """

    ITEM_STATE_NOT_ACTIVE = 0
    ITEM_STATE_ACTIVE = 1

    ITEM_STATE = (
        (ITEM_STATE_NOT_ACTIVE, _("Not Active")),
        (ITEM_STATE_ACTIVE, _("Active"))
    )

    ITEM_TAX_IVA_NONE = 0
    ITEM_TAX_IVA_ZERO = 1
    ITEM_TAX_IVA_TWELVE = 2

    ITEM_TAX_IVA = (
        (ITEM_TAX_IVA_NONE, _("No I.V.A.")),
        (ITEM_TAX_IVA_ZERO, _("I.V.A. 0%")),
        (ITEM_TAX_IVA_TWELVE, _("I.V.A. 12%")),
    )

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    description = models.CharField(verbose_name=_("Description"), max_length=2048, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255, blank=True)

    type = models.CharField(_('Type'), max_length=50, editable=False, db_index=True)
    image = models.ForeignKey('products.ProductImage', null=True)

    # This is the price show it to the client
    price_excl_tax = models.FloatField(verbose_name=_("Price"), default=0.00)
    # This is only to calculate profit margin.
    cost_price = models.FloatField(verbose_name=_("Cost price"), default=0.00)

    # Taxes
    iva_tax = models.IntegerField(verbose_name=_("Taxes"), choices=ITEM_TAX_IVA, default=ITEM_TAX_IVA_TWELVE)

    active = models.IntegerField(verbose_name=_("Active"), choices=ITEM_STATE,
                                 default=ITEM_STATE_ACTIVE)

    attributes = models.ManyToManyField('products.ProductAttribute', verbose_name=_('Attributes'),
                                        null=True, blank=True)

    category = models.ForeignKey('products.ProductsCategory', verbose_name=_('Category'))

    related_items = models.ForeignKey('products.Product', verbose_name=_('Related items'),
                                      blank=True, null=True)

    # Product score - used by analytics app
    score = models.FloatField(_('Score'), default=Decimal(0), db_index=True)

    date_created = models.DateField(_("Date Created"), default=date_default)

    selleabe_item_type_name = property(lambda self: self.partner_model())

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def save(self, *args, **kw):
        if not self.type:
            self.type = self.__class__.__name__
        return super(SelleAbleItem, self).save(*args, **kw)

    @property
    def type_verbose_name(self):
        return self.selleable_obj()._meta.verbose_name

    def object_model(self):
        return self.type

    def selleable_obj(self):
        return getattr(self, self.type.lower())

    def is_product(self):
        return self.type == 'Product'

    def is_service(self):
        return self.type == 'Service'

    def _get_partner_id(self):
        # make sure we always use the id even if this method is called on child instances.
        return getattr(self, 'selleableitem_ptr_id', self.id)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return "%s %s" % (self.name, self.description if self.description else _('No description'))


class Product(SelleAbleItem):
    """
    Products
    """

    # Universal product code
    upc = models.CharField(_("UPC"), max_length=64, blank=True, null=True, unique=True,
                           help_text=_("Universal Product Code (UPC)"))

    # ICE taxes
    ice_tax = models.ForeignKey('products.IceTax', verbose_name=_('Ice'), null=True, blank=True)

    # It could be big numbers in here
    items_stock_number = models.BigIntegerField(verbose_name=_("Number in stock"), blank=True,
                                                default=0)
    # Low stock threshold
    low_stock_threshold = models.IntegerField(verbose_name=_("Low Stock Threshold"),
                                              blank=True, null=True)

    class Meta:
        ordering = ['upc']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return "%s %s" % (self.name, self.upc if self.upc else "No UPC")

    @property
    def is_low_stock(self):
        """
        Return a low stock alarm
        :return: boolean
        """
        if self.items_stock_number < self.low_stock_threshold:
            return True
        else:
            return False


class Service(SelleAbleItem):
    """
    Service
    """

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return "%s" % self.name
