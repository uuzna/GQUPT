import MyGPT
from threading import Thread
import MySignals
from PySide6 import QtWidgets
import datetime
from PySide6.QtCore import Slot, Qt, QFile
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QApplication
# 在命令行窗口或终端中运行designer命令启动Qt Designer。

signal = MySignals.Signals()
old_answer = ''

# 继承QWidget类，以获取其属性和方法
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
          # 加载ui文件
        qfile = QFile(r"GQUPT-V2.0.ui")
        qfile.open(QFile.ReadOnly)

        # 创建ui窗口对象
        self.ui = QUiLoader().load(qfile)
        qfile.close()

        signal.text_print.connect(self.print_to_GUI)
        signal.question_clear.connect(self.clear_question_line)

        self.GPT3 = MyGPT.GPT3()

        # Connect buttons to their corresponding functions
        self.ui.ask_GPT_button.clicked.connect(self.ask_GPT)
        self.ui.clear_button.clicked.connect(self.clear_chat)
        self.ui.new_chat.clicked.connect(self.new_chat)
        self.ui.keep_file.clicked.connect(self.save_file)

        # 窗口置顶
        self.ui.setWindowFlag(Qt.WindowStaysOnTopHint)

    # @Slot("QVariant")
    # def print_to_GUI(self, plainTextEdit, answer):
    #     plainTextEdit.appendPlainText(answer)
    #     plainTextEdit.ensureCursorVisible()
    @Slot("QVariant")
    def print_to_GUI(self, plainTextEdit, answer): 
        if isinstance(plainTextEdit, QPlainTextEdit): 
            plainTextEdit.appendPlainText(answer) 
            plainTextEdit.ensureCursorVisible() 
        else: print("plainTextEdit is not a QPlainTextEdit object")
    
    @Slot("QVariant")
    def clear_question_line(self, question_line):
        clear = ""
        question_line.setPlainText(clear)

    # Button-related functions
    def ask_GPT(self):
        def run():
            text = self.ui.question.toPlainText()
            signal.question_clear.emit(self.ui.question)
            signal.text_print.emit(self.ui.plainTextEdit, '我: ' + text)
            self.ui.ask_GPT_button.setEnabled(False)
            try:
                global old_answer
                gpt_answer = self.GPT3.gpt3(old_answer + text)
                gpt_answer = gpt_answer.strip()  
                print(gpt_answer)
                old_answer = old_answer + 'Q:' + text + ' A:' + gpt_answer
                # print(old_answer)
            except:
                gpt_answer = '-----------------err: 未能成功获取结果-----------------'
                print(gpt_answer)
            signal.text_print.emit(self.ui.plainTextEdit, str('AI: ' + gpt_answer))
            self.ui.ask_GPT_button.setEnabled(True)

        t = Thread(target=run)
        t.start()
    
    def clear_chat(self):
        text = None
        self.ui.plainTextEdit.setPlainText(text)

    def new_chat(self):
        def run():
            text = None
            self.ui.plainTextEdit.setPlainText(text)
            self.ui.new_chat.setEnabled(False)
            global old_answer
            old_answer = '   '
            signal.text_print.emit(self.ui.new_chat, '-------------开始新的对话成功!!!-----------')
            self.ui.new_chat.setEnabled(True)

        t = Thread(target=run)
        t.start()
    
    def save_file(self):
        # get the filename and filepath from the user
        filename = self.ui.fileNameInput.text()
        filepath = self.ui.fileSavePath.text()

        # get the text from the plainTextEdit
        filetext = self.ui.plainTextEdit.toPlainText()

        # generate filename based on current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename_with_timestamp = f"{filename}_{timestamp}.txt"

        # write the text to the file
        if filename and filepath:
            fullpath = os.path.join(filepath, filename_with_timestamp)
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)
            with open(fullpath, 'w') as f:
                f.write(filetext)

            # show a message box to confirm that the file was saved
            QtWidgets.QMessageBox.information(
                self, "File saved", f"File saved as {fullpath}")
        else:
            # show an error message if the filename or filepath is missing
            QtWidgets.QMessageBox.critical(
                self, "Error", "Please enter a filename and select a save directory")

# 程序入口
if __name__ == "__main__":
    app = QApplication([])
    # app.setWindowIcon(QIcon("logo.png"))    # 添加图标
    w = MyWidget()
    w.ui.show()
    app.exec()