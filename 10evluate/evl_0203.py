# -*- encoding:utf-8 -*-
"""
@作者：WW.WCGS,YYL.WCGS
@文件名：evl_0203.py
@时间：2023/02/07  13:23
@文档说明:
"""
from PySide2.QtGui import QBrush, QStandardItem
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,Qt
import pandas as pd
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QStyledItemDelegate
import xlsxwriter
import openpyxl
from openpyxl.styles import PatternFill, Color
import evl_lib


class QColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, bg_role=Qt.BackgroundRole):
        super().__init__(parent)
        self.bg_role = bg_role

    def paint(self, painter, option, index):
        value = index.data()
        if isinstance(value, QColor):
            option.backgroundBrush = value
        super().paint(painter, option, index)

    def background_color(self, row):
        index = self.parent().model().index(row, 0)
        value = self.parent().model().data(index, self.bg_role)
        return value


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
        self.ui.list_xls.doubleClicked.connect(self.handle_list_xls_clicked)

        # 初始化窗体成员变量
        self.c_data = None  # 待评价数据
        self.c_model = evl_lib.PandasModel()
        self.c_stand = None  # 评价标准

        # 初始化控件设置
        # 从配置文件中读取评价标准
        self.load_eval_stand()
        # self.ui.txt_debug_info.setHidden(True)     # 调试按钮设置隐藏

        # 调试时用   "W:/09TEMP/2022/01/test.xlsx"  W:/09TEMP/001/test.xls
        self.ui.txt_path.setText(r"W:/09TEMP/001/test.xlsx")
        self.handle_open_xls()

    # 读取评价方法
    def load_eval_stand(self):
        # self.func_debug("读取评价标准")
        t_stand = pd.read_excel("评价标准.xlsx", index_col=0)
        # self.func_debug(t_stand, "读取评价标准")
        for i in range(2):
            # self.func_debug(t_stand.loc[i + 1], "单个评价标准")
            self.ui.cob_eval.addItem(str(i + 1) + '.' + t_stand.name[i + 1])

    # 解析函数
    def handle_debug(self):
        # self.c_model.testfun()
        QMessageBox.about(self.ui, '测试', '测试函数')
        self.func_debug("--------------测试---------------")
        # f_df = self.ui.list_xls.model()._df  # type: pd.DataFrame
        model = self.ui.list_xls.model()
        print(f'模型共有{model.rowCount()}行，{model.columnCount()}列')
        self.ui.list_xls.model().refresh()


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
        self.func_debug(f_df, "评价数据")

        # 针对每个待评价元素添加 评价列
        for col in f_df.columns:
            if evl_lib.is_element(col):
                f_df.insert(f_df.columns.get_loc(col) + 1, f"{col}评价结果", "")

        # 插入评价等级和超标元素列
        f_df.insert(f_df.shape[1], "评价等级", "")
        f_eval_index = f_df.shape[1] - 1
        f_df.insert(f_df.shape[1], "超标元素", "")
        f_exceed_ele_index = f_df.shape[1] - 1
        # 遍历数据行，进行评估
        for row_i, row_data in f_df.iterrows():
            t_cur_col_result = 1
            # 跳过第一行，因为第一行是单位
            if row_i == 0:
                continue
            # if row_i == 10:
            #     break   # 调试用，只判断前10行数据
            for col_i, col_data in row_data.iteritems():
                # 如果是测试元素列，则进行判断
                if evl_lib.is_element(col_i):
                    t_cur_result = evl_lib.eval_item(col_data, col_i)  # 评价单个元素
                    # 在这里添加评价结果
                    f_df.at[row_i, f"{col_i}评价结果"] = t_cur_result
                    # > 3 超标，超标则将此元素记录为超标元素,同时设置单元格颜色
                    if t_cur_result > 3:
                        f_df.iloc[row_i, f_exceed_ele_index] += col_i + " "
                    # 取各个元素评价指标的最大值
                    if t_cur_result > t_cur_col_result:
                        t_cur_col_result = t_cur_result
            # 赋予评价值
            f_df.iloc[row_i, f_eval_index] = t_cur_col_result
            # 评价完后更新model
        self.c_model.setDataFrame(f_df)

    # 选择评价标准时候触发
    def handle_sel_stand(self):
        self.func_debug(self.ui.cob_eval.currentText(), "选择了")

    # 保存函数
    def handle_save(self):
        savefile_name, file_type = QFileDialog.getSaveFileName(self.ui, '选择文件', ' ', 'Excel files(*.xlsx , *.xls)')
        QMessageBox.about(self.ui, '保存', '保存' + savefile_name)
        # # 强制刷新所有单元格的数据和背景色
        self.ui.list_xls.model().refresh()

        f_df = self.ui.list_xls.model()._df  # type: pd.DataFrame

        # 创建 ExcelWriter 实例
        writer = pd.ExcelWriter(savefile_name, engine='xlsxwriter', engine_kwargs={'options':{'nan_inf_to_errors': True}})

        # 将 DataFrame 输出到 Excel 中
        f_df.to_excel(writer, index=False, sheet_name='Sheet1')

        # 获取 ExcelWriter 中的 Workbook 对象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # 获取单元格背景颜色字典
        colors = self.ui.list_xls.model().colors
        # 循环设置每一列的单元格格式
        for col_idx in range(f_df.shape[1]):
            col_name = f_df.columns[col_idx]
            col_width = max(f_df[col_name].astype(str).map(len).max(), len(col_name))
            worksheet.set_column(col_idx, col_idx, width=col_width)

            # 循环设置每一个单元格的格式
            for row_idx in range(f_df.shape[0]):

                bg_color = colors.get((row_idx, col_idx))
                # print(f"保存{row_idx + 1}行，{col_idx + 1}列，底色为{bg_color}")
                cell_format = self.set_cell_format(workbook, bg_color)
                worksheet.write(row_idx + 1, col_idx, f_df.iloc[row_idx, col_idx], cell_format)
        # 保存 Excel 文件
        writer.save()
        # f_df.to_excel(savefile_name)

    # 双击列表事件
    def handle_list_xls_clicked(self,index):
        color = self.ui.list_xls.model().colors.get((index.row(), index.column()))
        print(f"双击了{index.row()+1}行，{index.column()+1}列，底色为{color}")

    # 调试信息方法，以字符串方式输出 p_msg , 参数p_clear_msg 为true时 清空对话框
    def func_debug(self, p_msg, p_str_title='调试', p_clear_msg=False):
        if p_clear_msg:
            self.ui.txt_debug_info.clear()
        t_str_msg = str(p_msg)
        self.ui.txt_debug_info.appendPlainText('{0:-^60}'.format(p_str_title))
        self.ui.txt_debug_info.appendPlainText(t_str_msg)

    def set_cell_format(self, workbook, bg_color=None):
        cell_format = workbook.add_format()
        if bg_color:
            # print(bg_color)
            cell_format.set_bg_color(bg_color.color().name())
        return cell_format


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
