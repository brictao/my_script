# from datetime import datetime
# print(datetime.now().strftime("%Y/%m/%d_%H:%M:%S"))

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import json

def fetch_user_data(username):
    url = f'https://countik.com/tiktok-analytics/user/{username}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    blocks = soup.find_all('div', class_='block')
    data = {}
    for block in blocks:
        key = block.find('h3').text.strip()
        value = block.find('p').text.strip()
        data[key] = value
    return data

usernames = [
    '@varvara6827', '@evelynlee754', '@naomi.harris70', '@harpergreen921', '@liamg337', 
    '@emilywilson_4', '@pujing66', '@alya.gavrilova', '@wangu176', '@ava_1833', 
    '@ava.williams911', '@everly746', '@sophiabrown927431', '@avawilliams183746', '@miajones495837', 
    '@emmasmith753619', '@helen87542', '@AbigailMoore728143', '@EmilyTaylor5629', '@juliette927461', 
    '@ellaharris375692', '@Jackie57321', '@ava969823', '@jessica568612', '@scarlett969424247', 
    '@ameliafaith_loved', '@lilychen0107', '@vickylee_heartfelt', '@mila_harper', '@nyla_last', 
    '@lilyannem1023', '@avaeparker', '@calmolivia0304', '@madisontay109', '@bellaroseinbloom', 
    '@IsabellaGAnderson', '@camilla2168', '@lilyking864215', '@celeste128143', '@janet_harris', 
    '@taylor_wilson27', '@faye_wz8qn', '@lily_everly', '@layla_parker27'
]

all_users_data = {}

for username in usernames:
    user_data = fetch_user_data(username)
    # 为每个用户添加当前时间戳
    user_data['update_time'] = datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
    all_users_data[username] = user_data

# 打印 JSON 格式的数据以供检查
print(json.dumps(all_users_data, indent=4))

# 使用当前时间戳来命名文件，确保文件名唯一
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'tiktok_user_data_{current_time}.csv'

# 添加 'update_time' 到列头列表
headers = ['Username'] + list(all_users_data[next(iter(all_users_data))].keys())

# 打开一个CSV文件以写入数据
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for username, stats in all_users_data.items():
        row = {'Username': username}
        row.update(stats)
        writer.writerow(row)
