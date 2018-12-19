import os
import re
import gevent
import urllib.request
from gevent import monkey
from bs4 import BeautifulSoup
monkey.patch_all()


class Server(object):
    def __init__(self,url):
        self.img_dict = {}
        self.url = url

    def request_content(self):
        content = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(content, 'lxml').prettify()
        return soup

    def request_dict(self):
        content = self.request_content()
        imgs = re.findall(r'(assets.*?\.\w+g)', content)
        for i in imgs:
            spl = i.split('/')
            title = spl[-1]
            self.img_dict[title] = i


    def download(self):
        gev_list = []
        for i in self.img_dict.keys():
            s = gevent.spawn(self.request_img, i, self.img_dict[i])
            gevent.sleep(0.05)
            gev_list.append(s)
        gevent.joinall(gev_list)


    def request_img(self,title, img):
        img_data = urllib.request.urlopen(self.url+ img).read()
        print('正在下载%s' % title)
        with open('./img/%s' % title, 'wb') as f:
            f.write(img_data)


def main():
    os.mkdir('img')
    server = Server('http://jx3.xoyo.com/zt/2018/06/13/topic/')
    server.request_dict()
    server.download()


if __name__ == '__main__':
    main()
