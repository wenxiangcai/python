#encoding=UTF-8

import requests
from  pymongo import MongoClient

Headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

all_type = []

#获得每页价值内容
def get_content(content):
	try:
		title = content["res"]["payload"]["title"]
		print "[-]title:"+title
		now_list = []
		for item in content["res"]["subjects"]:
			movie_title = item["title"].strip() #影片名称
			rate =  item["rating"]  #排名
			cover = item["cover"]  #封面
			url = item["url"] #豆瓣链接
			film_dicts = {
				'movie_title':movie_title,
				'rate':rate,
				'cover':cover,
				'url':url,
				'title':title
			}
			now_list.append(film_dicts)
		film_insert(now_list,title)
	except:
		pass
#插入数据库
def film_insert(film_list,title):
	#连接mongodb
	host = '127.0.0.1'
	port = 27017
	conn = MongoClient(host,port)
	#选择数据库
	db = conn['doubanfilm']
	#选择表
	film = db.film
	db.film.insert(film_list)
	#for items in film_list.find(): #file_list.find()是迭代对象
	#选择另一个表
	dbtitle = db.title
	type_title = {"title":title}
	dbtitle.insert(type_title)


if __name__ == '__main__':
	headers = Headers
	print '[-]正在抓取中...'
	for i in range(1,70):
		url = "https://movie.douban.com/ithil_j/activity/movie_annual2016/widget/{}".format(i)
		r = requests.get(url=url,headers=headers)
		content = json.loads(r.content)
		get_content(content)

