import translators as ts
import pandas as pd
import final1
import json
def translator(a):
    a = ts.baidu(a)
    print(a)
    return  a
def save_json(json):
    with open('cpi.json','w')as f:
        f.write(json)
        print('success')
def merge_data():
    d_json = []
    data = final1.get_data_from_mysql()
    for i in data:
        d_dict = {}
        d_list = list(i)
        # print(d_list)
        d_dict['country'] = d_list[2]
        d_dict[d_list[5]] = d_list[4]
        # d_dict[d_list[5]] = d_list[4].replace('%','')
        d_json.append(d_dict)
    return json.dumps(d_json)

def data2json():
    data = pd.read_json(merge_data())
    data = data.groupby('country').sum()
    print(data)
    a = data.to_dict('index')
    # print(a)
    save_json(json.dumps(a))
if __name__ == '__main__':
    try:
        #获取数据库数据并处理保存json
        data2json()
        #翻译数据库国家名 并保存。生成map要用到
        # with open('cpi_original.json', 'r')as f:
        #     b =f.read()
        # json_str = json.loads(b)
        # d={}
        # for key in json_str:
        #     print(key)
        #     print(json_str[key])
        #     d[translator(key)]=json_str[key]
        # save_json(json.dumps(d))
    except Exception as e:
        print(e)