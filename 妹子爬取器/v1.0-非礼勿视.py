import re
import os
import gevent
from urllib import request
import time
from gevent import monkey

monkey.patch_all()


class Download(object):
    def __init__(self, load_list):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'http://www.mm131.com/qipao/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36',
        }
        self.load_list = load_list

    def jpg_addr(self, url):
        """获取一个套图内每张图片的html并匹配jpg地址"""
        # first_jpg = re.findall(r'" src="(.*?jpg)" /',self.request_code(url+'.html').decode('gbk'))[0]
        file_name = re.findall(r'alt="(.*)\(图', self.request_code(url + '.html').decode('gbk'))[0]
        print('正在下载', file_name)
        save_name = re.findall(r'com/(.*)/', url)[0]
        os.mkdir('./' + save_name + '/' + file_name)
        # with open('./' + save_name + '/' + file_name + '/' + '1.jpg', 'ab') as f:
        #     data = self.request_code(first_jpg)
        #     f.write(data)

        num = 2
        while True:
            image_html_url = url + ('_%s.html' % num)
            content = self.request_code(image_html_url)
            if content:
                with open('./' + save_name + '/' + file_name + '/' + repr(num) + '.jpg', 'ab') as f:
                    jpg_add = re.findall('" src="(.*?jpg)" /', content.decode('gbk'))[0]
                    data = self.request_code(jpg_add)
                    f.write(data)
                num += 1
                gevent.sleep(1)  # 0.05
                continue
            break

    def download_begin(self):
        gev_list = []
        for i in self.load_list:
            s = gevent.spawn(self.jpg_addr, i)
            gev_list.append(s)
            time.sleep(1)  # 0.1
        gevent.joinall(gev_list)

    def request_code(self, url):
        req = request.Request(url=url, headers=self.headers, method="GET")
        try:
            response = request.urlopen(req)
        except Exception:
            return ''
        content = response.read()
        return content


class GetHtml(object):
    def __init__(self):
        self.headers = {
            'Referer': 'www.mm131.com/xinggan',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36',
        }
        self.load_list = []

    def request_sound_code(self, url):
        req = request.Request(url=url, headers=self.headers, method="GET")
        try:
            response = request.urlopen(req)
        except Exception:
            return ''
        content = response.read().decode("gbk")
        return content

    def analyze(self, content):
        pics_list = re.findall('href="(.*?).html"><img', content)
        for i in pics_list:
            self.load_list.append(i)
            time.sleep(0.001)

    def get_html(self, list_url):
        gev_list = []
        num = 2
        while True:
            url = list_url + ('%d.html' % num)
            content = self.request_sound_code(url)
            if content:
                print(url, '开始爬取')
                s = gevent.spawn(self.analyze, content)
                gev_list.append(s)
                time.sleep(0.05)
                num += 1
                continue
            break
        gevent.joinall(gev_list)


def main():
    os.mkdir('131套图')
    os.chdir('./131套图')
    os.mkdir('mingxing')
    os.mkdir('qingchun')
    os.mkdir('xinggan')
    os.mkdir('xiaohua')
    os.mkdir('chemo')
    os.mkdir('qipao')
    gev_list = []
    resource = ['http://www.mm131.com/xinggan/list_6_',
                'http://www.mm131.com/qingchun/list_1_',
                'http://www.mm131.com/xiaohua/list_2_',
                'http://www.mm131.com/chemo/list_3_',
                'http://www.mm131.com/qipao/list_4_',
                'http://www.mm131.com/mingxing/list_5_'
                ]
    server = GetHtml()
    star_time = time.time()
    for i in resource:
        s = gevent.spawn(server.get_html, i)
        gevent.sleep(1)  # 0.1
        gev_list.append(s)
    gevent.joinall(gev_list)
    end_time = time.time() - star_time
    print('套图地址爬取完毕,耗时:%ds' % int(end_time))
    print(server.load_list)
    down_time = time.time()
    down = Download(server.load_list)
    down.download_begin()
    down_endtime = time.time() - down_time
    print('套图下载完毕,耗时:%ds' % int(down_endtime))


if __name__ == '__main__':
    main()
