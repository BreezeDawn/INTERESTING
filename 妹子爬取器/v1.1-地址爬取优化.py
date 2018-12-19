import re
import os
import gevent
import http
import time
from gevent import pool
from gevent import monkey
from urllib import request

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

    def download_begin(self, gpool):
        """为每个相册集开协程,协程数控制在50以内"""
        gev_list = []
        for i in self.load_list:
            s = gpool.spawn(self.jpg_addr, i)
            gev_list.append(s)
            time.sleep(1)  # 0.1
        gevent.joinall(gev_list)

    def jpg_addr(self, url):
        """获取一个套图内每张图片的html并匹配jpg地址"""
        # 首先获取相册主题名
        try:
            file_name = re.findall(r'alt="(.*)\(图', self.request_code(url + '.html').decode('gbk'))[0]
        except AttributeError:
            return
        save_name = re.findall(r'com/(.*)/', url)[0]
        # 创建该相册主题文件夹
        try:
            os.mkdir('./' + save_name + '/' + file_name)
        except FileExistsError:
            return
        # 模拟翻页并下载数据到对应文件夹
        print('正在下载', file_name)
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
                gevent.sleep(0.05)  # 0.05
                continue
            break

    def request_code(self, url):
        """获取jpg数据并返回"""
        req = request.Request(url=url, headers=self.headers, method="GET")
        try:
            response = request.urlopen(req)
        except http.client.IncompleteRead as e:
            response = e.partial
        except Exception:
            return ''
        try:
            content = response.read()
        except http.client.IncompleteRead as e:
            content = e.partial
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
        self.stop = []

    def request_sound_code(self, url):
        """获取列表html源码"""
        req = request.Request(url=url, headers=self.headers, method="GET")
        try:
            response = request.urlopen(req)
        # 如果读不出html源码,则该html已该资源类的末页,添加进停止翻页请求列表
        except Exception:
            self.stop.append(re.findall('com/(.*)/', url)[0])
            print(url)
            return
        content = response.read().decode("gbk")
        if content:
            # print(url, '开始爬取')
            # 传入源码,进行分析抓取图片地址
            self.analyze(content)

    def analyze(self, content):
        """在html源码内匹配图片地址并添加到下载列表"""
        pics_list = re.findall('href="(.*?).html"><img', content)
        for i in pics_list:
            self.load_list.append(i)
            time.sleep(0.001)

    def get_html(self, list_url, gpool):
        """推出列表地址进行模拟翻页,并为每个列表地址创建协程,进行分析html源码"""
        gev_list = []
        num = 2
        while True:
            url = list_url + ('%d.html' % num)
            s = gpool.spawn(self.request_sound_code, url)
            time.sleep(0.05)
            gev_list.append(s)
            num += 1
            # 如果请求停止翻页的列表中出现该资源类名称,则停止翻页
            if re.findall('com/(.*)/', url)[0] in self.stop:
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
    resource = ['http://www.mm131.com/xinggan/list_6_',
                'http://www.mm131.com/qingchun/list_1_',
                'http://www.mm131.com/xiaohua/list_2_',
                'http://www.mm131.com/chemo/list_3_',
                'http://www.mm131.com/qipao/list_4_',
                'http://www.mm131.com/mingxing/list_5_'
                ]
    # 协程数量控制
    gpool = pool.Pool(50)
    # 抓取相册地址开始时间
    star_time = time.time()
    # 初始化模拟浏览器
    server = GetHtml()
    # 协程列表
    gev_list = []
    # 为每个资源网创建一个协程
    for i in resource:
        s = gevent.spawn(server.get_html, i, gpool)
        gevent.sleep(0.1)  # 0.1
        gev_list.append(s)
    gevent.joinall(gev_list)
    # 抓取相册地址完成时间
    end_time = time.time() - star_time
    print('套图地址爬取完毕,耗时:%ds' % int(end_time))
    print(server.load_list)
    # 相册下载开始时间
    down_time = time.time()
    # 初始化模拟浏览器并传入相册列表
    down = Download(server.load_list)
    # 下载
    down.download_begin(gpool)
    # 相册下载完成时间
    down_endtime = time.time() - down_time
    print('套图下载完毕,耗时:%ds' % int(down_endtime))


if __name__ == '__main__':
    main()
