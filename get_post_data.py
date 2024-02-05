import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime

def fetch_user_data(username):
    url = f'https://countik.com/tiktok-analytics/user/{username}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    analytics_section = soup.find('section', class_='analytics')
    container = analytics_section.find('div', class_='container') if analytics_section else None
    recent_posts = container.find('div', class_='recent-posts') if container else None
    items = recent_posts.find_all('div', class_='item') if recent_posts else []

    extracted_items = []
    for item in items:
        post_img = item.find('div', class_='post-img').find('img') if item.find('div', class_='post-img') else None
        image_src = post_img['src'] if post_img and post_img.has_attr('src') else 'No image'
        image_alt = post_img['alt'] if post_img and post_img.has_attr('alt') else 'No alt text'
        data_points = {}
        for data_point in item.select('.post-data .data'):
            title = data_point.find('p', class_='title').text.strip() if data_point.find('p', class_='title') else 'No title'
            value = data_point.find('p', class_='value').text.strip() if data_point.find('p', class_='value') else 'No value'
            data_points[title] = value
        engagement_rate = item.find('div', class_='eng').text.strip() if item.find('div', class_='eng') else 'No engagement rate'
        create_time = item.find('div', class_='create-time').get_text(strip=True) if item.find('div', class_='create-time') else 'No create time'

        extracted_items.append({
            'image_src': image_src,
            'image_alt': image_alt,
            'data': data_points,
            'engagement_rate': engagement_rate,
            'create_time': create_time
        })
    
    return extracted_items

# 替换为实际用户名
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
    all_users_data[username] = user_data

# 现在开始将数据写入CSV文件
# 使用当前时间戳来命名文件
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'tiktok_post_data_{current_time}.csv'

# 定义CSV文件的列标题
headers = ['username', 'image_src', 'image_alt', 'Views', 'Likes', 'Comments', 'Shares', 'Hashtags', 'Mentions', 'engagement_rate', 'create_time', 'update_time']

# 打开一个CSV文件以写入数据
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    for username, posts in all_users_data.items():
        for post in posts:
            row_data = {
                'username': username,
                'image_src': post.get('image_src', ''),
                'image_alt': post.get('image_alt', ''),
                'Views': post['data'].get('Views', ''),
                'Likes': post['data'].get('Likes', ''),
                'Comments': post['data'].get('Comments', ''),
                'Shares': post['data'].get('Shares', ''),
                'Hashtags': post['data'].get('Hashtags', ''),
                'Mentions': post['data'].get('Mentions', ''),
                'engagement_rate': post.get('engagement_rate', ''),
                'create_time': post.get('create_time', ''),
                'update_time': datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
            }
            writer.writerow(row_data)
