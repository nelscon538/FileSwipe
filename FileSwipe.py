import sys
import os
import send2trash
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSizePolicy

class FileOrganizerApp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Organizer")

        self.files = []
        self.current_file_index = 0

        self.layout = QVBoxLayout()

        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.canvas)

        self.filename_label = QLabel()
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.filename_label)

        self.keep_button = QPushButton("Keep")
        self.keep_button.setObjectName("KeepButton")
        self.keep_button.clicked.connect(self.keep_file)
        self.layout.addWidget(self.keep_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.clicked.connect(self.delete_file)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

        self.setMinimumSize(QSize(500, 600))

        self.load_files()
        self.show_current_file()

        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
            }
            QPushButton#KeepButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton#KeepButton:hover {
                background-color: #45a049;
            }
            QPushButton#DeleteButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton#DeleteButton:hover {
                background-color: #d32f2f;
            }
        """)

    def load_files(self):
        directory = QFileDialog.getExistingDirectory(self, "Select a directory")
        for root_dir, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if self.is_valid_file(file_path):
                    self.files.append(file_path)
        self.current_file_index = 0

    def is_valid_file(self, file_path):
        valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]  
        if os.path.isfile(file_path) and not file_path.lower().endswith(tuple(valid_extensions)):
            return False
        return True

    def show_current_file(self):
        if self.current_file_index < len(self.files):
            file_path = self.files[self.current_file_index]
            pixmap = self.load_thumbnail(file_path)
            if pixmap is not None:
                self.canvas.setPixmap(pixmap)
                self.filename_label.setText(os.path.basename(file_path))  

    def load_thumbnail(self, file_path):
        image_reader = QImageReader(file_path)
        image_reader.setAutoTransform(True)
        size = image_reader.size()
        if size.isValid():
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(
                self.canvas.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            return scaled_pixmap

    def keep_file(self):
        self.current_file_index += 1
        self.show_current_file()

    def delete_file(self):
        if self.current_file_index < len(self.files):
            file_path = self.files[self.current_file_index]
            normalized_path = os.path.normpath(file_path)  
            send2trash.send2trash(normalized_path)  
            del self.files[self.current_file_index]
            self.show_current_file()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())
