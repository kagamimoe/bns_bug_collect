# -*- coding: utf-8 -*-
'''
Created on 2014
Use for search bugs in the bbs of bns 
@author: kagamimoe
'''

import urllib2
import urllib
import cookielib
import hashlib
import re
import string
import xlwt
from datetime import date


url_min = 'http://bns.gamebbs.qq.com/forum.php?mod=forumdisplay&fid=30929&typeid=63&typeid=63&filter=typeid&page='

def get_buglist(html):
	r1 = r'class="xst" >(.*?)<' # title 
	title_re = re.compile(r1)
	title_list = title_re.findall(html)
	del title_list[0] # delete the first post
	# print 'start'
	r2 = r'BUG</a>]</em> <a href="(.*?)"'
	href_re = re.compile(r2)
	href_list_old = href_re.findall(html)
	href_list = []
	for i in href_list_old:
		i = 'http://bns.gamebbs.qq.com/' + i
		i = string.replace(i, '&amp;', '&')
		href_list.append(i)
	del href_list[0] # delete the first post
	# r3 = r'<em><span.*><span title="(.*?)">|<span>2014-\d{1,2}-\d{1,2}'
	r3 = r'<em>.{1,35}?(2014-\d{1,2}-\d{1,2})'
	date_re = re.compile(r3)
	date_list = date_re.findall(html)
	# print 'start3'
	# print  len(date_list)
	return  title_list, href_list, date_list

if __name__ == '__main__':
	t = date.today()
	page = 1
	f = xlwt.Workbook()
	table = f.add_sheet('bug list')
	all_title_list = []
	all_href_list = []
	all_date_list = []
	pages = int(raw_input("How many pages of bugs do you want to collect?"))
	while page <= pages:
		url =  url_min + str(page)
		resource = urllib2.urlopen(url)
		html =  resource.read()
		title_list, href_list, date_list = get_buglist(html)
		all_title_list = all_title_list + title_list
		all_href_list = all_href_list + href_list
		all_date_list = all_date_list + date_list
		page = page + 1
	for i in range(len(all_title_list)):
		table.write(i, 0, all_title_list[i].decode('utf-8'))
		table.write(i, 1, all_href_list[i])
		table.write(i, 2, all_date_list[i])
	f.save('bug- ' + t.isoformat().decode('utf-8') +'.xls')