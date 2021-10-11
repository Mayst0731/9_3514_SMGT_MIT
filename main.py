import time

from course import course_spider
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from detail import detail_spider
from fac_map_info import get_all_fac_info, delete_repeating_fac, re_scrape_shitty_fac
from filter_clean import clean_attrs
from re_scrape_faculty_for_detail import re_fetch_faculties
from read_write import write_to_json
from test import delete_wrong_cate, delete_category_file_wrong_cate, delete_blanck_facs, \
    check_invalid_category_in_detail
from write_final_files import write_categories, write_courses


def main(base_url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    courses = course_spider(base_url, driver)
    details = []
    for course in courses:
        detail = detail_spider(course['name'], course['url'], driver)
        details.append(detail)
    write_to_json(details, 'filestore/scraped_details.json')
    driver.quit()
    write_categories()
    re_fetch_faculties()
    re_fetch_faculties()
    clean_attrs()
    write_courses()
    get_all_fac_info()
    delete_repeating_fac()
    re_scrape_shitty_fac()
    delete_wrong_cate()
    delete_category_file_wrong_cate()
    delete_blanck_facs()
    check_invalid_category_in_detail()


if __name__ == '__main__':
    start_time = time.time()
    BASE_URL = "https://executive.mit.edu/course-finder"
    main(BASE_URL)
    duration = time.time() - start_time
    minutes = duration//60
    print(f"Crawled {duration} seconds, {minutes} mins")
