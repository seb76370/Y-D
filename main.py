import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow,QFileDialog
from PySide6.QtCore import QFile
from interface import Ui_MainWindow
from pytube import YouTube
from slugify import slugify


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.buttondirectory = self.ui.pushButton
        self.buttondownload = self.ui.pushButton_2

        self.buttondirectory.clicked.connect(self.select_directory)
        self.buttondownload.clicked.connect(self.Download_file)
        
        self.progressBar = self.ui.progressBar

        self.directory = ""
        self.label = self.ui.label

        self.groupBox = self.ui.groupBox
        self.mp3 = self.ui.radioButton
        self.mp4 = self.ui.radioButton_2

        # Connexion du signal "toggled" pour récupérer la valeur sélectionnée
        self.mp3.toggled.connect(lambda: self.select_format(self.mp3))
        self.mp4.toggled.connect(lambda: self.select_format(self.mp4))


        self.mp3.setChecked(True)
        self.only_audio = True

        self.url = self.ui.textEdit

    def progress_Check(self,stream,param2,size_downloaded):
        percent  = 100-round(self.percent(size_downloaded,stream.filesize),2)
        self.progressBar.setValue(percent)
    
    def percent(self, tem, total):
            return (float(tem) / float(total)) * float(100)

    def select_format(self,radio_button):
        self.only_audio = radio_button == "MP3"


    def select_directory(self):
        self.directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.label.setText(self.directory)

    def Download_file(self):
        if self.only_audio:
           self.download_audio()
        else:
            self.download_video()


    def download_video(self):
        # url input from user
        yt = YouTube(self.url.toPlainText(), on_progress_callback=self.progress_Check)   
        # path file     
        title = slugify(yt.title)
        path = f"{self.directory}/videos/{title}"

        #download video
        video = yt.streams.filter(progressive = True, file_extension = "mp4").first()
        video.download(output_path=path)

   
    def download_audio(self):
        # url input from user
        yt = YouTube(self.url.toPlainText(), on_progress_callback=self.progress_Check)
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()      
        # path file 
        title = slugify(yt.title)
        path = f"{self.directory}/audios/{title}"
        #download video
        out_file = video.download(output_path=path)
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = f'{base}.mp3'
        os.rename(out_file, new_file)
        print(new_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())