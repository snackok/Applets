# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_0216.py
@时间：2022/2/16  13:23
@文档说明:
"""

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd


class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile('ui/evl_ui.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)

        # 捆绑事件
        self.ui.btn_debug.clicked.connect(self.handle_debug)
        self.ui.btn_find_xls.clicked.connect(self.handle_find_xls)
        self.ui.btn_open_xls.clicked.connect(self.handle_open_xls)

        # 初始化
        # self.ui.txt_debug_info.setHidden(True)

        # 调试时用
        self.ui.txt_path.setText(r"W:/09TEMP/01/test.xlsx")

    # 解析函数
    def handle_debug(self):
        QMessageBox.about(self.ui, '测试', '测试函数')

    # 找到数据xlsx
    def handle_find_xls(self):
        openfile_name, file_type = QFileDialog.getOpenFileName(self.ui, '选择文件', ' ', 'Excel files(*.xlsx , *.xls)')
        self.ui.txt_path.setText(openfile_name)

    # 加载xlsx文件
    def handle_open_xls(self):
        QMessageBox.about(self.ui, '测试', '打开xls函数')
        t_filename = self.ui.txt_path.text()
        print(t_filename)
        t_data = pd.read_excel(t_filename)
        t_data_rows = t_data.shape[0]
        t_data_cols = t_data.shape[1]
        t_header = t_data.columns.values.tolist()  # 获取表头

        print(t_data)
        # data = pd.read_excel(self.ui.txt_path, converters={'Author': convert_author_cell})
        # ===========读取表格，转换表格，==============================
        # ===========给tablewidget设置行列表头========================
        self.ui.list_xls.setColumnCount(t_data_cols)  # 设置表格列数
        self.ui.list_xls.setRowCount(t_data_rows)  # 设置表格行数
        self.ui.list_xls.setHorizontalHeaderLabels(t_header)  # 给tablewidget设置行列表头
        # ===========遍历表格每个元素，同时添加到tablewidget中===========
        for i in range(t_data_rows):  # 行循环
            f_rows_values = t_data.iloc[[i]]  # 读入一行数据
            f_array = np.array(f_rows_values)  # 将该行数据放入数组中
            f_list = f_array.tolist()[0]  # 将该数组转换为列表
            for j in range(t_data_cols):  # 列循环
                f_items_list = f_list[j]  # 行列表中的每个元素放入列列表中
                # ==============将遍历的元素添加到tablewidget中并显示=======================
                f_items = str(f_items_list)  # 该数据转换成字符串
                f_newItem = QTableWidgetItem(f_items)  # 该字符串类型的数据新建为tablewidget元素
                f_newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 显示为水平居中、垂直居中
                self.ui.list_xls.setItem(i, j, f_newItem)  # 在表格第i行第j列显示newItem元素






app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
