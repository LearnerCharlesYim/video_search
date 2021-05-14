import requests
import time
import re
from lxml import etree
import os
DOMAIN = 'https://www.tukuppt.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Cookie': 'personasKey=a%3A2%3A%7Bs%3A12%3A%22isworkdesign%22%3Bi%3A1%3Bs%3A6%3A%22device%22%3Bi%3A0%3B%7D; hostfrom=www.tukuppt.com; Hm_lvt_a620c01aafc084582f0ec24d96b73ad8=1620990118; Hm_lpvt_a620c01aafc084582f0ec24d96b73ad8=1620992309'
}

def get_urls():
    '''
    获取视频所有urls
    :return:
    '''
    for i in range(1,51):
        url = f'https://www.tukuppt.com/video/zonghe_0_0_0_0_0_0_{i}.html'
        resp = requests.get(url=url,headers=headers)
        html = resp.text
        obj = re.compile(r'<dd>.*?<a href="(?P<url>.*?)" target="_blank">', re.S)  # re.S: 让.能匹配换行符
        result = obj.finditer(html)
        for index,it in enumerate(result):
            with open('url.txt','a',encoding='utf-8') as fp:
                url = DOMAIN + it.group("url")
                fp.write(url + '\n')
                print(f'完成{index+1}次')
        print('='*50)
        print(f'第{i}页完成')
        print('=' * 50)
    time.sleep(1)
    print('获取urls完毕- ^ -')


def get_details():
    from xiechengwang.settings import BASE_DIR
    path = os.path.join(os.path.join(BASE_DIR,'xiechengapp'),'url.txt')

    with open(path,'r',encoding='utf-8') as fp:
        for index,url in enumerate(fp):
            resp = requests.get(url=url.strip(),headers=headers)
            text = resp.text
            html = etree.HTML(text)
            name = html.xpath('/html/body/div[6]/div[1]/div[1]/h1/text()')[0]
            url = 'https:' + html.xpath('//video[@id="videoe"]/@src')[0]
            heat = html.xpath('//div[@class="d-msg "]/span[2]/text()')[0]
            format = html.xpath('//div[@class="work-info"]/ul/li[3]/span[2]/text()')[0]
            size = html.xpath('//div[@class="work-info"]/ul/li[4]/span[2]/text()')[0].strip('MB').strip()
            try:
                author = html.xpath('//div[@class="work-info"]/ul/li[5]/span[2]/text()')[0].strip()
            except Exception:
                from .models import Video
                video = Video(name=name, url=url, heat=heat, format=format, size=size, author='空缺')
                video.save()
                print(f'{index + 1}条数据已插入')
                time.sleep(1)
                continue
            from .models import Video
            video = Video(name=name,url=url,heat=heat,format=format,size=size,author=author)
            video.save()
            print(f'{index+1}条数据已插入')
            time.sleep(1)


if __name__ == '__main__':
    pass