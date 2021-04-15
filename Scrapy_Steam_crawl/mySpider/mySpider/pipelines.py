# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

import json
import codecs
import os

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_item(self, spider):
        self.file.close()
        pass

#写入Mysql
class WriteMysql(object):
    def open_spider(self,spider):
        self.conn = pymysql.Connection(host='127.0.0.1',port=3306,user='admin',password='admin',db='Steam',charset='utf8')
        print(self.conn)
        self.cursor = self.conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Steam_Data (
                    id int not null primary key auto_increment,
                    game_name VARCHAR(80),
                    detail_url VARCHAR(150),
                    release_date VARCHAR(15),
                    publisher VARCHAR(30),
                    developer VARCHAR(30),
                    tags VARCHAR(100),
                    game_price VARCHAR(8),
                    game_review VARCHAR(35),
                    price_discount VARCHAR(6));"""
        self.cursor.execute(sql)
    def process_item(self, item, spider):
        sql = 'insert into Steam_Data values (0,"%s","%s","%s","%s","%s","%s","%s","%s","%s");' \
              % (item['game_name'], item['detail_url'], item['release_date'],
                 item['publisher'],item['developer'],item['tags'],
                 item['game_price'],item['game_review'],item['price_discount'])
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
