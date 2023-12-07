# 导入PySide6的相关模块
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget,QFrame,QHBoxLayout
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
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
#        self.maximized = False # 用一个变量记录窗口是否最大化

    # 定义创建用户界面的方法
    def create_ui(self):
        # 创建一个QWidget作为中心部件
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # 创建一个垂直布局
        self.mainLayout = QVBoxLayout()
        self.widget.setLayout(self.mainLayout)


        # 创建一个QFrame作为视频的容器
        self.videoFrame = QFrame(self)
        self.videoFrame.mouseDoubleClickEvent = self.mouseDoubleClickVideoFrameEvent
        # 设置QFrame的背景颜色为黑色
        self.videoFrame.setStyleSheet("background-color: black;")
        # 将QFrame添加到布局中
        self.mainLayout.addWidget(self.videoFrame)


        # 创建一个 wigit 作为控制工具的容器
        self.controlWidget = QWidget(self)
        self.mainLayout.addWidget(self.controlWidget)        
        #設置其最大高度為 50，沒有邊框
        self.controlWidget.setMaximumHeight(50)


        



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
            # 创建一个vlc媒体对象，并且禁用按键和键盘，
            # 此处如果按键与键盘不禁用，会导致双击事件被 vlc 带走
            # 传入文件路径
            self.media = self.vlc_instance.media_new(filepath)
            self.player.set_media(self.media)
            self.player.video_set_key_input(False)
            self.player.video_set_mouse_input(False)

            # 将媒体对象设置给播放器
            self.player.set_media(self.media)
            # 将窗口的ID设置给播放器，用于显示视频
            #libvlc_media_player_set_hwnd是一个vlc库提供的函数，
            # 它的作用是将一个win32/win64窗口句柄设置给媒体播放器，用于显示视频。
            # 这个函数的第一个参数是媒体播放器的指针，第二个参数是窗口句柄。
            self.player.set_hwnd(self.videoFrame.winId())
            # 播放视频
            self.player.play()


#    def mouseDoubleClickEvent(self, event):
        # 调用自定义的函数切换窗口状态
#        self.maximize_restore()

 #   def maximize_restore(self):
  #      # 如果窗口是最大化状态，就恢复正常大小，并设置变量为False
   #     if self.maximized:
    #        self.showNormal()
     #       self.maximized = False
        # 否则就最大化窗口，并设置变量为True
      #  else:
        #    self.showMaximized()
       #     self.maximized = True
        
    #全屏/普通切換
    def fullScreen(self):
        self.controlWidget.hide()
        self.setWindowState(Qt.WindowFullScreen)

    def noFullScreen(self):
        self.setWindowState(Qt.WindowNoState)
        self.controlWidget.show()

    #雙擊全屏普通切換
    def mouseDoubleClickVideoFrameEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.isFullScreen():
                self.noFullScreen()
            else:
                self.fullScreen()


    # 定义一个方法，用于更新滑动条的值
    def update_position(self):
        # 获取视频的当前位置，是一个 0 到 1 之间的小数
        position = self.player.get_position()
        # 将位置转换为一个 0 到 1000 之间的整数
        position = int(position * 1000)
        # 设置滑动条的值为位置
        self.slider.setValue(position)

    # 定义一个方法，用于根据滑动条的值设置视频的位置
    def set_position(self, position):
        # 将位置转换为一个 0 到 1 之间的小数
        position = position / 1000.0
        # 设置视频的位置
        self.player.set_position(position)

# 重写 keyPressEvent 方法，用于捕捉按键事件
    def keyPressEvent(self, event):
        # 如果按下的是空格键，那么暂停或恢复视频播放
        if event.key() == Qt.Key_Space:
            self.play_pause()
        # 如果按下的是 F 键，那么切换全屏模式
        elif event.key() == Qt.Key_F:
            self.fullScreen()
        # 如果按下的是 Esc 键，那么退出全屏模式
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
        # 否则，调用父类的方法
        else:
            super().keyPressEvent(event)


    # 定义一个方法，用于暂停和恢复视频播放
    def play_pause(self):
        # 如果视频正在播放，那么暂停视频，并设置按钮的文本为“播放”
        if self.player.is_playing():
            self.player.pause()
            self.button.setText("播放")
        # 如果视频已经暂停，那么恢复视频，并设置按钮的文本为“暂停”
        else:
            self.player.play()
            self.button.setText("暂停")

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
