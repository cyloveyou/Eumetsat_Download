# -*- coding: utf-8 -*-
# @Time    :2023/12/2 14:25
# @Author  :小 y 同 学
# @公众号   :小y只会写bug
# @CSDN    :https://blog.csdn.net/weixin_64989228?type=blog
import multiprocessing

from ClassEumdac import *

# todo 设置参数
consumer_key = 'kKJgfhupQTkXbMEMPJ6unbr4mXIa'  # todo 设置key
consumer_secret = 'FxuQF4mRoM1MVUOWb4bQFq8RRJMa'  # todo 设置secret
products_url_path = "./products_url.txt"  # todo 设置产品信息文件保存路径
products_file_path = "./products_all.txt"  # todo 设置产品信息文件保存路径
download_path = "./test"  # todo 设置产品下载保存路径
IPPort = "127.0.0.1:10809"  # todo 设置代理
multiN = 5  # todo 进程个数

proxies = {
	"http": IPPort,
	"https": IPPort
}
user = UserInfo(consumer_key, consumer_secret, proxies=proxies)
save_param = SaveParam(download_path)

UserPrint.PrintRemind("Initialization completed!")

def multi(url):
	global user, save_param, proxies
	product = ProductInfo(url, user, save_param)
	product.DownloadFile(proxies)


if __name__ == '__main__':
	flag = input("Whether product information files need to be updated? (y/n):")
	ProductsInfoFile = ProductsInfoFile()
	if flag == 'y' or flag == 'Y':
		UserPrint.PrintRemind(f"Creating a product information file, Path: {products_file_path}")
		f = open(products_url_path, 'r')
		url = f.read().strip()
		f.close()
		ProductsInfoFile.CreateProductsFile(url, products_file_path, proxies)
		UserPrint.PrintAccept(f"Product information file created successfully,Path:{products_file_path}")

	# 多进程
	url_list = ProductsInfoFile.ReadProductsFile(products_file_path)
	stime = time.ctime()
	UserPrint.PrintRemind("There are {} products in total".format(len(url_list)))
	with multiprocessing.Pool(multiN) as p:
		p.map(multi, url_list)
	UserPrint.PrintRemind("All products have been downloaded,start time:{},end time:{}".format(stime, time.ctime()))

	# # 多线程
	# url_list = ReadProductsFile(products_file_path)
	# stime = time.ctime()
	# PrintRemind("There are {} products in total".format(len(url_list)))
	# with ThreadPool(multiN) as p:
	# 	p.map(multi, url_list)
	# PrintRemind("All products have been downloaded,stime:{},etime:{}".format(stime, time.ctime()))
	pass
