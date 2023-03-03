# import data request module
import requests
import parsel
import csv
import time

f = open('豆瓣Top250.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
        '标题',
        '导演',
        '主演',
        '上映年份',
        '国家',
        '类型',
        '简介',
        '评分',
        '评论人数',
])
csv_writer.writeheader()

num = 1

for page in range(0, 250, 25):
    print(f'正在爬取第{num}页')
    num += 1
    time.sleep(1)

    url = f'https://movie.douban.com/top250?start={page}&filter='

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)

    selector = parsel.Selector(response.text)

    lis = selector.css('.grid_view li')

    for li in lis:
        title = li.css('.info .hd span.title:nth-child(1)::text').get()
        movie_info_list = li.css('.bd p:nth-child(1)::text').getall()
        cast = movie_info_list[0].strip().split('\xa0\xa0\xa0')
        if len(cast) > 1:
            director = cast[0].replace('导演: ', '')
            actor = cast[1].replace('主演: ', '').replace('/...', '')
        else:
            director = cast[0].replace('导演: ', '')
            actor = 'None'
        movie_info = movie_info_list[1].strip().split('\xa0/\xa0')
        movie_country = movie_info[0]
        movie_year = movie_info[1]
        movie_type = movie_info[2]
        movie_sum = li.css('.inq::text').get()
        movie_ranking = li.css('.rating_num::text').get()
        comment_number = li.css('.star span:nth-child(4)::text').get().replace('人评价', '')

        dit = {
            '标题': title,
            '导演': director,
            '主演': actor,
            '上映年份': movie_year,
            '国家': movie_country,
            '类型': movie_type,
            '简介': movie_sum,
            '评分': movie_ranking,
            '评论人数': comment_number
        }
        csv_writer.writerow(dit)
        print(title, director, actor, movie_country, movie_year, movie_type, movie_sum, movie_ranking, comment_number, sep='|')
