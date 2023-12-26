# -*- coding: utf-8 -*-
# @Time    :2023/12/2 16:30
# @Author  :小 y 同 学
# @公众号   :小y只会写bug
# @CSDN    :https://blog.csdn.net/weixin_64989228?type=blog
import os
import random
import re
import shutil
import time

import requests
from requests.auth import HTTPBasicAuth
from tqdm import trange


class UserPrint:
	@staticmethod
	def PrintRemind(info: str) -> None:
		print("\033[33m" + info.ljust(130, " ") + "🤗" + "\033[0m", flush=True)

	@staticmethod
	def PrintAccept(info: str) -> None:
		print("\033[32m" + info.ljust(130, " ") + "√" + "\033[0m", flush=True)

	@staticmethod
	def PrintError(info: str) -> None:
		print("\033[31m" + info.ljust(130, " ") + "×" + "\033[0m", flush=True)


class ProductsInfoFile:
	@staticmethod
	def ProductIdList(url, proxies) -> list:
		url = url.strip()
		res = requests.get(url=url, proxies=proxies)
		resJson = res.json()
		temp = [resJson["features"][i]["properties"]["links"]["data"][0]["href"] for i in
				range(len(resJson["features"]))]
		return temp

	def CreateProductsFile(self, url, SavePath, proxies) -> None:
		url = url.strip()
		resJson = requests.get(url=url, proxies=proxies).json()
		itemsPerPage, totalResults = resJson['itemsPerPage'], resJson['totalResults']
		keyStr = re.findall(r"si=(\d+)", url)[0]

		idList = []
		for i in range(0, totalResults, itemsPerPage):
			new_url = url.replace(f"si={keyStr}", f"si={i}")
			idList += self.ProductIdList(new_url, proxies)
		with open(SavePath, 'w') as f:
			f.write("\n".join(list(map(lambda x: x + "?access_token=111", idList))))

	@staticmethod
	def ReadProductsFile(FilePath: str) -> list:
		"""
		读取txt文中的产品文件url
		@param FilePath: str txt文件路径
		@return: list 产品url列表
		"""
		with open(FilePath, 'r') as f:
			Products = f.readlines()
		Products = [i.strip() for i in Products]
		return Products


class SaveParam:
	def __init__(self, path: str, temp_path=None, finish_path=None):
		"""
		保存参数
		@param path: str 保存径路
		@param temp_path: str 临时文件夹路径，默认为path/temp
		@param finish_path: str 下载完成文件夹路径，默认为path/finish
		"""
		self.path = path
		self.temp_path = os.path.join(self.path, "temp") if temp_path is None else temp_path
		self.finish_path = os.path.join(self.path, "finish") if finish_path is None else finish_path
		self.CreatPath()

	def CreatPath(self) -> None:
		"""
		创建临时文件夹和下载完成文件夹
		@return:None
		"""
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
		"""
		获取token
		@param Proxies: str 是否使用代理
		@return:str token
		"""
		token_url = "https://api.eumetsat.int/token"
		token_headers = {
			'referer': 'https://eumetsatspace.atlassian.net/wiki/spaces/EUMDAC',
			'User-Agent': 'eumdac/2.1.0'
		}
		try:
			with requests.post(
					auth=self.auth, url=token_url,
					headers=token_headers, proxies=Proxies,
					data={"grant_type": "client_credentials"},
					timeout=10
			) as r:
				return r.json()['access_token']
		except Exception as e:
			UserPrint.PrintError("Network connection failure GetToken failure")
			return self.GetToken(Proxies=Proxies)


class ProductInfo:
	def __init__(self, product_url, user_info, save_param: SaveParam):
		"""
		单个下载文件的信息
		@param product_url: str 产品下载地址
		@param user_info: UserInfo 用户私密信息
		@param save_param: SaveParam 保存参数
		"""
		self.user_info = user_info
		self.save_param = save_param
		self.product_url = self.UpdateUrl(product_url)
		self.product_name = self.GetProductName() + '.zip'

	def GetProductName(self) -> str:
		"""
		根据url获取产品名称
		@return: str 产品名称
		"""
		return self.product_url.split('/')[-1].split('?')[0]

	def DownloadFile(self, Proxies=None) -> bool:
		"""
		下载文件
		@param Proxies: dict 默认不使用代理
		@return: bool 下载成功返回True，否则返回False
		"""
		temp_file = os.path.join(self.save_param.temp_path, self.product_name)
		finish_file = os.path.join(self.save_param.finish_path, self.product_name)
		if os.path.exists(finish_file):
			UserPrint.PrintAccept(f"{finish_file} existed")
			return True
		else:
			UserPrint.PrintRemind(f"{temp_file} downloading")
			f = open(temp_file, 'wb')
			try:
				with requests.get(self.product_url, stream=True, proxies=Proxies, timeout=10) as r:
					if r.status_code != 200:
						UserPrint.PrintError("token is invalid, obtain the token again")
						self.user_info.token = self.user_info.GetToken(Proxies)
						self.DownloadFile(Proxies)
					else:
						for chunk in r.iter_content(chunk_size=1024 * 4):
							if chunk:
								f.write(chunk)
				f.close()
			except Exception as e:
				UserPrint.PrintError(f"{temp_file} Download failure Because Network connection failure")
				t = random.randint(20, 60)
				for _ in trange(t, desc=f"wait {t} seconds"):
					time.sleep(1)
				self.DownloadFile(Proxies)
			shutil.move(temp_file, finish_file)
			UserPrint.PrintAccept(f"{temp_file} save success")
			return True

	def UpdateUrl(self, product_url) -> str:
		"""
		根据token更新url
		@param product_url: str 产品下载地址url
		@return: str 更新后的url
		"""
		body = re.findall("http.*?access_token=", product_url)
		return body[0] + self.user_info.token
