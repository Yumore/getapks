import json

import panda as pd
import requests

# from bs4 import BeautifulSoup

url = "https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&serviceType=13&reqPageNum=1&uri=34789c86f4654624ba9e63cf1353c860&maxResults=25&locale=zh_CN"


def getUrlText(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

    '''
    爬取网页的通用代码框架
    '''
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # 如果status_code不等于200,就抛出异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


first_url_text = getUrlText(url)
first_data = json.loads(first_url_text)
first_levels = first_data['layoutData'][1]['dataList']

col_num = 0  # 用来记录存取数据的行数
result = pd.DataFrame(columns=['一级标签', '二级标签', '三级标签', 'app名称'])  # 用来存放结果

for i in range(len(first_levels)):
    first_level = first_levels[i]['name']  # 一级标签
    # 游戏单独处理
    if first_level == "游戏":
        second_detailId = first_levels[i]['detailId']

        second_url = r"https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri=" + second_detailId + "&maxResults=25&reqPageNum=1&locale=zh_CN"
        second_url_text = getUrlText(second_url)
        second_data = json.loads(second_url_text)
        second_levels = second_data['layoutData'][0]['dataList']

        for j in range(len(second_levels)):
            third_detailId = second_levels[j]['detailId']
            second_level = second_levels[j]['name']  # 二级标签

            third_url = r"https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri=" + third_detailId + "&maxResults=25&reqPageNum=1&locale=zh_CN"
            third_url_text = getUrlText(third_url)
            third_data = json.loads(third_url_text)
            third_levels = third_data['layoutData']

            for k in range(len(third_levels)):
                third_level = third_levels[k]['dataList'][0]['name']  # 三级标签

                four_detailId = third_levels[k]['dataList'][0]['detailId']
                four_url = r"https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&serviceType=13&uri=" + four_detailId + "&maxResults=25&reqPageNum=1&locale=zh_CN"

                four_url_text = getUrlText(four_url)
                four_data = json.loads(four_url_text)
                four_levels = four_data['layoutData'][0]['dataList']

                for h in range(len(four_levels)):
                    app_name = four_levels[h]['name']  # 对应的app

                    #                     print([first_level,second_level,third_level,app_name])
                    result = result.append(pd.DataFrame({'一级标签': [first_level], '二级标签': [second_level],
                                                         '三级标签': [third_level], 'app名称': [app_name]}))
                    col_num += 1
                    if col_num % 100 == 1:
                        print(col_num)
result.to_excel('result.xlsx', sheet_name='游戏', encoding='utf-8', index=False)
