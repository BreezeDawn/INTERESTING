# 这是一个进程+线程的多用户服务器
import socket
import threading

import time


class Server(object):
    """服务器"""
    def __init__(self):
        """初始化服务器"""
        self.serv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_server.bind(('', 1234))
        self.serv_server.listen(128)
        self.service_list = []
        self.soc_dict = {}
        self.online = []

    def accept(self):
        """循环接收客户端连接"""
        while True:
            client_soc,client_addr = self.serv_server.accept()
            client_soc.send('连接成功'.encode())
            # 向上线客户端发送在线名单
            client_soc.send(('目前在线:'+repr(self.online)).encode())
            # 将客服套接字添加进服务列表
            self.service_list.append(client_soc)
            # 生成客户信息字典
            client_dic = {}
            client_dic['client_ip']=client_addr[0]
            client_dic['client_port'] = client_addr[1]
            client_dic['on_line'] = 1
            # 以客服套接字为键,客户字典为值,添加到套接字字典中
            self.soc_dict[client_soc] = client_dic

    def set_process(self):
        """循环判断服务列表是否有需要服务的客户端"""
        while True:
            if self.service_list:
                # 遍历服务列表,为每一个客服创建线程为客户端单独服务
                for service in self.service_list:
                    threading.Thread(target=self.recv,args=(service,)).start()
                    threading.Thread(target=self.on_lines,args=(service,)).start()
                    # 创建之后从服务列表中移除
                    self.service_list.remove(service)

    def on_lines(self,service):
        """循环判断客户端信息中的在线信息"""
        while True:
            try:
                for i in self.soc_dict.keys():
                    # 当客户端在线且不在在线列表中时,将客户端添加到在线列表
                    if (self.soc_dict[i]['on_line'] == 1) and (self.soc_dict[i]['client_ip'] not in self.online):
                        self.online.append(self.soc_dict[i]['client_ip'])
                        print('增加')
                        time.sleep(1)
                    # 当客户端下线且在在线列表中时,将客户端从在线列表中移除
                    if (self.soc_dict[i]['on_line'] == 0) and (self.soc_dict[i]['client_ip'] in self.online):
                        self.online.remove(self.soc_dict[i]['client_ip'])
                        print('删除')
                        time.sleep(1)
                        # 关闭对应的客服套接字并删除客户端信息字典
                        del self.soc_dict[i]
                        i.close()
            except Exception:
                pass



    def recv(self,service):
        """循环接收客户端消息"""
        while True:
            try:
                receive_data = service.recv(1024).decode()
                if receive_data:
                    print(receive_data)
                    continue
            except ConnectionResetError:
                pass
            # 当客户端断开连接,将客户端设为下线状态
            self.soc_dict[service]['on_line'] = 0
            print(self.soc_dict[service]['client_ip'],'断开链接')
            break

def main():
    server = Server()
    # 为接收连接和分配客服创建线程
    threading.Thread(target=server.set_process).start()
    threading.Thread(target=server.accept).start()

if __name__ == '__main__':
    main()