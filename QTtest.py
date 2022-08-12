from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from MainWindow import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

import numpy as np
import time
import cv2
import pyfirmata
from pymodbus.client.sync import ModbusTcpClient
import os


# R20000 成品放置數量
# R20001 成品是否到達指定位置
# R20002 是否吸取成品成功
# R20003 tray數量
# R20004 伺服開關
# R20005 緊急開關
class Robot:
    def __init__(self):
        HOST = '192.168.0.1'
        PORT = 502
        self.client = ModbusTcpClient(host=HOST, port=PORT)

    def start(self):
        self.client.write_registers(30450, [0, 1], unit=1)
        time.sleep(0.5)
        self.client.write_registers(30410, [0, 1], unit=1)
        time.sleep(0.5)

    def stop(self):
        self.client.write_registers(30412, [0, 1], unit=1)
        time.sleep(0.5)
        self.client.write_registers(30412, [0, 0], unit=1)
        time.sleep(0.5)

    def reset(self):
        self.client.write_registers(40000, [0, 1], unit=1)
        self.client.write_registers(40004, [0, 1], unit=1)
        self.client.write_registers(30414, [0, 1], unit=1)
        self.client.write_registers(30424, [0, 1], unit=1)
        time.sleep(0.5)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        """ 初始化
            - 物件配置
            - 相關屬性配置
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.viewData.setScaledContents(True)
        self.track_state = False
        self.camera_state = False
        self.robot_state = False
        self.lamp_state = False
        self.frame_num = 0
        self.NG_num = np.loadtxt("NG_num.txt", dtype=int)
        # 設定手臂
        self.ProcessRobot = Robot()
        if not self.ProcessRobot.client.connect():
            self.warning_display.setText("[Error] Fail to connect to robot")
        else:
            self.warning_display.setText("[Success] Connected to robot")
            self.ProcessRobot.client.write_registers(40000, [0, 1], unit=1)
            self.ProcessRobot.client.write_registers(40004, [0, 1], unit=1)
        # 設定相機功能
        self.ProcessCam = Camera()  # 建立相機物件
        # self.ProcessCam.board.digital[8].write(1)

        if self.ProcessCam.connect:
            # 連接影像訊號 (rawdata) 至 getRaw()
            self.ProcessCam.rawdata.connect(self.getRaw)  # 槽功能：取得並顯示影像
            # 攝影機啟動按鈕的狀態：ON
        self.ProcessCam.board.digital[9].write(1)
        self.ProcessCam.board.digital[8].write(1)
        # 連接按鍵
        self.Camera_switch.clicked.connect(self.switchCam)
        self.track.clicked.connect(self.track_switch)
        self.Open_all.clicked.connect(self.open_alls)
        self.emergency.clicked.connect(self.all_stop)
        self.stop_all.clicked.connect(self.all_close)
        self.ready.clicked.connect(self.ready_Process)
        self.robot_button.clicked.connect(self.robotswitch)
        self.lamp_switch.clicked.connect(self.lampswitch)

    def ready_Process(self):
        self.ProcessRobot.client.write_registers(40010, [0, 0], unit=1)
        time.sleep(0.1)
        self.ProcessRobot.client.write_registers(40008, [0, 1], unit=1)

    def all_stop(self):
        self.ProcessCam.stop()  # 影像讀取功能關閉
        self.camera_state = False
        self.camera_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")

        self.ProcessRobot.client.write_registers(40010, [0, 1], unit=1)
        self.robot_state = False
        self.robot_status.setStyleSheet("background-color : yellow;\n""border-radius: 85px;")

        self.ProcessCam.board.digital[8].write(1)
        time.sleep(0.1)
        self.track_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")
        self.track_state = False

    def all_close(self):
        self.ProcessCam.stop()  # 影像讀取功能關閉
        self.camera_state = False
        self.camera_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")

        self.ProcessRobot.stop()
        self.ProcessRobot.reset()
        self.ProcessRobot.client.write_registers(40010, [0, 0], unit=1)
        self.ProcessRobot.client.write_registers(40008, [0, 0], unit=1)
        self.robot_state = False
        self.robot_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")

        self.ProcessCam.board.digital[8].write(1)
        time.sleep(0.1)
        self.track_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")
        self.track_state = False
        sys.exit(app.exec_())

    def open_alls(self):
        self.ProcessCam.open()
        self.ProcessCam.start()
        self.camera_state = True
        self.camera_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")
        if not self.ProcessRobot.client.read_holding_registers(40011, 1, unit=1).registers[0]:
            self.ProcessRobot.start()
            self.robot_state = True
            self.robot_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")
        else:
            self.robot_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")
            self.warning_display.setText("[Warning] 手臂處於急停模式")

        self.ProcessCam.board.digital[8].write(0)
        time.sleep(0.1)
        self.track_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")
        self.track_state = True

    def switchCam(self):
        if self.ProcessCam.connect & (not self.camera_state):  # 判斷攝影機是否可用
            self.ProcessCam.open()  # 影像讀取功能開啟
            self.ProcessCam.start()  # 在子緒啟動影像讀取
            self.camera_state = True
            self.camera_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")

        else:
            self.ProcessCam.stop()  # 影像讀取功能關閉
            self.camera_state = False
            self.camera_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")

    def robotswitch(self):
        if self.ProcessRobot.client.connect() & (not self.robot_state):
            self.ProcessRobot.start()

            self.robot_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")
            self.robot_state = True
        else:
            self.ProcessRobot.stop()
            self.ProcessRobot.reset()
            self.robot_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")
            self.robot_state = False

    def lampswitch(self):
        if self.lamp_state:
            self.lamp_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")
            self.ProcessCam.board.digital[9].write(1)
            self.lamp_state = False
        else:
            self.lamp_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")
            self.ProcessCam.board.digital[9].write(0)
            self.lamp_state = True

    def track_switch(self):
        if self.track_state:
            self.ProcessCam.board.digital[8].write(1)
            time.sleep(0.1)
            self.track_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")
            self.track_state = False
        else:
            self.ProcessCam.board.digital[8].write(0)
            time.sleep(0.1)
            self.track_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")
            self.track_state = True

    def getRaw(self, data):  # data 為接收到的影像
        """ 取得影像 """
        self.showData(data)  # 將影像傳入至 showData()
        if self.ProcessCam.g & self.lamp_state:
            self.warning_display.setText("[Error] 燈光未開")
        if not self.ProcessCam.g & self.lamp_state:
            self.warning_display.setText("")
        if not self.ProcessRobot.client.connect():
            self.warning_display.setText("[Error] Fail to connect to robot")
        if (not self.ProcessCam.r) & self.robot_state:
            self.ProcessRobot.client.write_registers(40002, [0, 1], unit=1)
            if self.ProcessCam.error:
                self.all_stop()
                self.warning_display.setText("[Warning] 檢測到不良品")
                self.NG_num += 1
                self.NG.setText(str(self.NG_num))
                np.savetxt("NG_num.txt", np.array(self.NG_num))
        else:
            self.ProcessRobot.client.write_registers(40002, [0, 0], unit=1)
        if self.ProcessRobot.client.read_holding_registers(40005, 1, unit=1).registers == [3]:
            self.warning_display.setText("[Error] 吸取工件失敗")
            self.robot_state = False
            self.robot_status.setStyleSheet("background-color : yellow;\n""border-radius: 85px;")
            self.ProcessRobot.stop()
            self.ProcessRobot.client.write_registers(40004, [0, 0], unit=1)
        if self.ProcessRobot.client.read_holding_registers(40005, 1, unit=1).registers == [2]:
            self.warning_display.setText("[Error] 吸取Tray盤失敗")
            self.robot_state = False
            self.robot_status.setStyleSheet("background-color : yellow;\n""border-radius: 85px;")
            self.ProcessRobot.stop()
            self.ProcessRobot.client.write_registers(40004, [0, 0], unit=1)
        if self.ProcessRobot.client.read_holding_registers(40000, 1, unit=1).registers <= [8]:
            num = self.ProcessRobot.client.read_holding_registers(40000, 1, unit=1).registers[0] + (
                        self.ProcessRobot.client.read_holding_registers(40006, 1, unit=1).registers[0] * 8)
            self.total.setText(str(num))
        else:
            num = 8 + (self.ProcessRobot.client.read_holding_registers(40006, 1, unit=1).registers[0] * 8)
            self.total.setText(str(num))

    def showData(self, img):
        """ 顯示攝影機的影像 """
        self.Ny, self.Nx, _ = img.shape  # 取得影像尺寸

        # 建立 Qimage 物件 (RGB格式)
        qimg = QImage(img.data, self.Nx, self.Ny, QImage.Format_RGB888)

        # viewData 的顯示設定
        self.viewData.setScaledContents(True)  # 尺度可變
        ### 將 Qimage 物件設置到 viewData 上
        self.viewData.setPixmap(QPixmap.fromImage(qimg))
        # Frame Rate 計算並顯示到狀態欄上
        if self.frame_num == 0:
            self.time_start = time.time()
        if self.frame_num >= 0:
            self.frame_num += 1
            self.t_total = time.time() - self.time_start
            if self.frame_num % 100 == 0:
                self.frame_rate = float(self.frame_num) / self.t_total

    def closeEvent(self, event):
        """ 視窗應用程式關閉事件 """
        if self.ProcessCam.running:
            self.ProcessCam.close()  # 關閉攝影機
            time.sleep(1)
            self.ProcessCam.terminate()  # 關閉子緒
        QApplication.closeAllWindows()  # 關閉所有視窗


class Camera(QtCore.QThread):  # 繼承 QtCore.QThread 來建立 Camera 類別
    rawdata = QtCore.pyqtSignal(np.ndarray)  # 建立傳遞信號，需設定傳遞型態為 np.ndarray

    def __init__(self, parent=None):
        """ 初始化
            - 執行 QtCore.QThread 的初始化
            - 建立 cv2 的 VideoCapture 物件
            - 設定屬性來確認狀態
              - self.connect：連接狀態
              - self.running：讀取狀態
        """
        # 將父類初始化
        super().__init__(parent)
        # 建立 cv2 的攝影機物件
        # 設定攝影機 把自動調整的寫死
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -6)  # 曝光
        self.cap.set(cv2.CAP_PROP_FOCUS, 65)  # 焦距
        # 其他參數和設定
        self.startTime = 0  # 料盤進入時間
        self.curTime = 0  # 料盤進入時間
        self.num = 0  # 總畫面數
        self.detecting = False  # 料盤是否進入
        self.save_pic = False  # 是否儲存偵測畫面
        self.finish = False  # 是否完成偵測
        self.hash_val = [None] * 3  # 哈希值
        # 辨識區域相關參數
        self.reg_x0, self.reg_y0, self.reg_h, self.reg_w = [105, 225, 250, 500]  # 辨識區域
        self.region_list = np.int0(
            [[self.reg_x0, self.reg_y0], [self.reg_x0 + self.reg_w, self.reg_y0],
             [self.reg_x0 + self.reg_w, self.reg_y0 + self.reg_h], [self.reg_x0, self.reg_y0 + self.reg_h]])
        self.top_green = [56, 62, 31]  # 上框線平均顏色(綠色)
        self.bot_green = [140, 151, 131]  # 下框線平均顏色(綠色)

        # 檢查
        self.white_th = [95.5, 95.5, 125.5]  # 避免剛好某一幀白點數量剛好等於閥值 導致出問題 所以刻意加上小數
        self.count_max = [10, 8, 9]  # 鉚釘數量最大值
        self.white_max = [0, 0, 0]  # 白點最大值
        self.pass_count = [0, 0, 0]  # 鉚釘通過計數器(輪廓)
        self.time_count = [0, 0, 0]  # 鉚釘通過計數器(時間)
        self.loss_count = [0, 0, 0]  # 異常鉚釘數量
        self.tray = 0  # 料盤通過數量

        # 辨識框寬度
        self.normal = np.array([[135, 185], [245, 300], [325, 380]])  # 普通鉚釘
        self.spetial = np.array([[260, 315], [305, 360], [220, 275]])  # 特例鉚釘 1.中間 2.右邊 3.中間
        self.tl = 35  # 上線
        self.ml = 75  # 中線
        self.bl = 95  # 下線
        self.cut_left = [21, 56, 90, 123, 156, 168, 186, 223, 256, 290]  # 左邊鉚釘截圖幀數
        self.cut_middle = [21, 34, 68, 96, 135, 207, 230, 270]  # 中間鉚釘截圖幀數
        self.cut_right = [56, 90, 123, 156, 168, 187, 223, 256, 290]  # 右邊鉚釘截圖幀數
        self.error = False

        # 判斷攝影機是否正常連接
        if self.cam is None or not self.cam.isOpened():
            self.connect = False
            self.running = False
        else:
            self.connect = True
            self.running = False

        self.r = True
        self.g = False
        self.board = pyfirmata.Arduino('COM4')
        self.it = pyfirmata.util.Iterator(self.board)
        self.board.digital[7].mode = pyfirmata.INPUT
        self.board.digital[6].mode = pyfirmata.INPUT
        self.it.start()

    def run(self):
        """ 執行多執行緒
            - 讀取影像
            - 發送影像
            - 簡易異常處理
        """
        # 當正常連接攝影機才能進入迴圈
        while self.running and self.connect:
            ret, img = self.cpa.read()  # 讀取影像
            clear_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if ret:
                current_frame = clear_frame.copy()  # 避免直接在原始畫面上作圖
                # 框出辨識區域
                cmr_region = clear_frame[self.reg_y0:self.reg_y0 + self.reg_h, self.reg_x0:self.reg_x0 + self.reg_w]
                gray_cmr_region = cv2.cvtColor(cmr_region, cv2.COLOR_BGR2GRAY)  # 灰階
                '''邊緣偵測'''
                blur = cv2.GaussianBlur(gray_cmr_region, (5, 5), 0)
                canny = cv2.Canny(blur, 20, 160)  # , 20, 160)
                canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)

                # canny = cv2.Canny(gray_cmr_region, 20, 160)  # , 20, 160)
                # canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
                '''偵測零件'''
                # 設定上框線
                top_line = clear_frame[int(self.reg_y0), int(self.reg_x0):int(self.reg_x0 + self.reg_w)]
                top_mean = np.int0(np.mean(top_line, axis=0))
                top_color = (int(top_mean[0]), int(top_mean[1]), int(top_mean[2]))
                # 設定下框線
                bot_line = clear_frame[int(self.reg_y0 + self.reg_h), int(self.reg_x0):int(self.reg_x0 + self.reg_w)]
                bot_mean = np.int0(np.mean(bot_line, axis=0))
                bot_color = (int(bot_mean[0]), int(bot_mean[1]), int(bot_mean[2]))

                if not detecting:  # 沒有在偵測
                    top_err0 = abs(top_mean[0] - self.top_green[0])
                    top_err1 = abs(top_mean[1] - self.top_green[1])
                    top_err2 = abs(top_mean[2] - self.top_green[2])
                    if top_err0 > 10 and top_err1 > 10 and top_err2 > 10:  # 開始偵測的條件
                        cv2.drawContours(current_frame, [self.region_list], -1, (0, 0, 255), 2)  # 外框變紅色表示開始偵測
                        self.startTime = time.time()  # 開始計時
                        self.tray += 1
                        detecting = True
                    else:  # 閒置
                        cv2.drawContours(current_frame, [self.region_list], -1, (0, 255, 0), 2)  # 外框變綠色表示閒置
                else:  # 偵測中
                    top_err0 = abs(top_mean[0] - self.top_green[0])
                    top_err1 = abs(top_mean[1] - self.top_green[1])
                    top_err2 = abs(top_mean[2] - self.top_green[2])
                    bot_err0 = abs(bot_mean[0] - self.bot_green[0])
                    bot_err1 = abs(bot_mean[1] - self.bot_green[1])
                    bot_err2 = abs(bot_mean[2] - self.bot_green[2])
                    # 結束偵測的條件
                    if (
                            top_err0 < 10 and top_err1 < 10 and top_err2 < 10 and bot_err0 < 10 and bot_err1 < 10 and bot_err2 < 10) \
                            or self.finish or self.curTime >= 11:
                        cv2.drawContours(current_frame, [self.region_list], -1, (0, 255, 0), 2)  # 外框變綠色表示閒置
                        self.curTime = time.time() - self.startTime
                        print('第' + str(self.tray).rjust(2,
                                                          ' ') + '次: 花費時間:%.2F秒, %.0F frams, 鉚釘數量:%.0F/10,%.0F/8,%.0F/9' % (
                                  self.curTime, self.num, self.pass_count[0], self.pass_count[1], self.pass_count[2]))
                        # 重置
                        self.white_max = [0, 0, 0]
                        self.startTime = 0
                        self.curTime = 0
                        self.num = 0
                        self.hash_val = [None] * 3
                        self.white_max = [0, 0, 0]
                        self.pass_count = [0, 0, 0]
                        self.time_count = [0, 0, 0]
                        self.loss_count = [0, 0, 0]
                        self.finish = False
                        self.save_pic = False
                        self.detecting = False
                    else:  # 偵測中
                        cv2.drawContours(current_frame, [self.region_list], -1, (0, 0, 255), 2)  # 外框變紅色表示偵測中
                        '''檢查鉚釘'''
                        # 改變辨識框區域
                        if self.num < 28:
                            check = np.array(
                                [[[self.normal[0, 0], self.tl], [self.normal[0, 1], self.bl]],
                                 [[self.spetial[0, 0], self.tl], [self.spetial[0, 1], self.bl]],
                                 [[self.normal[2, 0], self.tl], [self.normal[2, 1], self.bl]]])
                        elif 175 < self.num <= 195:
                            check = np.array(
                                [[[self.normal[0, 0], self.tl], [self.normal[0, 1], self.bl]],
                                 [[self.normal[1, 0], self.tl], [self.normal[1, 1], self.bl]],
                                 [[self.spetial[1, 0], self.tl], [self.spetial[1, 1], self.bl]]])
                        elif 195 < self.num <= 220:
                            check = np.array(
                                [[[self.normal[0, 0], self.tl], [self.normal[0, 1], self.bl]],
                                 [[self.spetial[2, 0], self.tl], [self.spetial[2, 1], self.bl]],
                                 [[self.normal[2, 0], self.tl], [self.normal[2, 1], self.bl]]])
                        else:
                            check = np.array(
                                [[[self.normal[0, 0], self.tl], [self.normal[0, 1], self.bl]],
                                 [[self.normal[1, 0], self.tl], [self.normal[1, 1], self.bl]],
                                 [[self.normal[2, 0], self.tl], [self.normal[2, 1], self.bl]]])
                        # 改變辨識框大小
                        if self.num >= 165:
                            self.ml = 85
                        else:
                            self.ml = 75
                        ##### 用邊緣偵測判斷三個辨識區域 #####
                        for i in range(check.shape[0]):
                            # 記錄白點
                            h = self.ml - self.tl
                            w = check[i, 1, 0] - check[i, 0, 0]
                            white = 0
                            for y in range(h):
                                for x in range(w):
                                    if canny[self.tl + y, check[i, 0, 0] + x].all():
                                        white += 1
                            # 如果偵測區域的白點數量開始遞減時 偵測到的鉚釘數量+1
                            if self.white_max[i] != self.white_th[i] and self.pass_count[i] != self.count_max[
                                i] and self.num < 295:
                                # 如果白點數量遞減且大於閥值
                                if white - self.white_max[i] < 0 and white > self.white_th[i]:
                                    self.pass_count[i] += 1
                                    self.white_max[i] = self.white_th[i]  # 把最大值取代成閥值以結束偵測鉚釘的狀態
                                else:
                                    # 更新最大白點數量
                                    self.white_max[i] = white
                            # 截圖過後 白點數量小於閥值時重置最大白點數量
                            elif white < self.white_th[i]:
                                self.white_max[i] = white
                        ##### 用時間判斷三個辨識區域 #####
                        if self.time_count[0] < self.count_max[0]:
                            # 截圖後過6幀更新鉚釘數量
                            if self.num == (self.cut_left[self.time_count[0]] + 6):
                                self.time_count[0] += 1
                                if self.time_count[0] - self.pass_count[0] - self.loss_count[0] != 0:
                                    self.loss_count[0] += 1
                                    self.error = True
                                    print('左邊第' + str(self.time_count[0]) + '顆鉚釘異常')

                        if self.time_count[1] < self.count_max[1]:
                            # 截圖後過6幀更新鉚釘數量
                            if self.num == (self.cut_middle[self.time_count[1]] + 6):
                                self.time_count[1] += 1
                                if self.time_count[1] - self.pass_count[1] - self.loss_count[1] != 0:
                                    self.loss_count[1] += 1
                                    self.error = True
                                    print('中間第' + str(self.time_count[1]) + '顆鉚釘異常')

                        if self.time_count[2] < self.count_max[2]:
                            # 截圖後過6幀更新鉚釘數量
                            if self.num == (self.cut_right[self.time_count[2]] + 6):
                                self.time_count[2] += 1
                                if self.time_count[2] - self.pass_count[2] - self.loss_count[2] != 0:
                                    self.loss_count[2] += 1
                                    self.error = True
                                    print('右邊第' + str(self.time_count[2]) + '顆鉚釘異常')
                        '''結束檢查鉚釘'''
                        # 當前幀數
                        cv2.putText(current_frame, str(self.num),
                                    (int(self.reg_x0 + 10), self.reg_y0 + self.reg_h - 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        # 比對結果
                        cv2.putText(current_frame, 'Rivet', (int(self.reg_x0 + 10), self.reg_y0 + self.bl + 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        for i in range(check.shape[0]):
                            # 鉚釘數量
                            cv2.putText(current_frame, str(self.pass_count[i]),
                                        (int(self.reg_x0 + check[i, 0, 0] / 2 + check[i, 1, 0] / 2),
                                         self.reg_y0 + self.bl + 25),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        # 在畫面標記
                        cv2.line(current_frame, [self.reg_x0, self.reg_y0 + self.tl],
                                 [self.reg_x0 + self.reg_w, self.reg_y0 + self.tl], (0, 255, 255), 1)
                        cv2.line(current_frame, [self.reg_x0, self.reg_y0 + self.ml],
                                 [self.reg_x0 + self.reg_w, self.reg_y0 + self.ml], (255, 0, 255), 1)
                        cv2.line(current_frame, [self.reg_x0, self.reg_y0 + self.bl],
                                 [self.reg_x0 + self.reg_w, self.reg_y0 + self.bl], (255, 255, 0), 1)
                        cv2.rectangle(current_frame, (check[0, 0] + [self.reg_x0, self.reg_y0]),
                                      (check[0, 1] + [self.reg_x0, self.reg_y0]),
                                      (255, 0, 0), 1)
                        cv2.rectangle(current_frame, (check[1, 0] + [self.reg_x0, self.reg_y0]),
                                      (check[1, 1] + [self.reg_x0, self.reg_y0]),
                                      (0, 255, 0), 1)
                        cv2.rectangle(current_frame, (check[2, 0] + [self.reg_x0, self.reg_y0]),
                                      (check[2, 1] + [self.reg_x0, self.reg_y0]),
                                      (0, 0, 255), 1)

                        cv2.line(canny, [0, self.tl], [int(current_frame.shape[1]), self.tl], (0, 255, 255), 1)
                        cv2.line(canny, [0, self.ml], [int(current_frame.shape[1]), self.ml], (255, 0, 255), 1)
                        cv2.line(canny, [0, self.bl], [int(current_frame.shape[1]), self.bl], (255, 255, 0), 1)
                        cv2.rectangle(canny, (check[0, 0]), (check[0, 1]), (255, 0, 0), 1)
                        cv2.rectangle(canny, (check[1, 0]), (check[1, 1]), (0, 255, 0), 1)
                        cv2.rectangle(canny, (check[2, 0]), (check[2, 1]), (0, 0, 255), 1)
                        '''更新時間'''
                        self.curTime = time.time() - self.startTime
                        self.num += 1
                self.rawdata.emit(current_frame)  # 發送影像
            else:  # 例外處理
                self.warning_display.setText("[Error] 相機連線失敗")
                self.connect = False
            self.r = self.board.digital[7].read()
            self.g = self.board.digital[6].read()

    def open(self):
        """ 開啟攝影機影像讀取功能 """
        if self.connect:
            self.running = True  # 啟動讀取狀態

    def stop(self):
        """ 暫停攝影機影像讀取功能 """
        if self.connect:
            self.running = False  # 關閉讀取狀態

    def close(self):
        """ 關閉攝影機功能 """
        if self.connect:
            self.running = False  # 關閉讀取狀態
            time.sleep(1)
            self.cam.release()  # 釋放攝影機


if __name__ == "__main__":
    # board = pyfirmata.Arduino('COM3')
    # it = pyfirmata.util.Iterator(board)
    # it.start()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
