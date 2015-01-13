import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import ugettext_lazy as _

import pytz


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, branch=None, last_name=None, **kwargs):
        if not kwargs.get('is_admin', False) and branch is None:
            raise ValueError(_('Unless a super admin is being created branch must not be None.'))
        email = self.normalize_email(email)
        last_name = last_name or email.split('@')[0]
        user = self.model(email=email, branch=branch, last_name=last_name, **kwargs)

        if password in ['', None]:
            user.set_unusable_password()
        else:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, last_name=None, **kwargs):
        user = self.create_user(email, password=password, last_name=last_name, is_admin=True, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        if password in ['', None]:
            user.set_unusable_password()
        return user

    def get_queryset(self, *args, **kwargs):
        return super(UserManager, self).get_queryset(*args, **kwargs).select_related('branch', 'branch__company')


class User(AbstractBaseUser):
    TITLES = (
        (10, _('Mr')),
        (20, _('Mrs')),
        (30, _('Miss')),
        (40, _('Ms')),
        (50, _('Dr')),
    )

    GENDERS = (
        (1, _('Female')),
        (2, _('Male'))
    )
    email = models.EmailField(verbose_name=_('Email Address'), max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(
        _('Super Admin'), default=False,
        help_text=_('Systems admins with access to backend admin system and cross company permissions.'))

    branch = models.ForeignKey('company.Branch', verbose_name=_('Branch'), related_name='users', null=True)
    title = models.IntegerField(_('Title'), null=True, blank=True, choices=TITLES)
    first_name = models.CharField(_('First Name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255)
    mobile = models.CharField(_('Mobile Number'), max_length=255, null=True, blank=True)
    phone = models.CharField(_('Telephone Number'), max_length=255, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(_('Gender'), choices=GENDERS, null=True, blank=True)
    photo = models.ImageField(_('Photo'), upload_to=photo_processing.user_photo_path, null=True, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    date_created = models.DateField(_('Date Created'), auto_now_add=True)
    timezone = models.CharField(_('Timezone'), max_length=255,
                                choices=[(x, x.replace('_', ' ')) for x in pytz.common_timezones],
                                default='America/Guayaquil')
    street = models.TextField(_('Street Address'), null=True, blank=True)
    town = models.CharField(_('Town'), max_length=50, null=True, blank=True)
    country = models.ForeignKey('company.Country', related_name='users', null=True, blank=True)
    postcode = models.CharField(_('Postcode'), max_length=20, null=True, blank=True)

    objects = UserManager()
    _default_manager = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def get_full_name(self):
        fn = '%s %s' % (self.first_name or '', self.last_name or '')
        return fn.strip()
    get_full_name.short_description = 'Full Name'

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        # TODO: needs work
        return True

    def has_module_perms(self, app_label):
        # TODO: needs work
        return True

    def exists_in_company(self, company):
        """
        Checks if roles in given company exist for this user

        :param company: company object
        :return: bool
        """
        return self.branch.company == company

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def get_roles(self, role_obj):
        return role_obj.objects.filter(user=self)

    def get_role(self, role_model):
        return role_model.objects.get(user=self)

    def get_roles_string(self):
        roles = ', '.join(role.role_model() for role in self.roles.all())
        return roles

    # TODO: this needs to be improve to using caching
    def custom_css_url(self):
        if self.branch and self.branch.css:
            return self.branch.css.url

    def invalidate_email(self):
        if not self.email:
            if not self.branch:
                raise ValueError(_('Branch should be provided for users without emails.'))
            self.email = '%s@%s%s' % (uuid.uuid4(), self.branch.agency.code, settings.INACTIVE_EMAIL_DOMAIN)

    def save(self, *args, **kwargs):
        self.invalidate_email()
        super(User, self).save(*args, **kwargs)

    class Meta():
        app_label = 'axisauth'
        ordering = ['last_name', 'first_name']
        unique_together = [('email', 'branch')]


class HistoryManager(models.Manager):
    def company_queryset(self, request):
        return self.filter(user__branch=request.user.branch)


class History(models.Model):
    """
    Keep a history of user actions
    """
    LOGIN = 10
    LOGOUT = 20

    USER_ACTIONS = (
        (LOGIN, _('Login')),
        (LOGOUT, _('Logged Out'))
    )
    objects = HistoryManager()

    user = models.ForeignKey(User, verbose_name=_('User'), related_name='user_logs')
    action = models.PositiveSmallIntegerField(verbose_name=_('Action'), choices=USER_ACTIONS)
    timestamp = models.DateTimeField(verbose_name=_('Time stamp'), auto_now_add=True)


@receiver(user_logged_in)
def update_user_history(sender, user, **kwargs):
    user.user_logs.create(action=History.LOGIN)
    user.save()
