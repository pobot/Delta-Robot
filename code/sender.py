#!/usr/bin/env python
from PySide.QtGui import *
from PySide.QtCore import *


class CodeView(QTextEdit):

    def __init__(self):
        super(CodeView,self).__init__()
        #self.cursorPositionChanged.connect(self.__selectLine__)
        #self.selectionChanged.connect(self.__selectLine__)
        self.setReadOnly(True)
               
    def __selectLine__(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.LineUnderCursor) 
        self.setTextCursor(cursor)

    def mouseDoubleClickEvent(self,event):
        super(CodeView,self).mouseDoubleClickEvent(event)
        self.__selectLine__()
        print self.getLineNumber()

    def setSelectedLine(self,position):
        cursor = self.textCursor()
        cursor.movePostion(QTextCursor.Start)
        for x in range(position):
            cursor.movePosition(QTextCursor.Down)
        self.setTextCursor(cursor)

    def getLineNumber(self):
        cursor = self.textCursor()
        return cursor.blockNumber()

    def selectNextLine(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Down)
        self.setTextCursor(cursor)
        self.__selectLine__()

    def selectPreviousLine(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Up)
        self.setTextCursor(cursor)
        self.__selectLine__()


class MainView(QMainWindow):
    
    def __init__(self):
        super(MainView,self).__init__()
        self.initUI()

    def load_file(self,filename):
        f = open(filename,"r")
        doc = QTextDocument(f.read())
        self.code_view.setDocument(doc)

    def initUI(self):
        root_layout = QVBoxLayout()
        central_widget = QWidget()
         
        file_menu = QMenu("File")
        file_menu.addAction("Open")
        run_menu = QMenu("Run")
        run_menu.addAction("Run")
        run_menu.addAction("Stop")
        run_menu.addAction("Reset")
        run_menu.addAction("Step forward")
        run_menu.addAction("Step backward")
        
        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(run_menu)
        self.setMenuBar(menu_bar)    
        self.code_view = CodeView()
        
        self.load_file("test.gcode")
        self.config_ui = ConfigUI()
        root_layout.addWidget(self.config_ui)
        root_layout.setMenuBar(menu_bar)
        root_layout.addWidget(self.code_view)

        button_layout = QHBoxLayout()
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.code_view.selectNextLine)
        prev_button = QPushButton("Prev")
        prev_button.clicked.connect(self.code_view.selectPreviousLine)

        button_layout.addWidget(next_button)
        button_layout.addWidget(prev_button)
        
        root_layout.addLayout(button_layout)
        central_widget.setLayout(root_layout)
        self.setCentralWidget(central_widget)


class ConfigUI(QWidget):

    def __init__(self):
        super(ConfigUI,self).__init__()
        self.initUI()

    def initUI(self):
        root_layout = QHBoxLayout()
        self.port_edit = QLineEdit("/dev/tty")
        #root_layout.addWidget(QLabel("Serial Port"))
        root_layout.addWidget(self.port_edit)
        self.setLayout(root_layout)
        

def main():
    app = QApplication("")
    main_view = MainView()
    main_view.show()
    app.exec_()


if __name__ == "__main__":
    main()
