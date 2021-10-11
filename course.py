import time
from pprint import pprint


def course_spider(start_url, driver):
    print('come into course spider')
    driver.get(start_url)
    courses = []
    while True:
        try:
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            next = driver.find_element_by_xpath('//button[contains(text(),"More Results")]')
            next.click()
        except Exception as e:
            print(f'error encounter: {e}')
            break
        # products = response.css('div.container.search-results').css('div.col-6.col-sm-4')
    products = driver.find_elements_by_class_name('product')
    for product in products:
        url = product.find_element_by_css_selector('a.nameLink').get_attribute('href')
        name = product.find_element_by_css_selector('a.nameLink').text
        course = {'name': name,
                   'url': url}
        courses.append(course)
    print(f'---------------{len(courses)}')
    pprint(courses)
    return courses


