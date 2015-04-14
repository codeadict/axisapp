from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from products import models
from base.default_views import CustomListView, CustomDetailView
from django.contrib.contenttypes.models import ContentType
from base.default_views import EditModelView
from django.views.generic import CreateView, UpdateView
from base.default_views import DeleteObject
from products import forms
from view_utils import ListFilterMixin


class ProductsList(CustomListView):
    """
    CLass to list all the Employees
    """
    template_name = 'product/list.jinja'
    active_page = 'product-list'
    model = models.Product
    perms = []
    detail_view = 'product-details'
    display_items = [
        'name',
        'description',
        'upc',
        'active',
        'type',
        'func|image',
    ]
    button_menu = [
        {'name': _('Add Product'), 'rurl': 'product-add'},
        {'name': _('Filter'), 'rurl': 'product-filter'}
    ]
    #search_form = ProductSearchForm
    related_fields = ['image', 'category', 'ice_tax', 'attributes']

    def get_queryset(self):
        return super(ProductsList, self).get_queryset()

    @staticmethod
    def image(self, obj):
        pass
        #images = obj.image.image
        #return images[0] if images.count() > 1 else None

product_list = ProductsList.as_view()


class ProductFilter(ListFilterMixin, CustomListView):
    template_name = 'product/filter.jinja'
    active_page = 'product-list'
    model = models.Product
    perms = []
    display_items = []
    search_form = forms.ProductSearchForm
    related_fields = ['image', 'category', 'ice_tax', 'attributes']

    def get_context_data(self, **kwargs):
        context = super(ProductFilter, self).get_context_data(**kwargs)
        context['rurl'] = 'product-list'
        #context['search_form'] = forms.ProductSearchForm
        return context

product_filter = ProductFilter.as_view()


class ProductDetails(CustomDetailView):
    active_page = 'product-list'
    model = models.Product
    perms = ProductsList.perms
    display_items = [
        'name',
        'description',
        'upc',
        'active',
        'type',
        'func|image',
    ]
    button_menu = [
        [
            {'name': _('Edit'), 'urlfunc': 'edit_url'},
            {'name': _('Delete'), 'urlfunc': 'delete_url', 'classes': 'confirm-follow', 'method': 'POST',
             'msg': _('Are you going to delete this Product?')},
        ],
        [
            {'name': _('Change state'), 'dropdown':
                [
                    {
                        'name': display_name,
                        'urlfunc': 'set_status_url',
                        'classes': 'submit-post product-set-status',
                        'data': {'status': value}
                    } for value, display_name in models.Product.ITEM_STATE
                ]
            }
        ],
    ]

    def edit_url(self):
        return reverse('product-edit', kwargs={'pk': self.object.pk})

    def delete_url(self):
        return reverse('product-delete', kwargs={'pk': self.object.pk})

    def set_status_url(self):
        return reverse('product-set-status', kwargs={'pk': self.object.pk})

    @staticmethod
    def image(self, obj):
        pass
        #images = obj.image.image
        #return images[0] if images.count() > 1 else None

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        cont_type = ContentType.objects.get_for_model(models.Product)
        context['status_choices'] = dict(models.Product.ITEM_STATE)
        return context

product_details = ProductDetails.as_view()


class ProductCreate(EditModelView, CreateView):
    template_name = 'product/form.jinja'
    form_class = forms.CreateProductForm
    active_page = 'product-list'
    title = _('Add Product')
    perms = []

    def get_success_url(self):
        return reverse('product-details', kwargs={'pk': self.object.pk})

product_create = ProductCreate.as_view()


class ProductUpdate(EditModelView, UpdateView):
    template_name = 'product/form.jinja'
    perms = []
    form_class = forms.UpdateProductForm
    model = models.Product
    active_page = 'product-list'
    title = _('Edit Product')

    def get_success_url(self):
        return reverse('product-details', kwargs={'pk': self.object.pk})

product_update = ProductUpdate.as_view()


class ProductDelete(DeleteObject):
    model = models.Product
    reverse_name = 'product-list'
    perms = []

product_delete = ProductDelete.as_view()


#------------------ Product Category -----------------
class CategoryList(CustomListView):
    """
    CLass to list all the Employees
    """
    template_name = 'product/list.jinja'
    active_page = 'product-category-list'
    model = models.ProductsCategory
    perms = []
    detail_view = 'product-category-details'
    display_items = [
        'name',
        'full_name',
        'description',
        'date_created',
        'func|image',
    ]
    button_menu = [
        {'name': _('Add Category'), 'rurl': 'product-category-add'},
        {'name': _('Filter'), 'rurl': 'product-category-filter'}
    ]
    #search_form = ProductSearchForm
    related_fields = ['image', 'default_attributes']

    def get_queryset(self):
        return super(CategoryList, self).get_queryset()

    @staticmethod
    def image(self, obj):
        pass
        #images = obj.image
        #return images[0] if images.count() > 1 else None

category_list = CategoryList.as_view()


class CategoryFilter(ListFilterMixin, CustomListView):
    template_name = 'product/filter.jinja'
    active_page = 'category-list'
    model = models.ProductsCategory
    perms = []
    display_items = []
    search_form = forms.ProductsCategorySearchForm
    related_fields = ['image', 'default_attributes']

    def get_context_data(self, **kwargs):
        context = super(CategoryFilter, self).get_context_data(**kwargs)
        context['rurl'] = 'product-category-list'
        return context

category_filter = CategoryFilter.as_view()


class CategoryDetails(CustomDetailView):
    active_page = 'products-category-list'
    model = models.ProductsCategory
    perms = CategoryList.perms
    display_items = [
        'name',
        'full_name',
        'description',
        'date_created',
        'child',
        'default_attributes',
        'func|image',
    ]
    # TODO: display the child and attributes as a table
    #extra_content = 'hhrr/employee/extra_details.jinja'
    button_menu = [
        [
            {'name': _('Edit'), 'urlfunc': 'edit_url'},
            {'name': _('Delete'), 'urlfunc': 'delete_url', 'classes': 'confirm-follow', 'method': 'POST',
             'msg': _('Are you going to delete this Category?')},
        ],
    ]

    def edit_url(self):
        return reverse('product-category-edit', kwargs={'pk': self.object.pk})

    def delete_url(self):
        return reverse('product-category-delete', kwargs={'pk': self.object.pk})

    @staticmethod
    def image(self, obj):
        pass
        #images = obj.image.image
        #return images[0] if images.count() > 1 else None

    def get_context_data(self, **kwargs):
        context = super(CategoryDetails, self).get_context_data(**kwargs)
        cont_type = ContentType.objects.get_for_model(models.ProductsCategory)
        return context

category_details = CategoryDetails.as_view()


class CategoryCreate(EditModelView, CreateView):
    template_name = 'product/form.jinja'
    form_class = forms.CreateProductsCategoryForm
    active_page = 'product-category-list'
    title = _('Add Category')
    perms = []

    def get_success_url(self):
        return reverse('product-category-details', kwargs={'pk': self.object.pk})

category_create = CategoryCreate.as_view()


class CategoryUpdate(EditModelView, UpdateView):
    template_name = 'product/form.jinja'
    perms = []
    form_class = forms.UpdateProductsCategoryForm
    model = models.ProductsCategory
    active_page = 'products-category-list'
    title = _('Edit Category')

    def get_success_url(self):
        return reverse('product-category-details', kwargs={'pk': self.object.pk})

category_update = CategoryUpdate.as_view()


class CategoryDelete(DeleteObject):
    model = models.ProductsCategory
    reverse_name = 'product-category-list'
    perms = []

category_delete = CategoryDelete.as_view()



