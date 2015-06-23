# This Python file uses the following encoding: utf-8
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import ugettext_lazy as _

from base.querysets import BaseRequestQueryset


class UserQueryset(BaseRequestQueryset):
    def request_qs(self, request):
        return self.all()


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, branch=None, last_name=None, **kwargs):
        if not kwargs.get('is_admin', False) and branch is None:
            raise ValueError('Unless a super admin is being created branch must not be None.')
        email = self.normalize_email(email)
        last_name = last_name or email.split('@')[0]
        user = self.model(email=email, last_name=last_name, **kwargs)

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
        return super(UserManager, self).get_queryset(*args, **kwargs)


class User(AbstractBaseUser):
    GENDERS = (
        (1, _('Female')),
        (2, _('Male'))
    )
    email = models.EmailField(verbose_name=_('Correo'), max_length=255, blank=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Esta Activo'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Usuario Eliminado'))
    is_admin = models.BooleanField(_('Super Administrador?'), default=False)
    is_admin.help_text = _('Es el administrador del sistema con todo tipo de privilegios.')

    first_name = models.CharField(_('Nombres'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Apellidos'), max_length=255)
    mobile = models.CharField(_('Celular'), max_length=255, null=True, blank=True)
    phone = models.CharField(_('Telefono Convencional'), max_length=255, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(_('Genero'), choices=GENDERS, null=True, blank=True)
    date_of_birth = models.DateField(_('Cumpleanos'), null=True, blank=True)
    date_created = models.DateField(_('Fecha Creado'), auto_now_add=True)
    street = models.TextField(_('Direccion'), null=True, blank=True)
    city = models.CharField(_('Ciudad'), max_length=50, null=True, blank=True)

    objects = UserManager.from_queryset(UserQueryset)()
    _default_manager = UserManager.from_queryset(UserQueryset)()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        fn = u'%s %s' % (self.first_name or '', self.last_name or '')
        return fn.strip()
    get_full_name.short_description = 'Nombre Completo'

    @staticmethod
    def get_valid_email(email_address):
        """
        :param email_address: email address to check
        :return: the email address or None if it's "inactive"
        """
        return not email_address.endswith(settings.INACTIVE_EMAIL_DOMAIN) and email_address or None

    def display_email(self):
        return self.get_valid_email(self.email)
    display_email.short_description = _('Email')
    display_email.priority_short_description = _('Email')

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return unicode(self.email)

    def has_perm(self, perm, obj=None):
        # TODO: needs work
        return True

    def has_module_perms(self, app_label):
        # TODO: needs work
        return True

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

    class Meta():
        app_label = 'sdauth'
        ordering = ['last_name', 'first_name']


class History(models.Model):
    """
    Keep a history of user actions
    """
    LOGIN = 10

    USER_ACTIONS = (
        (LOGIN, _('Login')),
    )

    user = models.ForeignKey(User, verbose_name=_('Usuario'), related_name='user_logs')
    action = models.PositiveSmallIntegerField(verbose_name=_('Accion'), choices=USER_ACTIONS)
    timestamp = models.DateTimeField(verbose_name=_('Fecha/Hora'), auto_now_add=True)


@receiver(user_logged_in)
def update_user_history(sender, user, **kwargs):
    if settings.RECORD_LOGIN:
        user.user_logs.create(action=History.LOGIN)
        user.save(process_photo=False)
