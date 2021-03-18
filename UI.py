from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap, QFont, QPainter
from PyQt5.QtChart import QLineSeries, QValueAxis, QChartView

from src.entry import Ui_Entry
from src.random import Ui_Random
from src.register import Ui_Register
from src.myplot import Myplot
from src.WhiteBoard import WhiteBoard
from face import FaceRecognition

import sys
import os
import time
import threading
import scipy.io as scio
import pandas as pd
import numpy as np
import cv2


class GlobalVars(object):
    def __init__(self):
        self.init_time = time.time()
        self.alarm = False
        self.debug = True


globalVars = GlobalVars()

'''''''''''''''''''''''''''''''''''''''
UI_wrapper for Ui_Entry
Function:
1. timer -- show_time, time_warning, progress_bar
2. 
'''''''''''''''''''''''''''''''''''''''


# 时间戳转换函数
def TimeStamp2Time(timeStamp):
    timeTmp = time.localtime(timeStamp)  # time.localtime()格式化时间戳为本地时间
    myTime = time.strftime("%Y-%m-%d %H:%M:%S", timeTmp)  # 将本地时间格式化为字符串
    return myTime


def timer(timer_signal: QtCore.pyqtSignal(str), alarm_signal: QtCore.pyqtSignal(str),
          progress_signal: QtCore.pyqtSignal(int)):
    global globalVars
    t_ = time.time()
    progress: int = 0
    while True:
        t = time.time()
        if t - t_ >= 1:
            t_ = t
            timer_signal.emit(TimeStamp2Time(t))
        else:
            time.sleep(0.5)
        delta_t = t - globalVars.init_time
        if globalVars.alarm:
            if globalVars.debug:
                if delta_t > 35:
                    if delta_t > 75:
                        if delta_t > 90:
                            alarm_signal.emit("距第二节下课还有5分钟,请您注意上课时间")
                        else:
                            alarm_signal.emit("第二节课已过半,请您注意上课时间")
                    else:
                        alarm_signal.emit("距第一节下课还有10分钟,请您注意上课时间")
            else:
                if delta_t > 35 * 60 * 60:
                    if delta_t > 75 * 60 * 60:
                        if delta_t > 90 * 60 * 60:
                            alarm_signal.emit("距第二节下课还有5分钟,请您注意上课时间")
                        else:
                            alarm_signal.emit("第二节课已过半,请您注意上课时间")
                    else:
                        alarm_signal.emit("距第一节下课还有10分钟,请您注意上课时间")
        if globalVars.debug:
            new_progress = int(delta_t)
        else:
            new_progress = int(delta_t / (100 * 60 * 60) * 100)
        if new_progress != progress:
            progress = new_progress
            progress_signal.emit(new_progress)


class Entry(QtWidgets.QMainWindow, Ui_Entry):
    global globalVars, win_register, win_random, win_white_board
    time_signal = QtCore.pyqtSignal(str)
    alarm_signal = QtCore.pyqtSignal(str)
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Entry, self).__init__()
        self.setupUi(self)
        self.init()

        # set front style
        self.logo.setStyleSheet(
            '''
                border:none;
                color:yellowgreen;
            ''')
        self.time.setStyleSheet(
            '''
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial;
                color:purple;
            ''')

        self.time_signal.connect(self.update_time)
        self.alarm_signal.connect(self.update_alarm)
        self.progress_signal.connect(self.update_progress)

    def init(self):
        self.comboBox.addItems(("教室", "公司"))

        # start my timer
        thread = threading.Thread(target=timer, args=(self.time_signal, self.alarm_signal, self.progress_signal))
        thread.setDaemon(True)
        thread.start()

        self.plot = Myplot()
        self.btn6.setVisible(False)

    def update_time(self, string):
        '''
        callback for timer
        :param string:
        :return:
        '''
        self.time.setText(string)

    def update_alarm(self, string):
        '''
        callback for alarm
        :param string:
        :return:
        '''
        self.feedback.setText(string)

    def update_progress(self, i):
        self.progressBar.setValue(i)

    def closeEvent(self, event):
        '''
        redefine close Event if exit btn exits
        :param event:
        :return:
        '''
        sys.exit(0)

    def select_scene(self, index):
        print("scene:", index)

    def face_register(self):
        win_register.show()

    def random_register(self):
        win_random.show()

    def myplot(self):
        self.plot.exec()

    def whiteBoard(self):
        win_white_board.show()

    def system_monitor(self):
        pass

    def standby(self):
        pass

    def alarm(self):
        globalVars.alarm = not globalVars.alarm
        if globalVars.debug:
            print(f"Status alarm switched to {globalVars.alarm}")
        if globalVars.alarm:
            self.btn_alarm.setText("关闭时间提醒")
        else:
            self.btn_alarm.setText("打开时间提醒")


