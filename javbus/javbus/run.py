# -*- coding: utf-8 -*-
from scrapy import cmdline

from javbus import DataTools

import json


cmd = 'scrapy crawl %s' % 'javbus'
cmdline.execute(cmd.split())

# import re
#
# source = r"\r\n\tvar gid = 37042488304;\r\n\tvar uc = 0;\r\n\tvar img = 'https://pics.javcdn.pw/cover/6j8g_b.jpg';\r\n"
# parms = source.split(';')
# gid = re.search('\d+',parms[0]).group()
# uc = re.search('\d+',parms[1]).group()
# img = re.search("(?<=')[^']*",parms[2]).group()
#
# print(parms[0])
# print(gid)
# print(uc)
# print(img)
# from scrapy.utils.project import get_project_settings
#
# headers = get_project_settings()['DEFAULT_REQUEST_HEADERS'].copy_to_dict()
# print(headers)
