import types
import sys
import os
import re
import utils    # 个人常用功能函数

#from PyQt5.QtCore    import QObject, Qt, QTimer
#from PyQt5.QtGui     import QTransform, QPen
#from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

# 继承QGraphicsView，将鼠标滚轮事件重载
class MyGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

    def __del__(self):
        pass

    def wheelEvent(self, event):
        print('in wheelEvent')
        print(event.angleDelta().x(), event.angleDelta().y())

        if (event.angleDelta().y()>0):
            self.scale(1.2, 1.2)
        else:
            self.scale(1/1.2, 1/1.2)

        QGraphicsView.wheelEvent(self, event)


class ImageViewer(QObject):
    def __init__(self, dt=0.1, ui=None):
        QObject.__init__(self)

        # 自定义ui
        self.ui = ui

        ## 创建一个定时器
        #self.__working = False
        #self.__dt = dt 
        #self.__timer = QTimer(self)
        #self.__timer.timeout.connect(self.onTimer)
        #self.__on_timer_update = None

    def __del__(self):
        pass

    #def onTimer(self):
    #    if  isinstance(self.__on_timer_update, types.FunctionType): 
    #        self.__on_timer_update()
    #    else:
    #        print('on timer')


from PIL import Image
import numpy as np
import pds4_tools
import colour
import colour_demosaicing
from skimage import exposure
        

