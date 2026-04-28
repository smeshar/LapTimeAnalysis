import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QFileDialog,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal, QObject, Qt


# Класс для перенаправления логов из консоли в окно приложения
class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

    def flush(self):
        pass


def seconds_to_minutes(time):
    minutes = int(time // 60)
    seconds = time - minutes * 60
    return f"{minutes}:{seconds:.2f}"


class LapTimeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.initUI()

        # Перенаправление stdout (принтов) в QTextEdit
        sys.stdout = Stream(newText=self.onUpdateText)

    def initUI(self):
        self.setWindowTitle("Lap time improvement analysis")
        self.resize(400, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Кнопка загрузки файла
        self.btn_upload = QPushButton("Upload .consumption file")
        self.btn_upload.clicked.connect(self.upload_file)
        layout.addWidget(self.btn_upload)

        self.threshold_label = QLabel("Maximum analyzed lap time (in seconds)")
        self.threshold_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.threshold_label)

        # Поле для ввода threshold time
        self.input_threshold = QLineEdit("")
        self.input_threshold.setPlaceholderText("100.0")
        layout.addWidget(self.input_threshold)

        # Кнопка генерации
        self.btn_generate = QPushButton("Generate")
        self.btn_generate.clicked.connect(self.generate_plot)
        layout.addWidget(self.btn_generate)

        # Поле для вывода логов
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        layout.addWidget(self.output_log)

        self.setLayout(layout)

    def onUpdateText(self, text):
        cursor = self.output_log.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(text)
        self.output_log.setTextCursor(cursor)
        self.output_log.ensureCursorVisible()

    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Consumption File",
            "",
            "Consumption Files (*.consumption);;All Files (*)",
        )
        if file_name:
            self.file_path = file_name
            print(f"File loaded: {os.path.basename(self.file_path)}")

    def generate_plot(self):
        if not self.file_path:
            print("Error: Please upload a file first.")
            return

        try:
            threshold_str = self.input_threshold.text().replace(",", ".")
            threshold = float(threshold_str) if threshold_str else 96.0
        except ValueError:
            print("Error: Invalid threshold time format.")
            return

        print("Starting analysis...")
        self.process_data_and_plot(threshold)

    def process_data_and_plot(self, threshold):
        file_basename = os.path.basename(self.file_path)
        plot_title = os.path.splitext(file_basename)[0]

        try:
            df = pd.read_csv(self.file_path)
            df = df.iloc[::-1].reset_index(drop=True)

            valid_fast_laps = df[
                (df["isValidLap"] == 1) & (df["lapTimeLast"] <= threshold)
            ].copy()

            if valid_fast_laps.empty:
                print("Error: No valid laps found under the specified threshold.")
                return

            valid_fast_laps["session_lap"] = range(1, len(valid_fast_laps) + 1)
            x = valid_fast_laps["session_lap"].values
            y = valid_fast_laps["lapTimeLast"].values

            pb_evolution = valid_fast_laps["lapTimeLast"].cummin().values

            # Тренд
            z_all = np.polyfit(x, y, 2)
            p_all = np.poly1d(z_all)

            z_pb = np.polyfit(x, pb_evolution, 2)
            p_pb = np.poly1d(z_pb)

            # Отрисовка
            plt.figure(figsize=(16, 9), dpi=100)

            plt.plot(
                x,
                y,
                color="#1f77b4",
                alpha=0.3,
                linewidth=1,
                label="All Laps (Pace)",
                zorder=2,
            )
            plt.scatter(x, y, color="#1f77b4", alpha=0.3, s=25, zorder=2)

            plt.plot(
                x,
                pb_evolution,
                color="green",
                linewidth=1.5,
                linestyle="--",
                label="PB Evolution (Steps)",
                zorder=4,
                drawstyle="steps-post",
            )

            plt.plot(
                x,
                p_all(x),
                color="red",
                lw=1.5,
                ls=":",
                alpha=0.6,
                label="Overall Pace Trend",
            )
            plt.plot(
                x,
                p_pb(x),
                color="#9400D3",
                linewidth=4,
                label="PB Improvement Trend",
                zorder=5,
            )

            ax = plt.gca()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

            plt.title(plot_title, fontsize=18, fontweight="bold", pad=20)
            plt.xlabel("Lap Sequence Number", fontsize=14)
            plt.ylabel("Lap Time (seconds)", fontsize=14)

            plt.ylim(pb_evolution.min() - 0.4, threshold + 0.1)
            plt.xlim(0.5, x.max() + 0.5)

            plt.grid(True, which="major", linestyle="-", alpha=0.3, zorder=1)
            plt.grid(True, which="minor", linestyle=":", alpha=0.15, zorder=1)

            plt.legend(loc="upper right", frameon=True, shadow=True, fontsize=12)
            plt.tight_layout()

            # Сохранение файла
            plots_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "plots"
            )
            os.makedirs(plots_dir, exist_ok=True)
            save_path = os.path.join(plots_dir, f"{plot_title}.png")
            plt.savefig(save_path)

            print(f"Plot saved to: {save_path}")

            best_lap = seconds_to_minutes(pb_evolution[-1])
            print(f"Session Best Lap: {best_lap} s")
            print("Analysis complete.")

            plt.show()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LapTimeApp()
    window.show()
    sys.exit(app.exec())
