# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import re

class ParkPipeline(object):
    def __init__(self):
        self.flag = 0

    def process_item(self, item, spider):  # 数据清洗
        item["url"] = "https://you.ctrip.com" + item["url"]
        return item

class mysqlPipline(object):
    def open_spider(self, spider):  # 爬虫开始前调用一次,连接数据库
        try:
            # 从setting获取
            dbName = spider.settings.get("MYSQL_DB_NAME", "")
            host = spider.settings.get("MYSQL_HOST", "")
            user = spider.settings.get("MYSQL_USER", "")
            password = spider.settings.get("MYSQL_PASSWORD", "")
            listName = spider.settings.get("MYSQL_LISTNAME", "")
            # 连接mysql数据库
            self.db_conn = MySQLdb.connect(db=dbName,
                                           host=host,
                                           user=user,
                                           password=password,
                                           charset="utf8")

            self.db_cursor = self.db_conn.cursor()  # 得到游标
            sql = "truncate table " + listName
            self.db_cursor.execute(sql)
            print("db clear")
        except:
            print("initialization failed")

    def process_item(self, item, spider):  # 处理每个item
        try:
            listName = spider.settings.get("MYSQL_LISTNAME", "")
            values = (item["name"], item["city"],  item["hot"],
                      item["url"], item["author"], item["day"])

            sql = "insert into " + listName +\
                  "(name,city,hot,url,author,day)" + \
                  " values (%s,%s,%s,%s,%s,%s)"

            # print(sql)
            # print(item)
            self.db_cursor.execute(sql, values)

            return item
        except:
            print("fail to insert item")


    def close_spider(self, spider):  # 爬虫结束时调用一次，关闭数据库
        try:
            self.db_conn.commit()  # 统一提交数据
            self.db_cursor.close()
            self.db_conn.close()
            # spider.crawler.engine.close_spider(spider, "停止运行")

        except:
            print("db close error")
