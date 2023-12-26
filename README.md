# 从Eumetsat批量下载哨兵数据等各种数据

## 🌿前言

1. 脚本介绍：使用**Python+科学上网+多进程**，快速批量检索和下载Eumetsat官网的数据(Sentinel-3、Sentinel-6等数据产品)
2. Eumetsat官网：https://data.eumetsat.int/search?
3. Eumetsat简介：EUMETSAT(European Organisation for the Exploitation of Meteorological Satellites) 是欧洲气象卫星开发组织，其主要宗旨是建立、维护和运行欧洲的气象卫星系统，其官网不仅仅提供有Sentinel-3、Sentinel-6、Jason-3等卫星数据，还包括其他数据产品。具体可以进入官网进行查看。
   ![image-20231226231739365](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226231739365.png)
   ![image-20231226232308208](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226232308208.png)

## 🍀脚本构成

### ClassEumdac.py

包含了UserPrint、ProductsInfoFile、SaveParam、UserInfo、ProductInfo四个类。

1. UserPrint：包含了一些个性化打印提示函数。
2. ProductsInfoFile：主要是从获取的JSON数据提取下载链接、读取下载链接等功能。
3. SaveParam：保存参数，包含缓存文件路径和保存路径的创建
4. UserInfo：用户个人信息customer_key、customer_secret、token等
5. ProductInfo：对单个产品进行下载

### EUMETSATMain.py

&emsp;&emsp;程序入口，包含了一些参数设置，具体设置教程见下文。

## 🌸使用教程

&emsp;&emsp;主要包括设置products_url，设置用户参数。

### 设置products_url

1. 获取products_url，进入EUMETSATM官网https://data.eumetsat.int/search?，选择需要的产品数据文件进行检索。
   ![产品检索](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226234556406.png)

   ---

2. 获取JSON url
   ![获取JSON网址](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226234651924.png)
   ![image-20231226235434820](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235434820.png)

   ---

3. 将JSON url复制粘贴到products_url.txt文件中
   ![image-20231226235548912](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235548912.png)

### 设置参数

1. consumer_key和consumer_secret参数设置
   登录EUMETSAT，点击API Key，随后即可看到参数，复制替换到脚本
   ![image-20231226235729535](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235729535.png)
   ![image-20231226235858394](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235858394.png)

   ---

2. products_url_path、products_file_path以及download_path参数设置
   products_url_path：是存放JSON url的文件，这里默认为products_url.txt，也就是第一步的txt文件。
   products_file_path：用于存放从JSON url获取的产品下载链接文件，同时也用于下载脚本的输入数据。
   download_path：产品保存文件夹，程序会自动以该路径创建缓存文件夹(temp)和完成文件夹(finish)，下载完整的数据会被保存到finish文件夹中。

   ---

3. IPPort参数设置
   为本地代理参数，开启科学上网，具体八仙过海，此处做不赘述。**值得注意的是：需要保证代理流量足够**
   Windows自带搜索框，搜索`Internet属性`，按下图操作。
   ![image-20231118153242930](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311181532045.png)
   需要注意的是，程序中IPPort写法应为`替换位置一:替换位置二`

   ---

4. multiN参数设置

   multiN为多进程个数参数，一般小于CPU核数，不可过大

### 运行程序

经过上述参数设置完成后，可以运行程序，会出现以下提示：
![image-20231227002145037](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231227002145037.png)

---

对于下载出错的文件，会提示并随机等待几十秒后重新下载：

![image-20231227003510444](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231227003510444.png)

---

对于已经存在的文件，会跳过下载：

![image-20231227003002217](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231227003002217.png)

对于Token过期，会重新获取Token并重新下载（这里目前还未遇到，不便截图）

## 🌹结语

1. 就目前而言，脚本对于断网、token过期等常见现象抵抗能力良好，还遇到过异常情况，欢迎邮箱私信。
2. 对于本脚本，还有很多可以优化的地方，希望大家可以多给些建议，不忘收藏关注😉
3. 本人也是测绘遥感方向的学习者，愿意结交志同道合的伙伴，对于脚本的相关问题可在一定程度上提供帮助。
4. 脚本进程数不宜设置过大，若修改脚本进程过大放在多核服务器上执行导致对EUMETSAT服务器的攻击行为，本站不承担任何责任。
5. ......最终解释权归作者所有。作者邮箱：3232076199@qq.com，烦请说明来意。