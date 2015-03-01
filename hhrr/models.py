from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf.global_settings import LANGUAGES
from base import models as base_models
from phonenumber_field import modelfields
from django_countries import fields


class EmploymentHistory(models.Model):
    """
    Employment History
    """

    # Employent History Data
    # TODO: Leave now the company as CharField, Later will be an FK with company table
    company = models.CharField(max_length=255, verbose_name=_('Company Name'))
    position = models.CharField(max_length=255, verbose_name=_('Position'))
    date_in = models.DateField(default=timezone.now(), verbose_name='Date hired')
    date_out = models.DateField(default=timezone.now(), verbose_name='Date leaving')
    out_reason = models.CharField(max_length=255, verbose_name='Reason of leaving')

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return self.get_company_position()

    def get_company_position(self):
        return '%s %s' % (self.company, self.position)

    @property
    def time_worked(self):
        """
        Returns the number of days the
        Employee works into the company
        :return: Int
        """
        if self.date_in > self.date_out:
            return 0
        else:
            delta = self.date_in - self.date_out
            return delta.days

    class Meta:
        verbose_name = _('Employment history')
        verbose_name_plural = _('Employment history')
        ordering = ['company']


class Language(models.Model):
    """
    Language managed by Employees
    """

    NATIVE = 3
    HIGH = 2
    INTERMEDIATE = 1
    LOW = 0

    TYPES = (
        (LOW, _('Low')),
        (INTERMEDIATE, _('Intermediate')),
        (HIGH, _('High')),
        (NATIVE, _('Native')),
    )

    NAMES = tuple([(i, j) for i, j in enumerate(LANGUAGES)])

    name = models.PositiveIntegerField(choices=NAMES, default=19, verbose_name=_('Language Name'))
    speak = models.PositiveIntegerField(choices=TYPES, default=0, verbose_name=_('Speak skills'))
    write = models.PositiveIntegerField(choices=TYPES, default=0, verbose_name=_('Write skills'))
    read = models.PositiveIntegerField(choices=TYPES, default=0, verbose_name=_('Read skills'))

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s %s %s' % (self.name, self.speak, self.write, self.read)

    class Meta:
        verbose_name = _('Dominated language ')
        verbose_name_plural = _('Languages dominated')
        ordering = ['name']


class FamilyRelation(models.Model):
    """
    Model to record the family relation type
    """
    #TODO: Create the table from xml
    # https://github.com/cecep-edu/refactory/blob/staging/iaen_base/data/family_relationship_data.xml
    # To have it all set

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    code_mrl = models.CharField(max_length=255, verbose_name=_('Code MRL'))

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s' % (self.name, self.description)

    class Meta:
        verbose_name = _('Family relation')
        verbose_name_plural = _('Family relations')
        ordering = ['name']


class FamilyDependant(models.Model):
    """
    Model to record the Family information
    """

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last name'))
    relationship = models.ForeignKey(FamilyRelation, verbose_name=_('Relation ship'))
    birthday = models.DateField(default=timezone.now(), verbose_name=_('Birthday'))
    phone = modelfields.PhoneNumberField(verbose_name=_('Phone Number'))
    handicapped = models.BooleanField(default=False, verbose_name=_('Handicapped'))
    have_insurance = models.BooleanField(default=False, verbose_name=_('Insurance'))

    @property
    def age(self):
        if self.birthday > timezone.now():
            raise BaseException(_('Birthday can\'t in the future'))

        delta = self.birthday - timezone.now()
        return delta.days

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s %s' % (self.name, self.last_name, self.relationship.name)

    class Meta:
        verbose_name = _('Family dependant')
        verbose_name_plural = _('Family dependants')
        ordering = ['name']


