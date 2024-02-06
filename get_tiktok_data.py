import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_tiktok_analytics_result(username):
    """
    通过请求特定链接获取网页中的TikTok分析部分内容。
    """
    url = f'https://countik.com/tiktok-analytics/user/{username}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    analytics_sections = soup.find_all('section', class_='analytics')
    return analytics_sections

def get_tiktok_user_data(analytics_sections):
    """
    从分析结果中提取用户数据。
    """
    user_data = {}
    for section in analytics_sections:
        stats_blocks = section.find_all('div', class_='block')
        for block in stats_blocks:
            title = block.find('h3').text.strip()
            value = block.find('p').text.strip().split('\n')[0]
            user_data[title] = value
    return user_data

from datetime import datetime

def get_tiktok_post_data(analytics_sections):
    """
    从分析结果中提取关于最近帖子的数据。
    """
    posts_data = []
    for section in analytics_sections:
        recent_posts_section = section.find('div', class_='recent-posts')
        if recent_posts_section:
            posts = recent_posts_section.find_all('div', class_='item')
            for post in posts:
                post_data = {}
                
                # 提取创建时间，并转换格式
                create_time_div = post.find('div', class_='extra-data').find('p')
                create_time = create_time_div.text.strip() if create_time_div else "N/A"
                try:
                    # 尝试按照给定格式解析时间字符串
                    create_time_parsed = datetime.strptime(create_time, '%m/%d/%Y, %I:%M %p')
                    create_time = create_time_parsed.strftime('%Y/%m/%d %H:%M:%S')
                except ValueError:
                    # 如果解析失败，保留原始字符串
                    print(f"Time data '{create_time}' does not match format '%m/%d/%Y, %I:%M %p'")
                
                post_data['Create Time'] = create_time

                # 提取图片src和alt
                image = post.find('div', class_='post-img').find('img')
                post_data['Image Src'] = image['src'] if image else 'N/A'
                post_data['Image Alt'] = image['alt'] if image else 'N/A'

                # 提取其他数据
                data_blocks = post.find_all('div', class_='data')
                for block in data_blocks:
                    title = block.find('p', class_='title').text.strip()
                    value = block.find('p', class_='value').text.strip()
                    post_data[title] = value
                
                engagement_div = post.find('div', class_='eng')
                engagement_rate = engagement_div.text.strip().split(' ')[0] if engagement_div else "N/A"
                post_data['Engagement Rate'] = engagement_rate

                posts_data.append(post_data)
    return posts_data


def write_data_to_csv(filenames, headers, data):
    for filename, header, data_list in zip(filenames, headers, data):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            for data_row in data_list:
                writer.writerow(data_row)

# 用户名列表
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

user_data_list = []
post_data_list = []

# 遍历用户名列表，收集数据
for username in usernames:
    analytics_sections = get_tiktok_analytics_result(username.strip('@'))
    user_data = get_tiktok_user_data(analytics_sections)
    post_data = get_tiktok_post_data(analytics_sections)
    
    # 添加用户名和更新时间
    for post in post_data:
        post['Username'] = username
        post['Update Time'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    post_data_list.extend(post_data)

    user_data['Username'] = username
    user_data['Update Time'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    user_data_list.append(user_data)

# 定义CSV文件名和列头
current_time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
user_filename = f'tiktok_user_data_{current_time_str}.csv'
post_filename = f'tiktok_post_data_{current_time_str}.csv'

user_headers = ['Username', 'Total Followers', 'Total Likes', 'Total Videos', 'Following', 'Overall Engagement', 'Likes Rate', 'Comments Rate', 'Shares Rate', 'Avg. Views', 'Avg. Likes', 'Avg. Comments', 'Avg. Shares', 'Update Time']
post_headers = ['Username', 'Image Src', 'Image Alt', 'Views', 'Likes', 'Comments', 'Shares', 'Engagement Rate', 'Hashtags', 'Mentions', 'Create Time', 'Update Time']

# # 写入CSV
# write_data_to_csv([user_filename, post_filename], [user_headers, post_headers], [user_data_list, post_data_list])

# 决定是否写入用户数据或帖子数据
write_user_data = False
write_post_data = True

if write_user_data:
    # 写入用户数据到CSV
    write_data_to_csv([user_filename], [user_headers], [user_data_list])

if write_post_data:
    # 写入帖子数据到CSV
    write_data_to_csv([post_filename], [post_headers], [post_data_list])
