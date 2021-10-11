import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from read_write import read_from_json, write_to_json


def re_fetch_faculties():
    count = 0
    details = read_from_json('./filestore/scraped_details.json')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for detail in details:
        count += 1
        print(count)
        faculties = detail['course_faculties']
        if len(faculties) == 0 or (len(faculties) > 0 and faculties[0] == ''):
            new_faculties = get_faculties(detail['url'], driver)
            detail['course_faculties'] = new_faculties
    driver.quit()
    write_to_json(details, './filestore/scraped_details.json')


def get_faculties(url, driver):
    new_faculties = []
    driver.get(url)
    try:
        driver.execute_script("window.scrollTo(0, 800);")
        faculty_tab = driver.find_element_by_xpath('//ul[@id="productDetailTabs"]//a[@id="faculty-tab"]')
        faculty_tab.click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)
        name_sessions = driver.find_elements_by_xpath('//span[@class="font-weight-bold"]')
        for name_session in name_sessions:
            fac_name = name_session.text
            print(fac_name)
            new_faculties.append(fac_name)
    except Exception as e:
        print(e)
    return new_faculties


#re_fetch_faculties()