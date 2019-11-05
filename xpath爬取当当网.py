import requests
from lxml import etree
#from itertools import chain
#import json # 利用接口读取访问json文件
import time
'''
xpath爬取当当网图书畅销榜
'''

def main():
	#r = []
	d = {}

	for i in range(1,26):
		resp = requests.get('http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-'+str(i))
		res_xpath = etree.HTML(resp.text)
		title = res_xpath.xpath('///div[@class="name"]/a/text()') # 书名
		author = res_xpath.xpath('///div[@class="publisher_info"]/a[@title]/text()') # 作者
		price = res_xpath.xpath('///div[@class="price"]/p/span[@class="price_n"]/text()') # 价格
		#publisher = res_xpath.xpath('///div[@class="publisher_info"]/a[@href]/text()') # 出版社
		star = res_xpath.xpath('///div[@class="star"]/span[@class="tuijian"]/text()') # 推荐度
		date = res_xpath.xpath('///div[@class="publisher_info"]/span/text()') # 出版日期
		d.setdefault('_title',[]).append(title) # 格式化字典
		d.setdefault('_author',[]).append(author)
		d.setdefault('_price',[]).append(price)
		d.setdefault('_star',[]).append(star)
		d.setdefault('_date',[]).append(date)
		print('第%s页爬取完成！' % i)

		#r = list(chain(r,rst))
		time.sleep(1)
	print(d)
	# with open('D:/r/book4.txt','a+',encoding='utf-8') as f:
	# 	for i in range(0,len(r)):
	# 		f.write(str(i+1)+'. '+r[i]+'\n')
	# 	# data_model = json.loads(i)
	# 	# for news in data_model:
	# 	# 	print(news)
	# 	# #print(rst)

	# 	print('已全部写入！')
		


if __name__ == '__main__':
    main()