class Education(models.Model):
    """
    Model to record the studies
    """
    NO_INSTRUCTION = 0
    BASIC_INSTRUCTION = 1
    PRIMARY_INSTRUCTION = 2
    SECONDARY_INSTRUCTION = 3
    BACHELOR_INSTRUCTION = 4
    FOURTH_INSTRUCTION = 5
    TECH_SENIOR_INSTRUCTION = 6
    TECH_INSTRUCTION = 7
    THIRD_INSTRUCTION = 8

    INSTRUCTION_TYPE_LEVEL = (
        (NO_INSTRUCTION, _('No instruction')),
        (BASIC_INSTRUCTION, _('Basic school')),
        (PRIMARY_INSTRUCTION, _('Primary')),
        (SECONDARY_INSTRUCTION, _('Secondary')),
        (BACHELOR_INSTRUCTION, _('Bachelor')),
        (FOURTH_INSTRUCTION, _('Fourth')),
        (TECH_SENIOR_INSTRUCTION, _('Senior Technician')),
        (TECH_INSTRUCTION, _('Technics')),
        (THIRD_INSTRUCTION, _('Third')),

    )

    institution = models.CharField(max_length=255, verbose_name=_('Institution Name'))
    country = fields.CountryField(verbose_name=_('Institution Name'), blank_label=_('(select country)'))
    start_date = models.DateField(default=timezone.now(), verbose_name=_('Start date'))
    graduation_date = models.DateField(default=timezone.now(), verbose_name=_('Graduation date'))
    instruction_level = models.IntegerField(default=0, choices=INSTRUCTION_TYPE_LEVEL, verbose_name=_('Level'))
    degree = models.CharField(max_length=255, verbose_name=_('Degree'))
    is_finished = models.BooleanField(default=False, verbose_name=_('Finished?'))
    last_finished_semester = models.IntegerField(default=0, verbose_name=_('Last finished semester'))
    education_area = models.ForeignKey(EducationArea, verbose_name=_('Education Area'))

    @property
    def timespend(self):
        #Return teh time passed in the course
        return True

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s %i' % (self.institution, self.country, self.is_finished)

    class Meta:
        verbose_name = _('Studied education')
        verbose_name_plural = _('Studied educations')
        ordering = ['institution']


class EducationArea(models.Model):
    """
    Model to record the education areas
    """

    name = models.CharField(max_length=255, verbose_name=_('Area name'))

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s' % self.name


class EnterpriseDepartment(models.Model):
    """
    Model to record the Work Department
    """

    name = models.CharField(max_length=255, verbose_name=_('Department name'))

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s' % self.name


