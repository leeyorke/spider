## 爬取豆瓣读书排行榜并写入数据库

``` python
import urllib.request
from itertools import chain
import time
import re
import pymysql

'''
一个网页爬虫程序，可以实现以下反爬机制：
1.浏览器伪装
2.用户代理
3.IP代理
4.cookie
'''
class Spider(object): # 定义一个爬虫类
	"""docstring for Spider"""
	def __init__(self):
		super(Spider, self).__init__()

	def spider(self, ListUrl, pattern, headers): # 爬取
		self.headers = headers
		self.ListUrl = ListUrl
		self.pattern = pattern
		self.result = []

		
		
		for i in self.ListUrl:
			
			req = urllib.request.Request(url=i, headers=self.headers)
			resq = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
			#pat = pattern
			self.rst = re.compile(self.pattern).findall(resq)
			print(self.rst)
			self.result = list(chain(self.result,self.rst)) # 将各个页面结果合并到一个列表
			time.sleep(1)
		print('爬取完毕！')
		print('---' * 10)
		print(self.result)
		print('---' * 10)
			
		
		
	def clean(self): # 数据清洗
		self.s = set(self.result)
		self.s.remove('可试读')
		self.result = list(self.s)
		# for k in self.result:
		# 	if '可试读' in self.result:
		# 		self.result.remove('可试读')
		print('数据清洗成功！')
		print(self.result)
		print('---' * 10)



	def write_file(self, path): # 写入txt文件
		self.path = path
		global index
		fh=open(self.path,"a+")
		for i in range(0,len(self.rst)):
		    # if self.rst[i] == '可试读':
		    # 	continue
		    fh.write(str(index)+'.'+self.rst[i]+"\n")
		    index += 1
		fh.close()




	def database(self): # 写入数据库

		global index

		conn = pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = 'root',
			password = 'root',
			db = 'douban',
			charset = 'utf8',
			cursorclass = pymysql.cursors.DictCursor
		)

		cursor = conn.cursor() # 创建游标

		try:
			for i in self.result:
				sql = "INSERT INTO book(id,name)VALUE({},'{}')".format(index, i) # 定义sql语句
				print('--------------------{}'.format(sql)) # 打印sql语句看看是否正确
				cursor.execute(sql) # 执行sql
				print('第%s条插入成功!' % index)
				index += 1
		except Exception: print('插入失败！')

		conn.commit() # 提交，不然无法保存新建或者修改的数据
		print('数据已提交！')
		cursor.close() # 关闭游标
		conn.close() # 关闭连接


def main():

	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
	                  'AppleWebKit/537.36 (KHTML, like Gecko) '
	                  'Chrome/75.0.3770.142 Safari/537.36',
	}	
	pattern = 'title="(.*)"'
	#path = 'D:/r/book2.txt'
	ListUrl = []
	for x in range(0,250,25):
		url = 'https://book.douban.com/top250?start='+str(x)
		ListUrl.append(url)
	s = Spider()
	s.spider(ListUrl, pattern, headers)

	s.clean()
	#s.write_file()
	s.database()

	
	

if __name__ == '__main__':
	index = 1
	main()
```
思考：

 1. 代码还存在优化空间