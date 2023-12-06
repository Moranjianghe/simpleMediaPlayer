# 导入PySide6的相关模块
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget,QFrame
from PySide6.QtGui import QGuiApplication
# 导入vlc模块，用于播放视频
import vlc
# 导入sys模块，用于处理系统参数
import sys

# 定义一个Player类，继承自QMainWindow
class Player(QMainWindow):
    # 定义构造函数
    # self 是一个参数，用于指代类的实例。
    # 在 Python 中，类的方法默认会传递实例作为第一个参数，但是不会自动接收，
    # 所以需要在方法定义中显式地写出 self。
    # self 不是 Python 的关键字，也不是特殊的语法，只是一个约定俗成的名称
    def __init__(self):
        # 调用父类（QMainWindow）的构造函数
        super().__init__()
        # 设置窗口的标题
        self.setWindowTitle("媒体播放器")
        # 设置窗口的位置和大小
        screen = QGuiApplication.primaryScreen().geometry() # 获取屏幕类并调用geometry()方法获取屏幕大小
        width = screen.width() # 获取屏幕的宽
        height = screen.height() # 获取屏幕的高
        self.setGeometry(width/2-400, height/2-300, 800, 600)
        # 创建一个vlc实例
        self.vlc_instance = vlc.Instance()
        # 创建一个vlc媒体播放器
        self.player = self.vlc_instance.media_player_new()
        # 创建用户界面
        self.create_ui()

    # 定义创建用户界面的方法
    def create_ui(self):
        # 创建一个QWidget作为中心部件
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        # 创建一个垂直布局
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)


        # 创建一个QFrame作为视频的容器
        self.frame = QFrame(self)
        # 设置QFrame的背景颜色为黑色
        self.frame.setStyleSheet("background-color: black;")
        # 将QFrame添加到布局中
        self.layout.addWidget(self.frame)


        # 打开一个文件对话框，选择要播放的视频文件
        self.open_file()

    # 定义打开文件的方法
    def open_file(self):
        # 调用QFileDialog的静态方法，获取文件路径和过滤器
        #filepath, _ = QFileDialog.getOpenFileName(self, "Open Video")
        # 默认显示视频文件，但也可以选择其他文件
        filepath, _ = QFileDialog.getOpenFileName(self, "Open File", filter="视频文件(*.mp4 *.avi *.mkv *.wmv *.mov *.mpg *.mpeg *.m4v *.3gp *.webm *.flv *.vob *.ogv *.gif);;音频文件(*.mp3 *.m4a *.flac *.wav *.ogg *.aac *.wma *.mid *.midi *.amr *.opus *.aiff);;所有文件 (*)")
        # 如果文件路径不为空
        if filepath:
            # 创建一个vlc媒体对象，传入文件路径
            self.media = self.vlc_instance.media_new(filepath)
            # 将媒体对象设置给播放器
            self.player.set_media(self.media)
            # 将窗口的ID设置给播放器，用于显示视频
            #libvlc_media_player_set_hwnd是一个vlc库提供的函数，
            # 它的作用是将一个win32/win64窗口句柄设置给媒体播放器，用于显示视频。
            # 这个函数的第一个参数是媒体播放器的指针，第二个参数是窗口句柄。
            self.player.set_hwnd(self.frame.winId())
            # 播放视频
            self.player.play()

# 如果是主模块
if __name__ == "__main__":
    # 创建一个QApplication对象，传入系统参数
    app = QApplication(sys.argv)
    #sys.argv 是一个列表，它包含了从命令行传递给Python程序的参数


    # 创建一个Player对象
    player = Player()
    # 显示窗口
    player.show()
    # 进入事件循环
    # 用于启动Qt应用程序的主循环，并在应用程序结束时退出Python解释器。
    # 主循环是一个无限循环，它负责处理用户的输入事件，如鼠标点击、键盘按键等，并更新应用程序的界面。
    # app.exec()方法会返回一个整数值，表示应用程序的退出状态。
    # sys.exit()函数会将这个值作为参数，传递给操作系统，以便其他程序可以根据这个值判断应用程序是否正常退出。
    sys.exit(app.exec()) 
