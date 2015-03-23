__author__ = 'yo'

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm, Select
from suit.widgets import NumberInput

from products import models
from base import form_helper
from base.default_views import DeleteObject


class ProductSearchForm(form_helper.GenericFilterForm):
    name = forms.CharField(label=_('Name'))
    description = forms.CharField(label=_('Description'))
    tittle = forms.CharField(label=_('Tittle'))
    upc = forms.CharField(label=_('UPC'))
    #active = forms.IntegerField(label=_('Active'))
    category = forms.CharField(label=_('Category'))
    #type = forms.IntegerField(label=_('Type'))
    created_after = forms.DateTimeField(label=_('Created After'))
    created_before = forms.DateTimeField(label=_('Created Before'))

    fields_mapping = {
        'name': 'name__icontains',
        'description': 'description__icontains',
        'tittle': 'tittle__icontains',
        'upc': 'upc__eql',
        #s'active': 'active__eql',
        'category': 'category__name__eql',
        #'type': 'type__eql',
        'created_after': 'date_created__gte',
        'created_before': 'date_created__lte',
    }

    model = models.Product

    def __init__(self, *args, **kwargs):
        super(ProductSearchForm, self).__init__(*args, **kwargs)


class CreateProductForm(form_helper.TCModelForm):
    class Meta:
        model = models.Product
        #exclude = []


class UpdateProductForm(form_helper.TCModelForm):
    class Meta:
        model = models.Product

    def __init__(self, **kwargs):
        super(UpdateProductForm, self).__init__(**kwargs)


class DeleteProductsForm(DeleteObject):
    class Meta:
        model = models.Product
        exclude = []

#------------------------------------
class ProductsCategorySearchForm(form_helper.GenericFilterForm):
    name = forms.CharField(label=_('Name'))
    full_name = forms.CharField(label=_('Description'))
    created_after = forms.DateTimeField(label=_('Created After'))
    created_before = forms.DateTimeField(label=_('Created Before'))

    fields_mapping = {
        'name': 'name__icontains',
        'full_name': 'full_name__icontains',
        'created_after': 'date_created__gte',
        'created_before': 'date_created__lte',
    }
    model = models.Product

    def __init__(self, *args, **kwargs):
        super(ProductsCategorySearchForm, self).__init__(*args, **kwargs)


class CreateProductsCategoryForm(form_helper.TCModelForm):
    """
    Form to create the Products Category
    """

    class Meta:
        model = models.ProductsCategory
        exclude = []


class UpdateProductsCategoryForm(form_helper.TCModelForm):
    """
    Form to update the Products Category
    """

    class Meta:
        model = models.ProductsCategory

    def __init__(self, **kwargs):
        super(UpdateProductsCategoryForm, self).__init__(**kwargs)


class DeleteProductsCategoryForm(DeleteObject):
    class Meta:
        model = models.ProductsCategory
        exclude = []

#---------------------------------------------------
class CreateProductAttributeForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.ProductAttribute
        exclude = []


class UpdateProductAttributeForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = models.ProductAttribute
        exclude = []

    def __init__(self, **kwargs):
        super(UpdateProductAttributeForm, self).__init__(**kwargs)


class DeleteProductAttributeForm(DeleteObject):
    class Meta:
        model = models.ProductAttribute
        exclude = []


#---------------------------------------------------
class CreateProductAttributeValueForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.ProductAttributeValue
        exclude = []


class UpdateProductAttributeValueForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = models.ProductAttributeValue
        exclude = []

    def __init__(self, **kwargs):
        super(UpdateProductAttributeValueForm, self).__init__(**kwargs)


class DeleteProductAttributeValueForm(DeleteObject):
    class Meta:
        model = models.ProductAttributeValue
        exclude = []


#---------------------------------------------------
class CreateTaxesForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.Taxes
        exclude = []


class UpdateTaxesForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = models.Taxes

    def __init__(self, **kwargs):
        super(UpdateTaxesForm, self).__init__(**kwargs)


class DeleteTaxesForm(DeleteObject):
    class Meta:
        model = models.Taxes
        exclude = []


#---------------------------------------------------
class CreateTaxesValueForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.TaxesValue
        exclude = []


class UpdateTaxesValueForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = models.TaxesValue

    def __init__(self, **kwargs):
        super(UpdateTaxesValueForm, self).__init__(**kwargs)


class DeleteTaxesValueForm(DeleteObject):
    class Meta:
        model = models.TaxesValue
        exclude = []


#---------------------------------------------------
class CreateProductAttributeValueUnitMeasureForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.ProductAttributeValueUnitMeasure
        exclude = []


class UpdateProductAttributeValueUnitMeasureForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = models.ProductAttributeValueUnitMeasure

    def __init__(self, **kwargs):
        super(UpdateProductAttributeValueUnitMeasureForm, self).__init__(**kwargs)


class DeleteProductAttributeValueUnitMeasureForm(DeleteObject):
    class Meta:
        model = models.ProductAttributeValueUnitMeasure
        exclude = []
#-----------------------------------------------------------
class CreateStockForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.Stock
        exclude = []


class UpdateStockForm(form_helper.TCModelForm):
    """
    Form to update the Employment history
    """

    class Meta:
        model = models.Stock

    def __init__(self, **kwargs):
        super(UpdateStockForm, self).__init__(**kwargs)


class DeleteStockForm(DeleteObject):
    class Meta:
        model = models.Stock
        exclude = []