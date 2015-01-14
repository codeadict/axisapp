import os
import json
import jsonfield
import pystache
import django.dispatch

from django.conf import settings
from django.db.models import Q
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.mail import mail_admins, send_mail
from django.db.transaction import atomic

from axisapp.core.models import NameBase
from axisapp.core.fields import PercentageField
from axisapp.core.form_helper import DATETIME_FORMATS
from axisapp.core.mustache import load_mustache_template_source
from axisapp.storages import PublicStorage, PublicDebugStorage

from axisapp.security import models as auth


PUBLIC_STORAGE = settings.USE_S3 and PublicStorage() or PublicDebugStorage()


def branch_report_logo_path(branch, filename):
    _, ext = os.path.splitext(filename)
    return os.path.join(branch.company.code, 'logos/report_logo' + ext)


def branch_page_logo_path(branch, filename):
    _, ext = os.path.splitext(filename)
    return os.path.join(branch.company.code, 'logos/page_logo' + ext)


def company_page_logo_path(company, filename):
    _, ext = os.path.splitext(filename)
    return os.path.join(company.code, 'logos/page_logo' + ext)


class CompanyDirectManager(models.Manager):
    def company_queryset(self, request):
        return self.get_queryset().filter(company=request.user.branch.company)


class CompanyCommonManager(models.Manager):
    def company_queryset(self, request):
        if request.user.is_admin:
            # TODO: this could just be all?
            return self.get_queryset().filter(company_id__isnull=True)
        else:
            return self.get_queryset().filter(Q(company=request.user.branch.company) | Q(company_id__isnull=True))


class BranchDirectManager(models.Manager):
    def company_queryset(self, request):
        """
        this is either the company specific queryset or the branch specific queryset
        for each model if the model is branch specific.
        """
        return self.get_queryset().filter(branch=request.user.branch)


class BranchViaClientManager(models.Manager):
    def company_queryset(self, request):
        if request.user.is_admin:
            return self.get_queryset()
        return self.get_queryset().filter(client__user__branch=request.user.branch)


class Currency(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    code = models.CharField(_('Code'), max_length=5, unique=True)
    symbol = models.CharField(_('Symbol'), max_length=5)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.symbol)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class Country(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    abbreviation = models.CharField(_('Abbreviation'), max_length=10)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'), related_name='countries', null=True, blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.abbreviation)

    class Meta:
        ordering = ("name",)
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class GeographicRegion(NameBase):
    country = models.ForeignKey(Country, verbose_name=_('Country'), related_name='regions')

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.country.abbreviation)

    class Meta:
        verbose_name = _('Geographic Region')
        verbose_name_plural = _('Geographic Regions')


class Address(models.Model):
    street = models.TextField(_('Street Address'), null=True, blank=True)
    town = models.CharField(_('Town'), max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='model_%(class)ss', null=True, blank=True)
    postcode = models.CharField(_('Postcode'), max_length=20, null=True, blank=True)

    def __unicode__(self):
        parts = []
        for field in ['postcode', 'town', 'country']:
            value = getattr(self, field)
            if value:
                parts.append(str(value))
        return ', '.join(parts)

    class Meta:
        abstract = True


VOID_TRANSCODE = 'XX'
TRANS_CODES = (
    (VOID_TRANSCODE, 'None'),
    ('SE', 'Services'),
    ('RE', 'Retail'),
)


class Industry(NameBase):
    """
    Industry the company is operating in eg. academia, plumbing, sport, dance.
    Used for system translations and skills seperation
    """
    trans_code = models.CharField(_('Translation Code'), max_length=5,
                                  choices=TRANS_CODES, default=VOID_TRANSCODE)

    class Meta:
        verbose_name = _('Industry')
        verbose_name_plural = _('Industries')


class CompanyManager(models.Manager):
    def company_queryset(self, request):
        return self.get_queryset().filter(id=request.user.branch.company.pk)


def company_css_path(instance, filename):
    return os.path.join(instance.code, 'css', filename)


