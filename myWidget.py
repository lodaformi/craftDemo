# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TopButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(TopButton, self).__init__(*args, **kwargs)
        self.setMinimumSize(120, 50)
        self.setMaximumSize(120, 50)
        self.setDefault(True)
        self.setFont(QFont("楷体",14, QFont.Bold))

class RowResWidget(QFrame):
    def __init__(self, parent=None):
        super(RowResWidget, self).__init__(parent)
        self.pixmap = None
        self.boxesWidget = QWidget()
        self.scroll = QScrollArea()
        self.scroll.setVisible(False)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.boxesWidget)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)
        self.setLayout(layout)
        self.boxesWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setMaximumHeight(400)
        self.imglayout = QVBoxLayout()

    def initBox(self,typeRes):
        self.scroll.setVisible(True)
        self.cleanlayout()
        # self.imglayout = QVBoxLayout()
        for i in range(len(typeRes)):
            sublayout = QHBoxLayout()
            sublayout.setContentsMargins(0, 0, 0, 0)
            for j in  range(len(typeRes[i])):
                if j == 0:
                    typeLabel = QLabel('{}'.format(typeRes[i][0]))
                    typeLabel.setMaximumWidth(50)
                    typeLabel.setAlignment(Qt.AlignCenter)
                    sublayout.addWidget(typeLabel, 0, Qt.AlignLeft)
                else:
                    # myRect = (typeRes[i][j][0], typeRes[i][j][1], typeRes[i][j][2], typeRes[i][j][3])
                    img = showImg(minSize=QSize(120, 120))
                    img.setMinimumSize(QSize(120, 120))
                    img.setMaximumSize(QSize(120, 120))
                    img.pixmap = self.pixmap
                    img.showsmallImg(typeRes[i][j])
                    sublayout.addWidget(img, 1, Qt.AlignLeft)
            self.imglayout.addLayout(sublayout)
        self.boxesWidget.setLayout(self.imglayout)

    def cleanlayout(self):
        if self.imglayout:
            layout = self.imglayout
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                num = item.count()
                for j in reversed(range(num)):
                    if isinstance(item.itemAt(j), QWidgetItem):
                        item.itemAt(j).widget().close()
                    item.removeItem(item.itemAt(j))
                item.deleteLater()
            QWidget().setLayout(self.imglayout)
            self.imglayout = QVBoxLayout()

class showImg(QFrame):
    def __init__(self, parent=None, minSize = QSize(300, 360)):
        super(showImg, self).__init__(parent)
        self.default_pixmap = QPixmap('./imgs/blank.png')
        self.pixmap = None
        self.show_pix = None
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setMinimumSize(minSize)
        self.imageLabel.setMaximumSize(minSize)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imageLabel, Qt.AlignCenter)
        self.setContentsMargins(0, 0, 0, 0)
        self.imageLabel.setPixmap(self.default_pixmap)
        self.setLayout(layout)
        # self.setStyleSheet('''border: 1px solid black''')

    def updatePixmap(self, pixmap=None):
        if pixmap is not None:
            self.show_pix = pixmap

        if self.show_pix is None:
            self.show_pix = self.default_pixmap.copy()
        # print(self.imageLabel.height())
        show_pixmap = self.show_pix.copy()
        show_pixmap = show_pixmap.scaledToWidth(
            self.width(),
            Qt.SmoothTransformation)
        self.imageLabel.setPixmap(show_pixmap)
        self.update()

    def resizeEvent(self, event):
        self.updatePixmap()

    def showsmallImg(self, bbox):
        bbox_rect = QRect(bbox[0], bbox[1], bbox[2], bbox[3])
        qimg = QImage(self.pixmap.copy())
        smallImg = qimg.copy(bbox_rect)
        self.updatePixmap(QPixmap(smallImg))

