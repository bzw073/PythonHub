import requests
from lxml import etree
import json
import openpyxl

'''
获取新冠肺炎的实时数据
'''
url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
response = requests.get(url)
# print(response.text)
# 生成HTML对象
html = etree.HTML(response.text)
result = html.xpath('//script[@type="application/json"]/text()')
result = result[0]
# json.load()方法可以将字符串转化为python数据类型
result = json.loads(result)
# 创建工作簿
wb = openpyxl.Workbook()
# 创建工作表
ws = wb.active
ws.title = "国内疫情"
ws.append(['省份', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量'])
result_in = result['component'][0]['caseList']
data_out = result['component'][0]['globalList']
'''
area --> 大多为省份
city --> 城市
confirmed --> 累计
crued --> 值域
relativeTime -->
confirmedRelative --> 累计的增量
curedRelative --> 值域的增量
curConfirm --> 现有确镇
curConfirmRelative --> 现有确镇的增量
'''
for each in result_in:
    temp_list = [each['area'], each['confirmed'], each['died'], each['crued'], each['curConfirm'],
                 each['confirmedRelative'], each['diedRelative'], each['curedRelative'],
                 each['curConfirmRelative']]
    for i in range(len(temp_list)):
        if temp_list[i] == '':
            temp_list[i] = '0'
    ws.append(temp_list)
# 获取国外疫情数据
for each in data_out:
    sheet_title = each['area']
    # 创建一个新的工作表
    ws_out = wb.create_sheet(sheet_title)
    ws_out.append(['国家', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量'])
    for country in each['subList']:
        list_temp = [country['country'], country['confirmed'], country['died'], country['crued'],
                     country['curConfirm'], country['confirmedRelative']]
        for i in range(len(list_temp)):
            if list_temp[i] == '':
                list_temp[i] = '0'
        ws_out.append(list_temp)
wb.save('./data.xlsx')