class Company(models.Model):
    """
    Model for a Company, it a Customer of our system
    """
    STATUS_INACTIVE = 'inactive'
    STATUS_TRIAL = 'trial'
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_TERMINATED = 'terminated'
    STATUS_CHOICES = (
        (STATUS_INACTIVE, _('Not activated yet')),
        (STATUS_TRIAL, _('Trial Period')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_SUSPENDED, _('Suspended')),
        (STATUS_TERMINATED, _('Terminated'))
    )

    objects = CompanyManager()

    name = models.CharField(_('Company Name'), max_length=255, unique=True)
    status = models.CharField(_('Status'), max_length=30, db_index=True, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    industry = models.ForeignKey(Industry, related_name='companies')
    code = models.SlugField(_('Abbreviation'), max_length=40, unique=True, db_index=True, blank=True, help_text=_(
        'Used for login URL and files paths,  maybe continue only letters, numbers and underscores, '
        'Note: this field cannot be changed after initial setup.'))
    custom_css = models.FileField(_(u'Custom CSS'), upload_to=company_css_path, blank=True, null=True)
    page_logo = models.ImageField(_('Page Logo'), storage=PUBLIC_STORAGE, upload_to=company_page_logo_path,
                                  null=True, blank=True, help_text=_('Note: this image is publicly available.'))
    tax_id = models.CharField(_('VAT number'), max_length=50, null=True, blank=True)
    website = models.URLField(_('Website'), null=True, blank=True, help_text=_('Company Website'))
    invoice_due_days = models.IntegerField(_('Invoice Due Delay'), default=10,
                                           help_text=_('Days after sending that an invoice is due for payment.'))
    uses_electronic_invoicing = models.BooleanField(_('Use Electronic Invoicing?'), default=False)
    api_access = models.BooleanField(_(u'API access'), default=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    email_sending = models.BooleanField(_('Emails being sent'), default=True)
    email_sending.help_text = _('If False all emails from this company will be muted except password resets.')

    def __unicode__(self):
        return self.name

    # TODO use implement that and use as cached_property
    @property
    def admin(self):
        pass

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.code or self.name)
        return super(Company, self).save(*args, **kwargs)

    def send_new_company_email(self):
        if not self.email_sending:
            return

        if not self.admin:
            return

        if settings.COMPANY_NEEDS_APPROVAL:
            template_string = load_mustache_template_source('comms/emails/new_company_pending.mustache')
            html = pystache.render(template_string, {'company': self})
            # TODO can't have subject as a translation string until we implement company default language
            send_mail(
                subject=ugettext('"%s" Pending on AxisApps') % self.name,
                message=html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.admin.user.email]
            )
        else:
            send_company_activation_email(self, freshly_created=True)


@django.dispatch.receiver(models.signals.pre_save, sender=Company)
def send_company_activation_email(instance, freshly_created=False, **kwargs):
    if not instance.email_sending:
        return

    if not instance.pk:
        return

    old_status = Company.objects.get(pk=instance.pk).status
    send_activation = freshly_created
    send_activation |= instance.status == Company.STATUS_ACTIVE and old_status != Company.STATUS_ACTIVE

    if send_activation:
        template_string = load_mustache_template_source('comms/emails/new_company_activated.mustache')
        login_url = '%s/%s/login' % (settings.SITE_DOMAIN, instance.code)
        html = pystache.render(template_string, {'company': instance, 'login_url': login_url})
        send_mail(
            subject=ugettext('Welcome to AxisApps, your company is now active'),
            message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.admin.user.email]
        )
    if not freshly_created:
        # TODO: Implement that to welcome administrator
        from axisapp.core.models import Administrator, send_welcome_email_admin
        for admin in Administrator.objects.filter(user__branch__company=instance):
            send_welcome_email_admin(admin, True, override_inactive_check=True)


@django.dispatch.receiver(models.signals.post_save, sender=Company)
def notify_admins(instance, created, **kwargs):
    """
    Notify settings.ADMINS of a new Company
    :param instance: company
    """
    if not created:
        return

    if not settings.NOTIFY_ADMINS_ON_NEW_COMPANY:
        return

    if settings.DEBUG:
        return

    mail_admins('New Company Registered: %s' % instance.name,
                'New Company: %s/admin/company/company/%s/' % (settings.SITE_DOMAIN, instance.pk))


# more details about this is help in ..core.form_helper
DATETIME_FORMAT_CHOICES = (
    (1, '25/7/2014 14:30'),
    (2, '25/7/2014 2:30 pm'),
    (3, '7/25/2014 14:30'),
    (4, '7/25/2014 2:30 pm'),
    (5, '2014-07-25 14:30'),
)

DATETIME_OUTPUT_CHOICES = DATETIME_FORMAT_CHOICES + (
    (100, '25 July 2014, Wed 14:30'),
    (101, '25 July 2014, Wednesday 14:30'),
)


def branch_css_path(instance, filename):
    return os.path.join(instance.company.code, 'css', filename)


def branch_html_path(instance, filename):
    return os.path.join(instance.company.code, 'html', filename)


