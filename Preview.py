#Skiddadle skidoodle this code is a fucking noodle


import math
import cv2
import time
import sys 
import copy
import codecs
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import db_functions as db
import Shell as s

con = db.db_connect(".\\db.db")

def sql_parser(out):
    return [(y.split('\\')[-1],y,x) for x,y in out]

def temp_parser(out):
    return

#DO NOT DELETE LINE BELOW
#DO NOT
v_path="aa"
#[file name, file path, file id]


class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.threadactive = True
        self.i = 0
        self.path = v_path

    def stop(self):
        self.threadactive=False
        self.wait()

    def run(self):
        cap = cv2.VideoCapture(self.path)
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

class ClickableLabel(QtWidgets.QLabel):
    def __init__(self, data):
        super().__init__()
        self.name = data[0]
        self.path = data[1]
        self.id = data[2]
        self.par=""
        self.tags = []
        self.par = self.getParent()
        self.tags = self.getTags()
        self.ctxMenu()

    def ctxMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        changeParentAction = QtWidgets.QAction("Change Parent",self)
        changeParentAction.triggered.connect(self.changeParent)

        addTagAction = QtWidgets.QAction("Add tag",self)
        addTagAction.triggered.connect(self.addTag)

        changeTagAction = QtWidgets.QAction("Change tag",self)
        changeTagAction.triggered.connect(self.changeTag)

        self.addAction(changeParentAction)
        self.addAction(changeTagAction)
        self.addAction(addTagAction)

    def getParent(self):
        #vrni starša od tega fila
        parent = "aaa" #placeholder
        return parent
    def getTags(self):
        #vrni list vseh tagov od tega fila
        tags = ["a","b"] #placeholder
        return tags

    def changeTag(self):
        oldTag, ok = QtWidgets.QInputDialog().getText(self, "Get text", "Enter old tag", QtWidgets.QLineEdit.Normal, "")
        if ok:
            newTag, ok = QtWidgets.QInputDialog().getText(self, "Get text", "Enter new tag", QtWidgets.QLineEdit.Normal, "")
            if ok:
                try:
                    for i in range(len(self.tags)):
                        if self.tags[i]==oldTag:
                            self.tags[i]= newTag
                            #tukej dej funkcijo ki v bazi zamenja oldtag za new tag
                except BaseException as e:
                    print(e)
        self.window().tagsDisplay.setText(", ".join(self.tags))

    #tu napisi funkcijo ki zbriše iz baze
    def delete_from_database(self):
        db.db_delete(con,"Datoteka","ID = " + self.id)
        return

    def delete_physical(self):
        s.remove(["",self.path])
        self.delete_from_database()
        return

    

    def getNewTag(self):
        try:
            newTag, ok = QtWidgets.QInputDialog().getText(self, "Get text", "Enter new tag", QtWidgets.QLineEdit.Normal, "")
            if ok:
                return newTag
        except BaseException as e:
            print(e)

    def getNewParent(self):
        try:
            newParent, ok = QtWidgets.QInputDialog().getText(self, "Get text", "Enter new parent", QtWidgets.QLineEdit.Normal, "")
            if ok:
                return newParent
        except BaseException as e:
            print(e)

    def test(self):
        print("fuction from context menu {}".format(self.name))
    
    def deleteFile(self):
        try:
            self.delete_from_database()
            for i in range(len(self.window().files)):
                if self.window().files[i][2] == self.id:
                    del self.window().files[i]
                    break
            self.window().addStuff()
        except BaseException as e:
            print(e)

    def addTag(self):
        ntag=""   
        ntag = self.getNewTag()
        if ntag != "":
            #tle not dej funkcijo za filu dodat nov tag ntag
            self.tags.append(ntag)
        else:
            print("not a valid tag name")
        self.window().tagsDisplay.setText(", ".join(self.tags))

    def changeParent(self):
        try:
            pTag = ""
            pTag = self.getNewParent()
            if pTag != "":
                #tle not dej funkcijo za filu spremenit parent na pTag
                self.par=pTag
                self.window().ptagDisplay.setText(self.par)
            else:
                print("not a valid tag name")
        except BaseException as e:
            print(e)



    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.deleteFile()

    def mousePressEvent(self,event):
        self.setFocus()
        self.window().selected = self
        try:
            self.window().ptagDisplay.setText(self.par)
            self.window().tagsDisplay.setText(", ".join(self.tags))
        except BaseException as e:
            print(e)
        tip = self.path.split(".")[-1]
        if tip == "mkv" or tip == "mp4" or tip == "avi":
            self.parent().parent().parent().parent().parent().play_video(self.path)
        elif tip == "txt":
            self.parent().parent().parent().parent().parent().showText(self.path)
        elif tip == "jpg" or tip == "png":
            self.parent().parent().parent().parent().parent().showImage(self.path)
        else:
            pass

    def mouseDoubleClickEvent(self, event):
        #self.clicked.emit(self.name)
        file = self.path
        try:
            os.startfile(file)
        except:
            print("cannot execute from path {}".format(file))

    def enterEvent(self, event):
        self.setStyleSheet('background: rgb(200,200,200)')

    def leaveEvent(self, event):
        self.setStyleSheet('background: rgb(225,225,225)')


class TagLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.tag=""
        self.tmp = []
        self.setPlaceholderText("Tag based search")

    #s to funkcijo nrdi query select  where tag==self.tag
    def get_files_where_tag(self,tag):
        str = "SELECT d.ID,Path FROM Datoteka d LEFT JOIN oznacuje o ON d.ID==o.ID WHERE o.Tag == '" + tag+"'"
        tmp = db.db_custom(con,str)
        return sql_parser(tmp)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            try:
                self.tag = self.text()
                self.tmp = self.get_files_where_tag(self.tag)
                #self.tmp = test_list
            except BaseException as e:
                print(e)
            self.parent().parent().files = copy.deepcopy(self.tmp)
            self.parent().parent().addStuff()

        else:
            QtWidgets.QLineEdit.keyPressEvent(self,event)

class FileLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.file=""
        self.tmp = []
        self.setPlaceholderText("File based search")

    #s to funkcijo nrdi query select  where file_name==self.file
    def get_files_where_file(self,file):
        tmp = []
        return tmp
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            try:
                self.file = self.text()
                self.tmp = self.get_files_where_file(self.file)
            except BaseException as e:
                print(e)
            self.parent().parent().files = copy.deepcopy(self.tmp)
            self.parent().parent().addStuff()
        else:
            QtWidgets.QLineEdit.keyPressEvent(self,event)


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'File Manager'
        self.selected = 0
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800
        self.tst="aaaaaaaaaaaaaa"
        self.files = []
        self.initUI()

    
    def fillDatabaseFunction(self):
        dir = self.tInput.text()
        #build database dir
        print(dir)
        

    def addStuff(self):
        self.ScrollLayout = QtWidgets.QVBoxLayout()
        self.ScrollLayout.addStretch()

        for i in range(len(self.files)):
            lbl = ClickableLabel(self.files[i])
            lbl.setText(self.files[i][0])
            self.ScrollLayout.insertWidget(self.ScrollLayout.count()-1, lbl)

        self.scrollwidget = QtWidgets.QWidget()
        self.scrollwidget.setStyleSheet('background: rgb(225,225,225)')
        self.scrollwidget.setLayout(self.ScrollLayout)
        self.scrollarea.setWidget(self.scrollwidget)


    def play_video(self,nk):
        global v_path
        self.image_label.hide()
        self.textedit.hide()
        self.video_label.show()
        self.neki=nk
        v_path= self.neki
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()


    def showImage(self,path):
        self.video_label.hide()
        self.textedit.hide()
        self.image_label.show()

        img = cv2.imread(path)
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        lh = self.image_label.geometry().height()
        lw = self.image_label.geometry().width()
        p = convertToQtFormat.scaled(lw,lh,QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(p))
        
    
    def showText(self, path):
        try:
            self.video_label.hide()
            self.image_label.hide()
            self.textedit.show()
            FILE = codecs.open(path,"r",'UTF-8')
            text = FILE.read()
            FILE.close()
            self.textedit.setText(text)
        except BaseException as e:
            print(e)



    def test(self, string):
        print("string")

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):     
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(image))


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.createGridLayout()
        self.createVerticalLayout()

    #search bar layout
    def createHorizontalLayout(self):
        hLayout = QtWidgets.QHBoxLayout()
        file_search = FileLineEdit()
        tag_search = TagLineEdit()
        hLayout.addWidget(file_search)
        hLayout.addWidget(tag_search)
        self.horiz.setLayout(hLayout)
    #content layout
    def createGridLayout(self):
        layout = QtWidgets.QGridLayout()


        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.video_label.setScaledContents(1)

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.text_label.setScaledContents(1)

        self.textedit = QtWidgets.QTextEdit()
        self.textedit.setReadOnly(True)


        self.scrollarea = QtWidgets.QScrollArea()
        self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)        
        self.scrollarea.setWidgetResizable(True)
        self.addStuff()
        

        
        self.vwidget = QtWidgets.QWidget()
        self.vwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        vlayout = QtWidgets.QVBoxLayout()
        self.ptagDisplay = QtWidgets.QLabel()
        self.ptagDisplay.setStyleSheet("background:white")
        self.tagsDisplay = QtWidgets.QLabel()
        self.tagsDisplay.setStyleSheet("background:white")

        self.tInput = QtWidgets.QLineEdit()
        self.tInput.returnPressed.connect(self.fillDatabaseFunction)
        self.tInput.setPlaceholderText("PLACE HOLDER TEXT CHANGE THIS TO WHATEVER THE FUCK THIS DOES")

        self.plab = QtWidgets.QLabel()
        self.plab.setText("Parent tag:")
        self.tlab = QtWidgets.QLabel()
        self.tlab.setText("File tags:")

        vlayout.addWidget(self.tInput)
        vlayout.addWidget(self.plab)
        vlayout.addWidget(self.ptagDisplay)
        vlayout.addWidget(self.tlab)
        vlayout.addWidget(self.tagsDisplay)

        vlayout.addStretch()
        self.vwidget.setLayout(vlayout)

        layout.addWidget(self.scrollarea,0,0,2,1)
        layout.addWidget(self.vwidget,1,1)
        layout.addWidget(self.video_label,0,1)
        layout.addWidget(self.image_label,0,1)

        layout.addWidget(self.textedit,0,1)
        

        self.grid.setLayout(layout)
    #main layout
    def createVerticalLayout(self):
        vLayout = QtWidgets.QVBoxLayout()
        self.grid = QtWidgets.QWidget(self)
        self.createGridLayout()
        self.horiz = QtWidgets.QWidget(self)
        self.createHorizontalLayout()
        vLayout.addWidget(self.horiz,1)
        vLayout.addWidget(self.grid,20)
        self.setLayout(vLayout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())        
