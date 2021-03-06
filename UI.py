from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap, QPalette, QBrush

from src.entry import Ui_Entry
from src.random import Ui_Random
from src.register import Ui_Register
from src.myplot import Myplot
from app.face import FaceRecognition
from app.browser_tabbed.browser_tabbed import Browser
from app.paint.paint import Paint
from app.calculator.calculator import Calculator
from app.notes.notes import Notes, Note, session
from app.wordprocessor.wordprocessor import WordProcessor

import sys
import os
import time
import threading
import scipy.io as scio
import pandas as pd
import numpy as np
import cv2
import random
from xpinyin import Pinyin
import subprocess


class GlobalVars(object):
    def __init__(self):
        self.init_time = time.time()
        self.alarm = False
        self.debug = True
        self.scene = 0  # TODO


globalVars = GlobalVars()

'''''''''''''''''''''''''''''''''''''''
UI_wrapper for Ui_Entry
Function:
1. timer -- show_time, time_warning, progress_bar
2. scene -- classroom, workspace, meeting
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
    sign = [False] * 7
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
                if not sign[0]:
                    alarm_signal.emit("第一节课上课中")
                    sign[0] = True
                if delta_t > 35 and not sign[1]:
                    if delta_t > 45 and not sign[2]:
                        if delta_t > 55 and not sign[3]:
                            if delta_t > 75 and not sign[4]:
                                if delta_t > 90 and not sign[5]:
                                    if delta_t > 100 and not sign[6]:
                                        alarm_signal.emit("下课中...")
                                        sign[6] = True
                                    elif not sign[5]:
                                        alarm_signal.emit("距第二节下课还有5分钟,请您注意上课时间")
                                        sign[5] = True
                                elif not sign[4]:
                                    alarm_signal.emit("第二节课已过半,请您注意上课时间")
                                    sign[4] = True
                            elif not sign[3]:
                                alarm_signal.emit("第二节课上课中")
                                sign[3] = True
                        elif not sign[2]:
                            alarm_signal.emit("课间休息中")
                            sign[2] = True
                    elif not sign[1]:
                        alarm_signal.emit("距第一节下课还有10分钟,请您注意上课时间")
                        sign[1] = True
            else:
                if not sign[0]:
                    alarm_signal.emit("第一节课上课中")
                    sign[0] = True
                if delta_t > 35 * 60 * 60 and not sign[1]:
                    if delta_t > 45 * 60 * 60 and not sign[2]:
                        if delta_t > 55 * 60 * 60 and not sign[3]:
                            if delta_t > 75 * 60 * 60 and not sign[4]:
                                if delta_t > 90 * 60 * 60 and not sign[5]:
                                    if delta_t > 100 * 60 * 60 and not sign[6]:
                                        alarm_signal.emit("下课中...")
                                        sign[6] = True
                                    elif not sign[5]:
                                        alarm_signal.emit("距第二节下课还有5分钟,请您注意上课时间")
                                        sign[5] = True
                                elif not sign[4]:
                                    alarm_signal.emit("第二节课已过半,请您注意上课时间")
                                    sign[4] = True
                            elif not sign[3]:
                                alarm_signal.emit("第二节课上课中")
                                sign[3] = True
                        elif not sign[2]:
                            alarm_signal.emit("课间休息中")
                            sign[2] = True
                    elif not sign[1]:
                        alarm_signal.emit("距第一节下课还有10分钟,请您注意上课时间")
                        sign[1] = True
        if globalVars.debug:
            new_progress = int(delta_t)
        else:
            new_progress = int(delta_t / (100 * 60 * 60) * 100)
        if new_progress != progress:
            progress = new_progress
            progress_signal.emit(new_progress)


class Entry(QtWidgets.QMainWindow, Ui_Entry):
    global globalVars, win_register, win_random, win_paint
    time_signal = QtCore.pyqtSignal(str)
    alarm_signal = QtCore.pyqtSignal(str)
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Entry, self).__init__()
        self.setupUi(self)
        self.init()

        self.btn1.clicked.disconnect(self.face_register)
        self.btn2.clicked.disconnect(self.random_register)
        self.btn3.clicked.disconnect(self.myplot)
        self.btn4.clicked.disconnect(self.whiteBoard)
        self.btn5.clicked.disconnect(self.system_monitor)
        self.btn6.clicked.disconnect(self.standby)
        self.btn_alarm.clicked.disconnect(self.alarm)

        # set front style
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("src/background.jpeg")))
        self.comboBox.addItems(("教室", "办公", "会议"))
        self.setPalette(palette)

        self.time_signal.connect(self.update_time)
        self.alarm_signal.connect(self.update_alarm)
        self.progress_signal.connect(self.update_progress)

    def init(self):
        self.logo.setStyleSheet(
            '''
                border:none;
                color:yellowgreen;
                font-weight: bold;
            ''')
        self.time.setStyleSheet(
            '''
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial;
                color:cyan;
            ''')
        self.scrollArea.setStyleSheet(
            '''
                background-color:transparent;
            '''
        )
        self.btn1.setStyleSheet(
            '''
                QPushButton{
                    font-size: 16px;
                    border: none;
                    border-radius:10px;
                    background-color: white;
                }
                QPushButton:hover{
                    color:black;
                    font-weight:bold;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:LightGreen;
                }
            '''
        )
        self.btn2.setStyleSheet(
            '''
                QPushButton{
                    font-size: 16px;
                    border: none;
                    border-radius:10px;
                    background-color: white;
                }
                QPushButton:hover{
                    color:black;
                    font-weight:bold;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:LightGreen;
                }
            '''
        )
        self.btn3.setStyleSheet(
            '''
                QPushButton{
                    font-size: 16px;
                    border: none;
                    border-radius:10px;
                    background-color: white;
                }
                QPushButton:hover{
                    color:black;
                    font-weight:bold;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:LightGreen;
                }
            '''
        )
        self.btn4.setStyleSheet(
            '''
                QPushButton{
                    font-size: 16px;
                    border: none;
                    border-radius:10px;
                    background-color: white;
                }
                QPushButton:hover{
                    color:black;
                    font-weight:bold;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:LightGreen;
                }
            '''
        )
        self.btn5.setStyleSheet(
            '''
                QPushButton{
                    font-size: 16px;
                    border: none;
                    border-radius:10px;
                    background-color: white;
                }
                QPushButton:hover{
                    color:black;
                    font-weight:bold;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:LightGreen;
                }
            '''
        )
        self.btn6.setStyleSheet(
            '''
                QPushButton{
                    font-size: 16px;
                    border: none;
                    border-radius:10px;
                    background-color: white;
                }
                QPushButton:hover{
                    color:black;
                    font-weight:bold;
                    border:1px solid #F3F3F5;
                    border-radius:10px;
                    background:LightGreen;
                }
            '''
        )
        self.course_label.setStyleSheet(
            '''
                color: orange;
            '''
        )
        self.course.setStyleSheet(
            '''
                color: yellow;
                border:1px solid #ccc;
            '''
        )
        self.schedule_label.setStyleSheet(
            '''
                color: orange;
            '''
        )
        self.schedule.setStyleSheet(
            '''
                color: yellow;
                border:1px solid #ccc;
            '''
        )
        self.teacher_label.setStyleSheet(
            '''
                color: orange;
            '''
        )
        self.teacher.setStyleSheet(
            '''
                color: yellow;
                border:1px solid #ccc;
            '''
        )
        self.feedback.setStyleSheet(
            '''
                color: coral;
                border:1px solid coral;
            '''
        )
        self.function_label.setStyleSheet(
            '''
                color:lightblue;
            '''
        )
        self.comboBox.setStyleSheet(
            '''
                background:lightblue;
            '''
        )
        self.btn_alarm.setStyleSheet(
            '''
                background:black;
                color:white;
            '''
        )
        self.menubar.setStyleSheet(
            '''
                color:black;
                background:white;
            '''
        )

        # start my timer
        thread = threading.Thread(target=timer, args=(self.time_signal, self.alarm_signal, self.progress_signal))
        thread.setDaemon(True)
        thread.start()

        self.plot = Myplot()
        self.btn6.setVisible(False)

        self.course.setText("应用程序课程设计")
        self.schedule.setText("周五 10:00-11:40")
        self.teacher.setText("黄征老师")
        self.feedback.setText("上课中...")

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
        try:
            self.proc.terminate()
        except Exception as e:
            pass
        try:
            self.proc2.terminate()
        except Exception as e:
            pass
        sys.exit(0)

    def select_scene(self, index):
        print("scene:", index)
        if index == 0:
            self.retranslateUi(self)
            self.init()
            try:
                self.btn1.clicked.disconnect(self.browser)
                self.btn2.clicked.disconnect(self.calculate)
                self.btn3.clicked.disconnect(self.word)
                self.btn4.clicked.disconnect(self.note)
                self.btn5.clicked.disconnect(self.painter)
                self.btn6.clicked.disconnect(self.minesweep)
                self.btn_alarm.clicked.disconnect(self.media)
            except Exception as e:
                print(e)
            self.btn1.clicked.connect(self.face_register)
            self.btn2.clicked.connect(self.random_register)
            self.btn3.clicked.connect(self.myplot)
            self.btn4.clicked.connect(self.whiteBoard)
            self.btn5.clicked.connect(self.system_monitor)
            self.btn6.clicked.connect(self.standby)
            self.btn_alarm.clicked.connect(self.alarm)
            self.course.setMinimumSize(QtCore.QSize(131, 31))
            self.schedule_label.setVisible(True)
            self.schedule.setVisible(True)
            self.teacher_label.setVisible(True)
            self.teacher.setVisible(True)
        elif index == 1:
            _translate = QtCore.QCoreApplication.translate
            self.setWindowTitle(_translate("Entry", "MainWindow"))
            self.logo.setText(_translate("Entry", "System  Everywhere"))
            self.course_label.setText(_translate("Entry", "Course"))
            self.course.setText(_translate("Entry", "course"))
            self.schedule_label.setText(_translate("Entry", "Schedule"))
            self.schedule.setText(_translate("Entry", "schedule"))
            self.teacher_label.setText(_translate("Entry", "Teacher"))
            self.teacher.setText(_translate("Entry", "teacher"))
            self.feedback.setText(_translate("Entry", "TextLabel"))
            self.function_label.setText(_translate("Entry", "Function"))
            self.btn1.setText(_translate("Entry", "浏览器"))
            self.btn2.setText(_translate("Entry", "计算器"))
            self.btn3.setText(_translate("Entry", "文本编辑"))
            self.btn4.setText(_translate("Entry", "便笺"))
            self.btn5.setText(_translate("Entry", "绘图"))
            self.btn6.setText(_translate("Entry", "扫雷"))
            if globalVars.alarm:
                self.btn_alarm.setText(_translate("Entry", "关闭时间提醒"))
            else:
                self.btn_alarm.setText(_translate("Entry", "打开时间提醒"))
            self.menuFile.setTitle(_translate("Entry", "File"))
            self.actionImport.setText(_translate("Entry", "Import"))
            self.actionExit.setText(_translate("Entry", "Exit"))
            self.actionHelp.setText(_translate("Entry", "Help"))
            self.btn6.setVisible(True)
            self.feedback.clear()
            self.feedback.setText("该准备收拾行李了!")
            self.btn_alarm.setText("音乐播放器")
            self.schedule_label.setVisible(False)
            self.schedule.setVisible(False)
            self.teacher_label.setVisible(False)
            self.teacher.setVisible(False)
            self.course.setMinimumSize(QtCore.QSize(281, 300))
            self.course_label.setText("提醒事项")
            self.course.setText("明天8:00起床\n下午3:55的航班\n晚上公司年会")
            self.course.setStyleSheet(
                '''
                    color: yellow;
                    border:4px solid #ccc;
                    background:coral;
                '''
            )
            try:
                self.btn1.clicked.disconnect(self.face_register)
                self.btn2.clicked.disconnect(self.random_register)
                self.btn3.clicked.disconnect(self.myplot)
                self.btn4.clicked.disconnect(self.whiteBoard)
                self.btn5.clicked.disconnect(self.system_monitor)
                self.btn6.clicked.disconnect(self.standby)
                self.btn_alarm.clicked.disconnect(self.alarm)
            except Exception as e:
                print(e)
            self.btn1.clicked.connect(self.browser)
            self.btn2.clicked.connect(self.calculate)
            self.btn3.clicked.connect(self.word)
            self.btn4.clicked.connect(self.note)
            self.btn5.clicked.connect(self.painter)
            self.btn6.clicked.connect(self.minesweep)
            self.btn_alarm.clicked.connect(self.media)
            QtCore.QMetaObject.connectSlotsByName(self)
            globalVars.alarm = False
        else:
            print("该功能还未实现，敬请期待．")

    def face_register(self):
        win_register.show()

    def random_register(self):
        win_random.show()

    def myplot(self):
        self.plot.exec()

    def whiteBoard(self):
        win_paint.show()

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

    def browser(self):
        bs = Browser()
        bs.show()

    def calculate(self):
        ca = Calculator()
        ca.show()

    def note(self):
        existing_notes = session.query(Note).all()
        if len(existing_notes) == 0:
            Notes()
        else:
            for note in existing_notes:
                Notes(obj=note)

    def painter(self):
        win_paint.show()

    def word(self):
        wo = WordProcessor()
        wo.show()

    def minesweep(self):
        self.proc = subprocess.Popen(['python', 'app/minesweeper/minesweeper.py'], shell=False)

    def media(self):
        self.proc2 = subprocess.Popen(['python', 'app/mediaplayer/mediaplayer.py'], shell=False)


def timer2(timer_signal: QtCore.pyqtSignal(str)):
    t_ = time.time()
    while True:
        t = time.time()
        if t - t_ >= 1:
            t_ = t
            timer_signal.emit(TimeStamp2Time(t))


def timeout(t: float, signal: QtCore.pyqtSignal()):
    time.sleep(t)
    signal.emit()


'''''''''''''''''''''''''''''''''''''''
UI_wrapper for Ui_Register
Function:
1. timer -- show_time
2. read_file -- read from and write to xlsx, create new column
3. show_images -- show detections in real time
4. count down -- set duration for register
5. show log
'''''''''''''''''''''''''''''''''''''''


class Register(QtWidgets.QMainWindow, Ui_Register):
    global globalVars
    time_signal = QtCore.pyqtSignal(str)
    detect_signal = QtCore.pyqtSignal(np.ndarray, list)
    timeout_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.newCol = True
        self.directory = ''
        self.running = False

        self.student_list = []
        self.student_features = []

        self.logs = []

        self.init()

        self.time_signal.connect(self.update_time)
        self.detect_signal.connect(self.detect_callback)
        self.timeout_signal.connect(self.timeout_callback)

        # set front style
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("src/classroom.jpeg").scaled(979, 659)))
        self.setPalette(palette)

        self.new_line.setStyleSheet(
            '''
            /*checkbox样式设置*/
            QCheckBox::indicator { 
                width: 20px;
                height: 20px;
            }
            /*未选中*/
            QCheckBox::indicator::unchecked {   
                image: url(./icon/icon-unchecked.png);
            }
            /*选中*/
            QCheckBox::indicator::checked { 
                image: url(./icon/icon-checked.png);
            }
            '''
        )
        self.new_line.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.feedback.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.label_3.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.label_4.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.label_5.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.log.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.output.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )
        self.time.setStyleSheet(
            '''
            background-color:rgba(255,255,255,0.7);
            '''
        )

    def init(self):
        self.new_line.setChecked(True)
        # start my timer
        thread = threading.Thread(target=timer2, args=(self.time_signal,))
        thread.setDaemon(True)
        thread.start()

        self.date = time.strftime("%Y-%m-%d", time.localtime(time.time()))

        self.detector = None

    def load(self):
        # self.fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*)")  # ;;Text Files(*.txt)
        # print(self.fileName)
        # print(fileType)
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        print(self.directory)
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
        print(self.student_list)
        print(self.student_features)
        if self.newCol:
            self.df[self.date] = [False] * len(self.student_list)
            print(self.df)
        self.finish_loading_callback()

    def add_new_column(self):
        self.newCol = self.new_line.isChecked()
        if globalVars.debug:
            print("newCol: ", self.newCol)

    def set_minutes_seconds(self):
        minutes = self.spinBox_min.value()
        seconds = self.spinBox_s.value()
        self.output.setText(f"签到开始，时长{minutes}:{seconds}.")
        thread = threading.Thread(target=timeout, args=(minutes * 60 + seconds, self.timeout_signal))
        thread.daemon = True
        thread.start()

    def timeout_callback(self):
        self.startstop()
        self.output.setText("签到时间结束！已保存")

    def update_time(self, string):
        self.time.setText(string)

    def finish_loading_callback(self):
        self.feedback.setText("Loading finished.")
        self.detector = FaceRecognition(self.student_list, self.student_features, self.detect_signal)
        self.output.setText("签到开始.")

    def detect_callback(self, img, names):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.QtImg = QImage(shrink.data, shrink.shape[1], shrink.shape[0], QImage.Format_RGB888)
        self.image.setPixmap(QPixmap.fromImage(self.QtImg))
        for name in names:
            if name == 'Unknown':
                continue
            idx = self.student_list.index(name)
            print("idx: ", idx)
            flag = not self.df.loc[idx, self.date]
            print(flag)
            self.df.loc[idx, self.date] = True
            if flag:
                self.df.to_excel(excel_writer=self.directory + '/test.xlsx', header=True, index=False)
                self.logManager(f'{name} 签到成功！')

    def logManager(self, string):
        if len(self.logs) > 15:
            self.logs.pop(0)
        self.logs.append(string)
        self.log.setText('\n'.join(self.logs) + '\n\n\n未签到人数：　' + str(len(self.student_list) - len(self.logs)) + '人')

    def startstop(self):
        if self.running:
            self.btn_startstop.setText("结束")
            if self.detector is None:
                return
            self.df.to_excel(excel_writer=self.directory + '/test.xlsx', header=True, index=False)
            self.detector.start(self.detect_signal)
        else:
            self.btn_startstop.setText("开始")
            if self.detector is None:
                return 
            self.detector.stop()
        self.running = not self.running


'''''''''''''''''''''''''''''''''''''''
UI_wrapper for Ui_Random
Function:
1. call the roll -- yes, no, others
2. load file -- student list
3. show pinyin
4. show log
'''''''''''''''''''''''''''''''''''''''


class Random(QtWidgets.QMainWindow, Ui_Random):
    def __init__(self):
        super(Random, self).__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        self.spinBox.setValue(10)
        self.count = 10
        self.fileName = None
        self.p = Pinyin()

        self.logs = []
        self.student_list = []
        self.slm = QtCore.QStringListModel()  # 创建mode
        self.slm.setStringList(self.logs)  # 将数据设置到model
        self.listView.setModel(self.slm)  # 绑定 listView 和 model

        self.date = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    def start_call(self):
        if len(self.student_list) == 0:
            return
        self.count = self.spinBox.value()
        if self.count <= 0:
            return
        self.names = []
        while len(self.names) != self.count:
            num = random.randint(0, len(self.student_list) - 1)
            if num in self.names:
                continue
            self.names.append(num)
        self.name.setText(self.student_list[self.names[0]])
        result = self.p.get_pinyin(self.student_list[self.names[0]], tone_marks='marks')
        s = result.split('-')
        result = s[0].capitalize() + ' ' + ''.join(s[1:]).capitalize()
        self.pinyin.setText(result)
        self.index = 0

    def import_list(self):
        self.fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                        "Excel File (*.xlsx);;Excel File (*.xls)")  # ;;Text Files(*.txt)
        print(self.fileName)
        print(fileType)
        self.df: pd.DataFrame = pd.read_excel(self.fileName)
        for row in self.df.iteritems():
            self.student_list = list(row[1])
            print(self.student_list)
            break
        self.df[self.date] = [None] * len(self.student_list)
        print(self.df)
        count = self.slm.rowCount()
        self.slm.insertRow(count)
        index = self.slm.index(count, 0)
        self.slm.setData(index, f'导入成功!', QtCore.Qt.DisplayRole)
        self.df.to_excel(excel_writer=self.fileName, header=True, index=False)

    def yes(self):
        if len(self.student_list) == 0:
            return
        self.df.loc[self.names[self.index], self.date] = True
        count = self.slm.rowCount()
        self.slm.insertRow(count)
        index = self.slm.index(count, 0)
        self.slm.setData(index, f'{self.student_list[self.names[self.index]]} 签到成功!', QtCore.Qt.DisplayRole)
        self.index += 1
        if self.index == self.count:
            count = self.slm.rowCount()
            self.slm.insertRow(count)
            index = self.slm.index(count, 0)
            self.slm.setData(index, '本次随机点名完成!', QtCore.Qt.DisplayRole)
            self.df.to_excel(excel_writer=self.fileName, header=True, index=False)
            self.name.clear()
            self.pinyin.clear()
            return
        self.name.setText(self.student_list[self.names[self.index]])
        result = self.p.get_pinyin(self.student_list[self.names[self.index]], tone_marks='marks')
        s = result.split('-')
        result = s[0].capitalize() + ' ' + ''.join(s[1:]).capitalize()
        self.pinyin.setText(result)

    def no(self):
        if len(self.student_list) == 0:
            return
        self.df.loc[self.names[self.index], self.date] = False
        count = self.slm.rowCount()
        self.slm.insertRow(count)
        index = self.slm.index(count, 0)
        self.slm.setData(index, f'{self.student_list[self.names[self.index]]} 签到失败!', QtCore.Qt.DisplayRole)
        self.index += 1
        if self.index == self.count:
            count = self.slm.rowCount()
            self.slm.insertRow(count)
            index = self.slm.index(count, 0)
            self.slm.setData(index, '本次随机点名完成!', QtCore.Qt.DisplayRole)
            self.df.to_excel(excel_writer=self.fileName, header=True, index=False)
            self.name.clear()
            self.pinyin.clear()
            return
        self.name.setText(self.student_list[self.names[self.index]])
        result = self.p.get_pinyin(self.student_list[self.names[self.index]], tone_marks='marks')
        s = result.split('-')
        result = s[0].capitalize() + ' ' + ''.join(s[1:]).capitalize()
        self.pinyin.setText(result)

    def others_yes(self):
        if len(self.student_list) == 0:
            return
        for i in range(0, len(self.df)):
            if self.df.loc[i, self.date] is None:
                self.df.loc[i, self.date] = True
        count = self.slm.rowCount()
        self.slm.insertRow(count)
        index = self.slm.index(count, 0)
        self.slm.setData(index, '所有学生签到完成!', QtCore.Qt.DisplayRole)
        self.df.to_excel(excel_writer=self.fileName, header=True, index=False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win_entry = Entry()
    win_register = Register()
    win_random = Random()
    win_paint = Paint()
    win_entry.show()
    sys.exit(app.exec_())