class Employee(base_models.Partner):
    """
    Model to record Employees
    """

    RUC = 0
    PASSPORT = 1
    #Cedula: no encontre otra mejor traduccion
    ID = 2

    ID_TYPE = (
        (RUC, _('R.U.C.')),
        (PASSPORT, _('Passport')),
        (ID, _('Id')),
    )

    BLOOD_O = 0
    BLOOD_O_P = 1
    BLOOD_O_N = 2
    BLOOD_A = 3
    BLOOD_A_N = 4
    BLOOD_A_P = 5
    BLOOD_B = 6
    BLOOD_B_P = 7
    BLOOD_B_N = 8
    BLOOD_AB = 9
    BLOOD_AB_P = 10
    BLOOD_AB_N = 11

    BLOOD_TYPE = (
        (BLOOD_O, _('Type O')),
        (BLOOD_O_P, _('Type O+')),
        (BLOOD_O_N, _('Type O-')),
        (BLOOD_A, _('Type a')),
        (BLOOD_A_N, _('Type A-')),
        (BLOOD_A_P, _('Type A+')),
        (BLOOD_B, _('Type B')),
        (BLOOD_B_P, _('Type B+')),
        (BLOOD_B_N, _('Type B-')),
        (BLOOD_AB, _('Type AB')),
        (BLOOD_AB_P, _('Type AB+')),
        (BLOOD_AB_N, _('Type AB-')),
    )

    SINGLE = 0
    MARRIED = 1
    WIDOWED = 2
    DIVORCES = 3
    UNION_FREE = 4

    MARITAL_STATUS = (
        (SINGLE, _('Single')),
        (MARRIED, _('Married')),
        (WIDOWED, _('Widowed')),
        (DIVORCES, _('Divorces')),
        (UNION_FREE, _('Union free')),
    )

    GENDER_MALE = 0
    GENDER_FEMALE = 1

    GENDER_TYPE = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
    )

    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_SETTLED = 3

    STATUS_TYPE = (
        (STATUS_INACTIVE, _('Inactive')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_SETTLED, _('Settled')),
    )

    ETHNIC_RACE_WHITE = 0
    ETHNIC_RACE_BLACK = 1
    ETHNIC_RACE_MIXED = 2
    ETHNIC_RACE_INDIAN = 3
    ETHNIC_RACE_ASIAN = 4
    # Jedi maybe?
    ETHNIC_RACE_OTHER = 5

    ETHNIC_RACE_TYPE = (
        (ETHNIC_RACE_ASIAN, _('Asian')),
        (ETHNIC_RACE_BLACK, _('Black')),
        (ETHNIC_RACE_WHITE, _('White')),
        (ETHNIC_RACE_MIXED, _('Mixed')),
        (ETHNIC_RACE_OTHER, _('Other')),
    )

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last Name'))
    id_type = models.IntegerField(choices=ID_TYPE, default=2, verbose_name=_('Id type'))
    id = models.CharField(max_length=20, verbose_name=_('ID number'))
    photo = models.ImageField(verbose_name=_('Image'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    province = models.ForeignKey(base_models.Provincia, verbose_name=_('Province'))
    parish = models.ForeignKey(base_models.Parroquia, verbose_name=_('Parish'))
    canton = models.ForeignKey(base_models.Canton, verbose_name=_('Canton'))
    county = models.CharField(max_length=255, verbose_name=_('County'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    postcode = models.CharField(max_length=10, verbose_name=_('Postal Code'))
    nationality = fields.CountryField(verbose_name=_('Nationality'), blank_label=_('(select country)'))
    blood_type = models.IntegerField(choices=BLOOD_TYPE, default=0, verbose_name=_('Blood type'))
    handicapped = models.BooleanField(default=0, verbose_name=_('Is handicapped?'))
    handicap_percent = models.SmallIntegerField(default=0, verbose_name=_('Handicap percent'))
    handicap_type = models.CharField(max_length=255, verbose_name=_('Handicap type'))
    handicap_card_number = models.CharField(max_length=255, verbose_name=_('Handicap card number'))
    phone = modelfields.PhoneNumberField(verbose_name=_('Phone number'))
    cellphone = modelfields.PhoneNumberField(verbose_name=_('Cellphone number'))
    email = models.EmailField(max_length=255, verbose_name=_('Email'))
    skype = models.CharField(max_length=255, verbose_name=_('Skype user'))
    department = models.ForeignKey(EnterpriseDepartment, verbose_name=_('Department'))
    marital_status = models.IntegerField(choices=MARITAL_STATUS, default=0, verbose_name=_('Marital status'))
    sex = models.IntegerField(choices=GENDER_TYPE, default=-1, verbose_name=_('Gender'))
    birthday = models.DateField(default=timezone.now(), verbose_name=_('Birthday'))
    emergency_person = models.CharField(max_length=255, verbose_name=_('Name to call at emergency'))
    emergency_phone = modelfields.PhoneNumberField(verbose_name=_('Phone number to call at emergency'))
    #TODO: Write the name, i dont know what is this
    maintain_reserve_funds = models.BooleanField(default=False, verbose_name=_(''))
    status = models.IntegerField(choices=STATUS_TYPE, default=0, verbose_name=_('Status'))
    ethnic_race = models.IntegerField(choices=ETHNIC_RACE_TYPE, default=0, verbose_name=_('Ethnic race'))

    family_dependants = models.ForeignKey(FamilyDependant, verbose_name=_('Family dependants'))
    language_skill = models.ForeignKey(Language, verbose_name=_('Language skills'))
    employment_history = models.ForeignKey(EmploymentHistory, verbose_name=_('Employment history'))
    education = models.ForeignKey(Education, verbose_name=_('Education'))

    def __unicode__(self):
        """
        Object representation
        :return: Unicode String
        """
        return '%s %s %s' % (self.name, self.last_name, self.status)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['name']