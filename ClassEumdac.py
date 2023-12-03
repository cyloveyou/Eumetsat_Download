# -*- coding: utf-8 -*-
# @Time    :2023/12/2 16:30
# @Author  :小 y 同 学
# @公众号   :小y只会写bug
# @CSDN    :https://blog.csdn.net/weixin_64989228?type=blog

import os
import re
import shutil

import requests
from requests.auth import HTTPBasicAuth


def ReadProductsFile(FilePath):
	# todo 读取产品文件
	with open(FilePath, 'r') as f:
		Products = f.readlines()
	Products = [i.strip() for i in Products]
	return Products


def PrintRemind(info):
	print(info.ljust(130, " ") + "🤗")


def PrintAccept(info):
	print(info.ljust(130, " ") + "√")


def PrintError(info):
	print(info.ljust(130, " ") + "×")


class SaveParam:
	def __init__(self, path, temp_path=None, finish_path=None):
		self.path = path
		self.temp_path = os.path.join(self.path, "temp") if temp_path is None else temp_path
		self.finish_path = os.path.join(self.path, "finish") if finish_path is None else finish_path
		self.CreatPath()

	def CreatPath(self):
		if not os.path.exists(self.temp_path):
			os.makedirs(self.temp_path)
		if not os.path.exists(self.finish_path):
			os.makedirs(self.finish_path)


class UserInfo:
	def __init__(self, customer_key, customer_secret, proxies=None):
		self.customer_key = customer_key
		self.customer_secret = customer_secret
		self.auth = HTTPBasicAuth(self.customer_key, self.customer_secret)
		self.token = self.GetToken(Proxies=proxies)

	def GetToken(self, Proxies=None) -> str:
		token_url = "https://api.eumetsat.int/token"
		token_headers = {
			'referer': 'https://eumetsatspace.atlassian.net/wiki/spaces/EUMDAC',
			'User-Agent': 'eumdac/2.1.0'
		}
		with requests.post(
				auth=self.auth, url=token_url,
				headers=token_headers, proxies=Proxies,
				data={"grant_type": "client_credentials"},
				timeout=10
		) as r:
			return r.json()['access_token']


class ProductInfo:
	def __init__(self, product_url, user_info, save_param: SaveParam):
		self.user_info = user_info
		self.save_param = save_param
		self.product_url = self.UpdateUrl(product_url)
		self.product_name = self.GetProductName() + '.zip'

	def GetProductName(self):
		return self.product_url.split('/')[-1].split('?')[0]

	def DownloadFile(self, Proxies=None):
		temp_file = os.path.join(self.save_param.temp_path, self.product_name)
		finish_file = os.path.join(self.save_param.finish_path, self.product_name)
		if os.path.exists(finish_file):
			PrintAccept(f"{finish_file} existed".center(100, '*'))
			return True
		else:
			PrintRemind(f"{temp_file} downloading")
			f = open(temp_file, 'wb')
			with requests.get(self.product_url, stream=True, proxies=Proxies, timeout=10) as r:
				if r.status_code != 200:
					PrintError("token is invalid, obtain the token again")
					return False  # 返回值非200，token过期
				else:
					for chunk in r.iter_content(chunk_size=1024 * 4):
						if chunk:
							f.write(chunk)
			f.close()
			shutil.move(temp_file, finish_file)
			PrintAccept(f"{temp_file} save success")
			return True

	def UpdateUrl(self, product_url):
		body = re.findall("http.*?access_token=", product_url)
		return body[0] + self.user_info.token
