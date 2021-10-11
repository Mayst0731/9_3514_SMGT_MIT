import re


def start_end_date(info):
    year = get_year(info)
    start, end = info.split('–')
    start_date, start_month = get_start(start)

    start_date = year + "-" + start_date
    end_date = year + "-" + get_end(end, start_month)
    return start_date, end_date


def get_year(info):
    year = re.findall(r'\d{4}', info)[0]
    return str(year)


def get_start(start):
    month = get_month(start)
    date = re.findall(r'\d{1,2}', start)[0]
    if len(date) <= 1:
        date = '0'+date
    return f'{month}-{date}', month


def get_end(end, start_month):
    month = get_month(end)
    if not month:
        month = start_month
    date = re.findall(r'\d{1,2}', end)[0]
    if len(date) <= 1:
        data = '0'+date
    return f'{month}-{date}'


def get_month(info):
    map = {'Jan': '01',
           'Feb': "02",
           "Mar": '03',
           "Apr": "04",
           "May": "05",
           "Jun": '06',
           "Jul": "07",
           "Aug": "08",
           "Sep": "09",
           "Oct": "10",
           "Nov": "11",
           "Dec": "12"}
    for k,v in map.items():
        if k in info:
            return v
    return ''


def get_type(info):
    type_map = {'Live Online': "online-virtual",
                'In Person': "onsite",
                'Blended': "online-cvs",
                'Self-Paced Online': "online-selfpaced"}
    return type_map.get(info, '')


def get_tuition(info):
    if '$' in info:
        tuition = ''.join(re.findall(r'\d+', info))
        return int(tuition)
    else:
        return 0


def get_duration_type(info_lst):
    for info in info_lst:
        if 'days' in info:
            return 'days'
        elif 'weeks' in info:
            return 'weeks'
    return ''


def get_duration_num(info_lst):
    for info in info_lst:
        if 'days' in info or 'weeks' in info:
            num = re.findall('\d{1}', info)[0]
            return int(num)
    return ''


def get_location(info):
    if 'Massachusetts' in info:
        return 'Cambridge, MA, United States'



