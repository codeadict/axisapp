from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from base.models import Partner


def date_default():
    """
    :return: timezone timedate
    """
    return timezone.now()


class Taxes(models.Model):
    """
    Class to handle the taxes to the product
    """

    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s' % self.name


class TaxesValue(models.Model):
    """
    Class to handle the taxes value
    """

    tax_id = models.ForeignKey('products.Taxes', blank=True, null=True)

    # It must be a flat value
    value = models.FloatField(_("Value"), blank=True, null=True)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s' % self.name


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
    value_id = models.ForeignKey('products.ProductAttributeValue', verbose_name=_("Value"),
                                 blank=True, null=True)

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

    identification = models.CharField(verbose_name=_("Image identification"), max_length=255)
    display_order = models.IntegerField(verbose_name=_("Display order"))
    image = models.ImageField(_('Image'), upload_to='products', blank=True,
                              null=True, max_length=255)
    date_uploaded = models.DateField(verbose_name=_("Date added"), default=date_default)

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return "%s%s%s" % (self.identification, ugettext(' at position '), self.display_order)

    class Meta:
        ordering = ['identification']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


#TODO: Create a class for the tax (it could be ICE and IVA or others)
class Product(models.Model):
    """
    Products
    """

    PRODUCT_STATE_NOT_ACTIVE = 0
    PRODUCT_STATE_ACTIVE = 1

    PRODUCT_STATE = (
        (PRODUCT_STATE_NOT_ACTIVE, _("Not Active")),
        (PRODUCT_STATE_ACTIVE, _("Active"))
    )

    PRODUCT_TYPE_CONSUMABLE = 0
    PRODUCT_TYPE_SERVICE = 1

    PRODUCT_TYPE = (
        (PRODUCT_TYPE_CONSUMABLE, _("Consumable")),
        (PRODUCT_TYPE_SERVICE, _("Service"))
    )

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    description = models.CharField(verbose_name=_("Description"), max_length=2048, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255, blank=True)

    type = models.IntegerField(verbose_name=_("Type"), choices=PRODUCT_TYPE, default=0)
    #price = models.FloatField(verbose_name=_("Price"), default=0.00)
    #cost_price = models.FloatField(verbose_name=_("Cost price"), default=0.00)
    image = models.ForeignKey('products.ProductImage', null=True)

    # Taxes
    taxes = models.ManyToManyField('products.Taxes', verbose_name=_("Taxes"), blank=True, null=True)

    # Universal product code
    upc = models.CharField(_("UPC"), max_length=64, blank=True, null=True, unique=True,
                           help_text=_("Universal Product Code (UPC)"))

    active = models.IntegerField(verbose_name=_("Active"), choices=PRODUCT_STATE,
                                 default=PRODUCT_STATE_ACTIVE)
    attributes = models.ManyToManyField('products.ProductAttribute', verbose_name=_('Attributes'),
                                        null=True, blank=True)

    category = models.ForeignKey('products.ProductsCategory', verbose_name=_('Category'))

    related_products = models.ForeignKey('products.Product', verbose_name=_('Related products'),
                                         related_name='related', blank=True, null=True)

    # Product score - used by analytics app
    score = models.FloatField(_('Score'), default=0.00, db_index=True)

    date_created = models.DateField(_("Date Created"), default=date_default)

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


class Stock(models.Model):
    """
    It handle the stock from a product
    """

    product = models.ForeignKey('products.Product', verbose_name=_("Product"), db_index=True)

    # This is the price show it to the client
    price_excl_tax = models.FloatField(verbose_name=_("Price"), default=0.00)
    # This is only to calculate profit margin.
    cost_price = models.FloatField(verbose_name=_("Cost price"), default=0.00)

    #TODO: DO we have to create a model for this?
    # Currency
    price_currency = models.CharField(verbose_name=_("Currency"), max_length=12)

    # It could be big numbers in here
    items_number = models.BigIntegerField(verbose_name=_("Number in stock"), blank=True)
    low_stock_threshold = models.IntegerField(verbose_name=_("Low Stock Threshold"),
                                              blank=True, null=True)

    date_created = models.DateField(_("Date Created"), default=date_default)
    date_updated = models.DateField(_("Date Updated"), default=date_default)

    class Meta:
        verbose_name = _("Stock record")
        verbose_name_plural = _("Stock records")

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return "%s %s" % (self.product.name, self.price_excl_tax)

    @property
    def is_low_stock(self):
        """
        Return a low stock alarm
        :return: boolean
        """
        if self.items_number < self.low_stock_threshold:
            return True
        else:
            return False