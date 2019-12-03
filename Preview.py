import math
import cv2
import time
import sys 
import copy
from PyQt5 import QtWidgets, QtGui, QtCore

im_path = 'C:\\Users\\4L13N5\Desktop\\Capture.png'
file_path = 'C:\\Users\\4L13N5\\Desktop\\test.txt'

def im_disp(path):
    img = cv2.imread(path)
    cv2.imshow("im",img)
    cv2.waitKey(0)


v_path = 'D:\\Movies\\Comedy Central Roast of William Shatner Uncut & Uncensored DVDRip x264.mkv'

def v_disp(path):
    cap = cv2.VideoCapture(path)
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver)  < 3 :
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        fps = cap.get(cv2.CAP_PROP_FPS)
    wait_duration = math.ceil(1000 / fps)
    start = time.time()
    while(True):
        if time.time() - start > 5:
            break
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('video preview',frame)
            cv2.waitKey(wait_duration)

    cap.release()


#im_disp(im_path)
#v_disp(v_path)



class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self,parent=None):
        super(Thread, self).__init__(parent)
        self.threadactive = True
        self.i = 0

    def stop(self):
        self.threadactive=False
        self.wait()

    def run(self):
        cap = cv2.VideoCapture(v_path)
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver)  < 3 :
            fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        else :
            fps = cap.get(cv2.CAP_PROP_FPS)
        wait_duration = math.ceil(1000 / fps) / 1000
        start = time.time()
        while self.threadactive== True:
            if(time.time()-start > 5):
                self.stop()
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                lh = ex.video_label.geometry().height()
                lw = ex.video_label.geometry().width()
                p = convertToQtFormat.scaled(lw,lh,QtCore.Qt.IgnoreAspectRatio)
                self.changePixmap.emit(p)
                time.sleep(wait_duration)
        cap.release()




class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800
        self.initUI()
        self.showText()

    
    def play_video(self):
        self.image_label.hide()
        self.textedit.hide()
        self.video_label.show()
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()


    def showImage(self):
        self.video_label.hide()
        self.textedit.hide()
        self.image_label.show()

        img = cv2.imread(im_path)
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        lh = self.image_label.geometry().height()
        lw = self.image_label.geometry().width()
        p = convertToQtFormat.scaled(lw,lh,QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(p))
        

    def showText(self):
        self.video_label.hide()
        self.image_label.hide()
        #self.scrollarea.show()
        self.textedit.show()
        FILE = open(file_path,"r")
        text = ""
        cnt = 0
        for line in FILE:
            if cnt >= 20:
                break
            text+=line
            cnt+=1
        FILE.close()
        self.textedit.setText(text)


    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):     
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createGridLayout()




    def createGridLayout(self):
        layout = QtWidgets.QGridLayout()
        """
        self.overlabel = QtWidgets.QLabel(self)
        self.overlabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.overlabel.setStyleSheet('background: black')
        """

        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.video_label.setScaledContents(1)

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.image_label.setScaledContents(1)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.text_label.setScaledContents(1)

        self.button1 = QtWidgets.QPushButton("a")
        self.button1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.button1.clicked.connect(self.play_video)

        self.button3 = QtWidgets.QPushButton("c")
        self.button3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.button3.clicked.connect(self.showImage)

        self.textedit = QtWidgets.QTextEdit()
        self.textedit.setReadOnly(True)
        """
        self.scrollarea = QtWidgets.QScrollArea()
        self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollarea.setWidget(self.textedit)
        """
        layout.addWidget(self.button1,0,0,2,1)
        layout.addWidget(self.button3,1,1)
        layout.addWidget(self.video_label,0,1)
        layout.addWidget(self.image_label,0,1)
        #layout.addWidget(self.scrollarea,0,1)
        layout.addWidget(self.textedit,0,1)
        

        #layout.addWidget(self.overlabel,0,1)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())        