class ChangEViewer(ImageViewer):
    def __init__(self, dt=0.1, ui=None):
        ImageViewer.__init__(self, dt, ui)

        self.__current_image = -1
        self.__total_image = 0
        self.__images = []

        self.ui.lblPath.setText('PDS数据路径：')
        self.ui.edtPath.setText('../../pic/CE4_PCAM_2B/DATA')
        self.ui.btnOK.setText('扫描PDS数据')
        self.ui.pushButton_2.setText('放大')
        self.ui.pushButton_3.setText('缩小')
        self.ui.statusbar.showMessage('就绪')

        # 连接信号
        self.ui.btnOK.clicked.connect(self.onButtonOKClicked)
        self.ui.pushButton_2.clicked.connect(self.onButton2Clicked)
        self.ui.pushButton_3.clicked.connect(self.onButton3Clicked)
        self.ui.btnReset.clicked.connect(self.onButtonResetClicked)
        self.ui.btnNext.clicked.connect(self.onButtonNextClicked)
        self.ui.btnPrev.clicked.connect(self.onButtonPrevClicked)

    def readCurrentImage(self):
        img = self.__images[self.__current_image]

        if img['pds_data'] is None:
            # 读入pds label
            img['pds_data'] = pds4_tools.read('%s/%s' %(img['path'], img['filename']))

            # 将图像数据提取出来
            img['raw_data'] = np.asanyarray(img['pds_data'][0].data)
            print(img['raw_data'].shape, img['raw_data'].ndim)
            img['raw_data'] = img['raw_data'] / 1023      #10位的图像数据归一化 

            # de-bayer
            rgb_data = colour.cctf_encoding(colour_demosaicing.demosaicing_CFA_Bayer_bilinear(img['raw_data'], 'RGGB')) 
            print(rgb_data.shape, rgb_data.ndim)
            img['rgb_data'] = rgb_data

            ## 直方图拉伸
            #lower, upper = np.percentile(rgb_data, (0.2,99.8))
            #print(lower, upper)
            #scale_data = exposure.rescale_intensity(rgb_data, in_range=(lower, upper)) 

        return img

    def sortPDSFilesByDate(self, files):

        date_list = []
        # 用个正则表达式把日期提取出来，应该还有更简单的方法吧?
        for f in files:
            search_pattern = re.compile('.*([0-9]{14}).*')
            search_result  = None
            search_result  = search_pattern.search(f)
            if search_result is not None:
                match_result   = search_result.group(1)     # 第一个匹配
                date_list.append(match_result)
            else:
                date_list.append('99999999999999')
        pass
        
        # 将日期和文件名合并成一个list，然后以日期为key进行排序
        combine_list = []
        for k in range(len(files)):
            combine_list.append([date_list[k],files[k]])

        def takeFirst(e):
            return e[0]
        combine_list.sort(key=takeFirst)

        # 把排序后的list中的文件名单独抽取来形成新的list
        new_file_list = []
        for c in combine_list:
            new_file_list.append(c[1])

        return new_file_list

    ########### 信号响应函数 ##################################################
    def onButtonOKClicked(self):
        # 扫描目标文件夹中的PDS文件条目
        self.__images = []
        k = 0
        files = os.listdir(self.ui.edtPath.text())

        # 根据日期对文件条目排序
        files = self.sortPDSFilesByDate(files)

        for f in files:
            if f.endswith('2BL') or f.endswith('2bl') or f.endswith('2AL') or f.endswith('2al'):
                t = {}
                t['path'] = self.ui.edtPath.text()
                t['filename'] = f
                t['pds_data'] = None
                t['raw_data'] = None
                t['rgb_data'] = None
                self.__images.append(t)
                k = k + 1

        self.__total_image = k
        self.__current_image = k-1 
        self.ui.statusbar.showMessage('PDS数据共 %d 个，扫描完毕！' % (k))

    def onButton2Clicked(self):
        self.ui.graphicsView.scale(1.2, 1.2)
        pass

    def onButton3Clicked(self):
        self.ui.graphicsView.scale(1/1.2, 1/1.2)
        pass

    def onButtonNextClicked(self):
        # 清除显示场景
        self.ui.graphicsScene.clear()

        # 拨计数
        self.__current_image = self.__current_image + 1
        if self.__current_image >= self.__total_image:
            self.__current_image = 0
        print(self.__current_image, self.__total_image)

        # 读一个pds数据
        img = self.readCurrentImage()

        print(img['rgb_data'])

        if img['rgb_data'] is not None:
            p = img['rgb_data'] * 255
            p = p.astype('uint8')
            pixmap = Image.fromarray(p).toqpixmap()
            item = self.ui.graphicsScene.addPixmap(pixmap)
            item.setPos(0, 0)

            # 自适应显示内容
            self.ui.graphicsScene.setSceneRect(self.ui.graphicsScene.itemsBoundingRect())
            self.ui.statusbar.showMessage('显示第 %05d 个图像： %s' %(self.__current_image, img['filename']))
        else:
            self.ui.statusbar('显示第 %d 个图像错误！')

    def onButtonPrevClicked(self):
        # 清除显示场景
        self.ui.graphicsScene.clear()

        # 拨计数
        self.__current_image = self.__current_image - 1
        if self.__current_image <= -1:
            self.__current_image = self.__total_image - 1 
        print(self.__current_image, self.__total_image)

        # 读一个pds数据
        img = self.readCurrentImage()

        if img['rgb_data'] is not None:
            p = img['rgb_data'] * 255
            p = p.astype('uint8')
            pixmap = Image.fromarray(p).toqpixmap()
            item = self.ui.graphicsScene.addPixmap(pixmap)
            item.setPos(0, 0)

            # 自适应显示内容
            self.ui.graphicsScene.setSceneRect(self.ui.graphicsScene.itemsBoundingRect())
            self.ui.statusbar.showMessage('显示第 %05d 个图像： %s' %(self.__current_image, img['filename']))
        else:
            self.ui.statusbar('显示第 %d 个图像错误！')

    def onButtonResetClicked(self):
        # 设置显示场景，复位View的变换矩阵
        self.__ui.graphicsScene.setSceneRect(self.__ui.graphicsScene.itemsBoundingRect())
        self.__ui.graphicsView.resetTransform()



    #####   以下尚未修改    ############################################################

    def onPatchSizeEditChanged(self):
        size = utils.str2num(self.__ui.edtPatchSize.text())
        if size > 0:
            self.__imgpatcher.setSize(size)
        [fn, size, stride, img_shape, img_size, img_ndim] = self.__imgpatcher.info()
        print('file = %s，size = %d, stride = %d' % (fn, size, stride))
        print(img_shape, img_size, img_ndim)

    def onPatchStrideEditChanged(self):
        stride = utils.str2num(self.__ui.edtPatchStride.text())
        if stride > 0:
            self.__imgpatcher.setStride(stride)
        [fn, size, stride, img_shape, img_size, img_ndim] = self.__imgpatcher.info()
        print('file = %s，size = %d, stride = %d' % (fn, size, stride))
        print(img_shape, img_size, img_ndim)

    def onButtonChooseImageClicked(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self.__ui.btnChooseImage,  
                                    '选取文件',  
                                    '', 
                                    'JPG Files (*.jpg);;NPY Files(*.npy);;All Files (*)')   # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            print("\n取消选择")
            return

        print("\n你选择的文件为:")
        print(fileName_choose)
        print("文件筛选器类型: ",filetype)

        self.__ui.edtFileName.setText(fileName_choose)