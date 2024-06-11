import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QTableView, QWidget
import seaborn as sns

from PyQt5.QtCore import QAbstractTableModel, Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Library.text_reports import *


BOOKS = pd.read_excel('./Data/data.xlsx')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/main.ui', self)

        self.graphic_report.clicked.connect(self.open_graphic_report)

        self.dataset_view = self.findChild(QPushButton, 'dataset_view')
        self.dataset_view.clicked.connect(self.show_dataset_view)

        self.text_reports = self.findChild(QPushButton, 'text_reports')
        self.text_reports.clicked.connect(self.open_text_reports)

    def show_dataset_view(self):
        self.dataset_window = DatasetView(BOOKS)
        self.dataset_window.show()

    def open_graphic_report(self):
        self.graphic_window = GraphicReportView()
        self.graphic_window.show()

    def open_text_reports(self):
        self.text_reports_window = TextReportsView()
        self.text_reports_window.show()


class TextReportsView(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/text_reports.ui', self)
        self.tr1 = self.findChild(QPushButton, 'tr1')
        self.tr1.clicked.connect(self.tr1_clicked)

        self.tr2 = self.findChild(QPushButton, 'tr2')
        self.tr2.clicked.connect(self.tr2_clicked)

        self.tr3 = self.findChild(QPushButton, 'tr3')
        self.tr3.clicked.connect(self.tr3_clicked)

        self.tr4 = self.findChild(QPushButton, 'tr4')
        self.tr4.clicked.connect(self.tr4_clicked)

    def tr1_clicked(self):
        self.text_report1_view = TextReportView12(1)
        self.text_report1_view.show()

    def tr2_clicked(self):
        self.text_report2_view = TextReportView12(2)
        self.text_report2_view.show()

    def tr3_clicked(self):
        self.text_report3_view = TextReportView34(get_average_rating_by_country(BOOKS))
        self.text_report3_view.show()

    def tr4_clicked(self):
        self.text_report4_view = TextReportView34(get_average_price_per_year(BOOKS, 2009, 2019))
        self.text_report4_view.show()


class TextReportView12(QDialog):
    def __init__(self, num):
        super().__init__()
        uic.loadUi('Scripts/text_report.ui', self)
        self.num = num
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)

    def bulid_btn_clicked(self):
        # Настройка QTableView
        N = self.nLine.toPlainText()
        try:
            if 2 <= int(N) <= 550:
                self.text_report_view = self.findChild(QTableView, 'text_report_view')
                if self.num == 1:
                    self.df = get_most_expensive_books(BOOKS, int(N))
                elif self.num == 2:
                    self.df = get_most_discussed_authors(BOOKS, int(N))
                self.model = PandasModel(self.df)
                self.text_report_view.setModel(self.model)

        except Exception as ex:
            pass


class TextReportView34(QDialog):
    def __init__(self, df):
        super().__init__()
        uic.loadUi('Scripts/text_report3.ui', self)
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)
        self.df = df

    def bulid_btn_clicked(self):
        # Настройка QTableView
        self.text_report_view = self.findChild(QTableView, 'text_report_view')
        self.model = PandasModel(self.df)
        self.text_report_view.setModel(self.model)


class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            elif orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None


class DatasetView(QDialog):
    def __init__(self, df):
        super().__init__()
        uic.loadUi('Scripts/dataset_.ui', self)

        # Настройка QTableView
        self.dataset_view = self.findChild(QTableView, 'dataset_view')
        self.model = PandasModel(df)
        self.dataset_view.setModel(self.model)


