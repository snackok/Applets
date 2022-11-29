# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_0216.py
@时间：2022/11/24  13:23
@文档说明:
"""
from PyQt5.QtGui import QBrush
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
        self.ui.btn_eval.clicked.connect(self.handle_eval)
        self.ui.btn_save.clicked.connect(self.handle_save)


        #初始化窗体成员变量
        self.c_data = None
        self.c_model = evl_lib.PandasModel()

        # 初始化控件设置
        # 从配置文件中读取评价标准
        self.load_eval_stand()
        # self.ui.txt_debug_info.setHidden(True)     # 调试按钮设置隐藏

        # 调试时用
        self.ui.txt_path.setText(r"W:/09TEMP/01/test.xlsx")
        self.handle_open_xls()

    # 读取评价方法
    def load_eval_stand(self):
        self.func_debug("读取评价标准")
        t_stand = pd.read_excel("评价标准.xlsx", index_col=0)
        self.func_debug(t_stand, "读取评价标准")
        print(t_stand.shape[0])
        for i in range(2):
            self.func_debug(t_stand.loc[i+1], "单个评价标准")
            self.ui.cob_eval.addItem(str(i + 1) + '.' + t_stand.name[i+1])

    # 解析函数
    def handle_debug(self):
        self.c_model.testfun()
        QMessageBox.about(self.ui, '测试', '测试函数')
        self.func_debug("--------------测试---------------")
        # self.c_model.appendRow([])
        # self.ui.list_xls.setRowHeight(2,100)
        # self.ui.list_xls.show()
        self.c_model.change_color(1, 1, QBrush(Qt.red))

    # 找到数据xlsx
    def handle_find_xls(self):
        openfile_name, file_type = QFileDialog.getOpenFileName(self.ui, '选择文件', ' ', 'Excel files(*.xlsx , *.xls)')
        self.ui.txt_path.setText(openfile_name)

    # 用MVC 的方式加载xlsx
    def handle_open_xls(self):
        # QMessageBox.about(self.ui, '测试', '打开xls函数')
        t_filename = self.ui.txt_path.text()
        self.func_debug(t_filename)
        t_data = pd.read_excel(t_filename)
        self.c_data = t_data
        self.func_debug(self.c_data)
        self.c_model = evl_lib.PandasModel(self.c_data)
        self.ui.list_xls.setModel(self.c_model)

    # 评价函数
    def handle_eval(self):
        QMessageBox.about(self.ui, '评价', '评价函数')
        # 可从xls.model()._data 中获取 pandas的 series对象
        f_df = self.ui.list_xls.model()._df  # type: pd.DataFrame
        self.func_debug(self.ui.list_xls.model()._df, "评价数据")
        print(f_df.shape[0])
        print(f_df.shape[1])

        f_df.insert(f_df.shape[1], "评价等级", "")
        f_eval_index = f_df.shape[1]-1
        f_df.insert(f_df.shape[1], "超标元素", "")
        f_exceed_ele_index = f_df.shape[1]-1
        # 遍历数据行，进行评估
        for row_i in range(f_df.shape[0]):
            t_cur_col_result = 1
            for col_i in range(f_df.shape[1]):
                # print(f_df.loc[row_i][col_i])
                # 如果是测试元素列，则进行判断
                if evl_lib.is_element(f_df.columns.values[col_i]):
                    t_cur_result = evl_lib.eval_item(f_df.loc[row_i][col_i], f_df.columns.values[col_i])   # 评价单个元素
                    # print(t_cur_result)
                    # > 3 超标，超标则将此元素记录为超标元素,同时设置单元格颜色
                    if t_cur_result > 3:
                        f_df.iloc[row_i][f_exceed_ele_index] += f_df.columns.values[col_i] + " "

                    # 取各个元素评价指标的最大值
                    if t_cur_result > t_cur_col_result:
                        t_cur_col_result = t_cur_result
            # 赋予评价值
            f_df.iloc[row_i][f_eval_index] = t_cur_col_result
        # 评价完后更新model
        self.c_model.setDataFrame(f_df)
        #self.ui.list_xls.setModel(model)
        # 测试变颜色
        # self.c_model.cellPaint(2, 2, "#FFFF00")

    # 选择评价标准时候触发
    def handle_sel_stand(self):
        self.func_debug(self.ui.cob_eval.currentText(), "选择了")

    # 保存函数
    def handle_save(self):
        savefile_name, file_type = QFileDialog.getSaveFileName(self.ui, '选择文件', ' ', 'Excel files(*.xlsx , *.xls)')
        QMessageBox.about(self.ui, '保存', '保存'+savefile_name)
        f_df = self.ui.list_xls.model()._df  # type: pd.DataFrame
        f_df.to_excel(savefile_name)


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