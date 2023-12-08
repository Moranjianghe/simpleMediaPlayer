# 导入PySide6的相关模块
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget,QFrame,QHBoxLayout,QSlider,QStyle,QPushButton,QLabel,QMessageBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt,QTime,QTimer 
# 导入vlc模块，用于播放视频
import vlc
# 导入sys模块，用于处理系统参数
import sys

import os

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
        self.mainLayout = QVBoxLayout(self.widget)

        # 创建一个QFrame作为视频的容器
        self.videoFrame = QFrame(self)
        self.videoFrame.mouseDoubleClickEvent = self.mouseDoubleClickVideoFrameEvent
        self.videoFrame.mousePressEvent = self.mousePressVideoFrameEvent

        # 创建一个定时器
        self.videoFrame.timer = QTimer(self) 
         # 设置为单次触发
        self.videoFrame.timer.setSingleShot(True)
        # 连接到单击事件的函数
        self.videoFrame.timer.timeout.connect(self.videoFrameSingle_click) 
         # 获取系统的双击间隔时间
        self.videoFrameDouble_click_interval = QApplication.doubleClickInterval()
        # 设置定时器的间隔时间为双击间隔时间
        self.videoFrame.timer.setInterval(self.videoFrameDouble_click_interval) 

        # 设置QFrame的背景颜色为黑色
        self.videoFrame.setStyleSheet("background-color: black;")
        # 将QFrame添加到布局中
        self.mainLayout.addWidget(self.videoFrame)

        # 创建一个QWidget作为控制工具的容器
        self.controlWidget = QWidget(self)
        self.mainLayout.addWidget(self.controlWidget)
        # 设置其最大高度为50，没有边框
        self.controlWidget.setMaximumHeight(50)
        self.controlWidget.setContentsMargins(0, 0, 0, 0)

        # 创建一个水平布局
        self.controlLayout = QHBoxLayout(self.controlWidget)

        # 创建一个QPushButton作为暂停/播放按钮
        self.playButton = QPushButton(self.controlWidget)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # 修改了这里，使用lambda表达式，否则会直接调用play_pause函数，而不是等待点击事件
        #self.playButton.clicked.connect(self.play_pause())
        self.playButton.clicked.connect(lambda: self.play_pause())
        self.controlLayout.addWidget(self.playButton)

        # 创建一个QSlider作为进度条
        self.positionSlider = QSlider(Qt.Horizontal, self.controlWidget)
        #self.positionSlider.sliderMoved.connect(self.setPosition)
        # 修改了这里，使用lambda表达式，否则会直接调用setPosition函数，而不是等待滑动事件
        # self.positionSlider.valueChanged.connect(lambda: self.setPosition(self.positionSlider.value()))
        # 使用 valueChanged 会在进度条更新时发生卡顿，改为 sliderMoved
        self.positionSlider.sliderMoved.connect(lambda: self.setPosition(self.positionSlider.value()))
        self.controlLayout.addWidget(self.positionSlider)

        # 创建一个QLabel作为当前时间和总时间的显示
        self.timeLabel = QLabel("00:00 / 00:00", self.controlWidget)
        self.controlLayout.addWidget(self.timeLabel)

        # 创建一个QSlider作为音量条
        self.volumeLabel = QLabel("🔊", self.controlWidget) # 添加了一个标签，用于显示音量状态
        self.controlLayout.addWidget(self.volumeLabel)
        self.volumeSlider = QSlider(Qt.Horizontal, self.controlWidget)
        self.volumeSlider.setMaximum(100)
        # 设置初始值为 50 不然视频刚开始没声音
        self.volumeSlider.setValue(50) 
        self.controlLayout.addWidget(self.volumeSlider)
        #self.volumeSlider.valueChanged.connect(self.setVolume)
        # 修改了这里，使用lambda表达式，否则会直接调用setVolume函数，而不是等待滑动事件
        self.volumeSlider.valueChanged.connect(lambda: self.setVolume(self.volumeSlider.value()))


        #不知道为啥这里打开了两次文件，先注释了
        #self.open_file()

        # 打开一个文件对话框，选择要播放的视频文件
        self.open_file()

    # 定义打开文件的方法
    def open_file(self):
        # 调用QFileDialog的静态方法，获取文件路径和过滤器
        #filepath, _ = QFileDialog.getOpenFileName(self, "Open Video")
        # 默认显示视频文件，但也可以选择其他文件
        filepath, _ = QFileDialog.getOpenFileName(self, "Open File", filter="视频文件(*.mp4 *.avi *.mkv *.wmv *.mov *.mpg *.mpeg *.m4v *.3gp *.webm *.flv *.vob *.ogv *.gif);;音频文件(*.mp3 *.m4a *.flac *.wav *.ogg *.aac *.wma *.mid *.midi *.amr *.opus *.aiff);;所有文件 (*)")
        # 如果文件路径不为空
        if not filepath:
            return
         # 添加了一个判断条件，用于检测文件是否存在
        if not os.path.exists(filepath):
            # 如果文件不存在，就弹出一个提示框
                QMessageBox.warning(self, "文件不存在", "你选择的文件不存在或无法打开，请重新选择一个有效的文件。") 
                # 弹出一个警告提示框，标题为"文件不存在"，内容为"你选择的文件不存在或无法打开，请重新选择一个有效的文件。"
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

        #视频播放默认是静音的，需要切换一次，我也不知道为什么
        #好像不是，注释了
        #self.player.audio_toggle_mute()

        #设置一个定时器，每秒更新一次进度条和时间标签
        self.timer = self.startTimer(1000)#单位是好喵
        self.timerEvent(None)


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
        #去掉 layout margin 否则全屏的时候会有白边
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def noFullScreen(self):
        self.setWindowState(Qt.WindowNoState)
        self.controlWidget.show()
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

    #雙擊全屏普通切換
    def mouseDoubleClickVideoFrameEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.isFullScreen():
                self.noFullScreen()
            else:
                self.fullScreen()

    #单擊暂停/继续
    def mousePressVideoFrameEvent(self, event):
        if event.button() == Qt.LeftButton: # 如果是左键点击
            if self.videoFrame.timer.isActive(): # 如果定时器已经启动
                self.videoFrame.timer.stop() # 停止定时器
                self.videoFrameDouble_click() # 执行双击事件的函数
            else: # 如果定时器没有启动
                self.videoFrame.timer.start() # 启动定时器

    def videoFrameSingle_click(self):
        print("单击事件")
        self.play_pause()

    def videoFrameDouble_click(self):
        print("双击事件")
        if self.isFullScreen():
            self.noFullScreen()
        else:
            self.fullScreen()

