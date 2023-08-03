![badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Github 每日热搜榜爬虫使用python 编写，将抓取的数据自动存储到mysql数据库中。

![badge](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)

# 配置数据库连接用户名和密码
def db_connect():
    try:
        db = pymysql.connect(host='localhost', port=3306, user='数据库用户名', password='数据库密码', database='gitTrend_db',
                             charset='utf8')
                             

# 创建数据库和数据表

数据库名字：gitTrend_db

表名：github_trending_day

建表语句：

CREATE TABLE IF NOT EXISTS `github_trending_day` (

  `id` int NOT NULL AUTO_INCREMENT,
  
  `ranking` int DEFAULT NULL,
  
  `repo` varchar(50) DEFAULT NULL,
  
  `url` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8_general_ci DEFAULT NULL,
  
  `description` text CHARACTER SET utf8mb3 COLLATE utf8_general_ci,
  
  `lang` varchar(50) DEFAULT NULL,
  
  `stars` varchar(50) DEFAULT NULL,
  
  `forks` varchar(50) DEFAULT NULL,
  
  `added_stars` varchar(120) DEFAULT NULL,
  
  `time` datetime DEFAULT NULL,
  
  PRIMARY KEY (`id`)
  
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb3;



![badge](https://img.shields.io/badge/WeChat-07C160?style=for-the-badge&logo=wechat&logoColor=white)

# 使用上有问题，可扫下面的二维码与我联系

![image](https://github.com/EricLULU/githubDailyTrendSpider/blob/main/img/wechat.jpg)
