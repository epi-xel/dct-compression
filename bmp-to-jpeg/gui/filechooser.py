from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

def open_file_chooser(queue):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)   
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('Immagini BMP (*.bmp)')
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            queue.put(selected_files[0])