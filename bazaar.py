import re
from urllib import request

import data_utils


class bazaar:
    def __init__(self):
        self.base_url = "https://bazaar.abuse.ch/browse/"

    def get_url(self):
        response = request.urlopen(self.base_url)
        html = response.read()
        html = html.decode('utf-8')
        self.parse_html(html)

    def parse_html(self, html):
        print(html)
        tables = re.findall(r"<table.*?>.*?</table>", html, re.M | re.S)
        for table in tables:
            # print(table)
            # 匹配<th></th>之间的内容
            # 因为<tr>标签大多数不是在同一行，所以要加 re.S和re.M多行匹配
            theads = re.findall(r"<thead>(.*?)</thead>", table, re.S | re.M)
            for thead in theads:
                # print(thead)
                ths = re.findall(r"<th>(.*?)</th>", thead, re.S | re.M)
                th_list = []
                for index, th in enumerate(ths, start=0):
                    if index == 2:
                        temp = th.split('<th>')
                        for tmp in temp:
                            th_list.append(tmp)
                    else:
                        th_list.append(th)
                print("ths: %s" % th_list)
            tbodies = re.findall(r"<tbody>(.*?)</tbody>", table, re.S | re.M)
            for tbody in tbodies:
                trs = re.findall(r"<tr>(.*?)</tr>", tbody, re.S | re.M)
                for tr in trs:
                    # tr = tr.replace('&nbsp;', '').replace('/> ', '/>').replace('> <', '><')
                    # 匹配<td></td>之间的内容
                    # tds = re.findall(r"<td>(.*?)</td>", tr, re.S | re.M)
                    tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S | re.M)
                    # print(tds, len(tds))
                    sql_data = []
                    for index, td in enumerate(tds, start=0):
                        # print("index => td : %d => %s" % (index, td))
                        if index == 1:
                            href_list = []
                            values = re.findall(r'<a .*?>(.*?)</a>', td, re.S | re.M)
                            hrefs = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", td, re.I | re.S | re.M)
                            for href in hrefs:
                                href = 'https://bazaar.abuse.ch' + href
                                href_list.append(href)
                            print("values: %s --- hrefs: %s" % (values, href_list))
                            sql_data.extend(values)
                            sql_data.extend(href_list)
                            # https://bazaar.abuse.ch/sample/3b4ca27d15682368c2009bab10f874a48a16b69f5d1bc611c48877373244f9c8/
                        elif index == 4:
                            values = re.findall(r'<a .*?>(.*?)</a>', td, re.S | re.M)
                            sql_data.append(','.join(values))
                            print("values: %s, tags: %s" % (values, ','.join(values)))
                        elif index == (len(tds) - 1):
                            href_list = []
                            hrefs = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", td, re.I | re.S | re.M)
                            for href in hrefs:
                                href = 'https://bazaar.abuse.ch' + href
                                href_list.append(href)
                            print("download hrefs: %s" % href_list)
                            sql_data.extend(href_list)
                        # else:
                        # print("-" * 5 + ">", td)
                    print("sql_data: %s" % sql_data)
                    data_utils.update_bazaar(sql_data)

    def start(self):
        # data_utils.csv_mysql("./full-back.csv")
        self.get_url()
