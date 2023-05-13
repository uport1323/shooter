from PIL import Image
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QListWidget,QFileDialog, QInputDialog, QTextEdit, QLineEdit, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton
from PyQt5.QtGui import QPixmap
app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel('Картинка')
lw_files = QListWidget()

btn_dir = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)


participants = list()
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, exitensions):
    result = list()
    for filename in files:
        for exitension in exitensions:
            if filename.endswith(exitension):
                result.append(filename)
    return result

def showFilenamesList():
    chooseWorkdir()
    exitensions = ['png', 'jpg']
    files = os.listdir(workdir)
    filenames = filter(files, exitensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)
class ImageProcssor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save = 'save/'

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        paht = os.path.join(workdir, self.save)
        if not(os.path.exists(paht) or os.path.isdir(paht)):
            os.mkdir(paht)
        image_path = os.path.join(paht, self.filename)
        self.image.save(image_path)
    def pic_up(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save, self.filename)
        self.showImage(image_path)
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        image_path = os.path.join(workdir, self.save, self.filename)
        self.saveImage()
        self.showImage(image_path)
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


workimage = ImageProcssor()
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)




lw_files.currentRowChanged.connect(showChosenImage)

btn_flip.clicked.connect(workimage.pic_up)
btn_right.clicked.connect(workimage.right)
btn_left.clicked.connect(workimage.left)
btn_dir.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workimage.do_bw)
win.setLayout(row)
win.show()
app.exec_()

