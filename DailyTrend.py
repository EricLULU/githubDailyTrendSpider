import datetime
import pymysql
import requests
from bs4 import BeautifulSoup
import emoji
import re

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def replaces(str):
    return str.replace('\n', '').replace('\r', '').replace(' ', '')

def get_html(url):
    try:
        r = requests.get(url, verify=False)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print('requests error:{}\t{}'.format(str(e), str(datetime.datetime.now())))


def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    li_list = soup.find_all('li', {'class': 'col-12 d-block width-full py-4 border-bottom'})
    for i in range(len(li_list)):
        title = li_list[i].find('a').text
        url = 'https://github.com' + li_list[i].find('a')['href']
        developer = title.split('/')[0].strip()
        project_name = title.split('/')[1].strip()
        try:
            description = li_list[i].find('p', {'class': 'col-9 d-inline-block text-gray m-0 pr-4'}).text.strip()
        except:
            description = '无'
        try:
            language = li_list[i].find('span', {'itemprop': 'programmingLanguage'}).text.strip()
        except:
            language = '无'
        total_star = li_list[i].find('a', {'class': 'muted-link d-inline-block mr-3'}).text.strip().replace(',', '')
        try:
            today_star = li_list[i].find('span', {'class': 'd-inline-block float-sm-right'}).text.strip().split(' ')[0].replace(',', '')
        except:
            today_star = 0

        data = {'ranking': i + 1, 'author': developer, 'project_name': project_name, 'url': url,
                'description': description, 'language': language, 'total_star': total_star, 'today_star': today_star}
        yield data

def getRepo(since=None, lang=None):
    url = 'https://github.com/trending'
    url_prefix = 'https://github.com'
    if not lang is None:
        url = url + '/' + lang
    if not since is None:
        url = url + '?since=' + since
    response = requests.get(url, verify=False).text
    soup = BeautifulSoup(response, 'html.parser')
    articles = soup.find_all('article', {'class': 'Box-row'})
    trendings = []
    i = 0
    for article in articles:
        dic = {}
        dic['ranking'] = i = i + 1;
        repo = article.find('h2', {'class': 'lh-condensed'})
        if not repo is None:
            repo_a = repo.a
            if not repo_a is None:
                repo_text = replaces(repo_a.get('href'))
                dic['repo'] = repo_text
        dic['url'] = url_prefix + repo_text
        description = article.find('p', {'class': 'col-9'})
        if not description is None:
            dic['description'] = re.sub(':\S+?:', ' ', emoji.demojize(description.text.strip()))
            print("description %s", re.sub(':\S+?:', ' ', emoji.demojize(description.text.strip())))
        else:
            dic['description'] = ""

        lang = article.find('span', {'itemprop': 'programmingLanguage'})
        if not lang is None:
            dic['lang'] = lang.text.strip()
        else:
            dic['lang'] = ""

        # lang_color = article.find('span', {'class': 'repo-language-color'})
        # if not lang_color is None:
        #     dic['lang_color'] = lang_color.attrs['style'][-6:]

        fork_starts = article.find_all('a', {'class': 'Link Link--muted d-inline-block mr-3'})
        if not fork_starts is None:
            dic['stars'] = fork_starts[0].text.strip()
            dic['forks'] = fork_starts[1].text.strip()
        else:
            dic['stars'] = "0"
            dic['forks'] = "0"

        added_stars = article.find('span', {'class': 'float-sm-right'})
        if not added_stars is None:
            dic['added_stars'] = added_stars.text.strip()

        # bs_avatars = article.find_all('img', {'class': 'avatar'})
        # avatars = []
        # for bs_avatar in bs_avatars:
        #     avatar = bs_avatar.attrs['src']
        #     avatars.append(avatar)
        #
        # dic['avatars'] = avatars
        trendings.append(dic)
    return trendings

def db_connect():
    try:
        db = pymysql.connect(host='localhost', port=3306, user='数据库用户名', password='数据库密码', database='gitTrend_db',
                             charset='utf8')
        return db
    except Exception as e:
        print('db connect fail,e:{}\t{}'.format(str(e), str(datetime.datetime.now())))
        return None


def db_close(db):
    db.close()


def save_to_db(data):
    try:
        with db.cursor() as cursor:
            sql = 'insert into github_trending_day(ranking,repo,url,description,lang,stars,forks,added_stars, time)' \
                  'values(%s,%s,%s,%s,%s,%s,%s,%s, now())'
            cursor.execute(sql, (data['ranking'], data['repo'],  data['url'],   data['description'],
                                 data['lang'],    data['stars'], data['forks'], data['added_stars']))
            db.commit()
            print('insert to db success\t', str(datetime.datetime.now()))
    except Exception as e:
        print('insert to db fail,e:{}\t{}'.format(str(e), str(datetime.datetime.now())))

if __name__ == '__main__':
    db = db_connect()

    for data in getRepo():
        if db:
            save_to_db(data)
    db_close(db)
