# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import sys
import os
import time
import traceback

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from  myWidget import ImgWidget, TopButton, MyThread, showImg, RowResWidget


class aircraftUI(QWidget):
    def __init__(self, parent=None):
        super(aircraftUI, self).__init__(parent)
        self.setWindowTitle('aircraft detection')
        self.setMinimumSize(1400, 1000)
        self.font = QFont("楷体", 14, QFont.Bold)

        #whole widget
        self.wholeImg = QFrame()
        self.wholeImg.setVisible(False)
        # self.wholeImg.setStyleSheet('''border: 1px solid black''')
        self.w_showImg = ImgWidget()

        w_label = QLabel('全图')
        w_label.setFont(self.font)
        w_label.setAlignment(Qt.AlignCenter)
        w_label.setMaximumHeight(50)

        w_layout = QVBoxLayout()
        w_layout.setContentsMargins(0, 0, 0, 0)
        w_layout.addWidget(self.w_showImg)
        w_layout.addWidget(w_label)
        self.wholeImg.setLayout(w_layout)

        #target widget
        targetWidget = QFrame()
        # targetWidget.setStyleSheet('''border: 1px solid black''')
        self.info_label = QLabel()
        self.info_label.setFont(self.font)
        self.info_label.setMaximumHeight(50)
        self.res_widget = RowResWidget()
        t_label = QLabel('目标样例')
        t_label.setFont(self.font)
        t_label.setAlignment(Qt.AlignCenter)
        t_label.setMaximumHeight(50)
        t_layout = QVBoxLayout()
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.addWidget(self.res_widget)
        t_layout.addWidget(self.info_label)
        t_layout.addWidget(t_label)
        targetWidget.setLayout(t_layout)

        #thumbnail widget
        thumbnailWidget = QFrame()
        # thumbnailWidget.setStyleSheet("""border: 1px solid black""")
        tn_showImg = showImg()
        tn_lable = QLabel('缩略图')
        tn_lable.setFont(self.font)
        tn_lable.setAlignment(Qt.AlignCenter)
        tn_lable.setMaximumHeight(50)
        tn_layout = QVBoxLayout()
        tn_layout.setContentsMargins(0, 0, 0, 0)
        tn_layout.addWidget(tn_showImg)
        tn_layout.addWidget(tn_lable)
        thumbnailWidget.setLayout(tn_layout)

        #signal slot
        self.w_showImg.mysignal.connect(tn_showImg.updatePixmap)

        #right widget
        rightWidget = QWidget()
        r_layout = QVBoxLayout()
        rightWidget.setLayout(r_layout)
        r_layout.addWidget(targetWidget)
        r_layout.addWidget(thumbnailWidget)

        #self layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.wholeImg, 0, 0, 1, 8)
        self.layout.addWidget(rightWidget, 0, 8, 1, 3)

        #self button
        chooseDirButton = TopButton('选择文件')
        nextButton = TopButton('下一张图片')
        chooseDirButton.clicked.connect(self.openDir)
        nextButton.clicked.connect(self.nextImg)
        self.layout.addWidget(chooseDirButton, 1, 3, 1, 1)
        self.layout.addWidget(nextButton, 1, 7, 1, 1)

        #
        self.fileList = []
        self.index = 0

    def openDir(self):
        getFiles, _ = QFileDialog.getOpenFileNames(self, 'Open files', './', 'image files (*.jpg)')
        if not getFiles:
            return
        self.fileList = getFiles
        self.index = 0

    def nextImg(self):
        if self.index < len(self.fileList):
            showImg = self.fileList[self.index]
            self.updateImg(showImg)
            self.index += 1

            self.wholeImg.setVisible(True)
            thread = MyThread(self)
            thread.start_trigger.connect(self.startCompute)
            thread.end_trigger.connect(self.updateInfo)
            thread.start()

    def updateImg(self, showImg):
        self.w_showImg.pixmap = QPixmap(showImg)
        self.w_showImg.updatePixmap(self.w_showImg.pixmap)
        self.res_widget.pixmap = QPixmap(showImg)
        print(self.res_widget.pixmap)

    def updateInfo(self, res_list):
        self.info_label.setText('结果是: {}\n用时:  {:.2f}s'.format(res_list[0], res_list[1]))
        self.w_showImg.getBbox(res_list[2])
        self.res_widget.initBox(res_list[2])

    def startCompute(self):
        self.info_label.setText('正在计算...')

    def excepthook(excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions.
        @param excType exception type
        @param excValue exception value
        @param tracebackobj traceback object
        """
        separator = '-' * 80
        logFile = os.path.join("simple.log")
        notice = \
            """An unhandled exception occurred. Please report the problem\n""" \
            """using the error reporting dialog or via email to <%s>.\n""" \
            """A log has been written to "%s".\n\nError information:\n""" % \
            ("yourmail at server.com", logFile)
        versionInfo = "0.0.1"
        timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

        tbinfofile = StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        try:
            with open(logFile, "w") as f:
                f.write(msg)
                f.write(versionInfo)
        except IOError:
            pass
        errorbox = QMessageBox()
        errorbox.setText(str(notice)+str(msg)+str(versionInfo))
        errorbox.setWindowTitle(' An Unhandled Exception Occurred')
        errorbox.exec_()

    sys.excepthook = excepthook


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    au = aircraftUI()
    au.show()
    sys.exit(app.exec_())