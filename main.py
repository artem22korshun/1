#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка


from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel('картинка')
btn_dir = QPushButton('папка')
files = QListWidget()

lv_1 = QVBoxLayout()
lv_2 = QVBoxLayout()

lh_1 = QHBoxLayout()
lh_2 = QHBoxLayout()

lf_filkes = QListWidget()
left_button = QPushButton('лево')
right_button = QPushButton('право')
mirror_button = QPushButton('зеркало')
rezkost_button = QPushButton('резкость')
b_w_button = QPushButton('Ч|Б')
blur_button = QPushButton('блюр')



lv_1.addWidget(btn_dir)
lv_1.addWidget(files)

lh_1.addLayout(lv_1)

lv_2.addWidget(lb_image)
lh_2.addWidget(left_button)
lh_2.addWidget(right_button)
lh_2.addWidget(mirror_button)
lh_2.addWidget(rezkost_button)
lh_2.addWidget(b_w_button)
lh_2.addWidget(blur_button)

win.setLayout(lh_1)

lh_1.addLayout(lv_2)
lv_2.addLayout(lh_2)

workdir = ''

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files,extension):
    result = []
    for file in files:
        for ext in extension:
            if file.endswith(ext):
                result.append(file)
    return result
def showFilename():
    extension = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseworkdir()
    filenames = filter(os.listdir(workdir), extension)
    files.clear()
    for filename in filenames:
        files.addItem(filename)
btn_dir.clicked.connect(showFilename)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None 
        self.save_dir = 'Modified/'
    def loadimage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)
    def do_bw(self):
        try:
            self.image = self.image.convert('L')
            self.save_image()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)
        except:
            pass
    def do_left(self):
        try:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.save_image()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)
        except:
            pass
    def do_right(self):
        try:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.save_image()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)
        except:
            pass
    def do_rezkost(self):
        try:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.save_image()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)
        except:
            pass
    def do_mirror(self):
        try:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.save_image()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)
        except:
            pass
    def do_blur(self):
        try:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.save_image()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showimage(image_path)
        except:
            pass


    def save_image(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def showimage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
workimage = ImageProcessor()
    


def showChosenImage(): 
    if files.currentRow() >= 0:
        filename = files.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, filename)
        workimage.showimage(image_path)
files.currentRowChanged.connect(showChosenImage)
b_w_button.clicked.connect(workimage.do_bw)
left_button.clicked.connect(workimage.do_left)
right_button.clicked.connect(workimage.do_right)
rezkost_button.clicked.connect(workimage.do_rezkost)
mirror_button.clicked.connect(workimage.do_mirror)
blur_button.clicked.connect(workimage.do_blur)






win.show()
app.exec()




