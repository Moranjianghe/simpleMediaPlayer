# 导入PySide6的相关模块
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget,QScreen
# 导入vlc模块，用于播放视频
import vlc
# 导入sys模块，用于处理系统参数
import sys

# 定义一个Player类，继承自QMainWindow
class Player(QMainWindow):
    # 定义构造函数
    def __init__(self):
        # 调用父类的构造函数
        super().__init__()
        # 设置窗口的标题
        self.setWindowTitle("视频播放器")
        # 设置窗口的位置和大小
        self.setGeometry(100, 100, 800, 600)
        center = QScreen. availableGeometry (QApplication. primaryScreen ()).center ()
        geo = MyPyForm. frameGeometry ()
        MyPyForm. move (geo. topLeft ())
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
            self.player.set_xwindow(self.winId())
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
    sys.exit(app.exec())