DTI_HELP_TEXT = _('The first half will be used for date fields, this does not affect how dates are displayed.')
DTO_HELP_TEXT = _('The first half will be used for dates.')


class Branch(Address):
    """
    Model representing a physical branch of a Company
    """

    objects = CompanyDirectManager()

    name = models.CharField(_('Branch Name'), max_length=255)
    company = models.ForeignKey(Company, verbose_name=_('Company'), related_name='branches')

    pdf_logo = models.ImageField(_('PDF Logo'), storage=PUBLIC_STORAGE, upload_to=branch_report_logo_path,
                                 null=True, blank=True, help_text=_('Note: this image is publicly available.'))
    page_logo = models.ImageField(_('Page Logo'), storage=PUBLIC_STORAGE, upload_to=branch_page_logo_path,
                                  null=True, blank=True, help_text=_('Note: this image is publicly available.'))

    currency = models.ForeignKey(Currency, verbose_name=_('Currency'), related_name='branches')
    datetime_input = models.PositiveSmallIntegerField(_('Date Input Format'), choices=DATETIME_FORMAT_CHOICES,
                                                      default=1, help_text=DTI_HELP_TEXT)
    datetime_output = models.PositiveSmallIntegerField(_('Date Output Format'), choices=DATETIME_OUTPUT_CHOICES,
                                                       default=1, help_text=DTO_HELP_TEXT)
    custom_css = models.FileField(_('Custom CSS'), upload_to=branch_css_path, blank=True, null=True,
                                  help_text=_('Used to change the appearance of all pages.'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    @property
    def css(self):
        """
        Returns CSS for branch (custom or common from Company)
        :return: CSS file object or None
        """
        return self.custom_css or self.company.custom_css

    @property
    def datetime_formats(self):
        """
        Get datetime formats pack
        """
        return DATETIME_FORMATS[self.datetime_input]

    @property
    def datetime_output_formats(self):
        """
        Get datetime output formats pack
        """
        return DATETIME_FORMATS[self.datetime_output]

    @property
    def datetime_template_format(self):
        """
        Get current format for datetime
        """
        return self.datetime_output_formats['tpl_datetime']

    @property
    def date_template_format(self):
        """
        Get current format for date
        """
        return self.datetime_output_formats['tpl_date']

    @property
    def time_template_format(self):
        """
        Get current format for time
        """
        return self.datetime_output_formats['tpl_time']

    def __unicode__(self):
        return u'%s: %s' % (self.company, self.name)

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')
        ordering = ['pk']

    def save(self, *args, **kwargs):
        return super(Branch, self).save(*args, **kwargs)


def template_file_path(instance, filename):
    return os.path.join(instance.company.code, 'template', filename)


TEMPLATE_EMAIL = 1
TEMPLATE_INVOICE = 2
TEMPLATE_CSS = 3
TEMPLATE_TYPES = (
    (TEMPLATE_EMAIL, _('Email Template')),
    (TEMPLATE_INVOICE, _('Invoice Template')),
    (TEMPLATE_CSS, _('Site CSS Template')),
)


class Template(NameBase):
    """
    Template for emails, pdfs, html for clients page and others...
    """
    # TODO: we need to fix branch, email_style etc to use this
    objects = CompanyDirectManager()
    company = models.ForeignKey(Company, related_name='templates', editable=False)
    file = models.FileField(_('Template File'), upload_to=branch_html_path, editable=False)
    template_type = models.PositiveSmallIntegerField(_('Type'), choices=TEMPLATE_TYPES)

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')


######################
# Extra Attributes  #
######################

ROLE_TYPES_NO_ADMIN = models.Q(app_label='crm', model='contractor') | \
                      models.Q(app_label='crm', model='agent') | \
                      models.Q(app_label='crm', model='client') | \
                      models.Q(app_label='crm', model='servicerecipient')

ROLE_TYPES_INC_ADMIN = ROLE_TYPES_NO_ADMIN | \
                       models.Q(app_label='crm', model='administrator')

ROLE_REPORT_TYPES = ROLE_TYPES_NO_ADMIN | models.Q(app_label='comms', model='report')


class AttributeDefinition(NameBase):
    ATTR_BOOLEAN = 10
    ATTR_STRING = 20
    ATTR_TEXT = 30
    ATTR_INTEGER = 40
    ATTR_STARS = 50
    ATTR_SELECT = 60
    ATTR_DATETIME = 70
    ATTR_TYPE = (
        (ATTR_BOOLEAN, 'Boolean'),
        (ATTR_STRING, 'Text Short'),
        (ATTR_TEXT, 'Text Extended'),
        (ATTR_INTEGER, 'Integer'),
        (ATTR_STARS, 'Stars'),
        (ATTR_SELECT, 'Dropdown'),
        (ATTR_DATETIME, 'Datetime')
    )
    objects = CompanyDirectManager()

    help_text = models.CharField(_('Help Text'), null=True, blank=True, max_length=255)
    company = models.ForeignKey('company.Company', related_name='attributes', editable=False)
    content_type = models.ForeignKey(ContentType, verbose_name=_('Apply To'), limit_choices_to=ROLE_REPORT_TYPES)
    attrtype = models.PositiveSmallIntegerField(_('Type'), choices=ATTR_TYPE)
    required = models.BooleanField(_('Required'), default=False)
    list_show = models.BooleanField(_('Show in Lists'), default=False)
    filter_on = models.BooleanField(_('Available In Filters'), default=False)
    admin_only = models.BooleanField(_('Admin Only'), default=False,
                                     help_text=_('Attributes can only be seen and edited by Admins.'))

    dft_int = models.IntegerField(_('Integer default'), default=0)
    dft_str = models.TextField(_('String default'), null=True, blank=True)
    max_stars = models.IntegerField(_('Maximum Stars'), default=5)
    drop_options = models.TextField(_('Dropdown Options'), null=True, blank=True,
                                    help_text=_('Comma separated list of options on dropdown.'))

    class Meta:
        verbose_name = _('Attribute Definition')
        verbose_name_plural = _('Attribute Definitions')
        ordering = ['pk']

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.get_attrtype_display())

    @property
    def options_list(self):
        return self.drop_options and self.drop_options.split(',') or []

    @property
    def options_dict(self):
        return dict(self.options_choices)

    @property
    def is_bool(self):
        return self.attrtype == self.ATTR_BOOLEAN

    @property
    def is_string(self):
        return self.attrtype == self.ATTR_STRING

    @property
    def is_text(self):
        return self.attrtype == self.ATTR_TEXT

    @property
    def is_integer(self):
        return self.attrtype == self.ATTR_INTEGER

    @property
    def is_stars(self):
        return self.attrtype == self.ATTR_STARS

    @property
    def is_select(self):
        return self.attrtype == self.ATTR_SELECT

    @property
    def is_datetime(self):
        return self.attrtype == self.ATTR_DATETIME


class AttributeValue(models.Model):
    definition = models.ForeignKey(AttributeDefinition, related_name='attrs')
    content_type = models.ForeignKey(ContentType, limit_choices_to=ROLE_REPORT_TYPES)
    object_id = models.PositiveIntegerField()
    focus = GenericForeignKey()
    value_int = models.IntegerField(_('Integer value'), null=True, blank=True)
    value_str = models.TextField(_('String value'), null=True, blank=True)
    value_dt = models.DateTimeField(_('Datetime value'), null=True, blank=True)
    value_dec = models.DecimalField(
        _('Decimal value'), max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _('Attribute Value')
        verbose_name_plural = _('Attribute Values')

    def __unicode__(self):
        return '"%s", %s: %r' % (self.definition.name, self.get_type(), self.get_display())

    def get_type(self):
        return self.definition.get_attrtype_display()

    def get_value(self):
        if self.definition.is_bool and not self.value_int is None:
            return self.value_int == 1
        elif self.definition.is_string and not self.value_str is None:
            return self.value_str
        elif self.definition.is_text:
            return self.value_str
        elif self.definition.is_integer:
            return self.value_int
        elif self.definition.is_stars:
            return self.value_dec
        elif self.definition.is_select:
            return self.value_str
        elif self.definition.is_datetime:
            return self.value_dt

    def get_display(self):
        value = self.get_value()
        if self.definition.is_bool and not value is None:
            return '%r' % value
        elif self.definition.is_string and value:
            return '%s...' % value[:20]
        elif self.definition.is_text and value:
            return '%s...' % value[:20]
        elif self.definition.is_stars and value:
            return '%0.2f stars' % value

        return '%s' % (value or '')


def company_upload_path(instance, filename):
    return os.path.join(instance.company.code, filename)


class UploadsManager(models.Manager):
    def company_queryset(self, request):
        return self.filter(company=request.user.branch.company)


class Upload(models.Model):
    objects = UploadsManager()

    company = models.ForeignKey(Company)
    uploader = models.ForeignKey('security.User')
    file = models.FileField(storage=PUBLIC_STORAGE, upload_to=company_upload_path)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def file_name(self):
        return os.path.basename(self.file.url)
