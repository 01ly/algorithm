#coding:utf-8
import os
import requests
from bs4 import BeautifulSoup as bs 

headers= {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

threshold = 5
gap = 3
density  = 45

def get_content_lines(url):
	h = requests.get(url,headers=headers)
	c = bs(h.text,'lxml')
	[i.extract() for i in c('script')]
	[i.extract() for i in c('style')]
	[i.extract() for i in c('head')]
	return c.body.text.splitlines()


def get_content_dict(url):
	results={}
	comobo_num =0
	combo_len = 0
	combo_null=0
	combo_text = ''
	pre_len = 0
	lines_content = get_content_lines(url)
	for i in lines_content:
		if i.strip():
			pre_len = len(i)
			comobo_num += 1 
			combo_null = 0
			combo_len += pre_len
			combo_text = combo_text+i+ os.linesep
			if len(lines_content)==1 and pre_len >= density*threshold:
				results[pre_len]=combo_text
		else:
			combo_null +=1
			if pre_len:
				if combo_null > gap:
					if combo_len >= density*threshold \
					and comobo_num >= threshold:
						results[combo_len]=combo_text
				else:
					continue
			comobo_num = 0
			combo_len = 0 if combo_null > gap else combo_len
			pre_len = 0
			combo_text = '' if combo_null > gap else combo_text
	return results


def get_top_len_content(results,top):
	tops = [results[i] for _,i in enumerate(reversed(sorted(results))) if _< top]
	return tops


def extract(url,top=10):
	results = get_content_dict(url)
	return get_top_len_content(results,top)


if __name__ == '__main__':
	url = 'https://mathpretty.com/8664.html'
	top_results = extract(url,top=2)
	mostlike_content = top_results[0]
	print(mostlike_content)