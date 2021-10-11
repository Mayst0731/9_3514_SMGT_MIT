'''
faculty: name, title, pic_url, pdf_url, intro_desc, university_school

testimonials: name, title, company, active, publish, picture_url, visual_url, testimonial_statement

'''
import time
from pprint import pprint

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def detail_spider(name, url, driver):
    print(url)
    driver.get(url)
    time_info = driver.find_elements_by_tag_name('td')[:5]
    time_detail = []
    for info in time_info:
        time_detail.append(info.text)
    categories_ = driver.find_elements_by_xpath('//p[contains(text(),"Topics")]/following-sibling::p')
    category = []
    for cate in categories_:
        category.append(cate.text)
    desc_ps = driver.find_elements_by_xpath('//div[@class="value content"]/p')
    desc_ps.pop()
    desc = ''
    for desc_p in desc_ps:
        desc += desc_p.text.strip()

    video_url = ''
    video_title = ''
    try:
        video_ = driver.find_element_by_xpath('//iframe')
        video_url = video_.get_attribute('src')
        if video_url:
            video_title = f'MIT Sloan {name}'
    except Exception as e:
        print(e)
    # takeaways
    takeaways = ''
    try:
        driver.execute_script("window.scrollTo(0, 500);")
        takeaways_tab = driver.find_element_by_xpath('//ul[@id="productDetailTabs"]//a[@id="takeaways-tab"]')
        takeaways_tab.click()
        time.sleep(1)
        takeaways_items = driver.find_elements_by_xpath('//div[@class="mt-4"]/p')
        for item in takeaways_items:
            takeaways += item.text
    except Exception as e:
        print(e)

    try:
        takeaways_lists = driver.find_elements_by_xpath('//div[@class="mt-4"]/ul/li')
        for li in takeaways_lists:
            takeaways += li.text
    except Exception as e:
        print(e)

    # who_attend_desc
    who_attend_desc = ''
    try:
        driver.execute_script("window.scrollTo(0, 500);")
        who_tab = driver.find_element_by_xpath('//ul[@id="productDetailTabs"]//a[@id="participants-tab"]')
        who_tab.click()
        time.sleep(1)
        who_items = driver.find_elements_by_xpath('//div[@class="mt-4"]/p')
        for item in who_items:
            who_attend_desc += item.text
    except Exception as e:
        print(e)

    # faculties
    course_faculties = []
    try:
        driver.execute_script("window.scrollTo(0, 800);")
        faculty_tab = driver.find_element_by_xpath('//ul[@id="productDetailTabs"]//a[@id="faculty-tab"]')
        faculty_tab.click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)
        name_sessions = driver.find_elements_by_xpath('//span[@class="font-weight-bold"]')
        for name_session in name_sessions:
            fac_name = name_session.text
            print(fac_name)
            course_faculties.append(fac_name)
    except Exception as e:
        print(e)
    # testis
    testis = []
    try:
        driver.execute_script("window.scrollTo(0, 500);")
        testi_tab = driver.find_element_by_xpath('//ul[@id="productDetailTabs"]//a[@id="reviews-tab"]')
        testi_tab.click()
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3)
        reviews = driver.find_elements_by_xpath('//span[@class="tt-c-review__text-content"]')
        names = driver.find_elements_by_xpath('//span[@class="tt-o-byline__item tt-o-byline__author"]')
        for i, review in enumerate(reviews):
            testi = {
                "name": names[i].text,
                "testimonial_statement": review.text,
                "title": "",
                "company": "",
                "picture_url": "",
                "visual_url": "",
                "publish": 100,
                "active": True}
            testis.append(testi)
    except Exception as e:
        print(e)
    return {'name': name,
            'url': url,
            'category': category,
            'time': time_detail,
            'overview': {'desc':desc,
                         'video_url': video_url,
                         'video-title': video_title,
                         },
            'course_takeaways': takeaways,
            'who_attend_desc': who_attend_desc,
            'testimonials': testis,
            'course_faculties': course_faculties
            }



