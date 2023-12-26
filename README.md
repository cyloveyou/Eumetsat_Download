# 从Eumetsat批量下载哨兵数据等各种数据

## 🌿前言

1. 脚本介绍：使用**Python+科学上网+多进程**，快速批量检索和下载Eumetsat官网的数据(Sentinel-3、Sentinel-6等数据产品)
2. Eumetsat官网：https://data.eumetsat.int/search?
3. Eumetsat简介：EUMETSAT(European Organisation for the Exploitation of Meteorological Satellites) 是欧洲气象卫星开发组织，其主要宗旨是建立、维护和运行欧洲的气象卫星系统，其官网不仅仅提供有Sentinel-3、Sentinel-6、Jason-3等卫星数据，还包括其他数据产品。具体可以进入官网进行查看。
   ![image-20231226231739365](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226231739365.png)
   ![image-20231226232308208](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226232308208.png)

## 🍀脚本构成

### ClassEumdac.py

&emsp;&emsp;包含了UserPrint、ProductsInfoFile、SaveParam、UserInfo、ProductInfo四个类。

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
2. 获取
   ![获取JSON网址](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226234651924.png)
   ![image-20231226235434820](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235434820.png)
3. 将JSON url复制粘贴到products_url.txt文件中
   ![image-20231226235548912](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235548912.png)

### 设置参数

1. consumer_key和consumer_secret参数设置
   登录EUMETSAT，点击API Key，随后即可看到参数，复制替换到脚本
   ![image-20231226235729535](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235729535.png)
   ![image-20231226235858394](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226235858394.png)
2. products_url_path、products_file_path以及download_path参数设置
   products_url_path：是存放JSON url的文件，这里默认为products_url.txt，也就是第一步的txt文件。
   products_file_path：用于存放从JSON url获取的产品下载链接文件，同时也用于下载脚本的输入数据。
   download_path：产品保存文件夹，程序会自动以该路径创建缓存文件夹(temp)和完成文件夹(finish)，下载完整的数据会被保存到finish文件夹中。
3. IPPort参数设置
   为本地代理参数，开启科学上网，具体八仙过海，此处做不赘述。**值得注意的是：需要保证代理流量足够**
   Windows自带搜索框，搜索`Internet属性`，按下图操作。
   ![image-20231118153242930](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/202311181532045.png)
   需要注意的是，程序中IPPort写法应为`替换位置一:替换位置二`
4. multiN参数设置

### 运行程序

## 🌹结语

# ![image-20231226204554259](https://markdownf.oss-cn-shanghai.aliyuncs.com/mdimg/image-20231226204554259.png)