# pearson3_plot_widget.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGraphicsView, QComboBox
)
from PySide6.QtCore import Qt
from docutils.nodes import title
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import math

from matplotlib.ticker import FixedLocator, ScalarFormatter
from scipy.optimize import root_scalar
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

class PearsonIIIModule(QWidget):
    # 设置中文字体和解决负号显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei', 'FangSong', 'KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题
    def __init__(self):
        super().__init__()
        self.setWindowTitle("皮尔逊III型分布 PDF 曲线")
        self.resize(800, 600)

        self.mean_input = QLineEdit()
        self.cv_input = QLineEdit()
        self.cs_input = QLineEdit()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.x_input = QLineEdit()
        self.result_label = QLabel("暂无频率数据，请输入降雨量")
        self.result_cdf_label = QLabel("暂无累积频率数据，请输入降雨量")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 参数输入区域
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("样本平均值:"))
        form_layout.addWidget(self.mean_input)
        form_layout.addWidget(QLabel("变差系数Cv:"))
        form_layout.addWidget(self.cv_input)
        form_layout.addWidget(QLabel("偏态系数Cs:"))
        form_layout.addWidget(self.cs_input)

        self.dist_type_combo = QComboBox()
        self.dist_type_combo.addItems(["显示瞬时频率曲线", "显示累积频率曲线"])
        layout.addWidget(QLabel("分布类型:"))
        layout.addWidget(self.dist_type_combo)

        apply_button = QPushButton("应用参数")
        apply_button.clicked.connect(self.plot_distribution)
        # X 输入区域
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("输入降雨量:"))
        x_layout.addWidget(self.x_input)
        calc_button = QPushButton("计算频率")
        calc_button.clicked.connect(self.calculate_fx)
        x_layout.addWidget(calc_button)


        result_layout = QHBoxLayout()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(QLabel("累积频率:"))
        result_layout.addWidget(self.result_cdf_label)

        layout.addLayout(form_layout)
        layout.addWidget(apply_button)


        layout.addLayout(x_layout)
        layout.addLayout(result_layout)

        # 新增频率反查部分
        p_layout = QHBoxLayout()
        self.p_input = QLineEdit()
        p_label = QLabel("输入频率 (%):")
        lookup_button = QPushButton("查降雨量")

        p_layout.addWidget(p_label)
        p_layout.addWidget(self.p_input)
        p_layout.addWidget(lookup_button)

        # 新增结果显示标签
        self.result_lookup_label = QLabel("暂无结果，请输入频率")
        p_layout.addWidget(self.result_lookup_label)

        layout.addLayout(p_layout)

        # 绑定事件
        lookup_button.clicked.connect(self.lookup_x_by_frequency)




        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def compute_pdf(self, x, rain, cv, cs):
        alpha = 4 / (cs * cs)
        beta = 2 / (rain * cv * cs)
        a0 = rain * (1 - 2 * cv / cs)

        if x <= a0:
            return 0.0

        gamma_alpha = math.gamma(alpha)
        fx = ((beta ** alpha) / gamma_alpha) * ((x - a0) ** (alpha - 1)) * math.exp(-beta * (x - a0))
        return fx

    def plot_distribution(self):
        try:
            mean = float(self.mean_input.text())
            cv = float(self.cv_input.text())
            cs = float(self.cs_input.text())
        except ValueError:
            return

        x_min = 0
        x_max = 8 * mean
        x_values = [x_min + i * (x_max - x_min) / 500 for i in range(501)]

        dist_type = self.dist_type_combo.currentText()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        title =""
        if dist_type == "显示瞬时频率曲线":
            y_values = [self.compute_pdf(x, mean, cv, cs) for x in x_values]
            ylabel = f"频率(%)"
            title = f"24小时降雨量频率曲线"
            ax.plot(x_values, y_values, label=f"频率", color='blue')
            ax.set_ylim(bottom=0)

        elif dist_type == "显示累积频率曲线":
            # 计算的是 P(x > X) = 1 - F(x)，并转成百分比
            y_values = [self.compute_cdf_by_integration(x, mean, cv, cs) * 100 for x in x_values]
            ylabel = f"累积频率(%)"
            title = f"24小时累积降雨量频率曲线"
            ax.plot(x_values, y_values, label=f"累积频率", color='green')
            ax.set_ylim(0, 100)  # 设置 y 轴范围为 0-100%

        ax.set_title(title)
        ax.set_xlabel(f"降雨量mm")
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()
        ax.set_xlim(x_min, x_max)

        self.canvas.draw()

    def plot_pdf(self):
        try:
            mean = float(self.mean_input.text())
            cv = float(self.cv_input.text())
            cs = float(self.cs_input.text())
        except ValueError:
            return

        # 计算范围
        # a0 = mean * (1 - 2 * cv / cs)
        # x_min = max(a0, 0)
        # x_max = mean * (1 + 5 * cv)  # 简单扩展绘图范围

        x_min = 0
        x_max = 8 * mean

        x_values = [x_min + i * (x_max - x_min) / 500 for i in range(501)]
        y_values = [self.compute_pdf(x, mean, cv, cs) for x in x_values]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_values, y_values, label="Pearson III PDF", color='blue')
        ax.set_title("Pearson Type III Distribution PDF")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(bottom=0)

        self.canvas.draw()

    def compute_cdf_by_integration(self, x, rain, cv, cs):
        alpha = 4 / (cs * cs)
        beta = 2 / (rain * cv * cs)
        a0 = rain * (1 - 2 * cv / cs)

        if x <= a0:
            return 1.0

        def pdf(x_val):
            if x_val <= a0:
                return 1.0
            gamma_alpha = math.gamma(alpha)
            return ((beta ** alpha) / gamma_alpha) * ((x_val - a0) ** (alpha - 1)) * math.exp(-beta * (x_val - a0))

        # 使用 quad 自适应积分
        cdf_value, error_estimate = quad(pdf, a0, x)
        return 1 - cdf_value  # 返回频率 P(x) = 1 - CDF(x)

    def compute_cdf_by_integration1(self, x, rain, cv, cs, num_points=5120000):
        # 先计算参数
        alpha = 4 / (cs * cs)
        beta = 2 / (rain * cv * cs)
        a0 = rain * (1 - 2 * cv / cs)

        if x <= a0:
            return 0.0
        # 积分区间
        x_start = a0
        x_end = x

        # 生成积分点
        x_values = np.linspace(x_start, x_end, num_points)
        dx = x_values[1] - x_values[0]

        # 计算每个点的 PDF 值
        pdf_values = [self.compute_pdf(xi, rain, cv, cs) for xi in x_values]

        # 数值积分：梯形法或矩形法
        cdf_value = np.trapz(pdf_values, dx=dx)
        return 1-cdf_value

    def compute_x_given_p(self, p, rain, cv, cs):
        """
        已知频率 P(x > X) = p%，返回对应的降雨量 x
        使用数值积分 + 数值求解方法，与 compute_cdf_by_integration 保持一致
        """
        # 定义目标 CDF 值：CDF(x) = 1 - p / 100
        target_cdf = 1.0 - p / 100.0

        if target_cdf <= 0 or target_cdf >= 1:
            return float('nan')  # 超出定义域

        alpha = 4 / (cs * cs)
        beta = 2 / (rain * cv * cs)
        a0 = rain * (1 - 2 * cv / cs)

        def cdf_func(x):
            """ 返回当前 x 对应的 CDF 值（从 a0 到 x 的积分）"""
            if x <= a0:
                return 0.0
            """调用自己的数值积分函数。"""
            integral_value, error_estimate = quad(
                lambda t: self.compute_pdf(t, rain, cv, cs),
                a0,
                x
            )
            return integral_value  # 即 F(x) = P(X ≤ x)

        # 搜索区间 [a0, upper_bound]
        # 设置上限为均值的若干倍，比如 8 倍
        upper_bound = 8 * rain

        try:
            result = root_scalar(
                lambda x: cdf_func(x) - target_cdf,
                bracket=[a0, upper_bound],
                method='brentq'
            )
            x_result = result.root
            return x_result
        except ValueError as e:
            print(f"求解失败: {e}")
            return float('nan')

    def calculate_fx(self):
        try:
            mean = float(self.mean_input.text())
            cv = float(self.cv_input.text())
            cs = float(self.cs_input.text())
            x = float(self.x_input.text())
        except ValueError:
            self.result_label.setText("请输入合法数值！")
            return

        fx = self.compute_pdf(x, mean, cv, cs)
        cdf_value = self.compute_cdf_by_integration(x, mean, cv, cs) *100

        self.result_label.setText(f"f({x:.2f}) = {fx:.6f}")
        self.result_cdf_label.setText(f"P(x > {x:.2f}) = {cdf_value:.2f}%")

        # 绘图更新
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        dist_type = self.dist_type_combo.currentText()

        x_values = [x + dx for dx in np.linspace(-mean, mean, 500)]

        if dist_type == "显示瞬时频率曲线":
            y_values = [self.compute_pdf(xi, mean, cv, cs) for xi in x_values]
            point_y = fx
            ylabel = f"频率"
            title = f"降雨量：{x:.2f} mm 处局部频率曲线"
            ax.set_ylim(bottom=0)

        elif dist_type == "显示累积频率曲线":
            y_values = [( self.compute_cdf_by_integration(xi, mean, cv, cs)) * 100 for xi in x_values]
            point_y = (self.compute_cdf_by_integration(x, mean, cv, cs)) * 100
            ylabel = f"频率(%)"
            title = f"降雨量：{x:.2f} mm 处局部累积频率曲线"
            ax.set_ylim(0, 100)

            # 自动计算 y 轴范围
        y_min = min(y_values)
        y_max = max(y_values)
        y_pad = (y_max - y_min) * 0.1  # 加上 10% 的 padding
        ax.set_ylim(y_min - y_pad, y_max + y_pad)

        ax.plot(x_values, y_values, color='blue', label=f"{dist_type}")
        ax.plot(x, point_y, 'ro', label=f"x = {x:.2f}")
        ax.set_title(title)
        ax.set_xlabel(f"降雨量mm")
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()
        ax.set_xlim(min(x_values), max(x_values))

        self.canvas.draw()

    def lookup_x_by_frequency(self):
        try:
            mean = float(self.mean_input.text())
            cv = float(self.cv_input.text())
            cs = float(self.cs_input.text())
            p = float(self.p_input.text())  # 输入的是百分比频率，如 5%
        except ValueError:
            self.result_lookup_label.setText("请输入合法数值！")
            return

        x = self.compute_x_given_p(p, mean, cv, cs)

        if math.isnan(x) or x <= 0:
            self.result_lookup_label.setText(f"输入频率 {p}% 不在有效范围内")
        else:
            self.result_lookup_label.setText(f"对应降雨量 x = {x:.2f} mm")

        # 可选：在图上高亮该点
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        dist_type = self.dist_type_combo.currentText()

        x_values = [x + dx for dx in np.linspace(-mean, mean, 500)]

        if dist_type == "显示瞬时频率曲线":
            y_values = [self.compute_pdf(xi, mean, cv, cs) for xi in x_values]
            ylabel = "频率 (%)"
            title = "24小时降雨量频率曲线"
            title = f"频率：{p:.2f}%  处局部降雨量频率曲线"
            ax.set_ylim(bottom=0)

        elif dist_type == "显示累积频率曲线":
            y_values = [(self.compute_cdf_by_integration(xi, mean, cv, cs)) * 100 for xi in x_values]
            ylabel = "累积频率 (%)"
            title = "24小时累积降雨量频率曲线"
            title = f"频率：{p:.2f}%  处累积降雨量频率曲线"
            ax.set_ylim(0, 100)

            # 自动计算 y 轴范围
        y_min = min(y_values)
        y_max = max(y_values)
        y_pad = (y_max - y_min) * 0.1  # 加上 10% 的 padding
        ax.set_ylim(y_min - y_pad, y_max + y_pad)
        ax.plot(x_values, y_values, color='blue', label=f"{dist_type}")
        ax.plot(x, y_values[np.argmin([abs(val - x) for val in x_values])], 'go', label=f"x = {x:.2f} mm")
        ax.set_title(title)
        ax.set_xlabel("降雨量 (mm)")
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()
        ax.set_xlim(min(x_values), max(x_values))

        self.canvas.draw()

    def set_parameters(self, mean, cv, cs):
        self.mean_input.setText(str(mean))
        self.cv_input.setText(str(cv))
        self.cs_input.setText(str(cs))

    def get_parameters(self):
        return {
            'mean': float(self.mean_input.text()),
            'cv': float(self.cv_input.text()),
            'cs': float(self.cs_input.text())
        }

    def calculate_pdf(self, x):
        params = self.get_parameters()
        return self.compute_pdf(x, params['mean'], params['cv'], params['cs'])

    def calculate_cdf(self, x):
        params = self.get_parameters()
        return self.compute_cdf_by_integration(x, params['mean'], params['cv'], params['cs'])

    def calculate_x_by_frequency(self,frequency):
        params = self.get_parameters()
        x =self.compute_x_given_p(frequency, params['mean'], params['cv'], params['cs'])
        return round(x, 2)