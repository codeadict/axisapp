__author__ = 'codeadict'
import itertools

# everything should relapse to the same valid date format: '%Y-%m-%d %H:%M:%S'
# the "datetime" formats are generated afterwards.
# dj_date and dj_time related to django formatting (in the order they are tried),
# mt_date and mt_time realted to moment.js/bootstrap datepicker formatting
DATETIME_FORMATS = {
    # Input and output
    1: {
        'date_name': 'dd/mm/yyyy',
        'dj_date': ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'],
        'mt_date': 'DD/MM/YYYY',
        'tpl_date': '%d/%m/%Y',
        'time_name': 'HH:MM',
        'dj_time': ['%H:%M', '%H:%M:%S'],
        'mt_time': 'HH:mm',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%d/%m/%Y %H:%M',
    },
    2: {
        'date_name': 'dd/mm/yyyy',
        'dj_date': ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'],
        'mt_date': 'DD/MM/YYYY',
        'tpl_date': '%d/%m/%Y',
        'time_name': 'HH:MM am/pm',
        'dj_time': ['%I:%M %p', '%I:%M:%S %p', '%H:%M:%S'],
        'mt_time': 'hh:mm a',
        'tpl_time': '%I:%M %p',
        'tpl_datetime': '%d/%m/%Y %I:%M %p',  # TODO: Not sure dj_time is correct here
    },
    3: {
        'date_name': 'mm/dd/yyyy',
        'dj_date': ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'],
        'mt_date': 'MM/DD/YYYY',
        'tpl_date': '%m/%d/%Y',
        'time_name': 'HH:MM',
        'mt_time': 'HH:mm',
        'dj_time': ['%H:%M', '%H:%M:%S'],
        'tpl_time': '%H:%M',
        'tpl_datetime': '%m/%d/%Y %H:%M',
    },
    4: {
        'date_name': 'mm/dd/yyyy',
        'dj_date': ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'],
        'mt_date': 'MM/DD/YYYY',
        'tpl_date': '%m/%d/%Y',
        'time_name': 'HH:MM am/pm',
        'dj_time': ['%I:%M %p', '%I:%M:%S %p', '%H:%M:%S'],
        'mt_time': 'hh:mm a',
        'tpl_time': '%I:%M %p',
        'tpl_datetime': '%m/%d/%Y %I:%M %p',  # TODO: Not sure dj_time is correct here
    },
    5: {
        'date_name': 'yyyy-mm-dd',
        'dj_date': ['%Y-%m-%d', '%y-%m-%d'],
        'mt_date': 'YYYY-MM-DD',
        'tpl_date': '%Y-%m-%d',
        'time_name': 'HH:MM',
        'dj_time': ['%H:%M', '%H:%M:%S'],
        'mt_time': 'HH:mm',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%Y-%m-%d %H:%M',
    },

    # Output only
    100: {
        'tpl_date': '%d %B %Y, %a',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%d %B %Y, %a %H:%M',
    },
    101: {
        'tpl_date': '%d %B %Y, %A',
        'tpl_time': '%H:%M',
        'tpl_datetime': '%d %B %Y, %A %H:%M',
    },
}

for dfid, df in DATETIME_FORMATS.items():
    if 'dj_date' in df:
        DATETIME_FORMATS[dfid]['dj_datetime'] = [' '.join(v) for v in itertools.product(df['dj_date'], df['dj_time'])]
        DATETIME_FORMATS[dfid]['mt_datetime'] = '%(mt_date)s %(mt_time)s' % df
        DATETIME_FORMATS[dfid]['datetime_name'] = '%(date_name)s %(time_name)s' % df

