# Steam_Scrapy_Spider

Collect all game data from Steam  

#### 开发环境:Python3.7，Mysql5.6（可选），Redis6.0.9（可选）

#### 系统版本:Centos 8.1/Windows 10  

#### 项目爬取内容:
```
class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    game_name = scrapy.Field() #游戏名称
    detail_url = scrapy.Field() #详情页链接
    release_date = scrapy.Field() #发行日期
    publisher = scrapy.Field() #发行商
    developer = scrapy.Field() #开发商
    tags = scrapy.Field() #游戏标签
    game_review = scrapy.Field() #游戏好评率
    game_price = scrapy.Field()#游戏原价
    info = scrapy.Field()#游戏简介
    imgs = scrapy.Field()#游戏图片
    review_list = scrapy.Field()#玩家评价
    price_discount = scrapy.Field()#打折折扣
```

#### 云服务器部署Scrapyd：  
+ step1:pip install scrapyd  
+ step2:firewall-cmd --add-port=6800/tcp --permanent  
+ step3:aliyun安全组内开放6800端口  
+ step4:进入//python3.6/site-packages/scrapyd文件夹下面有一个default_scrapyd.conf 文件  
&emsp;&emsp;&ensp;找到 bind_address = 127.0.0.1 修改为 bind_address = 0.0.0.0（允许公网访问）   
+ step5:terminal 运行 scrapyd 即可访问  

#### 分布式爬虫部署:  
+ 使用gerapy进行调度分配  
  
##### 特别致谢:Stackoverflow论坛的各位大佬们  

 