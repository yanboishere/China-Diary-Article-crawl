import os
import re
import time
import requests
import datetime

from bs4 import BeautifulSoup

"""
--------------------------------------------------------------本程序说明--------------------------------------------------------------------------
程序功能：运行程序输入关键词后自动执行文章爬取，
以文章名为文件名保存成TXT文件.
关键参数：
        爬取网址：http://newssearch.chinadaily.com.cn
        max_pag = 10        # 默认爬取前10页，觉得数据少可以适当加大
        path = './china/'+name+'/'    # 文件存储路径为当前路径下的china文件夹内以搜索关键词为文件夹名，可以随便修改文件存储路径，路径不存在时程序会自动创建路径
        本程序只用做查找英语文章，进行英语学习之用.
--------------------------------------------------------------------------------------------------------------------------------------------        
"""


def get_url(dancis, max_pag):
    # 第一部分，获取文章网址
    name = dancis[0]
    first_url = []
    now_time = datetime.datetime.now().strftime('%Y%m/%d')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 QIHU 360SE/12.2.1696.0',
        'Referer': 'http://newssearch.chinadaily.com.cn/en/search?query=' + name,
        'Cookie': '__asc=f7f831bd178ac77079926e25e71;__auc=f7f831bd178ac77079926e25e71;__guid=155592356'
                  '.2229240286471539700.1617801213044.6062;monitor_count=1;UM_distinctid=178ac76ff804e-0a376cda6169f7'
                  '-45410429-1fa400-178ac76ff81357;wdcid=32971507909df1ef;',
    }
    page = 0
    url = 'http://newssearch.chinadaily.com.cn//rest/en/search?keywords={}&sort=dp&page={}&curType=story&type=&channel=&source= HTTP/1.1'.format(
        name, page)
    req = requests.get(url, headers=headers).json()
    long = req['totalPages']  # 获取总页数
    if max_pag > long:
        max_pag = long
    for page in range(max_pag):
        url = 'http://newssearch.chinadaily.com.cn//rest/en/search?keywords={}&sort=dp&page={}&curType=story&type=&channel=&source= HTTP/1.1'.format(
            name, page)
        req = requests.get(url, headers=headers).json()
        data = req['content']
        for i in data:
            first_url.append('https://www.chinadaily.com.cn/a/' + now_time + '/' + i['id'] + '.html')
        print("第%s页URL获取成功" % page)
        time.sleep(0.5)
    # print(first_url)
    return first_url


def get_content(name, url):
    # 第二部分，保存文章
    pre = [0 for i in range(len(name))]
    global num, sum
    try:
        page = requests.get(url)
        html = BeautifulSoup(page.text, 'html.parser')
        tittle = html.find('h1').text
        contents = html.find('div', id='Content').find_all('p')
        print(num, tittle)

        try:
            for content in contents:
                for k in range(len(name)):
                    matchObj = re.search(name[k], str(content), re.M | re.I)
                    if matchObj:
                        pre[k] = 1
            # print(pre)
            sum_pre = 0
            for tem1 in pre:
                sum_pre = sum_pre + tem1
            end_pre = sum_pre / len(name)
            # print(end_pre)
            # 写入文件
            flag = 0
            if end_pre >= 0.35:
                txt_path = './china/35%/'  # 文件存储路径为当前路径下的china文件夹
                flag = 1
            elif end_pre >= 0.3:
                txt_path = './china/30%/'
                flag = 1
            elif end_pre >= 0.25:
                txt_path = './china/25%/'
                flag = 1
            elif end_pre >= 0.2:
                txt_path = './china/20%/'
                flag = 1
            else:
                pass
            if flag:
                if not os.path.exists(txt_path):
                    os.makedirs(txt_path)
                txt_content = open(txt_path + tittle.replace(': ', '-') + '.txt', 'w', encoding="utf-8")
                txt_content.write(str(url) + '\n')
                txt_content.write(str(tittle) + '\n')
                for content in contents:
                    txt_content.write(
                        str(content).replace('</p>', '\n').replace('<p>', '  ').replace('<br/><br/>', '\n  '))
                txt_content.close()
                print("写入%s" % str(tittle))
                img = html.find('div', id='Content').find('img')
                img_url = img.get('src')  #
                #print(img_url)
                pic = requests.get('http:'+img_url).content
                with open(txt_path + tittle.replace(': ', '-') + '.jpeg', 'wb') as f:
                    f.write(pic)
            num += 1
        except:
            os.remove(txt_path + tittle.replace(': ', '-') + '.txt')
    except:
        pass


if __name__ == '__main__':
    max_pag = int(input("请输入爬取页面长度："))  # 10  # 爬取1-10页文章
    num = 1  # 计数器
    key = input("请输入关键词(多个词中间用英文逗号分隔)：")
    danci = key.split(',')
    url = get_url(danci, max_pag)  # help为关键词，可以任意修改
    for content_url in url:
        get_content(danci, content_url)
