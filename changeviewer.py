# generic PyQt Application framework
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

# user-defined ui file
import custom_frame

# user-defined class
from ImageViewer import ChangEViewer

# 初始化
my_app = {}
my_app['application']  = QApplication(sys.argv)
my_app['main_window']  = QMainWindow()
my_app['ui']           = custom_frame.Ui_MainWindow()
my_app['ui'].setupUi(my_app['main_window'])
my_app['user_class']   = ChangEViewer(0.1, my_app['ui'])

# 显示窗体
my_app['main_window'].show()

# 运行
re = my_app['application'].exec_()

# 运行结束
#my_app['user_class'].stopWorking()
sys.exit(re)
