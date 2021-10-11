from pprint import pprint

from format import start_end_date, get_type, get_tuition, get_duration_type, get_duration_num, get_location
from read_write import read_from_json, write_to_json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def clean_attrs():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    re_scrape_time_urls = ["https://executive.mit.edu/course/mastering-design-thinking/a056g00000URaa4AAD.html",
                           "https://executive.mit.edu/course/applied-business-analytics/a056g00000URaaVAAT.html",
                           'https://executive.mit.edu/course/cybersecurity-for-managers/a056g00000URaaIAAT.html',
                           'https://executive.mit.edu/course/mastering-negotiation-and-influence/a056g00000URaaRAAT.html']
    details = read_from_json('./filestore/scraped_details.json')
    for detail in details:
        time_detail = {"effective_date_start": '',
                       "effective_date_end": '',
                       "type": '',
                       "currency": 'USD',
                       "tuition_number": 0,
                       "location": '',
                       "version": 1,
                       "Repeatable": "Y",
                       "languages": "English",
                       "tuition_note": "",
                       "active": True,
                       "priority": 0,
                       "publish": 100,
                       "is_advanced_management_program": False,
                       "Repeatable": "Y",
                       "credential": "",
                       "schedule": [['', '', '', 'formal']]
                       }
        detail.update(time_detail)
        detail['category'] = clean_categories(detail)
        time_info = detail['time']
        if len(time_info) == 0 and detail['url'] not in re_scrape_time_urls:
            continue
        elif len(time_info) == 0 and detail['url'] in re_scrape_time_urls:
            time_info = re_fetch_time(detail['url'], driver)
        date_info = time_info[0]
        effective_date_start, effective_date_end = start_end_date(date_info)
        type = get_type(time_info[1])
        currency = "USD"
        tuition_number = get_tuition(time_info[-1])
        duration_type = get_duration_type(time_info[2:])
        duration_num = get_duration_num(time_info[2:])
        location = get_location(time_info[2:])
        if duration_type:
            duration_type = 'duration_'+duration_type
        detail["effective_date_start"] = effective_date_start
        detail["effective_date_end"] = effective_date_end
        detail["type"] = type
        detail["currency"] = currency
        detail["tuition_number"] = tuition_number
        detail["location"] = location
        detail["schedule"] = format_schedule(effective_date_start, effective_date_end, duration_num)
        if duration_type:
            detail[duration_type] = int(duration_num)
    driver.quit()
    write_to_json(details, './filestore/scraped_details.json')


def clean_categories(detail):
    cate_set = set()
    category_list = detail['category']
    for cate in category_list:
        if cate == '':
            del cate
        else:
            cate = cate.replace('-', '').strip()
            cate_set.add(cate)
    categories = list(cate_set)
    return categories


def filter_out_categories():
    details = read_from_json('./filestore/scraped_details.json')
    cate_set = set()
    for detail in details:
        category_list = detail['category']
        for cate in category_list:
            cate_set.add(cate)
    pprint(cate_set)


def re_fetch_time(url, driver):
    driver.get(url)
    time_info = driver.find_elements_by_tag_name('td')[:5]
    time_detail = []
    for info in time_info:
        time_detail.append(info.text)
    print(url)
    print(time_detail)
    return time_detail


def format_schedule(start_date, end_date, duration_num):
    schedule = [
                    [
                      start_date,
                      end_date,
                      str(duration_num),
                      'formal'
                    ]
                ]
    return schedule


# clean_attrs()
