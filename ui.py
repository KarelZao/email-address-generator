from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, \
    QApplication, QMessageBox
from PyQt5.QtGui import QFont, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QLabel, QComboBox, QHBoxLayout

from csv_handler import save_to_csv
from email_generator import generate_emails


class MarginWidget(QWidget):
    def __init__(self, widget, margin):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.addWidget(widget)
        self.setLayout(layout)


class MyTableWidget(QTableWidget):
    def mousePressEvent(self, event):
        self.parent().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.parent().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.parent().mouseReleaseEvent(event)


class EmailGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.mpos = None
        self.skip_prompt = False

        self.initUI()

    def save_to_csv(self):
        if self.text_area.rowCount() > 0:
            save_to_csv(self.text_area)
            self.skip_prompt = True
        else:
            QMessageBox.information(self, "Information", "There are no data to save.", QMessageBox.Ok)

    def initUI(self):
        self.setWindowTitle('Email address generator')
        self.resize(600, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.country_label = QLabel('Choose country for generated email addresses:')
        self.country_label.setFont(QFont("Helvetica", 16))
        main_layout.addWidget(MarginWidget(self.country_label, 20))

        self.country_combobox = QComboBox()
        self.country_combobox.setFont(QFont("Helvetica", 16))
        self.country_combobox.addItems(['France', 'Spain', 'Italy', 'England'])
        main_layout.addWidget(MarginWidget(self.country_combobox, 20))

        self.text_area = MyTableWidget(0, 1)
        self.text_area.horizontalHeader().setVisible(False)
        self.text_area.verticalHeader().setVisible(False)
        self.text_area.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(MarginWidget(self.text_area, 20))

        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate)
        main_layout.addWidget(MarginWidget(self.generate_button, 5))

        self.save_button = QPushButton('Save to CSV')
        self.save_button.clicked.connect(self.save_to_csv)
        main_layout.addWidget(MarginWidget(self.save_button, 5))

        self.clear_button = QPushButton('Clear form')
        self.clear_button.clicked.connect(self.clear)
        main_layout.addWidget(MarginWidget(self.clear_button, 5))

        self.close_button = QPushButton('Close application')
        self.close_button.clicked.connect(self.close_app)
        main_layout.addWidget(MarginWidget(self.close_button, 5))

        font = QFont("Helvetica", 16)
        self.generate_button.setFont(font)
        self.close_button.setFont(font)
        self.save_button.setFont(font)
        self.clear_button.setFont(font)
        self.text_area.setFont(font)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 15, 15)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        self.mpos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mpos:
            diff = event.pos() - self.mpos
            newpos = self.pos() + diff
            self.move(newpos)

    def mouseReleaseEvent(self, event):
        self.mpos = None

    def generate(self):
        self.skip_prompt = False
        country = self.country_combobox.currentText()
        country_code = {'France': 'fr_FR', 'Spain': 'es_ES', 'Italy': 'it_IT', 'England': 'en_GB'}
        emails = generate_emails(country=country_code[country])
        self.text_area.setRowCount(0)
        for i, email in enumerate(emails):
            self.text_area.insertRow(i)
            self.text_area.setItem(i, 0, QTableWidgetItem(email))

    def clear(self):
        self.text_area.clear()
        self.text_area.setRowCount(0)

    def close_app(self):
        if self.text_area.rowCount() > 0 and not self.skip_prompt:
            reply = QMessageBox.question(self, 'Unsaved data!',
                                         'Your session is not saved, do you really wish to end application',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QApplication.instance().quit()
        else:
            QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication([])
    window = EmailGeneratorApp()
    window.show()
    app.exec_()
