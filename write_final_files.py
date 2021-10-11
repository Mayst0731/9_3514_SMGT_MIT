from pprint import pprint

from read_write import read_from_json, write_to_json


def write_categories():
    details = read_from_json('./filestore/scraped_details.json')
    cates = []
    cates_set = set()
    for detail in details:
        categories = detail['category']
        for category in categories:
            category = category.replace('-', '').strip()
            if category != '' and category not in cates_set and category != 'Learn more about the live online ' \
                                                                            'experience.':
                info = {"category": category,
                        'url': 'https://executive.mit.edu/course-finder',
                        'parent_url': 'https://executive.mit.edu'}
                cates_set.add(category)
                cates.append(info)
    write_to_json(cates, './filestore/mit_category_3514_SMGT_XW_0705.json')
    pprint(cates)


def write_courses():
    details = read_from_json('./filestore/scraped_details.json')
    clean_details = []
    for detail in details:
        del detail['time']
        detail['location'] = ['Cambridge, MA, United States']
        clean_details.append(detail)
    write_to_json(clean_details, 'filestore/mit_detail_3514_SMGT_XW_0705.json')


# write_courses()