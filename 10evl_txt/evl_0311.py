# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_0216.py
@时间：2022/3/11  13:23
@文档说明:
"""

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QAbstractTableModel
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
import evl_lib


# from evl_lib import *


class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile('ui/evl_testui.ui')
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
        self.ui.btn_eval.clicked.connect(self.handle_eval)
        self.ui.btn_save.clicked.connect(self.handle_save)

        # 初始化控件设置
        # 从配置文件中读取评价标准
        self.load_eval_stand()
        # self.ui.txt_debug_info.setHidden(True)     # 调试按钮设置隐藏

        # 调试时用
        self.ui.txt_path.setText(r"W:/09TEMP/01/test.xlsx")

    # 读取评价方法
    def load_eval_stand(self):
        self.func_debug("读取评价标准")
        t_stand = pd.read_excel("评价标准.xlsx", index_col=0)
        self.func_debug(t_stand, "读取评价标准")
        for i in range(t_stand.shape[0]):
            self.func_debug(t_stand.loc[i+1], "单个评价标准")
            self.ui.cob_eval.addItem(str(i + 1) + '.' + t_stand.name[i+1])

    # 解析函数
    def handle_debug(self):
        QMessageBox.about(self.ui, '测试', '测试函数')
        self.func_debug("--------------测试---------------")

    # 找到数据xlsx
    def handle_find_xls(self):
        openfile_name, file_type = QFileDialog.getOpenFileName(self.ui, '选择文件', ' ', 'Excel files(*.xlsx , *.xls)')
        self.ui.txt_path.setText(openfile_name)

    # 用MVC 的方式加载xlsx
    def handle_open_xls(self):
        QMessageBox.about(self.ui, '测试', '打开xls函数')
        t_filename = self.ui.txt_path.text()
        self.func_debug(t_filename)
        t_data = pd.read_excel(t_filename)
        self.func_debug(t_data)
        model = evl_lib.PandasModel(t_data)
        self.ui.list_xls.setModel(model)

    # 评价函数
    def handle_eval(self):
        QMessageBox.about(self.ui, '评价', '评价函数')
        # 可从xls.model()._data 中获取 pandas的 series对象
        f_df = self.ui.list_xls.model().getData() # type: pd.DataFrame
        self.func_debug(self.ui.list_xls.model().getData(), "评价数据")
        print(f_df.shape[0])
        print(f_df.shape[1])

        # 遍历数据行，进行评估
        for row_i in range(f_df.shape[0]):
            t_cur_row_result = 1
            for col_i in range(f_df.shape[1]):
                print(f_df.loc[row_i][col_i])
#               t_cur_result = evl_lib.eval_item(data[i][j],header[j])   # 评价单个元素
#               if t_cur_result > 3：
#                   add_2_cell(ele_cell) # 添加超标元素到单元格
#               if t_cur_result > t_cur_row_result:  # 评价取最大值
#                   t_cur_row_result = t_cur_result

    # 选择评价标准时候触发
    def handle_sel_stand(self):
        self.func_debug(self.ui.cob_eval.currentText(), "选择了")

    # 保存函数
    def handle_save(self):
        QMessageBox.about(self.ui, '保存', '保存函数')

    # 调试信息方法，以字符串方式输出 p_msg , 参数p_clear_msg 为true时 清空对话框
    def func_debug(self, p_msg, p_str_title='调试', p_clear_msg=False):
        if p_clear_msg:
            self.ui.txt_debug_info.clear()
        t_str_msg = str(p_msg)
        self.ui.txt_debug_info.appendPlainText('{0:-^60}'.format(p_str_title))
        self.ui.txt_debug_info.appendPlainText(t_str_msg)



app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
