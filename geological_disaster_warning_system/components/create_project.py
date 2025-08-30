# components/project_form_dialog.py
import logging
import os
import sqlite3

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QCheckBox, QGroupBox,
    QScrollArea, QPushButton, QMessageBox, QFrame, QFileDialog
)
from PySide6.QtCore import Qt, Signal, QFile
import json

from components.loading_spinner import LoadingSpinner
from components.task_worker import TaskWorker


class ProjectFormDialog(QDialog):
    # 自定义信号（可选，也可以直接通过 exec 后获取数据）
    project_created = Signal(str, str)  # 成功：项目名, 文件路径
    project_creation_failed = Signal(str)  # 失败：错误信息

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建项目")
        self.resize(500, 450)

        # 数据
        self.data_map = {}
        self.selected_lines = []

        # 加载数据
        self.data_map = self.load_data_from_resource(":/resources/railway_lines_index.json")
        if not self.data_map :
            QMessageBox.critical(self, "错误", "无法加载线路数据，请检查资源文件！")
            self.reject()  # 直接关闭对话框

        self.init_ui()

    def load_text_from_resource(self, resource_path):
        file = QFile(resource_path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            logging.error(f"无法打开资源文件: {resource_path}")
            return None
        byte_array = file.readAll()
        file.close()
        try:
            # 尝试用 UTF-8 解码
            return str(byte_array, "utf-8")
        except Exception as e:
            logging.error(f"解码资源文件失败: {resource_path}, 错误: {e}")
            return None

    def load_data_from_resource(self, resource_path):
        file = QFile(resource_path)
        if not file.open(QFile.ReadOnly):
            return False
        byte_array = file.readAll()
        file.close()
        try:
            json_str = str(byte_array, "utf-8")
            return json.loads(json_str)
        except Exception as e:
            logging.error(f"加载数据失败: {e}")
            return None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 第一行：项目名称
        name_layout = QHBoxLayout()
        name_label = QLabel("请输入项目名称：")
        name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("例如：西南铁路项目")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # 第二行：选择线路
        line_layout = QHBoxLayout()
        line_label = QLabel("请选择线路分类：")
        line_label.setFixedWidth(120)
        self.combo_box = QComboBox()
        self.combo_box.addItems(self.data_map.keys())
        self.combo_box.currentTextChanged.connect(self.update_checkboxes)
        line_layout.addWidget(line_label)
        line_layout.addWidget(self.combo_box)
        layout.addLayout(line_layout)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # 第三行：复选框区域（带滚动）
        self.checkbox_group = QGroupBox("请选择线路（可多选）")
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_group.setLayout(self.checkbox_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.checkbox_group)
        scroll_area.setMinimumHeight(180)
        layout.addWidget(scroll_area)

        path_layout = QHBoxLayout()
        path_label = QLabel("保存路径：")
        path_label.setFixedWidth(120)
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("请选择项目保存的文件夹")
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.setFixedWidth(80)

        self.browse_btn.clicked.connect(self.select_folder)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton("取消")
        self.create_btn = QPushButton("创建项目")

        self.create_btn.setDefault(True)  # 回车默认触发
        self.create_btn.setAutoDefault(True)

        self.cancel_btn.clicked.connect(self.reject)
        self.create_btn.clicked.connect(self.on_create)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.create_btn)

        layout.addLayout(btn_layout)

        # 初始化复选框
        self.update_checkboxes(self.combo_box.currentText())

        self._current_worker = TaskWorker()
        self._current_worker.finished.connect(self.on_save_done)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择项目保存文件夹",
            "",  # 默认路径（空表示使用系统默认）
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.path_input.setText(folder)

    def on_save_done(self, result):
        spinner = LoadingSpinner.instance()
        spinner.stop_animate()  # 动画结束
        if result.get("success"):
            file_path = result["file_path"]
            project_name = result["project_name"]
            self.project_created.emit(project_name, file_path)  # 发送成功信号
            self.accept()  # 关闭对话框
        else:
            error_msg = result["error"]
            self.project_creation_failed.emit(error_msg)  # 发送失败信号
            QMessageBox.critical(self, "创建失败", f"无法创建项目：\n{error_msg}")


    def update_checkboxes(self, key):
        for i in reversed(range(self.checkbox_layout.count())):
            widget = self.checkbox_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        items = self.data_map.get(key, [])
        for item in items:
            cb = QCheckBox(item)
            self.checkbox_layout.addWidget(cb)

    def get_project_name(self):
        return self.name_input.text().strip()

    def get_selected_lines(self):
        checked = []
        for i in range(self.checkbox_layout.count()):
            widget = self.checkbox_layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                checked.append(widget.text())
        return checked

    def create_project_thread(self,name,lines,save_dir):
        tmp_railway_data = self.load_data_from_resource(":/resources/railway_lines.json")
        selected_data = {}
        for line_name in lines:
            if line_name in tmp_railway_data:
                selected_data[line_name] = tmp_railway_data[line_name]
            else:
                logging.warning(f"线路未找到: {line_name}")

        print(selected_data)

        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_name:
            raise Exception("项目名称无效，无法生成文件名")
        db_path = os.path.join(save_dir, f"{safe_name}.gdws")

        # 检查是否已存在
        if os.path.exists(db_path):
            raise FileExistsError(f"项目文件已存在：\n{db_path}")
        try:
            # 连接 SQLite 数据库（文件会自动创建）
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # ========================
            # STEP 1: 创建主表结构
            # ========================

            # self._create_main_tables(cursor)
            schema_sql = """
            DROP TABLE IF EXISTS `railway_line_dict`;
            CREATE TABLE railway_line_dict (
                id INTEGER PRIMARY KEY,
                "线路" TEXT NOT NULL
            );
            DROP TABLE IF EXISTS `train_station_dict`;
            CREATE TABLE train_station_dict (
                id INTEGER PRIMARY KEY,
                "火车站ID"  INTEGER NOT NULL,
                "线路ID"  INTEGER NOT NULL,
                "火车站名" TEXT NOT NULL
            );
            """
            cursor.executescript(schema_sql)

            # ========================
            # STEP 2: 插入线路和站点数据
            # ========================
            line_id_map = {}
            # 插入线路
            for line_name in selected_data:
                cursor.execute("INSERT INTO railway_line_dict (线路) VALUES (?)", (line_name,))
                line_id_map[line_name] = cursor.lastrowid

            # 插入站点
            station_data = []
            for line_name, stations in selected_data.items():
                line_id = line_id_map[line_name]
                sorted_stations = sorted(stations.items(), key=lambda x: int(x[0]))
                for station_id, station_name in sorted_stations:
                    station_data.append((int(station_id), line_id,station_name))

            cursor.executemany(
                "INSERT INTO train_station_dict (火车站ID, 线路ID, 火车站名) VALUES (?, ?, ?)",
                station_data
            )

            # ========================
            # STEP 3: 执行外部 .sql 脚本
            # ========================
            sql_script = self.load_text_from_resource(":/resources/menu_content_release.sql")
            if sql_script is None:
                raise Exception("无法加载 menu_content_release.sql 脚本文件")
            if isinstance(sql_script, bytes):
                sql_script = sql_script.decode('utf-8')
            cursor.executescript(sql_script)
            logging.info("创建menu_content_release结束-----开始创建release")
            sql_script = self.load_text_from_resource(":/resources/release.sql")
            if sql_script is None:
                raise Exception("无法加载 release.sql 脚本文件")
            if isinstance(sql_script, bytes):
                sql_script = sql_script.decode('utf-8')
            cursor.executescript(sql_script)


            # 提交并关闭
            conn.commit()
            conn.close()
            self.db_path = db_path
            logging.info(f"SQLite 数据库已保存至: {db_path}")
            return {
                "success": True,
                "file_path": db_path,
                "project_name": name
            }

        except Exception as e:
            # 如果失败且文件已创建，删除残损文件
            conn.commit()
            conn.close()
            if os.path.exists(db_path):
                try:
                    os.remove(db_path)
                except:
                    pass
            logging.exception("保存 SQLite 数据库失败")
            return {
                "success": False,
                "error": str(e)
            }


    def on_create(self):
        name = self.get_project_name()
        lines = self.get_selected_lines()
        save_dir = self.path_input.text().strip()

        if not name:
            QMessageBox.warning(self, "输入错误", "请输入项目名称！")
            self.name_input.setFocus()
            return

        if not lines:
            QMessageBox.warning(self, "选择错误", "请至少选择一条线路！")
            return

        if not os.path.isdir(save_dir):
            QMessageBox.critical(self, "路径错误", "所选路径无效，请重新选择！")
            return

        self._current_worker.set_task(lambda: self.create_project_thread(name,lines,save_dir))
        self._current_worker.start()
        spinner = LoadingSpinner.instance()
        spinner.start_animate("正在创建数据库，这个过程可能需要几分钟...")

        # 打印输出（你可以改为保存逻辑）
        # print("=" * 50)
        # print("📋 新建项目信息")
        # print(f"项目名称: {name}")
        # print("选中线路:")
        # for line in lines:
        #     print(f"  - {line}")
        # print("=" * 50)


        # # 设置结果（供调用方获取）
        self.selected_project_name = name
        # self.selected_lines = lines

        # # 发出信号
        # self.project_created.emit(name, lines)

        # # 接受并关闭
        # self.accept()  # 返回 QDialog.Accepted


    # -------------------- 供外部调用获取数据 --------------------
    def get_result(self):
        """
        调用示例：
        if dialog.exec() == QDialog.Accepted:
            name, lines = dialog.get_result()
        """
        return getattr(self, "selected_project_name", ""), getattr(self, "db_path", "")