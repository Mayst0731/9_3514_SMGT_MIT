import time
from pprint import pprint

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from read_write import read_from_json, write_to_json


def get_all_fac_info():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    details = read_from_json('./filestore/mit_detail_3514_SMGT_XW_0705.json')
    final_faculties = []
    for detail in details:
        print(detail['url'])
        faculties = detail['course_faculties']
        if len(faculties) > 0:
           final_faculties += get_one_course_facs(detail['url'], driver)
    driver.quit()
    write_to_json(final_faculties, './filestore/complete_faculties.json')


def get_one_course_facs(url, driver):
    driver.get(url)
    course_faculties = []
    try:
        driver.execute_script("window.scrollTo(0, 800);")
        faculty_tab = driver.find_element_by_xpath('//ul[@id="productDetailTabs"]//a[@id="faculty-tab"]')
        faculty_tab.click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)
        fac_sessions = driver.find_elements_by_css_selector('div.row.faculty-row.mb-5')
        for fac_session in fac_sessions:
            name = fac_session.find_element_by_css_selector('span.font-weight-bold').text
            title = ''
            ti_ps = fac_session.find_element_by_css_selector('div.mb-0.faculty-titles').find_elements_by_tag_name('p')
            for ti_p in ti_ps:
                title += ti_p.text
            pic_url = fac_session.find_element_by_css_selector('img').get_attribute('src')
            intro_desc = fac_session.find_element_by_css_selector(
                'div.collapse.mt-5.faculty-bio').find_element_by_tag_name('p').text
            fac_info = {'name': name,
                        'title': title,
                        'pic_url': pic_url,
                        'pdf_url': '',
                        'intro_desc': intro_desc,
                        'university_school': '3514_SMGT'}
            course_faculties.append(fac_info)
        print(len(fac_sessions))
    except Exception as e:
        print(e)
    pprint(course_faculties)
    return course_faculties


def delete_repeating_fac():
    new_facs = []
    facs = read_from_json('./filestore/complete_faculties.json')
    fac_set = set()
    for fac in facs:
        if fac['name'] not in fac_set and fac['name'] != '':
            fac_set.add(fac['name'])
            new_facs.append(fac)
        if fac['name'] == 'Daniela Rus':
            fac['title'] = ''
    write_to_json(new_facs, './filestore/complete_faculties.json')


def re_scrape_shitty_fac():
    print('come into shitty fac')
    facs = read_from_json('./filestore/complete_faculties.json')
    fac_set = set()
    for fac in facs:
        if fac['name'] not in fac_set and fac['name'] != '':
            fac_set.add(fac['name'])

    details = read_from_json('./filestore/mit_detail_3514_SMGT_XW_0705.json')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    needed_fac_names = set()
    rest_facs = []
    for detail in details:
        url = detail['url']
        detail_facs = detail['course_faculties']
        for fac in detail_facs:
            if fac not in fac_set:
                needed_fac_names.add(fac)
                print(fac, url)
                rest_facs += get_one_course_facs(url, driver)
    driver.quit()
    to_write_facs = []
    to_write_facs_set = set()
    for fac in needed_fac_names:
        for scraped_fac in rest_facs:
            if fac == scraped_fac['name'] and fac not in to_write_facs_set:
                to_write_facs.append(scraped_fac)
                to_write_facs_set.add(fac)
    pprint(to_write_facs)
    print(len(to_write_facs))
    write_to_json(to_write_facs, './filestore/the_rest_facs.json')

#delete_repeating_fac()
#re_scrape_shitty_fac()