#    def positionChanged(self, position):
#        # 根据视频的当前位置，更新进度条的值
#        self.positionSlider.setValue(position)
#        # 根据视频的当前位置，更新时间标签的文本
#        currentTime = QTime(0, 0, 0).addMSecs(position)
#        totalTime = QTime(0, 0, 0).addMSecs(self.player.get_length())
#        self.timeLabel.setText(currentTime.toString("mm:ss") + " / " + totalTime.toString("mm:ss"))

#    def durationChanged(self, duration):
#        # 根据视频的总时长，设置进度条的范围
#        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        # 根据进度条的值，设置视频的当前位置
        self.player.set_time(position)


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
        elif event.key() == Qt.Key_M: # 添加了一个快捷键，用于切换静音模式
            self.toggle_mute()
        else:
            super().keyPressEvent(event)


    # 定义一个方法，用于暂停和恢复视频播放
    def play_pause(self):
        # 如果视频正在播放，那么暂停视频，并设置按钮的文本为“播放”
        if self.player.is_playing():
            self.player.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
#            self.button.setText("播放")
        # 如果视频已经暂停，那么恢复视频，并设置按钮的文本为“暂停”
        else:
            self.player.play()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
#            self.button.setText("暂停")

    def setVolume(self, volume):
        # 根据音量条的值，设置视频的音量
        self.player.audio_set_volume(volume)

    # 添加了这里，定义一个定时器事件，用于更新进度条和时间标签
    def timerEvent(self, event):
        if self.player.is_playing():
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # 获取当前的播放位置和总时长，单位是毫秒
        # GPT 弄混了 time 和 position 这两个类似但不同的方法，
        # position 返回的是一个 0~1 的浮点数，
        # 而 time 返回的才是毫秒
        # 这导致我在这个问题上卡了很久
        position = self.player.get_time()
        duration = self.player.get_length()

        # 如果总时长不为0，更新进度条的最大值和当前值
        if duration > 0:
            self.positionSlider.setMaximum(duration)
            self.positionSlider.setValue(position)
            print("duration="+str(duration))
            print("position="+str(position))

        # 将毫秒转换为时分秒的格式
        currentTime = QTime(0, 0, 0).addMSecs(position)
        totalTime = QTime(0, 0, 0).addMSecs(duration)

        # 更新时间标签的文本
        self.timeLabel.setText(currentTime.toString("hh:mm:ss") + " / " + totalTime.toString("hh:mm:ss"))

    def toggle_mute(self): # 添加了一个方法，用于切换静音模式
        self.player.audio_toggle_mute() # 调用播放器的方法，切换静音状态
        if not self.player.audio_get_mute(): # 判断当前是否是静音状态
            self.volumeLabel.setText("🔇") # 如果是静音，就显示一个静音的图标
        else:
            self.volumeLabel.setText("🔊") # 如果不是静音，就显示一个正常的图标
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
