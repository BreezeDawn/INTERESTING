import os
import re
import gevent
import urllib.request
from gevent import monkey
from bs4 import BeautifulSoup

monkey.patch_all()


class Server(object):
    def __init__(self, url):
        self.videos_dict = {}
        self.url = url

    def request_content(self):
        content = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(content, 'lxml').prettify()
        return soup

    def request_dict(self):
        content = self.request_content()
        videos = re.findall(r'(static.*?mp4)"', content)
        for i in videos:
            title = i.split('/')[-1]
            self.videos_dict[title] = i

    def download(self):
        for i in self.videos_dict.keys():
            self.request_video(i, self.videos_dict[i])

    @staticmethod
    def request_video(title, video):
        print('正在下载%s' % title)
        video_data = urllib.request.urlopen('http://' + video).read()
        with open('./video/%s' % title, 'wb') as f:
            f.write(video_data)


def main():
    os.mkdir('video')
    server = Server('http://jx3.xoyo.com/zt/2018/06/13/topic/')
    server.request_dict()
    server.download()


if __name__ == '__main__':
    main()
