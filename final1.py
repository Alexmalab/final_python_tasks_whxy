import pymysql
import requests
from lxml import etree

#具体字段包括年份、排名、国家/地区、所在洲、通胀率；
def get_list_data(year): #返回某年数据
    base_url= 'https://www.kylc.com/stats/global/yearly/g_inflation_consumer_prices'
    url = base_url+'/'+str(year)+'.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'}
    r = requests.get(url=url,headers=headers)
    html = etree.HTML(r.text)
    tr_l = html.xpath('.//tbody/tr')#获取tr标签
    data=[]
    for item in tr_l:#遍历tr标签
        list = []
        for td in item:#遍历td标签 获得内容
            if len(td.text) < 15:  # 排除广告td，广告td的长度较长，采用长度判断来排除
                list.append(td.text)
        if list:  # 排除空list
            list.append(str(year))#添加年份字段
            data.append(list)
    return data


#存储方式采用MySQL数据库；
def save_data_mysql(list):#创建数据库
    # 创建了数据库连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Musk', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 创建数据库
    sql = 'CREATE DATABASE IF NOT EXISTS countrys_cpi_rank CHARACTER SET utf8'
    # 创建数据库countrys_cpi_rank,并使用数据库countrys_cpi_rank
    cursor.execute(sql)
    cursor.execute('USE countrys_cpi_rank')

    sql = '''CREATE TABLE IF NOT EXISTS cpi_info(id int(10) PRIMARY KEY AUTO_INCREMENT,
    rank varchar(20) NOT NULL, country varchar(20) NOT NULL, region varchar(20) NOT NULL, cpi varchar(20) NOT NULL , years varchar(20) NOT NULL)'''
    cursor.execute(sql)  # 创建表
    sql = '''INSERT INTO cpi_info(rank, country, region, cpi, years) VALUES(%s, %s, %s, %s, %s)'''
    result = cursor.executemany(sql, list)  # 返回执行的条数
    print('存储条数为：', result)
    conn.commit()
    cursor.close()
    conn.close()

def get_data_from_mysql():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Cherry', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 创建数据库
    sql = 'CREATE DATABASE  IF NOT EXISTS countrys_cpi_rank CHARACTER SET utf8'
    # 创建数据库movie_info,并使用数据库movie_info
    cursor.execute(sql)
    cursor.execute('USE countrys_cpi_rank')
    cursor.execute('SELECT * FROM cpi_info')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

if __name__ == '__main__':
    try:
        # 循环获取1960~2021年62年数据， 并且存入数据库
        for year in range(1960,2022):
            list = get_list_data(year)
            # print(list)
            save_data_mysql(list)
        # 读取mysql数据
        get_data_from_mysql()
        # print(result)
    except Exception as e:
        print(e)