def timer2(timer_signal: QtCore.pyqtSignal(str)):
    t_ = time.time()
    while True:
        t = time.time()
        if t - t_ >= 1:
            t_ = t
            timer_signal.emit(TimeStamp2Time(t))


class Register(QtWidgets.QMainWindow, Ui_Register):
    global globalVars
    time_signal = QtCore.pyqtSignal(str)
    detect_signal = QtCore.pyqtSignal((np.ndarray, list))

    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.newCol = True
        self.directory = ''
        self.ready = False

        self.student_list = []
        self.student_features = []

        self.init()

        self.time_signal.connect(self.update_time)
        self.detect_signal.connect(self.detect_callback)

    def init(self):
        self.new_line.setChecked(True)
        # start my timer
        thread = threading.Thread(target=timer2, args=(self.time_signal,))
        thread.setDaemon(True)
        thread.start()

        self.date = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    def load(self):
        # self.fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*)")  # ;;Text Files(*.txt)
        # print(self.fileName)
        # print(fileType)
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        print(self.directory)
        self.ready = False
        if self.directory == '':
            return
        print(os.listdir(self.directory))
        for file in os.listdir(self.directory):
            if os.path.splitext(file)[-1] == '.xlsx':  # xlsx
                self.df: pd.DataFrame = pd.read_excel(self.directory + rf"/{file}")
                for row in self.df.iteritems():
                    self.student_list = list(row[1])
                    print(self.student_list)
                    break
        for stu in self.student_list:
            if os.path.exists(self.directory + '/' + stu + '.mat'):
                self.student_features.append(scio.loadmat(self.directory + '/' + stu + '.mat')['X'].squeeze())
            else:
                print(f"{stu}'s feature not exists.")
                return
        self.ready = True
        print(self.student_list)
        print(self.student_features)
        if self.newCol:
            self.df[self.date] = [False] * len(self.student_list)
            print(self.df)
        #### TODO
        self.df.to_excel(excel_writer='test.xlsx', header=True, index=False)
        self.finish_loading_callback()

    def add_new_column(self):
        self.newCol = self.new_line.isChecked()
        if globalVars.debug:
            print("newCol: ", self.newCol)

    def set_minutes_seconds(self):
        pass

    def update_time(self, string):
        self.time.setText(string)

    def finish_loading_callback(self):
        self.output.setText("Loading finished.")
        self.detector = FaceRecognition(self.student_list, self.student_features, self.detect_signal)
        self.detector.detect(self.detect_signal)

    def detect_callback(self, img, names):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.QtImg = QImage(shrink.data, shrink.shape[1], shrink.shape[0], QImage.Format_RGB888)
        self.image.setPixmap(QPixmap.fromImage(self.QtImg))
        for name in names:
            if name != 'unknown':
                continue
            idx = self.student_list.index(name)
            print(idx)


class Random(QtWidgets.QMainWindow, Ui_Random):
    def __init__(self):
        super(Random, self).__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_entry = Entry()
    win_register = Register()
    win_white_board = WhiteBoard()
    win_random = Random()
    win_entry.show()
    sys.exit(app.exec_())
