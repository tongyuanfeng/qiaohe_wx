import re
import os
import pymysql


def select(db, sql_cmd):
    cursor = db.cursor()

    cursor.execute(sql_cmd)
    return cursor.fetchall()


import  requests
if __name__ == '__main__':
    db = pymysql.connect(host="web.chong.so", user="caihua", passwd="caihua", db="caihua", port=3306,
                         charset='utf8')

    cmd = "SELECT  SYMBOL,EXCHANGE FROM CHDQUOTE WHERE tdate='20170823'"
    res=select(db,cmd)
    print(res)
    for line in res:
        symbol = line[0]
        exchange = line[1]
        cmd="http://mysql00.chong.so:8085/dam/v1/tsdb/q?db=caihua&series=QUOTE.{}.{}&start=20160101".format(symbol,exchange)
    #     # print(cmd)
        s=requests.get(cmd)
        r=s.json()
        p=r['points']
        if len(p)==0:
            # print((symbol,exchange))
            print(cmd)
    db.close()
