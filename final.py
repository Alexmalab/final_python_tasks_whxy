import pymysql
import requests
from lxml import etree

#具体字段包括年份、排名、国家/地区、所在洲、通胀率；
def get_list_data(year): #返回某年数据
    base_url= 'https://www.kylc.com/stats/global/yearly/g_inflation_consumer_prices'
    url = base_url+'/'+str(year)+'.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'}
    r = requests.get(url=url,headers=headers)
    return r
def parse_data():
    data = []
    for year in range(2017,2022):
        r = get_list_data(year)
        html = etree.HTML(r.text)
        tr_l = html.xpath('.//tbody/tr')
        for item in tr_l:
            list =[]
            for td in item:
                if len(td.text)<15: #排除广告td
                    list.append(td.text)
            if list:  #排除空list
                data.append(list)
                # print(list)
    return data
def merge_data(list,year):
    print()

#存储方式采用MySQL数据库；
def save_data_mysql(list,year):#创建5个表分别用于存储5年的数据
    year=str(year)
    # 创建了数据库连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Cherry', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 创建数据库
    sql = 'CREATE DATABASE IF NOT EXISTS countrys_cpi_rank CHARACTER SET utf8'
    # 创建数据库movie_info,并使用数据库movie_info
    cursor.execute(sql)
    cursor.execute('USE countrys_cpi_rank')

    sql = '''CREATE TABLE IF NOT EXISTS cpi_info_'''+year+'''(id int(10) PRIMARY KEY AUTO_INCREMENT,
    rank varchar(20) NOT NULL, country varchar(20) NOT NULL, region varchar(20) NOT NULL, cpi varchar(20) NOT NULL)'''
    cursor.execute(sql)  # 创建表
    sql = '''INSERT INTO cpi_info_'''+year+'''(rank, country, region, cpi) VALUES(%s, %s, %s, %s)'''
    result = cursor.executemany(sql, list)  # 返回执行的条数
    print('存储条数为：', result)
    conn.commit()

    cursor.close()
    conn.close()
#可视化处理
def get_data_from_mysql(year):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Cherry', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    # 创建数据库
    sql = 'CREATE DATABASE  IF NOT EXISTS countrys_cpi_rank CHARACTER SET utf8'
    # 创建数据库movie_info,并使用数据库movie_info
    cursor.execute(sql)
    cursor.execute('USE countrys_cpi_rank')
    cursor.execute('SELECT * FROM cpi_info_'+str(year))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

if __name__ == '__main__':
    try:
        data = parse_data()
        print(data)
        # 循环获取2017~2021年 5年数据， 并且存入数据库
        # for year in range(2017,2022):
        #     list = get_list_data(year)
        #     print(list)
        #     merge_data(list,year)
            # save_data_mysql(list,year)
        # 读取mysql数据
        # for year in range(1960,2022):
        #     result = get_data_from_mysql(year)
        #     print(result)
    except Exception as e:
        print(e)
