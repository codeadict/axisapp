__author__ = 'malbalat85'

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


class EditProductForm(form_helper.TCModelForm):
    class Meta:
        model = models.Product
        exclude = []


class CreateProductForm(EditProductForm):
    pass


class UpdateProductForm(EditProductForm):
    pass


class DeleteProductsForm(DeleteObject):
    class Meta:
        model = models.Product
        exclude = []


#------------------------------------
class ProductsCategorySearchForm(form_helper.GenericFilterForm):
    name = forms.CharField(label=_('Name'))
    full_name = forms.CharField(label=_('Description'))

    fields_mapping = {
        'name': 'name__icontains',
        'full_name': 'full_name__icontains',
    }
    model = models.Product

    def __init__(self, *args, **kwargs):
        super(ProductsCategorySearchForm, self).__init__(*args, **kwargs)


class EditProductsCategoryForm(form_helper.TCModelForm):
    """
    Form for the ProductCategory
    """

    class Meta:
        model = models.ProductsCategory
        exclude = []


class CreateProductsCategoryForm(EditProductsCategoryForm):
    """
    Form to create the Products Category
    """
    pass


class UpdateProductsCategoryForm(EditProductsCategoryForm):
    """
    Form to update the Products Category
    """
    pass


class DeleteProductsCategoryForm(DeleteObject):
    class Meta:
        model = models.ProductsCategory
        exclude = []


#---------------------------------------------------
class EditProductAttributeForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.ProductAttribute
        exclude = []


class CreateProductAttributeForm(EditProductAttributeForm):
    """
    Form to create the Employment history
    """
    pass


class UpdateProductAttributeForm(EditProductAttributeForm):
    """
    Form to update the Employment history
    """
    pass


class DeleteProductAttributeForm(DeleteObject):
    class Meta:
        model = models.ProductAttribute
        exclude = []


#---------------------------------------------------
class EditProductAttributeValueForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.ProductAttributeValue
        exclude = []


class CreateProductAttributeValueForm(EditProductAttributeValueForm):
    """
    Form to create the Employment history
    """
    pass


class UpdateProductAttributeValueForm(EditProductAttributeValueForm):
    """
    Form to update the Employment history
    """
    pass


class DeleteProductAttributeValueForm(DeleteObject):
    class Meta:
        model = models.ProductAttributeValue
        exclude = []


#---------------------------------------------------
class EditIceTaxForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.IceTax
        exclude = []


class CreateIceTaxForm(EditIceTaxForm):
    """
    Form to create the Employment history
    """
    pass


class UpdateIceTaxForm(EditIceTaxForm):
    """
    Form to update the Employment history
    """
    pass


class DeleteTaxesForm(DeleteObject):
    class Meta:
        model = models.IceTax
        exclude = []


#---------------------------------------------------
class EditProductAttributeValueUnitMeasureForm(form_helper.TCModelForm):
    """
    Form to create the Employment history
    """

    class Meta:
        model = models.ProductAttributeValueUnitMeasure
        exclude = []


class CreateProductAttributeValueUnitMeasureForm(EditProductAttributeValueUnitMeasureForm):
    """
    Form to create the Employment history
    """
    pass


class UpdateProductAttributeValueUnitMeasureForm(EditProductAttributeValueUnitMeasureForm):
    """
    Form to update the Employment history
    """
    pass


class DeleteProductAttributeValueUnitMeasureForm(DeleteObject):
    class Meta:
        model = models.ProductAttributeValueUnitMeasure
        exclude = []
