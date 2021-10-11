from read_write import read_from_json, write_to_json

'''
No faculties: 
https://executive.mit.edu/course/neuroscience-for-leadership/a056g00000URaZXAA1.html
https://executive.mit.edu/course/executive-program-in-general-management/a056g00000URaZZAA1.html
https://executive.mit.edu/course/building%2C-leading%2C-and-sustaining-the-innovative-organization/a056g00000URaMjAAL.html
https://executive.mit.edu/course/achieving-operational-excellence-through-people/a056g00000URaZwAAL.html
https://executive.mit.edu/course/applied-neuroscience/a056g00000URaZnAAL.html
https://executive.mit.edu/course/impactful-leadership/a056g00000achmcAAA.html
https://executive.mit.edu/course/becoming-a-more-digitally-savvy-board-member/a056g00000WV2TMAA1.html
https://executive.mit.edu/coaching/executive-coaching/a056g00000WUN2SAAX.html
https://executive.mit.edu/coaching/extended-executive-coaching/a056g00000WUN2DAAX.html

no time info:
https://executive.mit.edu/course/neuroscience-for-leadership/a056g00000URaZXAA1.html
https://executive.mit.edu/course/executive-program-in-general-management/a056g00000URaZZAA1.html
https://executive.mit.edu/course/closing-the-gap-between-strategy-and-execution/a056g00000URaZjAAL.html
https://executive.mit.edu/course/building%2C-leading%2C-and-sustaining-the-innovative-organization/a056g00000URaMjAAL.html
https://executive.mit.edu/course/achieving-operational-excellence-through-people/a056g00000URaZwAAL.html
https://executive.mit.edu/course/applied-neuroscience/a056g00000URaZnAAL.html
https://executive.mit.edu/course/impactful-leadership/a056g00000achmcAAA.html
https://executive.mit.edu/course/becoming-a-more-digitally-savvy-board-member/a056g00000WV2TMAA1.html
https://executive.mit.edu/coaching/executive-coaching/a056g00000WUN2SAAX.html
https://executive.mit.edu/coaching/extended-executive-coaching/a056g00000WUN2DAAX.html
https://executive.mit.edu/course/owning-impact/a056g00000acbRZAAY.html

'''


def test_faculties():
    details = read_from_json('./filestore/scraped_details.json')
    for detail in details:
        facs = detail['course_faculties']
        if len(facs) == 0:
            print(detail['url'])


def test_time_attrs():
    rescraped_url = ["https://executive.mit.edu/course/mastering-design-thinking/a056g00000URaa4AAD.html",
                     "https://executive.mit.edu/course/applied-business-analytics/a056g00000URaaVAAT.html",
                     'https://executive.mit.edu/course/cybersecurity-for-managers/a056g00000URaaIAAT.html',
                     'https://executive.mit.edu/course/mastering-negotiation-and-influence/a056g00000URaaRAAT.html']
    details = read_from_json('./filestore/scraped_details.json')
    for detail in details:
        if not detail['time'] and detail['url'] not in rescraped_url:
            print(detail['url'])


def test_locations():
    details = read_from_json('./filestore/mit_detail_3514_SMGT_XW_0705.json')
    for detail in details:
        print(detail['location'])


def test_other_attrs():
    details = read_from_json('./filestore/mit_detail_3514_SMGT_XW_0705.json')
    for detail in details:
        need = {
            "name": "",
            "url": "",
            "category": [],
            "location": [],
            "languages": "Dutch",
            "currency": "EUR",
            "tuition_note": "\u20ac 2.295 (excl. btw)",
            "type": "blended-ov",
            "effective_date_start": "2021-05-31",
            "schedule": [
                [
                    "2021-05-31",
                    "",
                    "6",
                    "formal"
                ]
            ],
            "active": True,
            "priority": 0,
            "publish": 100,
            "is_advanced_management_program": False,
            "tuition_number": 2295,
            "Repeatable": "Y",
            "credential": "",
            "course_takeaways": "",
            "who_attend_desc": "",
            "overview": {},
            "version": 1
        }
        for k in need.keys():
            if k not in detail:
                print(f"do not have {k}")


def delete_wrong_cate():
    details = read_from_json('./filestore/mit_detail_3514_SMGT_XW_0705.json')
    for detail in details:
        cates = detail['category']
        new_cates = []
        for cate in cates:
            if cate != 'Learn more about the live online experience.' and "*" not in cate:
                new_cates.append(cate)
        detail['category']=new_cates
    write_to_json(details, './filestore/mit_detail_3514_SMGT_XW_0705.json')


def delete_category_file_wrong_cate():
    cates = read_from_json('./filestore/mit_category_3514_SMGT_XW_0705.json')
    new_cates = []
    for cate in cates:
        name = cate['category']
        if 'Learn more.' not in name and '*' not in name:
            new_cates.append(cate)
    write_to_json(new_cates, 'filestore/mit_category_3514_SMGT_XW_0920.json')


def delete_blanck_facs():
    details = read_from_json('./filestore/mit_detail_3514_SMGT_XW_0705.json')
    for detail in details:
        facs = detail['course_faculties']
        new_fac = []
        for fac in facs:
            if fac != '':
                new_fac.append(fac)
            else:
                continue
        detail['course_faculties'] = new_fac
    write_to_json(details, 'filestore/mit_detail_3514_SMGT_XW_0920.json')


def check_invalid_category_in_detail():
    details = read_from_json('filestore/mit_detail_3514_SMGT_XW_0920.json')
    for detail in details:
        new_cates = []
        cates = detail['category']
        for cate in cates:
            if 'Learn more' not in cate:
                new_cates.append(cate)
        detail['category'] = new_cates
    write_to_json(details, 'filestore/mit_detail_3514_SMGT_XW_0920.json')

# test_other_attrs()
# test_locations()
# delete_wrong_cate()
# delete_fac()
# delete_category_file_wrong_cate()
# delete_blanck_facs()
# check_invalid_category_in_detail()