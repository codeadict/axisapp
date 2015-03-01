#This is to handle very happy al the stuff about datetime
from django.utils.translation import ugettext


def humanize_time(relative_data):
    """
    Return the date as string
    :param relative_data:
    :return: string
    """
    result = ""

    if relative_data.years and relative_data.years > 0:
        if relative_data.years == 1:
            result = result + ugettext('1 year, ' % relative_data.years)
        else:
            result = result + ugettext('%s years, ' % relative_data.years)

    if relative_data.months and relative_data.months > 0:
        if relative_data.months == 1:
            result = result + ugettext('1 month, ' % relative_data.months)
        else:
            result = result + ugettext('%s months, ' % relative_data.months)

    if relative_data.days and relative_data.days > 0:
        if relative_data.days == 1:
            result = result + ugettext('1 day, ' % relative_data.days)
        else:
            result = result + ugettext('%s days, ' % relative_data.days)

    if result != "":
        return result.rstrip(',')
    else:
        return ugettext('No time')
