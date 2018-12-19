# 天命随机系统!
import sys
import time
from random import randint
from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import (QGridLayout, QWidget, QMainWindow,
                             QApplication, QLabel, QPushButton)


class GUI(QMainWindow):
    """窗体"""

    def __init__(self):
        super().__init__()
        # 位置大小窗体名
        self.move(510, 347)
        self.resize(362, 250)
        self.setWindowTitle('天命')
        self.btn1 = 0

        # 状态消息栏文本
        self.statusBar().showMessage("天命")

        # 标签
        self.label1 = QLabel('Python16', )
        self.label3 = QLabel('')
        self.label4 = QLabel('')
        self.label5 = QLabel('')
        self.label6 = QLabel('')
        self.label7 = QLabel('')
        # 为标签设字体
        self.label1.setFont(QFont("cour", 25, QFont.Bold))
        self.label5.setFont(QFont("cour", 20, QFont.Bold))

        # 两个按钮
        self.pushButton1 = QPushButton('天灵灵地灵灵')
        self.pushButton1.setFont(QFont("cour", 15))
        self.pushButton2 = QPushButton('>>急急如律令<<')
        self.pushButton2.setFont(QFont("cour", 15))
        # 为按钮绑定函数操作
        self.pushButton1.clicked.connect(self.god_will)
        self.pushButton2.clicked.connect(self.god_well)

        # 创建一个网格布局对象
        grid_layout = QGridLayout()
        # 在网格中添加窗口部件
        grid_layout.addWidget(self.label1)  # 放置在0行0列
        grid_layout.addWidget(self.label3)  # 放置在2行0列
        grid_layout.addWidget(self.pushButton1)  # 3行0列
        grid_layout.addWidget(self.label4)  # 放置在3行0列
        grid_layout.addWidget(self.label5)  # 放置在3行0列
        grid_layout.addWidget(self.label6)  # 放置在3行0列
        grid_layout.addWidget(self.label7)  # 放置在3行0列
        grid_layout.addWidget(self.pushButton2)  # 4行0列

        # 对齐方式
        grid_layout.setAlignment(Qt.AlignTop)
        grid_layout.setAlignment(self.label1, Qt.AlignCenter)
        grid_layout.setAlignment(self.pushButton1, Qt.AlignCenter)
        grid_layout.setAlignment(self.label5, Qt.AlignCenter)

        # 创建一个窗口对象
        layout_widget = QWidget()
        # 设置窗口的布局层
        layout_widget.setLayout(grid_layout)
        self.setCentralWidget(layout_widget)
        # 无边框
        self.setWindowFlags(Qt.FramelessWindowHint)

    def god_will(self):
        """天灵灵随机显示"""
        name_list = ['史怀威','王海康','刘祥','熊洋','王立','郑仙强','王炜','彭欢','张立超','朱安琪','沙强','王玉坤','陶海鹏','陈德渤',
                     '游文杰','黄辉','李勇','赵涛涛','孙梦豪','朱赞聪','程骋','陈强','黄唯淳','罗标','朱海涛','张晓文','吴振宇',
                     '何航波','程超','闫海宾','强光文','陈谞实','刘孝衡','朱得粮','崔玉涛','黄小龙','黄伟楠','颜奎','胡创业',
                     '陈林满','刘旭祥','党巨然','窦志强','窦志扬','李陈中','赵智永','徐豆豆','叶洪亮','王俊','王奇奇','邢铭博',
                     '江燕群','赵卫兵','张发辉','程鑫','顾栩龙','李尧','周磊','秦炎申','李肖辉','邢烨','化欢龙','张云飞','林上涛',
                     '邢浩','张耀','许勇','张生强','苏猛','李林景','张晓峰','黄长松','孟亚旗','陈凯','张梦辉','严瑞平','雷炳杰',
                     '李查德','郭飞','孙政','王广辉','李萨','孔南飞','买宁','朱磊','吴晶','黄旭','修心旖','洪子豪','黄璐璐',
                     '叶祥军','王德宏','张岩','徐利元','苗亚晖','黄金金','丁娟','杜军','徐耀','杨阳','欧阳世童']
        self.btn2 = 0
        while self.pushButton1.clicked:
            god = randint(0, 7)
            str_n = name_list[god]
            self.label5.setText(str_n)
            QApplication.processEvents()
            time.sleep(1 / 24)
            if self.btn2 == 0:
                continue
            else:
                break

    def god_well(self):
        """如律令最终结果"""
        name_list = ['史怀威','王海康','刘祥','熊洋','王立','郑仙强','王炜','彭欢','张立超','朱安琪','沙强','王玉坤','陶海鹏','陈德渤',
                     '游文杰','黄辉','李勇','赵涛涛','孙梦豪','朱赞聪','程骋','陈强','黄唯淳','罗标','朱海涛','张晓文','吴振宇',
                     '何航波','程超','闫海宾','强光文','陈谞实','刘孝衡','朱得粮','崔玉涛','黄小龙','黄伟楠','颜奎','胡创业',
                     '陈林满','刘旭祥','党巨然','窦志强','窦志扬','李陈中','赵智永','徐豆豆','叶洪亮','王俊','王奇奇','邢铭博',
                     '江燕群','赵卫兵','张发辉','程鑫','顾栩龙','李尧','周磊','秦炎申','李肖辉','邢烨','化欢龙','张云飞','林上涛',
                     '邢浩','张耀','许勇','张生强','苏猛','李林景','张晓峰','黄长松','孟亚旗','陈凯','张梦辉','严瑞平','雷炳杰',
                     '李查德','郭飞','孙政','王广辉','李萨','孔南飞','买宁','朱磊','吴晶','黄旭','修心旖','洪子豪','黄璐璐',
                     '叶祥军','王德宏','张岩','徐利元','苗亚晖','黄金金','丁娟','杜军','徐耀','杨阳','欧阳世童']
        god = randint(0, 7)
        str_n = name_list[god]
        self.label5.setText(str_n)
        QApplication.processEvents()
        self.btn2 = 1

    def keyPressEvent(self, e):
        """ESC退出"""
        if e.key() == Qt.Key_Escape:
            self.close()

    # 无边框的拖动窗口
    def mousePressEvent(self, event):
        """标记鼠标左键摁下的响应与改变鼠标图标效果"""
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        """鼠标左键摁下时执行"""
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        """标记鼠标松手并改变图标"""
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.setWindowOpacity(0.8)
    gui.show()
    sys.exit(app.exec_())
