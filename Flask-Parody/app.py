import re
import time
import socket
import gevent
from gevent import monkey
from urllib import parse

monkey.patch_all()


def render_template(url):
    with open('./' + url, 'rb') as f:
        return f.read()


class Request(object):
    def __init__(self):
        self.method = None
        self.form = {}


request = Request()


class App(object):
    dict = {}

    def __init__(self):
        print('app is run:http://127.0.0.1')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 80))
        self.s.listen(123)
        self.header = 'HTTP/1.1 200 OK\n\n'

    def run(self):
        gev_list = []
        while True:
            client_soc, client_addr = self.s.accept()
            s = gevent.spawn(self.source, client_soc)
            gev_list.append(s)
            time.sleep(.01)
        # gevent.joinall(gev_list)

    def source(self, client_soc):

        client_request = client_soc.recv(1024).decode()

        request.method = re.findall(r'([^/]*) /', client_request)[0]

        try:
            req = re.findall(r'[^/]*(/.*?) ', client_request)[0]
        except IndexError:
            client_soc.close()
            return
        client_soc.send(self.header.encode())

        if ('.html' in req) and (req not in App.dict):
            req = '/Not_yet_done.html'
        if req == '/':
            req = '/index.html'

        if 'html' in req:
            if request.method == 'POST':
                data = re.findall(r'\r\n\r\n(.*)', client_request)[0].split('&')
                for i in data:
                    request.form[i.split('=')[0]] = parse.unquote_plus(i.split('=')[1])
            body = App.dict[req](req)
            client_soc.send(body)
            client_soc.close()
            return

        self.not_html(client_soc, req)

    @staticmethod
    def not_html(client_soc, file):
        try:
            body = render_template(file)
        except FileNotFoundError as e:
            print(e)
            body = 'not found source'.encode()
        except Exception as a:
            print(a)
            return
        client_soc.send(body)
        client_soc.close()

    @staticmethod
    def route(url):
        def set_fun(func):
            def call_fun(*args, **kwargs):
                return func(*args, **kwargs)
            App.dict[url + '.html'] = call_fun
            return call_fun

        return set_fun
