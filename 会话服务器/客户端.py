# 这是一个直连本地回环地址的客户端
import socket
import threading


def recv(client_server):
    """使用独立线程循环接收消息"""
    while True:
        print('等待消息~~~~~~')
        recv_data = client_server.recv(1024)
        print(recv_data.decode('utf-8'))


def send(client_server):
    """使用独立线程循环发送消息"""
    while True:
        msg = input('请输入：').encode('utf-8')
        client_server.send(msg)


def main():
    client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """客户端直连"""
    try:
        client_server.connect(('127.0.0.1', 1234))
        print('连接成功')
        # 为发送消息和接收消息创建线程
        threading.Thread(target=send, args=(client_server,)).start()
        threading.Thread(target=recv, args=(client_server,)).start()
    except Exception as exp:
        print(exp)


if __name__ == '__main__':
    main()