class ImgWidget(QFrame):
    mysignal = pyqtSignal(QPixmap)

    def __init__(self, parent = None, minSize = QSize(260, 260)):
        QWidget.__init__(self, parent)
        self.default_pixmap = QPixmap('./imgs/blank.png')
        self.pixmap = None
        self.show_pix = None
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setMinimumSize(minSize)
        # self.imageLabel.setMaximumSize(minSize)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imageLabel, Qt.AlignCenter)
        # print(self.default_pixmap.isNull())
        # self.imageLabel.setMinimumSize(200,200)
        self.setContentsMargins(0, 0, 0, 0)
        self.imageLabel.setPixmap(self.default_pixmap)
        self.setLayout(layout)
        # self.setStyleSheet('''
        # border: 1px solid black
        # ''')
        # self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
        #                    QtGui.QSizePolicy.MinimumExpanding,)
        self.filename = ''
        self.box = []
        self.image_save = None
        self.imgLabelWidth = 0
        self.imgLabelHeight = 0
        self.pX = 0
        self.pY = 0
        self.pW = 0
        self.pH = 0
        self.multiple = 0

    def resizeEvent(self, event):
        self.updatePixmap()
        self.imgLabelWidth = self.imageLabel.size().width()
        self.imgLabelHeight = self.imageLabel.size().height()

    def updatePixmap(self, pixmap=None):
        if pixmap is not None:
            self.show_pix = pixmap

        if self.show_pix is None:
            self.show_pix = self.default_pixmap.copy()
        # print(self.imageLabel.height())
        show_pixmap = self.show_pix.copy()
        show_pixmap = show_pixmap.scaledToWidth(
            # self.imageLabel.width(),
            self.width(),
            Qt.SmoothTransformation)
        # print(self.imageLabel.width())
        # print('show_pixmap {}'.format(show_pixmap))
        self.imageLabel.setPixmap(show_pixmap)
        self.update()

    def paintEvent(self, event):
        pass

    def getBbox(self, bbox):
        self.box = bbox

    def smallImgDra(self):
        smallPix = self.pixmap.copy()
        for i in range(len(self.box)):
            for j in range(len(self.box[i])):
                if j != 0:
                    list = self.box[i][j]
                    x = list[0]
                    y = list[1]
                    w = list[2]
                    h = list[3]
                    print('x {}'.format(x))
                    print('y {}'.format(y))
                    print('w {}'.format(w))
                    print('h {}'.format(h))
                    if x > self.pX and (x + w) < self.pX+ self.pW \
                            and y > self.pY and (y + h) < self.pY + self.pH:
                        qp = QPainter()
                        pen = QPen()
                        pen.setColor(Qt.red)
                        pen.setWidth(1)
                        qp.begin(smallPix)
                        qp.setPen(pen)
                        qp.drawRect(x, y, w, h)
                        qp.end()
        simg = QImage(smallPix)
        smallImg = simg.copy(self.pX, self.pY, self.pW, self.pH)
        smallImg.save('D:/Develop/code/airCraftUI/imgs/saveImg/sdfa.jpg', 'jpg')
        self.image_save = QPixmap(smallImg)

    def mydrawRect(self, bbox):
        bbox_rect = QRect(bbox[0], bbox[1], bbox[2], bbox[3])
        pixmap = self.pixmap.copy()
        qimg = QImage(self.pixmap.copy())

        qp = QPainter()
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(3)
        qp.begin(pixmap)
        qp.setPen(pen)
        qp.drawRect(bbox_rect)
        qp.end()
        self.updatePixmap(pixmap)

        smallImg = qimg.copy(bbox_rect)
        self.image_save = QPixmap(smallImg)

    def mousePressEvent(self,QMouseEvent):
        mouseX= QMouseEvent.x()
        mouseY = QMouseEvent.y()
        frameWidth = self.width()
        frameHeight = self.height()
        width = 100
        height = 100
        self.multiple = self.pixmap.width() * 1.0 / frameWidth
        print(self.multiple)
        print('x is {}'.format(QMouseEvent.x())+ '\n' + 'y is {}'.format(QMouseEvent.y()))

        startY = frameHeight / 2.0 - self.pixmap.height() / 2.0 / self.multiple

        if mouseX < width / 2.0 or frameWidth - width / 2.0 < mouseX or \
                (mouseY < startY + height / 2.0) or \
                (startY + self.pixmap.height() * 1.0 / self.multiple - height / 2.0 < mouseY):
            return

        pointX = mouseX - width / 2.0
        pointY = mouseY - startY - height / 2.0
        self.pX = int(pointX * self.multiple)
        self.pY = int(pointY * self.multiple)
        self.pW = int(width * self.multiple)
        self.pH = int(height * self.multiple)

        pointList = [self.pX, self.pY, self.pW , self.pH]
        self.mydrawRect(pointList)
        self.smallImgDra()
        # print(self.box)
        print(pointList)

        self.mysignal.emit(self.image_save)

class MyThread(QThread):
    start_trigger = pyqtSignal()
    end_trigger = pyqtSignal(list)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def run(self):
        print('sleep ..')
        self.start_trigger.emit()
        startTime = time.time()

        time.sleep(1)
        totalTime = time.time() - startTime

        # self.end_trigger.emit(['xxx', totalTime, [[752,415,36,18], [759,450,33,13]]])
        self.end_trigger.emit(['xxx', totalTime, [['type1', [752,415,36,18], [759,450,33,50]], ['type2', [300,350,26,44],[200,150,26,44],[100,250,26,44]], ['type3', [752,415,36,18]]]])