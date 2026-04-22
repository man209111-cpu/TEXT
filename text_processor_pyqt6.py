# -*- coding: utf-8 -*-
import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QGroupBox, QPushButton, QLabel, QCheckBox, QComboBox,
    QLineEdit, QTabWidget, QListWidget, QTextEdit, QStatusBar, QFrame,
    QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QAction, QColor, QPalette


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
            self.setIconSize(QSize(20, 20))
        self.setMinimumHeight(36)
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
            header.setFixedHeight(36)
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(12, 0, 12, 0)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Microsoft YaHei UI", 10, QFont.Weight.Bold))
            header_layout.addWidget(title_label)
            
            self.layout.addWidget(header)
            
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFixedHeight(1)
            self.layout.addWidget(separator)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addWidget(self.content_widget)
    
    def add_widget(self, widget):
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        self.content_layout.addLayout(layout)


class TextProcessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本处理工具")
        self.setMinimumSize(900, 600)
        self.resize(1100, 750)
        
        self.current_theme = "system"
        self.actual_theme = ThemeManager.detect_system_theme()
        self.theme_colors = ThemeManager.LIGHT if self.actual_theme == "light" else ThemeManager.DARK
        
        self.current_file = None
        self.file_content = []
        self.newline_char = '\n'
        self.history_file = Path(__file__).parent / "history.json"
        self.history = {"imported": [], "generated": []}
        self.max_history = 20
        
        self.use_separator = False
        self.use_specific_param = False
        
        self.load_history()
        self.setup_ui()
        self.apply_theme(self.actual_theme)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("文本处理工具")
        title_label.setFont(QFont("Microsoft YaHei UI", 16, QFont.Weight.Bold))
        top_bar_layout.addWidget(title_label)
        
        top_bar_layout.addStretch()
        
        theme_label = QLabel("主题:")
        theme_label.setFont(QFont("Microsoft YaHei UI", 9))
        top_bar_layout.addWidget(theme_label)
        
        self.theme_light_btn = StyledButton("浅色", button_type="secondary")
        self.theme_light_btn.setMinimumWidth(60)
        self.theme_light_btn.setMinimumHeight(28)
        self.theme_light_btn.clicked.connect(lambda: self.set_theme("light"))
        top_bar_layout.addWidget(self.theme_light_btn)
        
        self.theme_dark_btn = StyledButton("深色", button_type="secondary")
        self.theme_dark_btn.setMinimumWidth(60)
        self.theme_dark_btn.setMinimumHeight(28)
        self.theme_dark_btn.clicked.connect(lambda: self.set_theme("dark"))
        top_bar_layout.addWidget(self.theme_dark_btn)
        
        self.theme_system_btn = StyledButton("跟随系统", button_type="secondary")
        self.theme_system_btn.setMinimumWidth(80)
        self.theme_system_btn.setMinimumHeight(28)
        self.theme_system_btn.clicked.connect(lambda: self.set_theme("system"))
        top_bar_layout.addWidget(self.theme_system_btn)
        
        main_layout.addWidget(top_bar)
        
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        actions_card = CardWidget("操作")
        
        self.import_btn = StyledButton("导入文件", button_type="primary")
        self.import_btn.setMinimumHeight(40)
        self.import_btn.clicked.connect(self.import_file)
        actions_card.add_widget(self.import_btn)
        
        self.process_btn = StyledButton("去重处理", button_type="primary")
        self.process_btn.setMinimumHeight(40)
        self.process_btn.clicked.connect(self.process_deduplication)
        actions_card.add_widget(self.process_btn)
        
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFixedHeight(1)
        actions_card.add_widget(separator1)
        
        self.open_folder_btn = StyledButton("打开目录", button_type="secondary")
        self.open_folder_btn.setMinimumHeight(32)
        self.open_folder_btn.clicked.connect(self.open_containing_folder)
        actions_card.add_widget(self.open_folder_btn)
        
        self.clear_history_btn = StyledButton("清空历史", button_type="secondary")
        self.clear_history_btn.setMinimumHeight(32)
        self.clear_history_btn.clicked.connect(self.clear_history)
        actions_card.add_widget(self.clear_history_btn)
        
        left_layout.addWidget(actions_card)
        
        history_card = CardWidget("历史记录")
        
        history_tabs = QTabWidget()
        
        import_tab = QWidget()
        import_layout = QVBoxLayout(import_tab)
        import_layout.setContentsMargins(8, 8, 8, 8)
        
        self.import_listbox = QListWidget()
        self.import_listbox.itemClicked.connect(self.on_import_select)
        self.import_listbox.itemDoubleClicked.connect(self.on_import_double_click)
        import_layout.addWidget(self.import_listbox)
        
        history_tabs.addTab(import_tab, "导入记录")
        
        generated_tab = QWidget()
        generated_layout = QVBoxLayout(generated_tab)
        generated_layout.setContentsMargins(8, 8, 8, 8)
        
        self.generated_listbox = QListWidget()
        self.generated_listbox.itemClicked.connect(self.on_generated_select)
        self.generated_listbox.itemDoubleClicked.connect(self.on_generated_double_click)
        generated_layout.addWidget(self.generated_listbox)
        
        history_tabs.addTab(generated_tab, "生成记录")
        
        history_card.add_widget(history_tabs)
        
        left_layout.addWidget(history_card, stretch=1)
        
        content_splitter.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        config_card = CardWidget("去重配置")
        
        self.separator_check = QCheckBox("使用分隔符分割行进行比较")
        self.separator_check.stateChanged.connect(self.toggle_separator_options)
        config_card.add_widget(self.separator_check)
        
        separator_row = QHBoxLayout()
        
        separator_label = QLabel("分隔符:")
        separator_row.addWidget(separator_label)
        
        self.separator_combo = QComboBox()
        self.separator_combo.addItems([',', ';', '\\t', '|', ' ', '其他'])
        self.separator_combo.setEnabled(False)
        self.separator_combo.setMinimumWidth(80)
        separator_row.addWidget(self.separator_combo)
        
        custom_label = QLabel("自定义:")
        separator_row.addWidget(custom_label)
        
        self.custom_separator = QLineEdit()
        self.custom_separator.setEnabled(False)
        self.custom_separator.setMaximumWidth(80)
        separator_row.addWidget(self.custom_separator)
        
        separator_row.addStretch()
        
        config_card.add_layout(separator_row)
        
        self.param_check = QCheckBox("仅根据指定列参数去重")
        self.param_check.stateChanged.connect(self.toggle_param_options)
        config_card.add_widget(self.param_check)
        
        param_row = QHBoxLayout()
        
        param_label = QLabel("参数位置 (从1开始):")
        param_row.addWidget(param_label)
        
        self.param_position = QLineEdit("1")
        self.param_position.setEnabled(False)
        self.param_position.setMaximumWidth(60)
        param_row.addWidget(self.param_position)
        
        param_row.addStretch()
        
        config_card.add_layout(param_row)
        
        suffix_row = QHBoxLayout()
        
        suffix_label = QLabel("输出文件名后缀:")
        suffix_row.addWidget(suffix_label)
        
        self.output_suffix = QLineEdit("_去重复")
        self.output_suffix.setMaximumWidth(120)
        suffix_row.addWidget(self.output_suffix)
        
        suffix_row.addStretch()
        
        config_card.add_layout(suffix_row)
        
        right_layout.addWidget(config_card)
        
        preview_card = CardWidget("文件预览")
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont("Consolas", 10))
        self.preview_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        preview_card.add_widget(self.preview_text)
        
        right_layout.addWidget(preview_card, stretch=1)
        
        content_splitter.addWidget(right_panel)
        content_splitter.setSizes([300, 800])
        
        main_layout.addWidget(content_splitter, stretch=1)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label, stretch=1)
        
        self.line_count_label = QLabel("行数: 0")
        self.status_bar.addPermanentWidget(self.line_count_label)
        
        self.newline_label = QLabel("换行符: 未知")
        self.status_bar.addPermanentWidget(self.newline_label)
        
        self.update_history_display()
        self.setup_icons()
    
    def setup_icons(self):
        from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen
        from PyQt6.QtCore import Qt, QRectF
        
        def create_icon(icon_type):
            pixmap = QPixmap(20, 20)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            if self.actual_theme == "dark":
                primary_color = QColor(self.theme_colors['button_primary'])
            else:
                primary_color = QColor(self.theme_colors['button_primary'])
            
            painter.setPen(QPen(primary_color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            if icon_type == "folder":
                painter.drawRoundedRect(QRectF(2, 6, 16, 12), 2, 2)
                painter.drawRect(QRectF(2, 3, 8, 5))
                painter.drawLine(10, 3, 18, 3)
                painter.drawLine(18, 3, 18, 6)
            elif icon_type == "reload":
                painter.drawArc(QRectF(3, 3, 14, 14), 30 * 16, 300 * 16)
                painter.drawLine(16, 6, 18, 3)
                painter.drawLine(16, 6, 13, 8)
            elif icon_type == "open":
                painter.drawRoundedRect(QRectF(2, 4, 16, 12), 2, 2)
                painter.drawLine(2, 8, 18, 8)
                painter.drawLine(6, 8, 8, 11)
                painter.drawLine(10, 8, 14, 8)
                painter.drawLine(14, 8, 12, 11)
            elif icon_type == "trash":
                painter.drawRoundedRect(QRectF(5, 2, 10, 16), 2, 2)
                painter.drawLine(2, 4, 18, 4)
                painter.drawLine(7, 6, 7, 14)
                painter.drawLine(10, 6, 10, 14)
                painter.drawLine(13, 6, 13, 14)
            
            painter.end()
            return QIcon(pixmap)
        
        self.import_btn.setIcon(create_icon("folder"))
        self.process_btn.setIcon(create_icon("reload"))
        self.open_folder_btn.setIcon(create_icon("open"))
        self.clear_history_btn.setIcon(create_icon("trash"))
    
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
        
        self.update_history_display()
        self.update_styles()
    
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
            CardWidget {{
                background-color: {self.theme_colors['card_bg']};
                border: 1px solid {card_border};
                border-radius: 6px;
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
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: normal;
            }}
            QPushButton:hover {{
                background-color: {primary_hover};
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
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {entry_border};
                border-radius: 3px;
                background-color: {entry_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {primary_bg};
                border-color: {primary_bg};
            }}
            QComboBox {{
                background-color: {entry_bg};
                color: {entry_fg};
                border: 1px solid {entry_border};
                border-radius: 4px;
                padding: 5px 10px;
                min-height: 20px;
            }}
            QComboBox:hover {{
                border-color: {entry_focus};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
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
                border-radius: 4px;
                padding: 5px 8px;
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
            QListWidget {{
                background-color: {listbox_bg};
                color: {listbox_fg};
                border: 1px solid {card_border};
                border-radius: 4px;
            }}
            QListWidget::item {{
                padding: 5px;
                border-radius: 3px;
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
                border-radius: 4px;
            }}
            QTabWidget::pane {{
                border: 1px solid {card_border};
                border-radius: 4px;
                background-color: {self.theme_colors['card_bg']};
            }}
            QTabBar::tab {{
                background-color: {self.theme_colors['header_bg']};
                color: {self.theme_colors['header_fg']};
                padding: 8px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.theme_colors['card_bg']};
                color: {self.theme_colors['fg']};
            }}
            QTabBar::tab:hover {{
                background-color: {self.theme_colors['card_bg']};
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
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.theme_colors['scrollbar_thumb']};
                min-height: 30px;
                border-radius: 6px;
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
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {self.theme_colors['scrollbar_thumb']};
                min-width: 30px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {self.theme_colors['fg']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
    
    def set_theme(self, theme):
        self.current_theme = theme
        if theme == "system":
            self.actual_theme = ThemeManager.detect_system_theme()
        else:
            self.actual_theme = theme
        self.apply_theme(self.actual_theme)
    
    def toggle_separator_options(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.separator_combo.setEnabled(enabled)
        self.custom_separator.setEnabled(enabled)
        self.use_separator = enabled
        
        if not enabled:
            self.param_check.setChecked(False)
    
    def toggle_param_options(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.use_specific_param = enabled
        
        if enabled:
            self.separator_check.setChecked(True)
        
        self.param_position.setEnabled(enabled)
    
    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = {"imported": [], "generated": []}
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def add_import_history(self, filepath):
        self._add_to_history("imported", filepath)
    
    def add_generated_history(self, filepath):
        self._add_to_history("generated", filepath)
    
    def _add_to_history(self, history_type, filepath):
        filepath = str(Path(filepath).resolve())
        if filepath in self.history[history_type]:
            self.history[history_type].remove(filepath)
        self.history[history_type].insert(0, filepath)
        if len(self.history[history_type]) > self.max_history:
            self.history[history_type] = self.history[history_type][:self.max_history]
        self.save_history()
        self.update_history_display()
    
    def update_history_display(self):
        self.import_listbox.clear()
        for filepath in self.history["imported"]:
            self.import_listbox.addItem(Path(filepath).name)
        
        self.generated_listbox.clear()
        for filepath in self.history["generated"]:
            self.generated_listbox.addItem(Path(filepath).name)
    
    def on_import_select(self, item):
        idx = self.import_listbox.row(item)
        if idx < len(self.history["imported"]):
            filepath = self.history["imported"][idx]
            self._preview_file(filepath)
    
    def on_generated_select(self, item):
        idx = self.generated_listbox.row(item)
        if idx < len(self.history["generated"]):
            filepath = self.history["generated"][idx]
            self._preview_file(filepath)
    
    def on_import_double_click(self, item):
        idx = self.import_listbox.row(item)
        if idx < len(self.history["imported"]):
            filepath = self.history["imported"][idx]
            self.load_file(filepath)
    
    def on_generated_double_click(self, item):
        idx = self.generated_listbox.row(item)
        if idx < len(self.history["generated"]):
            filepath = self.history["generated"][idx]
            self.open_file(filepath)
    
    def _preview_file(self, filepath):
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'rb') as f:
                raw_content = f.read(10000)
            
            detected = self.detect_encoding_and_newline(raw_content)
            encoding = detected['encoding']
            newline_char = detected['newline_char']
            
            content = raw_content.decode(encoding, errors='replace')
            
            lines = content.split(newline_char)
            preview_lines = lines[:100]
            
            self.preview_text.clear()
            self.preview_text.setPlainText(newline_char.join(preview_lines))
            if len(lines) > 100:
                cursor = self.preview_text.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                cursor.insertText(f"\n\n... 共 {len(lines)} 行，仅显示前100行 ...")
            
            self.status_label.setText(f"预览: {Path(filepath).name} ({len(lines)} 行)")
        except Exception as e:
            self.preview_text.clear()
            self.preview_text.setPlainText(f"预览失败: {str(e)}")
    
    def open_containing_folder(self):
        import_selection = self.import_listbox.currentRow()
        generated_selection = self.generated_listbox.currentRow()
        
        filepath = None
        
        if import_selection >= 0:
            if import_selection < len(self.history["imported"]):
                filepath = self.history["imported"][import_selection]
        elif generated_selection >= 0:
            if generated_selection < len(self.history["generated"]):
                filepath = self.history["generated"][generated_selection]
        
        if filepath and os.path.exists(filepath):
            folder_path = os.path.dirname(filepath)
            os.startfile(folder_path)
        else:
            QMessageBox.information(self, "提示", "请先选择一个历史记录文件")
    
    def clear_history(self):
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有历史记录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.history = {"imported": [], "generated": []}
            self.save_history()
            self.update_history_display()
            QMessageBox.information(self, "完成", "历史记录已清空")
    
    def open_file(self, filepath):
        if os.path.exists(filepath):
            os.startfile(filepath)
        else:
            QMessageBox.critical(self, "错误", f"文件不存在: {filepath}")
    
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
            self.load_file(filepath)
    
    def load_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                raw_content = f.read()
            
            detected = self.detect_encoding_and_newline(raw_content)
            encoding = detected['encoding']
            newline_char = detected['newline_char']
            newline_name = detected['newline_name']
            
            content = raw_content.decode(encoding, errors='replace')
            self.file_content = content.split(newline_char)
            self.newline_char = newline_char
            self.current_file = filepath
            
            self.add_import_history(filepath)
            
            self._preview_file(filepath)
            self.line_count_label.setText(f"行数: {len(self.file_content)}")
            self.newline_label.setText(f"换行符: {newline_name}")
            self.status_label.setText(f"已加载: {Path(filepath).name}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取文件失败: {str(e)}")
    
    def detect_encoding_and_newline(self, raw_content):
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
        
        return {
            'encoding': encoding,
            'newline_char': newline_char,
            'newline_name': newline_name
        }
    
    def get_separator(self):
        if self.separator_combo.currentText() == '其他':
            return self.custom_separator.text()
        elif self.separator_combo.currentText() == '\\t':
            return '\t'
        else:
            return self.separator_combo.currentText()
    
    def get_dedup_key(self, line):
        if not self.use_separator:
            return line.strip()
        
        separator = self.get_separator()
        if not separator:
            return line.strip()
        
        parts = line.split(separator)
        
        if not self.use_specific_param:
            return tuple(p.strip() for p in parts)
        
        try:
            pos = int(self.param_position.text()) - 1
            if 0 <= pos < len(parts):
                return parts[pos].strip()
            else:
                return line.strip()
        except:
            return line.strip()
    
    def process_deduplication(self):
        if not self.file_content:
            QMessageBox.warning(self, "警告", "请先导入文件")
            return
        
        seen = set()
        unique_lines = []
        duplicate_count = 0
        
        for line in self.file_content:
            key = self.get_dedup_key(line)
            if key not in seen:
                seen.add(key)
                unique_lines.append(line)
            else:
                duplicate_count += 1
        
        if duplicate_count == 0:
            QMessageBox.information(self, "提示", "没有发现重复行")
            return
        
        original_path = Path(self.current_file)
        suffix = self.output_suffix.text()
        new_filename = f"{original_path.stem}{suffix}{original_path.suffix}"
        new_filepath = original_path.parent / new_filename
        
        try:
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(self.newline_char.join(unique_lines))
                if unique_lines and not unique_lines[-1].endswith(self.newline_char):
                    f.write(self.newline_char)
            
            self.add_generated_history(str(new_filepath))
            
            msg = f"去重完成！\n\n原始行数: {len(self.file_content)}\n去重后行数: {len(unique_lines)}\n删除重复行: {duplicate_count}\n\n文件已保存至:\n{new_filepath}"
            QMessageBox.information(self, "完成", msg)
            
            self._preview_file(str(new_filepath))
            self.status_label.setText(f"已生成: {new_filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = TextProcessorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
