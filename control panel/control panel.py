import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QSizePolicy, QFrame, QPushButton
)
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtGui import QFont

CSV_PATH = "wyniki.csv"

class FullScreenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pełnoekranowa aplikacja prognozy")
        self.showFullScreen()

        self.setStyleSheet("""
            QTableWidget::item:hover {
                background-color: transparent;
            }
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(10)

        self.setup_header_container()
        self.setup_table_container()


        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)
        self.refresh()
        self.setStyleSheet(self.styleSheet() + "QWidget { background-color: #add8e6; }")

    def setup_header_container(self):
        self.header_container = QFrame()
        self.header_container.setFixedHeight(270)
        header_layout = QHBoxLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(30)

        self.time_frame = QFrame()
        self.time_frame.setFrameShape(QFrame.Box)
        self.time_frame.setLineWidth(4)
        self.time_frame.setFixedSize(400, 240)
        self.time_frame.setStyleSheet("background-color: white;")

        time_layout = QVBoxLayout(self.time_frame)
        time_layout.setContentsMargins(40, 20, 40, 20)
        time_layout.setSpacing(10)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        time_font = QFont()
        time_font.setPointSize(52)
        time_font.setBold(True)
        self.time_label.setFont(time_font)

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        date_font = QFont()
        date_font.setPointSize(24)
        self.date_label.setFont(date_font)

        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.date_label)

        self.update_frame = QFrame()
        self.update_frame.setFrameShape(QFrame.Box)
        self.update_frame.setLineWidth(2)
        self.update_frame.setFixedSize(420, 130)
        self.update_frame.setStyleSheet("background-color: white;")

        update_layout = QVBoxLayout(self.update_frame)
        update_layout.setContentsMargins(20, 20, 20, 20)
        update_layout.setSpacing(10)

        self.update_title = QLabel("Ostatnia aktualizacja")
        self.update_title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.update_title.setFont(title_font)

        self.update_date = QLabel()
        self.update_date.setAlignment(Qt.AlignCenter)
        update_font = QFont()
        update_font.setPointSize(16)
        self.update_date.setFont(update_font)

        update_layout.addWidget(self.update_title)
        update_layout.addWidget(self.update_date)

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                font-size: 20px;
                border: 2px solid black;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: red;
                color: white;
            }
        """)
        self.close_button.clicked.connect(QApplication.quit)

        header_layout.addWidget(self.time_frame, alignment=Qt.AlignLeft | Qt.AlignBottom)
        header_layout.addStretch()
        header_layout.addWidget(self.update_frame, alignment=Qt.AlignBottom)
        header_layout.addStretch()
        header_layout.addWidget(self.close_button, alignment=Qt.AlignTop | Qt.AlignRight)

        self.main_layout.addWidget(self.header_container)

    def setup_table_container(self):
        self.table_container = QFrame()
        self.table_container.setStyleSheet("background-color: white;")
        table_layout = QVBoxLayout(self.table_container)
        table_layout.setContentsMargins(70, 10, 10, 10)  # marginesy 10px z każdej strony
        table_layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.ElideRight)
        self.table.setStyleSheet("background-color: white;")

        table_layout.addWidget(self.table)
        self.main_layout.addWidget(self.table_container)

    def refresh(self):
        self.update_time()
        self.load_csv_and_fill_table()
        self.resize_table()

    def update_time(self):
        now = QDateTime.currentDateTime()
        self.time_label.setText(now.toString("HH:mm"))
        self.date_label.setText(now.toString("yyyy-MM-dd"))

    def load_csv_and_fill_table(self):
        try:
            with open(CSV_PATH, newline='') as csvfile:
                reader = list(csv.reader(csvfile))
                if not reader:
                    self.update_title.setText("BRAK DANYCH W PLIKU CSV")
                    self.update_date.setText("")
                    self.table.clear()
                    return

                last_line = reader[-1]
                year, month, day, hour, minute = last_line[:5]
                self.update_date.setText(f"{hour.zfill(2)}:{minute.zfill(2)} {day.zfill(2)}.{month.zfill(2)}.{year}")

                header_values = ["+3h", "+6h", "+9h", "+12h"]
                left_labels = ["Opady GFS:", "Temperatura:", "Opady stacja:", "Opady Smart AD"]
                data_values = last_line[5:]

                self.table.setRowCount(4)
                self.table.setColumnCount(5)
                self.table.setHorizontalHeaderLabels(["", *header_values])

                for i in range(1, 5):
                    header_item = self.table.horizontalHeaderItem(i)
                    font = header_item.font()
                    font.setBold(True)
                    font.setPointSize(16)
                    header_item.setFont(font)

                for row, label in enumerate(left_labels):
                    item = QTableWidgetItem(label)
                    font = item.font()
                    font.setPointSize(18)
                    font.setBold(True)
                    item.setFont(font)
                    item.setFlags(Qt.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    item.setData(Qt.TextWrapAnywhere, False)
                    self.table.setItem(row, 0, item)

                for row in range(4):
                    for col in range(1, 5):
                        idx = row * 4 + (col - 1)
                        value = data_values[idx] if idx < len(data_values) else ""
                        item = QTableWidgetItem(value)
                        font = item.font()
                        font.setPointSize(16)
                        item.setFont(font)
                        item.setFlags(Qt.ItemIsEnabled)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setData(Qt.TextWrapAnywhere, False)
                        self.table.setItem(row, col, item)

        except Exception as e:
            self.update_title.setText("Błąd wczytywania CSV")
            self.update_date.setText(str(e))
            self.table.clear()

    def resize_table(self):
        scale_factor = 0.9

        total_width = (self.width() - 60) * scale_factor
        min_col_width = 150 * scale_factor

        col0_width = max(300 * scale_factor, total_width // 4)

        rest_width = max(total_width - col0_width, 0)
        col_width = max(min_col_width, rest_width // 4)

        total_needed = col0_width + 4 * col_width
        if total_needed > total_width:
            scale = total_width / total_needed
            col0_width = int(col0_width * scale)
            col_width = int(col_width * scale)

        self.table.setColumnWidth(0, int(col0_width))
        for col in range(1, 5):
            self.table.setColumnWidth(col, int(col_width))

        row_height = max(50, int(self.table.height() * scale_factor) // 4)
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, row_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullScreenApp()
    window.show()
    sys.exit(app.exec())
