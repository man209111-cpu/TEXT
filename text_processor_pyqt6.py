# -*- coding: utf-8 -*-
import sys
import os
import json
import re
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QPushButton, QLabel, QCheckBox, QComboBox,
    QLineEdit, QListWidget, QListWidgetItem, QTextEdit, QStatusBar, QFrame,
    QFileDialog, QMessageBox, QTabWidget, QSpinBox, QGroupBox,
    QButtonGroup, QRadioButton, QDialog, QDialogButtonBox, QScrollArea
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QAction, QColor, QPalette, QBrush


class ThemeManager:
    LIGHT = {
        'bg': '#fafafa',
        'fg': '#212121',
        'card_bg': '#ffffff',
        'card_fg': '#212121',
        'card_border': '#e0e0e0',
        'accent': '#2196F3',
        'accent_hover': '#1976D2',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#f44336',
        'text_bg': '#ffffff',
        'text_fg': '#212121',
        'select_bg': '#E3F2FD',
        'select_fg': '#1565C0',
        'disabled_bg': '#f5f5f5',
        'disabled_fg': '#9e9e9e',
        'scrollbar_bg': '#e0e0e0',
        'scrollbar_thumb': '#bdbdbd',
        'header_bg': '#f5f5f5',
        'header_fg': '#424242',
        'statusbar_bg': '#eeeeee',
        'statusbar_fg': '#616161',
        'button_primary': '#2196F3',
        'button_primary_hover': '#1976D2',
        'button_primary_text': '#ffffff',
        'button_secondary': '#ffffff',
        'button_secondary_hover': '#f5f5f5',
        'button_secondary_text': '#424242',
        'button_secondary_border': '#e0e0e0',
        'danger': '#f44336',
        'danger_hover': '#d32f2f',
        'danger_text': '#ffffff',
        'listbox_bg': '#ffffff',
        'listbox_fg': '#212121',
        'listbox_select_bg': '#BBDEFB',
        'listbox_select_fg': '#0D47A1',
        'entry_bg': '#ffffff',
        'entry_fg': '#212121',
        'entry_border': '#e0e0e0',
        'entry_focus_border': '#2196F3',
        'separator': '#e0e0e0',
    }

    DARK = {
        'bg': '#121212',
        'fg': '#e0e0e0',
        'card_bg': '#1e1e1e',
        'card_fg': '#e0e0e0',
        'card_border': '#2d2d2d',
        'accent': '#64B5F6',
        'accent_hover': '#42A5F5',
        'success': '#66BB6A',
        'warning': '#FFB74D',
        'error': '#EF5350',
        'text_bg': '#1e1e1e',
        'text_fg': '#e0e0e0',
        'select_bg': '#263238',
        'select_fg': '#81D4FA',
        'disabled_bg': '#1e1e1e',
        'disabled_fg': '#616161',
        'scrollbar_bg': '#2d2d2d',
        'scrollbar_thumb': '#424242',
        'header_bg': '#1e1e1e',
        'header_fg': '#bdbdbd',
        'statusbar_bg': '#1e1e1e',
        'statusbar_fg': '#9e9e9e',
        'button_primary': '#64B5F6',
        'button_primary_hover': '#42A5F5',
        'button_primary_text': '#0D47A1',
        'button_secondary': '#2d2d2d',
        'button_secondary_hover': '#3d3d3d',
        'button_secondary_text': '#e0e0e0',
        'button_secondary_border': '#3d3d3d',
        'danger': '#EF5350',
        'danger_hover': '#E53935',
        'danger_text': '#ffffff',
        'listbox_bg': '#1e1e1e',
        'listbox_fg': '#e0e0e0',
        'listbox_select_bg': '#37474F',
        'listbox_select_fg': '#81D4FA',
        'entry_bg': '#2d2d2d',
        'entry_fg': '#e0e0e0',
        'entry_border': '#3d3d3d',
        'entry_focus_border': '#64B5F6',
        'separator': '#2d2d2d',
    }

    @staticmethod
    def get_windows_theme():
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if value == 1 else "dark"
        except:
            return "light"

    @staticmethod
    def detect_system_theme():
        if os.name == 'nt':
            return ThemeManager.get_windows_theme()
        return "light"


class StyledButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None, button_type="primary"):
        super().__init__(text, parent)
        self.button_type = button_type
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(16, 16))
        self.setMinimumHeight(28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class CardWidget(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        if title:
            header = QFrame()
            header.setFixedHeight(32)
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(12, 0, 12, 0)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Microsoft YaHei UI", 9, QFont.Weight.Bold))
            header_layout.addWidget(title_label)
            
            self.layout.addWidget(header)
            
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFixedHeight(1)
            self.layout.addWidget(separator)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(8)
        self.layout.addWidget(self.content_widget)
    
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        self.content_layout.addLayout(layout)


class FileListItem:
    def __init__(self, filepath):
        self.filepath = str(Path(filepath).resolve())
        self.name = Path(filepath).name
        self.lines = []
        self.encoding = 'utf-8'
        self.newline_char = '\n'
        
    def load(self):
        try:
            with open(self.filepath, 'rb') as f:
                raw_content = f.read()
            
            self.encoding, self.newline_char, _ = self._detect_encoding_and_newline(raw_content)
            content = raw_content.decode(self.encoding, errors='replace')
            self.lines = content.split(self.newline_char)
            return True
        except:
            return False
    
    def _detect_encoding_and_newline(self, raw_content):
        if raw_content.startswith(b'\xef\xbb\xbf'):
            encoding = 'utf-8-sig'
        elif raw_content.startswith(b'\xff\xfe') or raw_content.startswith(b'\xfe\xff'):
            encoding = 'utf-16'
        else:
            try:
                raw_content.decode('utf-8')
                encoding = 'utf-8'
            except UnicodeDecodeError:
                encoding = 'gbk'
        
        crlf_count = raw_content.count(b'\r\n')
        lf_count = raw_content.count(b'\n') - crlf_count
        cr_count = raw_content.count(b'\r') - crlf_count
        
        if crlf_count > lf_count and crlf_count > cr_count:
            newline_char = '\r\n'
            newline_name = 'CRLF (Windows)'
        elif lf_count > cr_count:
            newline_char = '\n'
            newline_name = 'LF (Unix/Linux)'
        elif cr_count > 0:
            newline_char = '\r'
            newline_name = 'CR (Old Mac)'
        else:
            newline_char = '\n'
            newline_name = 'LF (默认)'
        
        return encoding, newline_char, newline_name
    
    def line_count(self):
        return len(self.lines)


class SettingsDialog(QDialog):
    def __init__(self, parent=None, work_dir=""):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumWidth(450)
        self.work_dir = work_dir
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        work_dir_group = QGroupBox("工作目录设置")
        work_dir_layout = QVBoxLayout(work_dir_group)
        
        desc_label = QLabel("所有生成的文件将保存到以下目录：")
        desc_label.setWordWrap(True)
        work_dir_layout.addWidget(desc_label)
        
        dir_layout = QHBoxLayout()
        self.dir_edit = QLineEdit(self.work_dir)
        dir_layout.addWidget(self.dir_edit)
        
        browse_btn = StyledButton("浏览...", button_type="secondary")
        browse_btn.clicked.connect(self.browse_dir)
        dir_layout.addWidget(browse_btn)
        
        work_dir_layout.addLayout(dir_layout)
        
        default_btn = StyledButton("恢复默认", button_type="secondary")
        default_btn.clicked.connect(self.restore_default)
        work_dir_layout.addWidget(default_btn)
        
        layout.addWidget(work_dir_group)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def browse_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择工作目录", self.dir_edit.text())
        if dir_path:
            self.dir_edit.setText(dir_path)
    
    def restore_default(self):
        default_dir = str(Path(__file__).parent / "txt")
        self.dir_edit.setText(default_dir)
    
    def get_work_dir(self):
        return self.dir_edit.text()


class ColumnSelectDialog(QDialog):
    def __init__(self, parent=None, max_columns=10, current_columns=None):
        super().__init__(parent)
        self.setWindowTitle("选择导出列")
        self.setMinimumWidth(400)
        self.max_columns = max_columns
        self.selected_columns = current_columns or []
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        desc_label = QLabel("选择要导出的列（从1开始），用逗号分隔（如：1,3,5）：")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        self.columns_edit = QLineEdit()
        if self.selected_columns:
            self.columns_edit.setText(','.join(str(c) for c in self.selected_columns))
        layout.addWidget(self.columns_edit)
        
        example_label = QLabel("示例：\n- 导出第1列：输入 1\n- 导出第1、3、5列：输入 1,3,5\n- 导出第1到第5列：输入 1-5")
        example_label.setWordWrap(True)
        layout.addWidget(example_label)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_columns(self):
        text = self.columns_edit.text().strip()
        if not text:
            return []
        
        columns = []
        parts = text.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start_end = part.split('-')
                if len(start_end) == 2:
                    try:
                        start = int(start_end[0].strip())
                        end = int(start_end[1].strip())
                        if start > 0 and end > 0:
                            columns.extend(range(min(start, end), max(start, end) + 1))
                    except:
                        pass
            else:
                try:
                    col = int(part)
                    if col > 0:
                        columns.append(col)
                except:
                    pass
        
        return sorted(list(set(columns)))


class TextProcessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本处理工具")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        
        self.current_theme = "system"
        self.actual_theme = ThemeManager.detect_system_theme()
        self.theme_colors = ThemeManager.LIGHT if self.actual_theme == "light" else ThemeManager.DARK
        
        self.default_work_dir = str(Path(__file__).parent / "txt")
        self.settings_file = Path(__file__).parent / "settings.json"
        self.load_settings()
        
        self.file_list = []
        self.current_file_item = None
        
        self.config_file = Path(__file__).parent / "config.json"
        self.load_config()
        
        self.setup_menu_bar()
        self.setup_ui()
        self.apply_theme(self.actual_theme)
        
        self.ensure_work_dir()
    
    def load_settings(self):
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.work_dir = settings.get("work_dir", self.default_work_dir)
                    self.current_theme = settings.get("theme", "system")
                    if self.current_theme == "system":
                        self.actual_theme = ThemeManager.detect_system_theme()
                    else:
                        self.actual_theme = self.current_theme
            except:
                self.work_dir = self.default_work_dir
        else:
            self.work_dir = self.default_work_dir
    
    def save_settings(self):
        try:
            settings = {
                "work_dir": self.work_dir,
                "theme": self.current_theme
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_config(self):
        self.export_separator = ','
        self.export_columns = []
        self.extract_keywords = []
        self.extract_regex = ""
        self.split_lines = 1000
        self.split_prefix = "_分割文本"
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.export_separator = config.get("export_separator", ',')
                    self.export_columns = config.get("export_columns", [])
                    self.extract_keywords = config.get("extract_keywords", [])
                    self.extract_regex = config.get("extract_regex", "")
                    self.split_lines = config.get("split_lines", 1000)
                    self.split_prefix = config.get("split_prefix", "_分割文本")
            except:
                pass
    
    def save_config(self):
        try:
            config = {
                "export_separator": self.export_separator,
                "export_columns": self.export_columns,
                "extract_keywords": self.extract_keywords,
                "extract_regex": self.extract_regex,
                "split_lines": self.split_lines,
                "split_prefix": self.split_prefix
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def ensure_work_dir(self):
        try:
            os.makedirs(self.work_dir, exist_ok=True)
        except:
            pass
    
    def setup_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("文件(&F)")
        
        import_action = QAction("导入文件...", self)
        import_action.triggered.connect(self.import_file)
        file_menu.addAction(import_action)
        
        import_multi_action = QAction("导入多个文件...", self)
        import_multi_action.triggered.connect(self.import_multi_files)
        file_menu.addAction(import_multi_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction("设置...", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        view_menu = menubar.addMenu("视图(&V)")
        
        theme_menu = view_menu.addMenu("主题")
        
        self.light_action = QAction("浅色", self, checkable=True)
        self.light_action.triggered.connect(lambda: self.set_theme("light"))
        theme_menu.addAction(self.light_action)
        
        self.dark_action = QAction("深色", self, checkable=True)
        self.dark_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(self.dark_action)
        
        self.system_action = QAction("跟随系统", self, checkable=True)
        self.system_action.triggered.connect(lambda: self.set_theme("system"))
        theme_menu.addAction(self.system_action)
        
        self.update_theme_menu()
    
    def update_theme_menu(self):
        self.light_action.setChecked(self.current_theme == "light")
        self.dark_action.setChecked(self.current_theme == "dark")
        self.system_action.setChecked(self.current_theme == "system")
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)
        
        toolbar_card = CardWidget("工具栏")
        
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(6)
        
        self.import_btn = StyledButton("导入文件", button_type="primary")
        self.import_btn.clicked.connect(self.import_multi_files)
        toolbar_layout.addWidget(self.import_btn)
        
        toolbar_layout.addStretch()
        
        toolbar_card.add_layout(toolbar_layout)
        
        left_layout.addWidget(toolbar_card)
        
        file_list_card = CardWidget("文件列表（可多选，右键菜单）")
        
        self.file_list_widget = QListWidget()
        self.file_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list_widget.customContextMenuRequested.connect(self.show_file_list_context_menu)
        self.file_list_widget.itemClicked.connect(self.on_file_select)
        self.file_list_widget.itemDoubleClicked.connect(self.on_file_double_click)
        file_list_card.add_widget(self.file_list_widget)
        
        info_layout = QHBoxLayout()
        self.file_count_label = QLabel("文件数: 0")
        info_layout.addWidget(self.file_count_label)
        
        self.total_lines_label = QLabel("总行数: 0")
        info_layout.addWidget(self.total_lines_label)
        
        info_layout.addStretch()
        
        file_list_card.add_layout(info_layout)
        
        left_layout.addWidget(file_list_card, stretch=1)
        
        work_dir_card = CardWidget("工作目录")
        
        work_dir_layout = QHBoxLayout()
        self.work_dir_label = QLabel(f"输出目录: {self.work_dir}")
        self.work_dir_label.setWordWrap(True)
        work_dir_layout.addWidget(self.work_dir_label)
        
        work_dir_layout.addStretch()
        
        self.set_work_dir_btn = StyledButton("设置", button_type="secondary")
        self.set_work_dir_btn.setMaximumWidth(60)
        self.set_work_dir_btn.clicked.connect(self.set_work_dir_dialog)
        work_dir_layout.addWidget(self.set_work_dir_btn)
        
        self.open_work_dir_btn = StyledButton("打开", button_type="secondary")
        self.open_work_dir_btn.setMaximumWidth(60)
        self.open_work_dir_btn.clicked.connect(self.open_work_dir)
        work_dir_layout.addWidget(self.open_work_dir_btn)
        
        work_dir_card.add_layout(work_dir_layout)
        
        left_layout.addWidget(work_dir_card)
        
        content_splitter.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        
        self.function_tabs = QTabWidget()
        
        deduplication_tab = self.create_deduplication_tab()
        self.function_tabs.addTab(deduplication_tab, "去重")
        
        export_tab = self.create_export_tab()
        self.function_tabs.addTab(export_tab, "指定格式导出")
        
        extract_tab = self.create_extract_tab()
        self.function_tabs.addTab(extract_tab, "文本提取")
        
        split_merge_tab = self.create_split_merge_tab()
        self.function_tabs.addTab(split_merge_tab, "分割/合并")
        
        compare_tab = self.create_compare_tab()
        self.function_tabs.addTab(compare_tab, "差异对比")
        
        right_layout.addWidget(self.function_tabs)
        
        preview_card = CardWidget("文件预览")
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 10))
        self.preview_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        preview_card.add_widget(self.preview_text)
        
        right_layout.addWidget(preview_card, stretch=1)
        
        content_splitter.addWidget(right_panel)
        content_splitter.setSizes([350, 850])
        
        main_layout.addWidget(content_splitter, stretch=1)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label, stretch=1)
        
        self.line_count_label = QLabel("行数: 0")
        self.status_bar.addPermanentWidget(self.line_count_label)
        
        self.newline_label = QLabel("换行符: 未知")
        self.status_bar.addPermanentWidget(self.newline_label)
        
        self.setup_icons()
    
    def create_deduplication_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        config_group = QGroupBox("去重配置")
        config_layout = QVBoxLayout(config_group)
        config_layout.setSpacing(8)
        
        row1 = QHBoxLayout()
        
        self.dedup_separator_check = QCheckBox("使用分隔符分割行进行比较")
        self.dedup_separator_check.stateChanged.connect(self.toggle_dedup_separator)
        row1.addWidget(self.dedup_separator_check)
        
        row1.addStretch()
        
        config_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        
        self.dedup_separator_label = QLabel("分隔符:")
        row2.addWidget(self.dedup_separator_label)
        
        self.dedup_separator_combo = QComboBox()
        self.dedup_separator_combo.addItems([',', ';', '\\t', '|', ' ', '其他'])
        self.dedup_separator_combo.setEnabled(False)
        self.dedup_separator_combo.setMaximumWidth(80)
        row2.addWidget(self.dedup_separator_combo)
        
        self.dedup_custom_label = QLabel("自定义:")
        row2.addWidget(self.dedup_custom_label)
        
        self.dedup_custom_separator = QLineEdit()
        self.dedup_custom_separator.setEnabled(False)
        self.dedup_custom_separator.setMaximumWidth(70)
        row2.addWidget(self.dedup_custom_separator)
        
        row2.addStretch()
        
        config_layout.addLayout(row2)
        
        row3 = QHBoxLayout()
        
        self.dedup_param_check = QCheckBox("仅根据指定列参数去重")
        self.dedup_param_check.stateChanged.connect(self.toggle_dedup_param)
        row3.addWidget(self.dedup_param_check)
        
        row3.addStretch()
        
        config_layout.addLayout(row3)
        
        row4 = QHBoxLayout()
        
        self.dedup_param_label = QLabel("参数位置 (从1开始):")
        row4.addWidget(self.dedup_param_label)
        
        self.dedup_param_position = QSpinBox()
        self.dedup_param_position.setMinimum(1)
        self.dedup_param_position.setMaximum(999)
        self.dedup_param_position.setValue(1)
        self.dedup_param_position.setEnabled(False)
        self.dedup_param_position.setMaximumWidth(70)
        row4.addWidget(self.dedup_param_position)
        
        row4.addStretch()
        
        config_layout.addLayout(row4)
        
        row5 = QHBoxLayout()
        
        self.dedup_suffix_label = QLabel("输出文件名后缀:")
        row5.addWidget(self.dedup_suffix_label)
        
        self.dedup_output_suffix = QLineEdit("_去重复")
        self.dedup_output_suffix.setMaximumWidth(120)
        row5.addWidget(self.dedup_output_suffix)
        
        row5.addStretch()
        
        config_layout.addLayout(row5)
        
        layout.addWidget(config_group)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.dedup_process_btn = StyledButton("执行去重", button_type="primary")
        self.dedup_process_btn.setMinimumWidth(120)
        self.dedup_process_btn.clicked.connect(self.execute_deduplication)
        action_layout.addWidget(self.dedup_process_btn)
        
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_export_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        config_group = QGroupBox("导出配置")
        config_layout = QVBoxLayout(config_group)
        config_layout.setSpacing(8)
        
        row1 = QHBoxLayout()
        
        self.export_separator_label = QLabel("输入分隔符:")
        row1.addWidget(self.export_separator_label)
        
        self.export_input_separator = QComboBox()
        self.export_input_separator.addItems([',', ';', '\\t', '|', ' ', '其他'])
        self.export_input_separator.setMaximumWidth(80)
        row1.addWidget(self.export_input_separator)
        
        self.export_custom_label = QLabel("自定义:")
        row1.addWidget(self.export_custom_label)
        
        self.export_custom_input = QLineEdit()
        self.export_custom_input.setMaximumWidth(70)
        row1.addWidget(self.export_custom_input)
        
        row1.addStretch()
        
        config_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        
        self.export_columns_label = QLabel("导出列:")
        row2.addWidget(self.export_columns_label)
        
        self.export_columns_btn = StyledButton("选择列...", button_type="secondary")
        self.export_columns_btn.clicked.connect(self.select_export_columns)
        row2.addWidget(self.export_columns_btn)
        
        self.export_columns_display = QLabel("全部列")
        self.export_columns_display.setStyleSheet("font-style: italic;")
        row2.addWidget(self.export_columns_display)
        
        row2.addStretch()
        
        config_layout.addLayout(row2)
        
        row3 = QHBoxLayout()
        
        self.export_output_sep_label = QLabel("输出分隔符:")
        row3.addWidget(self.export_output_sep_label)
        
        self.export_output_separator = QComboBox()
        self.export_output_separator.addItems([',', ';', '\\t', '|', ' ', '其他'])
        self.export_output_separator.setCurrentText(self.export_separator)
        self.export_output_separator.setMaximumWidth(80)
        row3.addWidget(self.export_output_separator)
        
        self.export_custom_output_label = QLabel("自定义:")
        row3.addWidget(self.export_custom_output_label)
        
        self.export_custom_output = QLineEdit()
        self.export_custom_output.setMaximumWidth(70)
        row3.addWidget(self.export_custom_output)
        
        row3.addStretch()
        
        config_layout.addLayout(row3)
        
        row4 = QHBoxLayout()
        
        self.export_suffix_label = QLabel("输出文件名后缀:")
        row4.addWidget(self.export_suffix_label)
        
        self.export_output_suffix = QLineEdit("_导出")
        self.export_output_suffix.setMaximumWidth(120)
        row4.addWidget(self.export_output_suffix)
        
        row4.addStretch()
        
        config_layout.addLayout(row4)
        
        layout.addWidget(config_group)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.export_process_btn = StyledButton("执行导出", button_type="primary")
        self.export_process_btn.setMinimumWidth(120)
        self.export_process_btn.clicked.connect(self.execute_export)
        action_layout.addWidget(self.export_process_btn)
        
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_extract_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        mode_group = QGroupBox("提取模式")
        mode_layout = QVBoxLayout(mode_group)
        
        self.extract_mode_group = QButtonGroup(self)
        
        self.extract_keyword_radio = QRadioButton("关键词提取")
        self.extract_keyword_radio.setChecked(True)
        self.extract_mode_group.addButton(self.extract_keyword_radio)
        mode_layout.addWidget(self.extract_keyword_radio)
        
        self.extract_regex_radio = QRadioButton("正则提取")
        self.extract_mode_group.addButton(self.extract_regex_radio)
        mode_layout.addWidget(self.extract_regex_radio)
        
        self.extract_rule_radio = QRadioButton("规则匹配导出（行存在即导出）")
        self.extract_mode_group.addButton(self.extract_rule_radio)
        mode_layout.addWidget(self.extract_rule_radio)
        
        layout.addWidget(mode_group)
        
        config_group = QGroupBox("提取配置")
        config_layout = QVBoxLayout(config_group)
        config_layout.setSpacing(8)
        
        keyword_row = QHBoxLayout()
        
        self.keyword_label = QLabel("关键词 (多个用逗号分隔):")
        keyword_row.addWidget(self.keyword_label)
        
        self.keyword_edit = QLineEdit()
        self.keyword_edit.setPlaceholderText("例如: 关键词1,关键词2,关键词3")
        keyword_row.addWidget(self.keyword_edit)
        
        config_layout.addLayout(keyword_row)
        
        regex_row = QHBoxLayout()
        
        self.regex_label = QLabel("正则表达式:")
        regex_row.addWidget(self.regex_label)
        
        self.regex_edit = QLineEdit()
        self.regex_edit.setPlaceholderText("例如: \\d+ 匹配数字")
        regex_row.addWidget(self.regex_edit)
        
        config_layout.addLayout(regex_row)
        
        case_row = QHBoxLayout()
        
        self.case_sensitive_check = QCheckBox("区分大小写")
        case_row.addWidget(self.case_sensitive_check)
        
        self.invert_check = QCheckBox("反向匹配（导出不匹配的行）")
        case_row.addWidget(self.invert_check)
        
        case_row.addStretch()
        
        config_layout.addLayout(case_row)
        
        suffix_row = QHBoxLayout()
        
        self.extract_suffix_label = QLabel("输出文件名后缀:")
        suffix_row.addWidget(self.extract_suffix_label)
        
        self.extract_output_suffix = QLineEdit("_提取")
        self.extract_output_suffix.setMaximumWidth(120)
        suffix_row.addWidget(self.extract_output_suffix)
        
        suffix_row.addStretch()
        
        config_layout.addLayout(suffix_row)
        
        layout.addWidget(config_group)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.extract_process_btn = StyledButton("执行提取", button_type="primary")
        self.extract_process_btn.setMinimumWidth(120)
        self.extract_process_btn.clicked.connect(self.execute_extract)
        action_layout.addWidget(self.extract_process_btn)
        
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_split_merge_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        tabs = QTabWidget()
        
        split_tab = QWidget()
        split_layout = QVBoxLayout(split_tab)
        split_layout.setContentsMargins(0, 0, 0, 0)
        split_layout.setSpacing(8)
        
        split_config = QGroupBox("分割配置")
        split_config_layout = QVBoxLayout(split_config)
        split_config_layout.setSpacing(8)
        
        row1 = QHBoxLayout()
        
        self.split_lines_label = QLabel("每个文件行数:")
        row1.addWidget(self.split_lines_label)
        
        self.split_lines_spin = QSpinBox()
        self.split_lines_spin.setMinimum(1)
        self.split_lines_spin.setMaximum(999999)
        self.split_lines_spin.setValue(self.split_lines)
        self.split_lines_spin.setMaximumWidth(100)
        row1.addWidget(self.split_lines_spin)
        
        row1.addStretch()
        
        split_config_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        
        self.split_prefix_label = QLabel("文件名前缀后缀:")
        row2.addWidget(self.split_prefix_label)
        
        self.split_prefix_edit = QLineEdit(self.split_prefix)
        self.split_prefix_edit.setPlaceholderText("例如: _分割文本")
        self.split_prefix_edit.setMaximumWidth(150)
        row2.addWidget(self.split_prefix_edit)
        
        row2.addStretch()
        
        split_config_layout.addLayout(row2)
        
        split_layout.addWidget(split_config)
        
        split_action = QHBoxLayout()
        split_action.addStretch()
        
        self.split_process_btn = StyledButton("执行分割", button_type="primary")
        self.split_process_btn.setMinimumWidth(120)
        self.split_process_btn.clicked.connect(self.execute_split)
        split_action.addWidget(self.split_process_btn)
        
        split_action.addStretch()
        
        split_layout.addLayout(split_action)
        split_layout.addStretch()
        
        tabs.addTab(split_tab, "分割")
        
        merge_tab = QWidget()
        merge_layout = QVBoxLayout(merge_tab)
        merge_layout.setContentsMargins(0, 0, 0, 0)
        merge_layout.setSpacing(8)
        
        merge_config = QGroupBox("合并配置")
        merge_config_layout = QVBoxLayout(merge_config)
        merge_config_layout.setSpacing(8)
        
        info_label = QLabel("合并说明：\n1. 在左侧文件列表中多选要合并的文件\n2. 文件将按列表中的顺序合并\n3. 输出文件将保存到工作目录")
        info_label.setWordWrap(True)
        merge_config_layout.addWidget(info_label)
        
        row1 = QHBoxLayout()
        
        self.merge_filename_label = QLabel("输出文件名:")
        row1.addWidget(self.merge_filename_label)
        
        self.merge_filename_edit = QLineEdit("合并结果")
        self.merge_filename_edit.setMaximumWidth(150)
        row1.addWidget(self.merge_filename_edit)
        
        row1.addStretch()
        
        merge_config_layout.addLayout(row1)
        
        merge_layout.addWidget(merge_config)
        
        merge_action = QHBoxLayout()
        merge_action.addStretch()
        
        self.merge_process_btn = StyledButton("执行合并", button_type="primary")
        self.merge_process_btn.setMinimumWidth(120)
        self.merge_process_btn.clicked.connect(self.execute_merge)
        merge_action.addWidget(self.merge_process_btn)
        
        merge_action.addStretch()
        
        merge_layout.addLayout(merge_action)
        merge_layout.addStretch()
        
        tabs.addTab(merge_tab, "合并")
        
        layout.addWidget(tabs)
        
        return widget
    
    def create_compare_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        file_select_group = QGroupBox("文件选择")
        file_select_layout = QVBoxLayout(file_select_group)
        file_select_layout.setSpacing(8)
        
        row1 = QHBoxLayout()
        
        self.compare_file_a_label = QLabel("文件A:")
        row1.addWidget(self.compare_file_a_label)
        
        self.compare_file_a_combo = QComboBox()
        self.compare_file_a_combo.setMinimumWidth(200)
        row1.addWidget(self.compare_file_a_combo)
        
        row1.addStretch()
        
        file_select_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        
        self.compare_file_b_label = QLabel("文件B:")
        row2.addWidget(self.compare_file_b_label)
        
        self.compare_file_b_combo = QComboBox()
        self.compare_file_b_combo.setMinimumWidth(200)
        row2.addWidget(self.compare_file_b_combo)
        
        row2.addStretch()
        
        file_select_layout.addLayout(row2)
        
        layout.addWidget(file_select_group)
        
        mode_group = QGroupBox("对比模式")
        mode_layout = QVBoxLayout(mode_group)
        
        self.compare_mode_group = QButtonGroup(self)
        
        self.compare_remove_radio = QRadioButton("功能1: 去除A文件中含有B文件的重复数据（A - B）")
        self.compare_remove_radio.setChecked(True)
        self.compare_mode_group.addButton(self.compare_remove_radio)
        mode_layout.addWidget(self.compare_remove_radio)
        
        self.compare_common_radio = QRadioButton("功能2: 得到A文件中含有B文件的共有数据（A ∩ B）")
        self.compare_mode_group.addButton(self.compare_common_radio)
        mode_layout.addWidget(self.compare_common_radio)
        
        layout.addWidget(mode_group)
        
        config_group = QGroupBox("文件B分析配置（可选）")
        config_layout = QVBoxLayout(config_group)
        config_layout.setSpacing(8)
        
        self.compare_use_param_check = QCheckBox("文件B只分析指定参数列")
        self.compare_use_param_check.stateChanged.connect(self.toggle_compare_param)
        config_layout.addWidget(self.compare_use_param_check)
        
        row1 = QHBoxLayout()
        
        self.compare_separator_label = QLabel("分隔符:")
        row1.addWidget(self.compare_separator_label)
        
        self.compare_separator_combo = QComboBox()
        self.compare_separator_combo.addItems([',', ';', '\\t', '|', ' ', '其他'])
        self.compare_separator_combo.setEnabled(False)
        self.compare_separator_combo.setMaximumWidth(80)
        row1.addWidget(self.compare_separator_combo)
        
        self.compare_custom_label = QLabel("自定义:")
        row1.addWidget(self.compare_custom_label)
        
        self.compare_custom_separator = QLineEdit()
        self.compare_custom_separator.setEnabled(False)
        self.compare_custom_separator.setMaximumWidth(70)
        row1.addWidget(self.compare_custom_separator)
        
        row1.addStretch()
        
        config_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        
        self.compare_col_label = QLabel("列位置:")
        row2.addWidget(self.compare_col_label)
        
        self.compare_col_spin = QSpinBox()
        self.compare_col_spin.setMinimum(1)
        self.compare_col_spin.setMaximum(999)
        self.compare_col_spin.setValue(1)
        self.compare_col_spin.setEnabled(False)
        self.compare_col_spin.setMaximumWidth(70)
        row2.addWidget(self.compare_col_spin)
        
        row2.addStretch()
        
        config_layout.addLayout(row2)
        
        layout.addWidget(config_group)
        
        suffix_row = QHBoxLayout()
        
        self.compare_suffix_label = QLabel("输出文件名后缀:")
        suffix_row.addWidget(self.compare_suffix_label)
        
        self.compare_output_suffix = QLineEdit("_对比结果")
        self.compare_output_suffix.setMaximumWidth(120)
        suffix_row.addWidget(self.compare_output_suffix)
        
        suffix_row.addStretch()
        
        layout.addLayout(suffix_row)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.refresh_files_btn = StyledButton("刷新文件列表", button_type="secondary")
        self.refresh_files_btn.clicked.connect(self.refresh_compare_file_list)
        action_layout.addWidget(self.refresh_files_btn)
        
        self.compare_process_btn = StyledButton("执行对比", button_type="primary")
        self.compare_process_btn.setMinimumWidth(120)
        self.compare_process_btn.clicked.connect(self.execute_compare)
        action_layout.addWidget(self.compare_process_btn)
        
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        layout.addStretch()
        
        return widget
    
    def setup_icons(self):
        from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen
        from PyQt6.QtCore import Qt, QRectF
        
        def create_icon(icon_type):
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            primary_color = QColor(self.theme_colors['button_primary'])
            
            painter.setPen(QPen(primary_color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            if icon_type == "folder":
                painter.drawRoundedRect(QRectF(2, 5, 12, 9), 1, 1)
                painter.drawRect(QRectF(2, 3, 6, 4))
                painter.drawLine(8, 3, 14, 3)
                painter.drawLine(14, 3, 14, 5)
            elif icon_type == "reload":
                painter.drawArc(QRectF(2, 2, 12, 12), 30 * 16, 300 * 16)
                painter.drawLine(13, 5, 15, 3)
                painter.drawLine(13, 5, 11, 6)
            elif icon_type == "open":
                painter.drawRoundedRect(QRectF(2, 3, 12, 10), 1, 1)
                painter.drawLine(2, 8, 14, 8)
                painter.drawLine(5, 8, 6, 10)
                painter.drawLine(8, 8, 11, 8)
                painter.drawLine(11, 8, 10, 10)
            elif icon_type == "trash":
                painter.drawRoundedRect(QRectF(4, 2, 8, 12), 1, 1)
                painter.drawLine(1, 4, 15, 4)
                painter.drawLine(6, 5, 6, 11)
                painter.drawLine(8, 5, 8, 11)
                painter.drawLine(10, 5, 10, 11)
            
            painter.end()
            return QIcon(pixmap)
        
        self.import_btn.setIcon(create_icon("folder"))
        self.dedup_process_btn.setIcon(create_icon("reload"))
        self.export_process_btn.setIcon(create_icon("reload"))
        self.extract_process_btn.setIcon(create_icon("reload"))
        self.split_process_btn.setIcon(create_icon("reload"))
        self.merge_process_btn.setIcon(create_icon("reload"))
        self.compare_process_btn.setIcon(create_icon("reload"))
    
    def apply_theme(self, theme_name):
        if theme_name == "light":
            self.theme_colors = ThemeManager.LIGHT
        else:
            self.theme_colors = ThemeManager.DARK
        
        palette = QPalette()
        
        bg_color = QColor(self.theme_colors['bg'])
        fg_color = QColor(self.theme_colors['fg'])
        card_bg = QColor(self.theme_colors['card_bg'])
        
        palette.setColor(QPalette.ColorRole.Window, bg_color)
        palette.setColor(QPalette.ColorRole.WindowText, fg_color)
        palette.setColor(QPalette.ColorRole.Base, QColor(self.theme_colors['text_bg']))
        palette.setColor(QPalette.ColorRole.Text, QColor(self.theme_colors['text_fg']))
        palette.setColor(QPalette.ColorRole.Button, card_bg)
        palette.setColor(QPalette.ColorRole.ButtonText, fg_color)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(self.theme_colors['select_bg']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.theme_colors['select_fg']))
        
        self.setPalette(palette)
        
        self.update_styles()
        self.setup_icons()
    
    def update_styles(self):
        primary_bg = self.theme_colors['button_primary']
        primary_hover = self.theme_colors['button_primary_hover']
        primary_text = self.theme_colors['button_primary_text']
        secondary_bg = self.theme_colors['button_secondary']
        secondary_hover = self.theme_colors['button_secondary_hover']
        secondary_text = self.theme_colors['button_secondary_text']
        secondary_border = self.theme_colors['button_secondary_border']
        danger = self.theme_colors['danger']
        danger_hover = self.theme_colors['danger_hover']
        danger_text = self.theme_colors['danger_text']
        card_border = self.theme_colors['card_border']
        header_bg = self.theme_colors['header_bg']
        header_fg = self.theme_colors['header_fg']
        separator = self.theme_colors['separator']
        entry_bg = self.theme_colors['entry_bg']
        entry_fg = self.theme_colors['entry_fg']
        entry_border = self.theme_colors['entry_border']
        entry_focus = self.theme_colors['entry_focus_border']
        listbox_bg = self.theme_colors['listbox_bg']
        listbox_fg = self.theme_colors['listbox_fg']
        listbox_select_bg = self.theme_colors['listbox_select_bg']
        listbox_select_fg = self.theme_colors['listbox_select_fg']
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme_colors['bg']};
            }}
            QWidget {{
                background-color: {self.theme_colors['bg']};
                color: {self.theme_colors['fg']};
                font-family: "Microsoft YaHei UI";
                font-size: 9pt;
            }}
            QMenuBar {{
                background-color: {self.theme_colors['header_bg']};
                color: {self.theme_colors['header_fg']};
                border-bottom: 1px solid {card_border};
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 5px 12px;
            }}
            QMenuBar::item:selected {{
                background-color: {primary_bg};
                color: {primary_text};
            }}
            QMenu {{
                background-color: {self.theme_colors['card_bg']};
                color: {self.theme_colors['fg']};
                border: 1px solid {card_border};
            }}
            QMenu::item {{
                padding: 6px 30px;
            }}
            QMenu::item:selected {{
                background-color: {primary_bg};
                color: {primary_text};
            }}
            QMenu::item:checked {{
                background-color: {primary_bg};
                color: {primary_text};
            }}
            CardWidget {{
                background-color: {self.theme_colors['card_bg']};
                border: 1px solid {card_border};
                border-radius: 4px;
            }}
            CardWidget QLabel {{
                background-color: transparent;
            }}
            CardWidget QFrame {{
                background-color: transparent;
            }}
            QFrame[frameShape="HLine"] {{
                background-color: {separator};
                border: none;
                max-height: 1px;
            }}
            QLabel {{
                color: {self.theme_colors['fg']};
                background-color: transparent;
            }}
            QPushButton {{
                border-radius: 4px;
                padding: 5px 12px;
                font-weight: normal;
            }}
            StyledButton[button_type="primary"] {{
                background-color: {primary_bg};
                color: {primary_text};
                border: none;
            }}
            StyledButton[button_type="primary"]:hover {{
                background-color: {primary_hover};
            }}
            StyledButton[button_type="secondary"] {{
                background-color: {secondary_bg};
                color: {secondary_text};
                border: 1px solid {secondary_border};
            }}
            StyledButton[button_type="secondary"]:hover {{
                background-color: {secondary_hover};
            }}
            StyledButton[button_type="danger"] {{
                background-color: {danger};
                color: {danger_text};
                border: none;
            }}
            StyledButton[button_type="danger"]:hover {{
                background-color: {danger_hover};
            }}
            QCheckBox {{
                color: {self.theme_colors['fg']};
                spacing: 6px;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {entry_border};
                border-radius: 2px;
                background-color: {entry_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {primary_bg};
                border-color: {primary_bg};
            }}
            QRadioButton {{
                color: {self.theme_colors['fg']};
                spacing: 6px;
            }}
            QRadioButton::indicator {{
                width: 14px;
                height: 14px;
            }}
            QComboBox {{
                background-color: {entry_bg};
                color: {entry_fg};
                border: 1px solid {entry_border};
                border-radius: 3px;
                padding: 4px 8px;
                min-height: 16px;
            }}
            QComboBox:hover {{
                border-color: {entry_focus};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 16px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {entry_bg};
                color: {entry_fg};
                selection-background-color: {listbox_select_bg};
                selection-color: {listbox_select_fg};
            }}
            QLineEdit {{
                background-color: {entry_bg};
                color: {entry_fg};
                border: 1px solid {entry_border};
                border-radius: 3px;
                padding: 4px 6px;
                selection-background-color: {self.theme_colors['select_bg']};
                selection-color: {self.theme_colors['select_fg']};
            }}
            QLineEdit:focus {{
                border-color: {entry_focus};
            }}
            QLineEdit:disabled {{
                background-color: {self.theme_colors['disabled_bg']};
                color: {self.theme_colors['disabled_fg']};
            }}
            QSpinBox {{
                background-color: {entry_bg};
                color: {entry_fg};
                border: 1px solid {entry_border};
                border-radius: 3px;
                padding: 3px 6px;
            }}
            QSpinBox:focus {{
                border-color: {entry_focus};
            }}
            QSpinBox:disabled {{
                background-color: {self.theme_colors['disabled_bg']};
                color: {self.theme_colors['disabled_fg']};
            }}
            QListWidget {{
                background-color: {listbox_bg};
                color: {listbox_fg};
                border: 1px solid {card_border};
                border-radius: 3px;
            }}
            QListWidget::item {{
                padding: 4px;
                border-radius: 2px;
            }}
            QListWidget::item:selected {{
                background-color: {listbox_select_bg};
                color: {listbox_select_fg};
            }}
            QListWidget::item:hover {{
                background-color: {self.theme_colors['header_bg']};
            }}
            QTextEdit {{
                background-color: {self.theme_colors['text_bg']};
                color: {self.theme_colors['text_fg']};
                border: 1px solid {card_border};
                border-radius: 3px;
            }}
            QTabWidget::pane {{
                border: 1px solid {card_border};
                border-radius: 3px;
                background-color: {self.theme_colors['card_bg']};
            }}
            QTabBar::tab {{
                background-color: {self.theme_colors['header_bg']};
                color: {self.theme_colors['header_fg']};
                padding: 6px 15px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                margin-right: 1px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.theme_colors['card_bg']};
                color: {self.theme_colors['fg']};
            }}
            QTabBar::tab:hover {{
                background-color: {self.theme_colors['card_bg']};
            }}
            QGroupBox {{
                background-color: transparent;
                border: 1px solid {card_border};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QStatusBar {{
                background-color: {self.theme_colors['statusbar_bg']};
                color: {self.theme_colors['statusbar_fg']};
            }}
            QStatusBar QLabel {{
                color: {self.theme_colors['statusbar_fg']};
            }}
            QSplitter::handle {{
                background-color: {separator};
            }}
            QSplitter::handle:horizontal {{
                width: 2px;
            }}
            QScrollBar:vertical {{
                background-color: {self.theme_colors['scrollbar_bg']};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.theme_colors['scrollbar_thumb']};
                min-height: 25px;
                border-radius: 5px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {self.theme_colors['fg']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background-color: {self.theme_colors['scrollbar_bg']};
                height: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {self.theme_colors['scrollbar_thumb']};
                min-width: 25px;
                border-radius: 5px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {self.theme_colors['fg']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QDialog {{
                background-color: {self.theme_colors['bg']};
            }}
        """)
    
    def set_theme(self, theme):
        self.current_theme = theme
        if theme == "system":
            self.actual_theme = ThemeManager.detect_system_theme()
        else:
            self.actual_theme = theme
        self.apply_theme(self.actual_theme)
        self.update_theme_menu()
        self.save_settings()
    
    def show_settings(self):
        dialog = SettingsDialog(self, self.work_dir)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_dir = dialog.get_work_dir()
            if new_dir:
                self.work_dir = new_dir
                self.work_dir_label.setText(f"输出目录: {self.work_dir}")
                self.ensure_work_dir()
                self.save_settings()
    
    def set_work_dir_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择工作目录", self.work_dir)
        if dir_path:
            self.work_dir = dir_path
            self.work_dir_label.setText(f"输出目录: {self.work_dir}")
            self.ensure_work_dir()
            self.save_settings()
    
    def show_file_list_context_menu(self, pos):
        from PyQt6.QtGui import QAction
        from PyQt6.QtWidgets import QMenu
        
        menu = QMenu(self)
        
        import_action = QAction("导入文件...", self)
        import_action.triggered.connect(self.import_multi_files)
        menu.addAction(import_action)
        
        menu.addSeparator()
        
        remove_action = QAction("移除选中文件", self)
        remove_action.triggered.connect(self.remove_selected_files)
        menu.addAction(remove_action)
        
        clear_action = QAction("清空所有文件", self)
        clear_action.triggered.connect(self.clear_all_files)
        menu.addAction(clear_action)
        
        menu.exec(self.file_list_widget.mapToGlobal(pos))
    
    def open_work_dir(self):
        if os.path.exists(self.work_dir):
            os.startfile(self.work_dir)
        else:
            QMessageBox.information(self, "提示", "工作目录不存在")
    
    def import_file(self):
        filetypes = [
            ("文本文件", "*.txt"),
            ("CSV文件", "*.csv"),
            ("所有文件", "*.*")
        ]
        
        filepath, _ = QFileDialog.getOpenFileName(
            self, "选择要处理的文件", "", ";;".join([f"{t[0]} ({t[1]})" for t in filetypes])
        )
        
        if filepath:
            self.add_file_to_list(filepath)
    
    def import_multi_files(self):
        filetypes = [
            ("文本文件", "*.txt"),
            ("CSV文件", "*.csv"),
            ("所有文件", "*.*")
        ]
        
        filepaths, _ = QFileDialog.getOpenFileNames(
            self, "选择要处理的文件", "", ";;".join([f"{t[0]} ({t[1]})" for t in filetypes])
        )
        
        for filepath in filepaths:
            self.add_file_to_list(filepath)
    
    def add_file_to_list(self, filepath):
        filepath = str(Path(filepath).resolve())
        
        for item in self.file_list:
            if item.filepath == filepath:
                return
        
        file_item = FileListItem(filepath)
        if file_item.load():
            self.file_list.append(file_item)
            
            list_item = QListWidgetItem(file_item.name)
            list_item.setData(Qt.ItemDataRole.UserRole, file_item.filepath)
            self.file_list_widget.addItem(list_item)
            
            self.update_file_info()
            self.refresh_compare_file_list()
    
    def remove_selected_files(self):
        selected_items = self.file_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "提示", "请先选择要移除的文件")
            return
        
        for item in selected_items:
            filepath = item.data(Qt.ItemDataRole.UserRole)
            self.file_list = [f for f in self.file_list if f.filepath != filepath]
            self.file_list_widget.takeItem(self.file_list_widget.row(item))
        
        self.update_file_info()
        self.refresh_compare_file_list()
    
    def clear_all_files(self):
        if not self.file_list:
            return
        
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有文件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.file_list.clear()
            self.file_list_widget.clear()
            self.preview_text.clear()
            self.current_file_item = None
            self.update_file_info()
            self.refresh_compare_file_list()
    
    def update_file_info(self):
        self.file_count_label.setText(f"文件数: {len(self.file_list)}")
        total_lines = sum(f.line_count() for f in self.file_list)
        self.total_lines_label.setText(f"总行数: {total_lines}")
    
    def refresh_compare_file_list(self):
        current_a = self.compare_file_a_combo.currentText()
        current_b = self.compare_file_b_combo.currentText()
        
        self.compare_file_a_combo.clear()
        self.compare_file_b_combo.clear()
        
        for item in self.file_list:
            self.compare_file_a_combo.addItem(item.name, item.filepath)
            self.compare_file_b_combo.addItem(item.name, item.filepath)
        
        if current_a:
            index = self.compare_file_a_combo.findText(current_a)
            if index >= 0:
                self.compare_file_a_combo.setCurrentIndex(index)
        if current_b:
            index = self.compare_file_b_combo.findText(current_b)
            if index >= 0:
                self.compare_file_b_combo.setCurrentIndex(index)
    
    def on_file_select(self, item):
        filepath = item.data(Qt.ItemDataRole.UserRole)
        self.preview_file(filepath)
    
    def on_file_double_click(self, item):
        filepath = item.data(Qt.ItemDataRole.UserRole)
        if os.path.exists(filepath):
            os.startfile(filepath)
    
    def preview_file(self, filepath):
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'rb') as f:
                raw_content = f.read(50000)
            
            file_item = None
            for item in self.file_list:
                if item.filepath == filepath:
                    file_item = item
                    break
            
            if not file_item:
                file_item = FileListItem(filepath)
                file_item.load()
            
            lines = file_item.lines[:200]
            
            self.preview_text.clear()
            self.preview_text.setPlainText(file_item.newline_char.join(lines))
            if len(file_item.lines) > 200:
                cursor = self.preview_text.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                cursor.insertText(f"\n\n... 共 {len(file_item.lines)} 行，仅显示前200行 ...")
            
            self.current_file_item = file_item
            self.line_count_label.setText(f"行数: {len(file_item.lines)}")
            self.status_label.setText(f"预览: {file_item.name}")
        except Exception as e:
            self.preview_text.clear()
            self.preview_text.setPlainText(f"预览失败: {str(e)}")
    
    def toggle_dedup_separator(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.dedup_separator_combo.setEnabled(enabled)
        self.dedup_custom_separator.setEnabled(enabled)
        
        if not enabled:
            self.dedup_param_check.setChecked(False)
    
    def toggle_dedup_param(self, state):
        enabled = state == Qt.CheckState.Checked.value
        
        if enabled:
            self.dedup_separator_check.setChecked(True)
        
        self.dedup_param_position.setEnabled(enabled)
    
    def toggle_compare_param(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.compare_separator_combo.setEnabled(enabled)
        self.compare_custom_separator.setEnabled(enabled)
        self.compare_col_spin.setEnabled(enabled)
    
    def select_export_columns(self):
        dialog = ColumnSelectDialog(self, 100, self.export_columns)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            columns = dialog.get_columns()
            self.export_columns = columns
            if columns:
                self.export_columns_display.setText(f"已选: {','.join(str(c) for c in columns)}")
            else:
                self.export_columns_display.setText("全部列")
    
    def get_dedup_separator(self):
        if self.dedup_separator_combo.currentText() == '其他':
            return self.dedup_custom_separator.text()
        elif self.dedup_separator_combo.currentText() == '\\t':
            return '\t'
        else:
            return self.dedup_separator_combo.currentText()
    
    def get_export_input_separator(self):
        if self.export_input_separator.currentText() == '其他':
            return self.export_custom_input.text()
        elif self.export_input_separator.currentText() == '\\t':
            return '\t'
        else:
            return self.export_input_separator.currentText()
    
    def get_export_output_separator(self):
        if self.export_output_separator.currentText() == '其他':
            return self.export_custom_output.text()
        elif self.export_output_separator.currentText() == '\\t':
            return '\t'
        else:
            return self.export_output_separator.currentText()
    
    def get_compare_separator(self):
        if self.compare_separator_combo.currentText() == '其他':
            return self.compare_custom_separator.text()
        elif self.compare_separator_combo.currentText() == '\\t':
            return '\t'
        else:
            return self.compare_separator_combo.currentText()
    
    def get_dedup_key(self, line, use_separator, separator, use_param, param_pos):
        if not use_separator:
            return line.strip()
        
        if not separator:
            return line.strip()
        
        parts = line.split(separator)
        
        if not use_param:
            return tuple(p.strip() for p in parts)
        
        try:
            pos = int(param_pos) - 1
            if 0 <= pos < len(parts):
                return parts[pos].strip()
            else:
                return line.strip()
        except:
            return line.strip()
    
    def save_output_file(self, content, suffix, base_name=None):
        self.ensure_work_dir()
        
        if base_name and self.current_file_item:
            original_name = Path(base_name).stem
        elif self.current_file_item:
            original_name = Path(self.current_file_item.name).stem
        else:
            original_name = "output"
        
        new_filename = f"{original_name}{suffix}.txt"
        new_filepath = Path(self.work_dir) / new_filename
        
        counter = 1
        while new_filepath.exists():
            new_filename = f"{original_name}{suffix}_{counter}.txt"
            new_filepath = Path(self.work_dir) / new_filename
            counter += 1
        
        try:
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(new_filepath)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")
            return None
    
    def execute_deduplication(self):
        if not self.current_file_item and not self.file_list:
            QMessageBox.warning(self, "警告", "请先导入文件")
            return
        
        target_item = self.current_file_item
        if not target_item and self.file_list:
            target_item = self.file_list[0]
        
        if not target_item:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return
        
        use_separator = self.dedup_separator_check.isChecked()
        separator = self.get_dedup_separator()
        use_param = self.dedup_param_check.isChecked()
        param_pos = self.dedup_param_position.value()
        
        seen = set()
        unique_lines = []
        duplicate_count = 0
        
        for line in target_item.lines:
            if not line.strip():
                unique_lines.append(line)
                continue
            
            key = self.get_dedup_key(line, use_separator, separator, use_param, param_pos)
            if key not in seen:
                seen.add(key)
                unique_lines.append(line)
            else:
                duplicate_count += 1
        
        if duplicate_count == 0:
            QMessageBox.information(self, "提示", "没有发现重复行")
            return
        
        suffix = self.dedup_output_suffix.text() or "_去重复"
        content = target_item.newline_char.join(unique_lines)
        if unique_lines and not unique_lines[-1].endswith(target_item.newline_char):
            content += target_item.newline_char
        
        output_path = self.save_output_file(content, suffix, target_item.filepath)
        
        if output_path:
            msg = f"去重完成！\n\n原始行数: {len(target_item.lines)}\n去重后行数: {len(unique_lines)}\n删除重复行: {duplicate_count}\n\n文件已保存至:\n{output_path}"
            QMessageBox.information(self, "完成", msg)
            self.status_label.setText(f"已生成: {Path(output_path).name}")
    
    def execute_export(self):
        if not self.current_file_item and not self.file_list:
            QMessageBox.warning(self, "警告", "请先导入文件")
            return
        
        target_item = self.current_file_item
        if not target_item and self.file_list:
            target_item = self.file_list[0]
        
        if not target_item:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return
        
        input_separator = self.get_export_input_separator()
        output_separator = self.get_export_output_separator()
        columns = self.export_columns
        
        if not input_separator:
            QMessageBox.warning(self, "警告", "请指定输入分隔符")
            return
        
        result_lines = []
        max_col = 0
        
        for line in target_item.lines:
            if not line.strip():
                result_lines.append(line)
                continue
            
            parts = line.split(input_separator)
            max_col = max(max_col, len(parts))
            
            if columns:
                selected_parts = []
                for col in columns:
                    idx = col - 1
                    if 0 <= idx < len(parts):
                        selected_parts.append(parts[idx].strip())
                    else:
                        selected_parts.append("")
                result_lines.append(output_separator.join(selected_parts))
            else:
                result_lines.append(output_separator.join([p.strip() for p in parts]))
        
        suffix = self.export_output_suffix.text() or "_导出"
        content = target_item.newline_char.join(result_lines)
        if result_lines and not result_lines[-1].endswith(target_item.newline_char):
            content += target_item.newline_char
        
        output_path = self.save_output_file(content, suffix, target_item.filepath)
        
        if output_path:
            col_info = f"已选列: {','.join(str(c) for c in columns)}" if columns else "全部列"
            msg = f"导出完成！\n\n总行数: {len(target_item.lines)}\n{col_info}\n输入分隔符: {repr(input_separator)}\n输出分隔符: {repr(output_separator)}\n\n文件已保存至:\n{output_path}"
            QMessageBox.information(self, "完成", msg)
            self.status_label.setText(f"已生成: {Path(output_path).name}")
    
    def execute_extract(self):
        if not self.current_file_item and not self.file_list:
            QMessageBox.warning(self, "警告", "请先导入文件")
            return
        
        target_item = self.current_file_item
        if not target_item and self.file_list:
            target_item = self.file_list[0]
        
        if not target_item:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return
        
        is_keyword = self.extract_keyword_radio.isChecked()
        is_regex = self.extract_regex_radio.isChecked()
        is_rule = self.extract_rule_radio.isChecked()
        
        case_sensitive = self.case_sensitive_check.isChecked()
        invert = self.invert_check.isChecked()
        
        result_lines = []
        match_count = 0
        
        if is_keyword:
            keyword_text = self.keyword_edit.text().strip()
            if not keyword_text:
                QMessageBox.warning(self, "警告", "请输入关键词")
                return
            
            keywords = [k.strip() for k in keyword_text.split(',') if k.strip()]
            
            for line in target_item.lines:
                matched = False
                for kw in keywords:
                    if case_sensitive:
                        if kw in line:
                            matched = True
                            break
                    else:
                        if kw.lower() in line.lower():
                            matched = True
                            break
                
                if (matched and not invert) or (not matched and invert):
                    result_lines.append(line)
                    match_count += 1
        
        elif is_regex:
            pattern_text = self.regex_edit.text().strip()
            if not pattern_text:
                QMessageBox.warning(self, "警告", "请输入正则表达式")
                return
            
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = re.compile(pattern_text, flags)
                
                for line in target_item.lines:
                    matched = bool(pattern.search(line))
                    if (matched and not invert) or (not matched and invert):
                        result_lines.append(line)
                        match_count += 1
            except Exception as e:
                QMessageBox.critical(self, "错误", f"正则表达式错误: {str(e)}")
                return
        
        elif is_rule:
            rule_text = self.keyword_edit.text().strip()
            if not rule_text:
                QMessageBox.warning(self, "警告", "请输入匹配规则（关键词）")
                return
            
            rules = [r.strip() for r in rule_text.split(',') if r.strip()]
            
            for line in target_item.lines:
                matched = False
                for rule in rules:
                    if case_sensitive:
                        if rule in line:
                            matched = True
                            break
                    else:
                        if rule.lower() in line.lower():
                            matched = True
                            break
                
                if (matched and not invert) or (not matched and invert):
                    result_lines.append(line)
                    match_count += 1
        
        if match_count == 0:
            QMessageBox.information(self, "提示", "没有找到匹配的行")
            return
        
        suffix = self.extract_output_suffix.text() or "_提取"
        content = target_item.newline_char.join(result_lines)
        if result_lines and not result_lines[-1].endswith(target_item.newline_char):
            content += target_item.newline_char
        
        output_path = self.save_output_file(content, suffix, target_item.filepath)
        
        if output_path:
            mode_text = "关键词" if is_keyword else ("正则" if is_regex else "规则匹配")
            msg = f"提取完成！\n\n原始行数: {len(target_item.lines)}\n提取行数: {match_count}\n提取模式: {mode_text}\n\n文件已保存至:\n{output_path}"
            QMessageBox.information(self, "完成", msg)
            self.status_label.setText(f"已生成: {Path(output_path).name}")
    
    def execute_split(self):
        if not self.current_file_item and not self.file_list:
            QMessageBox.warning(self, "警告", "请先导入文件")
            return
        
        target_item = self.current_file_item
        if not target_item and self.file_list:
            target_item = self.file_list[0]
        
        if not target_item:
            QMessageBox.warning(self, "警告", "请先选择文件")
            return
        
        lines_per_file = self.split_lines_spin.value()
        prefix = self.split_prefix_edit.text() or "_分割文本"
        
        total_lines = len(target_item.lines)
        file_count = (total_lines + lines_per_file - 1) // lines_per_file
        
        if file_count <= 1:
            QMessageBox.information(self, "提示", f"文件行数不足，无需分割\n总行数: {total_lines}\n每文件行数: {lines_per_file}")
            return
        
        self.ensure_work_dir()
        original_name = Path(target_item.name).stem
        saved_files = []
        
        for i in range(file_count):
            start = i * lines_per_file
            end = min((i + 1) * lines_per_file, total_lines)
            chunk_lines = target_item.lines[start:end]
            
            content = target_item.newline_char.join(chunk_lines)
            if chunk_lines and not chunk_lines[-1].endswith(target_item.newline_char):
                content += target_item.newline_char
            
            new_filename = f"{original_name}{prefix}{i + 1}.txt"
            new_filepath = Path(self.work_dir) / new_filename
            
            counter = 1
            while new_filepath.exists():
                new_filename = f"{original_name}{prefix}{i + 1}_{counter}.txt"
                new_filepath = Path(self.work_dir) / new_filename
                counter += 1
            
            try:
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(str(new_filepath))
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")
                return
        
        if saved_files:
            msg = f"分割完成！\n\n原始行数: {total_lines}\n每文件行数: {lines_per_file}\n生成文件数: {file_count}\n\n文件已保存至工作目录"
            QMessageBox.information(self, "完成", msg)
            self.status_label.setText(f"已生成 {file_count} 个分割文件")
    
    def execute_merge(self):
        selected_items = self.file_list_widget.selectedItems()
        if len(selected_items) < 2:
            QMessageBox.warning(self, "警告", "请至少选择2个文件进行合并\n（按住Ctrl或Shift可多选）")
            return
        
        ordered_filepaths = []
        for i in range(self.file_list_widget.count()):
            item = self.file_list_widget.item(i)
            if item.isSelected():
                ordered_filepaths.append(item.data(Qt.ItemDataRole.UserRole))
        
        if len(ordered_filepaths) < 2:
            QMessageBox.warning(self, "警告", "请至少选择2个文件进行合并")
            return
        
        output_name = self.merge_filename_edit.text().strip() or "合并结果"
        
        merged_lines = []
        total_files = len(ordered_filepaths)
        total_lines = 0
        
        for filepath in ordered_filepaths:
            for item in self.file_list:
                if item.filepath == filepath:
                    merged_lines.extend(item.lines)
                    total_lines += len(item.lines)
                    break
        
        if not merged_lines:
            QMessageBox.warning(self, "警告", "没有内容可合并")
            return
        
        newline_char = '\n'
        if self.file_list:
            newline_char = self.file_list[0].newline_char
        
        content = newline_char.join(merged_lines)
        if merged_lines and not merged_lines[-1].endswith(newline_char):
            content += newline_char
        
        output_path = self.save_output_file(content, "", output_name)
        
        if output_path:
            msg = f"合并完成！\n\n合并文件数: {total_files}\n总行数: {total_lines}\n\n文件已保存至:\n{output_path}"
            QMessageBox.information(self, "完成", msg)
            self.status_label.setText(f"已生成: {Path(output_path).name}")
    
    def execute_compare(self):
        idx_a = self.compare_file_a_combo.currentIndex()
        idx_b = self.compare_file_b_combo.currentIndex()
        
        if idx_a < 0 or idx_b < 0:
            QMessageBox.warning(self, "警告", "请选择文件A和文件B")
            return
        
        filepath_a = self.compare_file_a_combo.currentData()
        filepath_b = self.compare_file_b_combo.currentData()
        
        if filepath_a == filepath_b:
            QMessageBox.warning(self, "警告", "文件A和文件B不能是同一个文件")
            return
        
        file_a = None
        file_b = None
        
        for item in self.file_list:
            if item.filepath == filepath_a:
                file_a = item
            if item.filepath == filepath_b:
                file_b = item
        
        if not file_a or not file_b:
            QMessageBox.warning(self, "警告", "请确保文件已正确加载")
            return
        
        use_param_b = self.compare_use_param_check.isChecked()
        separator_b = self.get_compare_separator()
        col_pos_b = self.compare_col_spin.value()
        
        is_remove_mode = self.compare_remove_radio.isChecked()
        
        set_b = set()
        
        for line in file_b.lines:
            if not line.strip():
                continue
            
            if use_param_b:
                key = self.get_dedup_key(line, True, separator_b, True, col_pos_b)
            else:
                key = line.strip()
            set_b.add(key)
        
        result_lines = []
        match_count = 0
        
        for line in file_a.lines:
            if not line.strip():
                if not is_remove_mode:
                    result_lines.append(line)
                continue
            
            key = line.strip()
            in_b = key in set_b
            
            if is_remove_mode:
                if not in_b:
                    result_lines.append(line)
                    match_count += 1
            else:
                if in_b:
                    result_lines.append(line)
                    match_count += 1
        
        if match_count == 0:
            mode_text = "去除重复" if is_remove_mode else "提取共有"
            QMessageBox.information(self, "提示", f"没有找到匹配的行\n模式: {mode_text}")
            return
        
        suffix = self.compare_output_suffix.text() or "_对比结果"
        mode_suffix = "_去除重复" if is_remove_mode else "_共有数据"
        full_suffix = suffix + mode_suffix
        
        content = file_a.newline_char.join(result_lines)
        if result_lines and not result_lines[-1].endswith(file_a.newline_char):
            content += file_a.newline_char
        
        output_path = self.save_output_file(content, full_suffix, file_a.filepath)
        
        if output_path:
            mode_text = "去除A中含B的重复数据 (A - B)" if is_remove_mode else "提取A和B的共有数据 (A ∩ B)"
            msg = f"对比完成！\n\n模式: {mode_text}\n文件A行数: {len(file_a.lines)}\n文件B行数: {len(file_b.lines)}\n结果行数: {match_count}\n\n文件已保存至:\n{output_path}"
            QMessageBox.information(self, "完成", msg)
            self.status_label.setText(f"已生成: {Path(output_path).name}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = TextProcessorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
