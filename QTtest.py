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
        self.robot_button.clicked.connect(self.robotswitch)
        self.lamp_switch.clicked.connect(self.lampswitch)


    def all_stop(self):
        self.ProcessCam.stop()  # 影像讀取功能關閉
        self.camera_state = False
        self.camera_status.setStyleSheet("background-color : red;\n""border-radius: 85px;")

        self.ProcessRobot.stop()
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

        self.ProcessRobot.start()
        self.robot_state = True
        self.robot_status.setStyleSheet("background-color : green;\n""border-radius: 85px;")

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
        else:
            self.ProcessRobot.client.write_registers(40002, [0, 0], unit=1)
        if self.ProcessRobot.client.read_holding_registers(40005, 1, unit=1).registers == [3]:
            self.warning_display.setText("[Error] 吸取工件失敗")
            self.robot_state = False
            self.robot_status.setStyleSheet("background-color : yellow;\n""border-radius: 85px;")
            self.ProcessRobot.stop()
            self.ProcessRobot.client.write_registers(40004, [0, 1], unit=1)

    def showData(self, img):
        """ 顯示攝影機的影像 """
        self.Ny, self.Nx, _ = img.shape  # 取得影像尺寸

        # 建立 Qimage 物件 (灰階格式)
        # qimg = QtGui.QImage(img[:,:,0].copy().data, self.Nx, self.Ny, QtGui.QImage.Format_Indexed8)

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
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_EXPOSURE, -6)  # 曝光
        self.cam.set(cv2.CAP_PROP_FOCUS, 65)  # 焦距
        # cap.set(cv2.CAP_PROP_SETTINGS, 0)  # 相機設定介面
        # 其他參數和設定
        self.startTime = 0
        num = 0
        self.reg_x0, self.reg_y0, self.reg_h, self.reg_w = [105, 220, 250, 500]  # 辨識區域
        self.detect_on_off = False
        self.detecting = False
        self.save_pic = False
        self.finish = False
        self.top_green = [57, 46, 41]
        self.bot_green = [125, 133, 109]

        self.focus = []
        self.tray = 0

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
            ret, img = self.cam.read()  # 讀取影像
            clear_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if ret:
                current_frame = clear_frame.copy()  # 避免直接在原始畫面上作圖
                # 框出辨識區域
                cmr_region = clear_frame[self.reg_y0:self.reg_y0 + self.reg_h, self.reg_x0:self.reg_x0 + self.reg_w]
                gray_cmr_region = cv2.cvtColor(cmr_region, cv2.COLOR_BGR2GRAY)  # 灰階
                region_list = np.int0([[self.reg_x0, self.reg_y0], [self.reg_x0 + self.reg_w, self.reg_y0], [self.reg_x0 + self.reg_w, self.reg_y0 + self.reg_h],
                                       [self.reg_x0, self.reg_y0 + self.reg_h]])

                '''邊緣偵測'''
                blur = cv2.GaussianBlur(gray_cmr_region, (5, 5), 0)
                canny = cv2.Canny(blur, 20, 160)  # , 20, 160)
                canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)

                '''組合圖片'''
                cur_reg = np.hstack((canny, cmr_region))

                '''偵測零件'''
                # 由上往下
                # 設定上辨識線

                top_line = clear_frame[int(self.reg_y0), int(self.reg_x0):int(self.reg_x0 + self.reg_w)]
                top_mean = np.int0(np.mean(top_line, axis=0))
                top_color = (int(top_mean[0]), int(top_mean[1]), int(top_mean[2]))
                # 設定下辨識線

                bot_line = clear_frame[int(self.reg_y0 + self.reg_h), int(self.reg_x0):int(self.reg_x0 + self.reg_w)]
                bot_mean = np.int0(np.mean(bot_line, axis=0))
                bot_color = (int(bot_mean[0]), int(bot_mean[1]), int(bot_mean[2]))

                # 上辨識線偵測到非綠色的 就開始辨識
                if self.detect_on_off:
                    if not self.detecting:
                        # 開始偵測
                        top_err0 = abs(top_mean[0] - self.top_green[0])
                        top_err1 = abs(top_mean[1] - self.top_green[1])
                        top_err2 = abs(top_mean[2] - self.top_green[2])
                        if (top_err0 > 15 and top_err1 > 15 and top_err2 > 15):
                            cv2.drawContours(current_frame, [region_list], -1, (0, 0, 255), 2)  # 外框變紅色表示偵測中
                            cv2.line(current_frame, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                                     [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)
                            cv2.line(canny, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                                     [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)
                            self.startTime = time.time()  # 開始計時
                            # 生成資料夾 如果資料夾已經存在會有錯誤
                            if self.save_pic:
                                folder_name = f"test"
                                folder_path = "C:/Users/ccu/Documents/oCam"
                                path = os.path.join(folder_path, folder_name)
                                os.mkdir(path)
                            self.detecting = True
                        # 閒置
                        else:
                            cv2.drawContours(current_frame, [region_list], -1, (0, 255, 0), 2)  # 外框變綠色表示閒置
                            cv2.line(current_frame, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                                     [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)
                            cv2.line(canny, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                                     [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)
                    else:
                        # 結束偵測
                        top_err0 = abs(top_mean[0] - self.top_green[0])
                        top_err1 = abs(top_mean[1] - self.top_green[1])
                        top_err2 = abs(top_mean[2] - self.top_green[2])
                        bot_err0 = abs(bot_mean[0] - self.bot_green[0])
                        bot_err1 = abs(bot_mean[1] - self.bot_green[1])
                        bot_err2 = abs(bot_mean[2] - self.bot_green[2])
                        if (top_err0 < 15 and top_err1 < 15 and top_err2 < 15) and (
                                bot_err0 < 15 and bot_err1 < 15 and bot_err2 < 15) or self.finish:
                            cv2.drawContours(current_frame, [region_list], -1, (0, 255, 0), 2)  # 外框變綠色表示閒置
                            curTime = time.time() - self.startTime
                            if self.save_pic:
                                print('第%.0F次 花費時間: %.2F, Frams: %.0F' % (self.tray, curTime, num))
                            else:
                                print('花費時間: %.2F, Frams: %.0F' % (curTime, num))
                            # print(np.mean(self.focus))
                            self.startTime = 0
                            num = 0
                            self.detecting = False
                            self.finish = False
                        # 偵測中
                        else:
                            cv2.drawContours(current_frame, [region_list], -1, (0, 0, 255), 2)  # 外框變紅色表示偵測中
                            cv2.line(current_frame, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                                     [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)
                            cv2.line(canny, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                                     [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)

                            curTime = time.time() - self.startTime
                            self.focus.append(self.cam.get(cv2.CAP_PROP_self.focus))
                            num += 1
                            if self.save_pic:
                                name = 'cur_reg' + f'{num}'.rjust(3, '0')
                                cv2.imwrite(f"C:/Users/ccu/Documents/oCam/test/{name}.jpg", cmr_region)  # 把當前的完成圖儲存
                else:
                    cv2.drawContours(current_frame, [region_list], -1, (0, 255, 255), 2)  # 外框變黃色表示閒置
                    cv2.line(current_frame, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                             [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)
                    cv2.line(canny, [self.reg_x0, int(self.reg_y0 + 0.5 * self.reg_h)],
                             [self.reg_x0 + self.reg_w, int(self.reg_y0 + 0.5 * self.reg_h)], (255, 255, 0), 1)

                if self.save_pic:
                    # 顯示特效表示開啟存圖模式
                    cv2.circle(current_frame, [int(self.reg_x0 + 10), self.reg_y0 - 15], 5, (0, 0, 255), -1)
                    cv2.putText(current_frame, 'rec', (int(self.reg_x0 + 20), self.reg_y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2)


                self.rawdata.emit(current_frame)  # 發送影像
            else:  # 例外處理
                print("Warning!!!")
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
