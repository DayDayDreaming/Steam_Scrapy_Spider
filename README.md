# Steam_Scrapy_Spider
## 本项目仅供学习交流使用，禁止商用！
Collect all game data from Steam

###系统版本：centos 8.1
###云服务器部署Scrapyd：  
step1：pip install scrapyd  
step2：firewall-cmd --add-port=6800/tcp --permanent  
step3：aliyun安全组内开放6800端口  
step4：进入//python3.6/site-packages/scrapyd文件夹下面有一个default_scrapyd.conf 文件  
&emsp;&emsp;&emsp;找到 bind_address = 127.0.0.1 修改为 bind_address = 0.0.0.0（允许公网访问）   
step5:terminal 运行 scrapyd 即可访问  

###分布式爬虫部署：  
使用gerapy进行调度分配
