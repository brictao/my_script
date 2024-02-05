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
    '@XXXXX', '@XXXXX'
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
