# -*- coding: utf-8 -*-
# @Time    :2023/12/2 14:25
# @Author  :小 y 同 学
# @公众号   :小y只会写bug
# @CSDN    :https://blog.csdn.net/weixin_64989228?type=blog
import multiprocessing
import random
import time

from tqdm import trange

from ClassEumdac import *

# todo 设置参数
consumer_key = 'kKJgfhupQTkXbMEMPJ6unbr4mXIa'  # todo 设置key
consumer_secret = 'FxuQF4mRoM1MVUOWb4bQFq8RRJMa'  # todo 设置secret
products_file_path = "./products_all.txt"  # todo 设置产品信息文件路径
download_path = "./test"  # todo 设置下载路径
IPPort = "127.0.0.1:10809"  # todo 设置代理
multiN = 10  # todo 进程个数

proxies = {
	"http": IPPort,
	"https": IPPort
}
user = UserInfo(consumer_key, consumer_secret, proxies=proxies)
save_param = SaveParam(download_path)


def multi(url):
	global user, save_param, proxies
	product = ProductInfo(url, user, save_param)
	try:
		if not product.DownloadFile(proxies):
			user.token = user.GetToken(proxies)
			product.DownloadFile(proxies)
	except:
		PrintError("Network connection failure Download failure")
		t = random.randint(20, 60)
		for _ in trange(t, desc=f"wait {t} seconds"):
			time.sleep(1)


if __name__ == '__main__':
	url_list = ReadProductsFile(products_file_path)
	stime = time.ctime()
	PrintRemind("There are {} products in total".format(len(url_list)))
	with multiprocessing.Pool(multiN) as p:
		p.map(multi, url_list)
	PrintRemind("All products have been downloaded,stime:{},etime:{}".format(stime, time.ctime()))