class GraphicReportView(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/graphic_reports.ui', self)
        self.kach_kach.clicked.connect(self.kach_kach_clicked)
        self.kol_kach.clicked.connect(self.kol_kach_clicked)
        self.baw_kol_kach.clicked.connect(self.baw_kol_kach_clicked)
        self.twokol_kach.clicked.connect(self.twokol_kach_clicked)

    def kach_kach_clicked(self):
        self.kach_kach_window = GraphicsReport_kach_kach()
        self.kach_kach_window.show()

    def kol_kach_clicked(self):
        self.kol_kach_window = GraphicsReport_kol_kach()
        self.kol_kach_window.show()

    def baw_kol_kach_clicked(self):
        self.baw_kol_kach_window = GraphicsReport_baw_kol_kach()
        self.baw_kol_kach_window.show()

    def twokol_kach_clicked(self):
        self.twokol_kach_window = GraphicsReport_twokol_kach()
        self.twokol_kach_window.show()


class GraphicsReport_twokol_kach(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/2kol_kach_window.ui', self)
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)

    def bulid_btn_clicked(self):
        selected_text = self.comboBox.currentText().split(' - ')
        first_param, second_param, third_param = selected_text[0], selected_text[1], selected_text[2]
        print(first_param, second_param, third_param)
        self.build_window = GraphicsReport_twokol_kach_View(first_param, second_param, third_param)
        self.build_window.show()


# Класс для отображения графика
class GraphicsReport_twokol_kach_View(QWidget):
    def __init__(self, first_param, second_param, third_param, parent=None):
        super().__init__(parent)
        self.first_param = first_param
        self.second_param = second_param
        self.third_param = third_param
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Создаем холст (canvas)
        self.canvas = MplCanvas(self)
        self.layout.addWidget(self.canvas)

        # Строим график
        self.plot()

    def plot(self):
        self.canvas.axes.clear()
        data = {
            self.first_param: BOOKS[self.first_param],
            self.second_param: BOOKS[self.second_param],
            self.third_param: BOOKS[self.third_param]
        }

        df = pd.DataFrame(data)

        # Построение диаграммы рассеивания
        sns.scatterplot(x=self.first_param, y=self.second_param, hue=self.third_param, data=df, ax=self.canvas.axes)
        self.canvas.axes.set_xlabel(self.first_param)
        self.canvas.axes.set_ylabel(self.second_param)
        self.canvas.axes.set_title(f'Categorized Scatter Plot for Numeric Attributes by {self.third_param}')

        # Обновление холста
        self.canvas.draw()


class GraphicsReport_baw_kol_kach(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/kol_kach_baw_window.ui', self)
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)

    def bulid_btn_clicked(self):
        selected_text = self.comboBox.currentText().split(' - ')
        first_param, second_param = selected_text[0], selected_text[1]
        print(first_param, second_param)
        self.build_window = GraphicsReport_baw_kol_kach_View(first_param, second_param)
        self.build_window.show()


# Класс для отображения графика
class GraphicsReport_baw_kol_kach_View(QWidget):
    def __init__(self, first_param, second_param, parent=None):
        super().__init__(parent)
        self.first_param = first_param
        self.second_param = second_param
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Создаем холст (canvas)
        self.canvas = MplCanvas(self)
        self.layout.addWidget(self.canvas)

        # Строим график
        self.plot()

    def plot(self):
        self.canvas.axes.clear()
        data = {
            self.first_param: BOOKS[self.first_param],
            self.second_param: BOOKS[self.second_param]
        }

        df = pd.DataFrame(data)
        # Построение боксплота
        df.boxplot(column=self.first_param, by=self.second_param, vert=False, ax=self.canvas.axes)
        self.canvas.axes.set_xlabel(self.first_param)
        self.canvas.axes.set_ylabel(self.second_param)
        self.canvas.axes.set_title(
            f'Categorized Box-and-Whiskers Diagram for {self.first_param} by {self.second_param}')

        # Обновление холста
        self.canvas.draw()


class GraphicsReport_kach_kach(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/kach_kach_window.ui', self)
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)

    def bulid_btn_clicked(self):
        selected_text = self.comboBox.currentText().split(' - ')
        first_param, second_param = selected_text[0], selected_text[1]
        self.build_window = GraphicsReport_kach_kach_View(first_param, second_param)
        self.build_window.show()


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphicsReport_kach_kach_View(QDialog):
    def __init__(self, first_param, second_param):
        super().__init__()
        self.first_param = first_param
        self.second_param = second_param

        self.setWindowTitle('Качественный-Качественный')
        self.setGeometry(100, 100, 800, 600)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Пример данных и создание DataFrame
        data = {
            self.first_param: BOOKS[self.first_param],
            self.second_param: BOOKS[self.second_param]
        }
        df = pd.DataFrame(data)
        # Исключение данных по стране "США"
        df = df[df[self.first_param] != 'USA']
        df = df[df[self.second_param] != 'USA']
        count_data = df.groupby([self.first_param, self.second_param]).size().unstack()

        # Создание кластеризованной столбчатой диаграммы
        count_data.plot(kind='bar', stacked=False, ax=sc.axes)
        sc.axes.set_xlabel(self.first_param)
        sc.axes.set_ylabel(self.second_param)
        sc.axes.set_title(f'Clustered Bar Chart for {self.first_param} and {self.second_param}')
        sc.axes.legend(title=self.second_param)

        layout = QVBoxLayout()
        layout.addWidget(sc)

        self.setLayout(layout)


class GraphicsReport_kol_kach(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Scripts/kol_kach_window.ui', self)
        self.bulid_btn.clicked.connect(self.bulid_btn_clicked)

    def bulid_btn_clicked(self):
        selected_text = self.comboBox.currentText().split(' - ')
        first_param, second_param = selected_text[0], selected_text[1]

        self.build_window = GraphicsReport_kol_kach_View(first_param, second_param)
        self.build_window.show()


class GraphicsReport_kol_kach_View(QDialog):
    def __init__(self, first_param, second_param):
        super().__init__()
        self.first_param = first_param
        self.second_param = second_param

        self.setWindowTitle('Количественный-Качественный')
        self.setGeometry(100, 100, 800, 600)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Пример данных и создание DataFrame
        data = {
            self.first_param: BOOKS[self.first_param],
            self.second_param: BOOKS[self.second_param]
        }
        df = pd.DataFrame(data)

        if 'Country' in (self.first_param, self.second_param):
            df = df[df['Country'] != 'USA']

        for category in df[self.second_param].unique():
            subset = df[df[self.second_param] == category]
            sc.axes.hist(subset[self.first_param], alpha=0.5, label=category)

        sc.axes.set_xlabel(self.first_param)
        sc.axes.set_ylabel('Frequency')
        sc.axes.set_title(f'Categorized Histogram for {self.first_param} by {self.second_param}')
        sc.axes.legend(title=self.second_param)

        layout = QVBoxLayout()
        layout.addWidget(sc)
        self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
