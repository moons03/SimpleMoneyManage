import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from time import sleep
import subprocess

def create_webview():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setGeometry(100, 100, 500, 650)
    window.setWindowTitle("알뜨리")

    web = QWebEngineView()
    web.setGeometry(0, 0, 500, 650)
    web.load(QUrl('http://127.0.0.1:8000/index.html'))  # 원하는 URL로 변경
    window.setCentralWidget(web)

    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    process = subprocess.Popen(["python", 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(1)
    create_webview()