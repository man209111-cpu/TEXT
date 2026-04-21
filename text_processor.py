# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from pathlib import Path


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
        'checkbutton_bg': '#ffffff',
        'checkbutton_fg': '#424242',
        'notebook_bg': '#f5f5f5',
        'notebook_fg': '#616161',
        'notebook_active_bg': '#ffffff',
        'notebook_active_fg': '#212121',
        'separator': '#e0e0e0',
        'tooltip_bg': '#f5f5f5',
        'tooltip_fg': '#424242',
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
        'checkbutton_bg': '#1e1e1e',
        'checkbutton_fg': '#bdbdbd',
        'notebook_bg': '#1e1e1e',
        'notebook_fg': '#9e9e9e',
        'notebook_active_bg': '#2d2d2d',
        'notebook_active_fg': '#e0e0e0',
        'separator': '#2d2d2d',
        'tooltip_bg': '#2d2d2d',
        'tooltip_fg': '#e0e0e0',
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


class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.theme_colors = None
        
        self.height = kwargs.get('height', 36)
        self.width = kwargs.get('width', 120)
        self.corner_radius = kwargs.get('corner_radius', 6)
        self.padding = kwargs.get('padding', 10)
        
        super().__init__(
            parent,
            width=self.width,
            height=self.height,
            highlightthickness=0,
            cursor='hand2'
        )
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self.bind('<ButtonRelease-1>', self._on_release)
    
    def set_theme(self, theme_colors):
        self.theme_colors = theme_colors
        self._draw()
    
    def _get_colors(self):
        if not self.theme_colors:
            return {
                'bg': '#2196F3',
                'fg': '#ffffff',
                'hover': '#1976D2',
                'border': None
            }
        
        if self.style == 'primary':
            return {
                'bg': self.theme_colors['button_primary'],
                'fg': self.theme_colors['button_primary_text'],
                'hover': self.theme_colors['button_primary_hover'],
                'border': None
            }
        elif self.style == 'danger':
            return {
                'bg': self.theme_colors['danger'],
                'fg': self.theme_colors['danger_text'],
                'hover': self.theme_colors['danger_hover'],
                'border': None
            }
        else:
            return {
                'bg': self.theme_colors['button_secondary'],
                'fg': self.theme_colors['button_secondary_text'],
                'hover': self.theme_colors['button_secondary_hover'],
                'border': self.theme_colors['button_secondary_border']
            }
    
    def _draw(self, hover=False):
        colors = self._get_colors()
        bg_color = colors['hover'] if hover else colors['bg']
        
        self.delete('all')
        
        self._create_rounded_rect(
            0, 0, self.winfo_width(), self.winfo_height(),
            self.corner_radius,
            fill=bg_color,
            outline=colors.get('border', '')
        )
        
        self.create_text(
            self.winfo_width() // 2,
            self.winfo_height() // 2,
            text=self.text,
            fill=colors['fg'],
            font=('Microsoft YaHei UI', 10, 'normal')
        )
    
    def _create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2 - radius,
            x1, y1 + radius
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _on_enter(self, event):
        self._draw(hover=True)
    
    def _on_leave(self, event):
        self._draw(hover=False)
    
    def _on_click(self, event):
        pass
    
    def _on_release(self, event):
        if self.command:
            self.command()
    
    def configure(self, **kwargs):
        if 'text' in kwargs:
            self.text = kwargs.pop('text')
            self._draw()
        super().configure(**kwargs)


class ModernCard(ttk.Frame):
    def __init__(self, parent, text="", theme_colors=None, **kwargs):
        self.theme_colors = theme_colors or ThemeManager.LIGHT
        super().__init__(parent, style='Card.TFrame', **kwargs)
        
        if text:
            header_frame = tk.Frame(
                self,
                bg=self.theme_colors['header_bg'],
                padx=12,
                pady=8
            )
            header_frame.pack(fill=tk.X)
            
            self.header_label = tk.Label(
                header_frame,
                text=text,
                bg=self.theme_colors['header_bg'],
                fg=self.theme_colors['header_fg'],
                font=('Microsoft YaHei UI', 10, 'bold')
            )
            self.header_label.pack(anchor=tk.W)
            
            tk.Frame(
                self,
                bg=self.theme_colors['separator'],
                height=1
            ).pack(fill=tk.X)
    
    def set_theme(self, theme_colors):
        self.theme_colors = theme_colors


class TextProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("文本处理工具")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        
        self.current_theme = "system"
        self.actual_theme = ThemeManager.detect_system_theme()
        self.theme_colors = ThemeManager.LIGHT if self.actual_theme == "light" else ThemeManager.DARK
        
        self.current_file = None
        self.file_content = []
        self.newline_char = '\n'
        self.history_file = Path(__file__).parent / "history.json"
        self.history = {"imported": [], "generated": []}
        self.max_history = 20
        
        self.load_history()
        self.setup_styles()
        self.setup_ui()
        self.apply_theme(self.actual_theme)
    
    def setup_styles(self):
        self.style = ttk.Style()
        
        self.style.configure('Card.TFrame', background=self.theme_colors['card_bg'])
        self.style.configure('Main.TFrame', background=self.theme_colors['bg'])
        self.style.configure('Status.TLabel', 
            background=self.theme_colors['statusbar_bg'],
            foreground=self.theme_colors['statusbar_fg'],
            padding=(8, 4)
        )
        
        self.style.configure('TNotebook',
            background=self.theme_colors['notebook_bg'],
            borderwidth=0
        )
        self.style.configure('TNotebook.Tab',
            background=self.theme_colors['notebook_bg'],
            foreground=self.theme_colors['notebook_fg'],
            padding=(15, 6),
            font=('Microsoft YaHei UI', 9)
        )
        self.style.map('TNotebook.Tab',
            background=[('selected', self.theme_colors['notebook_active_bg'])],
            foreground=[('selected', self.theme_colors['notebook_active_fg'])]
        )
        
        self.style.configure('TCheckbutton',
            background=self.theme_colors['checkbutton_bg'],
            foreground=self.theme_colors['checkbutton_fg'],
            font=('Microsoft YaHei UI', 9)
        )
        
        self.style.configure('TLabel',
            background=self.theme_colors['card_bg'],
            foreground=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        )
        
        self.style.configure('TSeparator',
            background=self.theme_colors['separator']
        )
    
    def create_rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2 - radius,
            x1, y1 + radius
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_modern_entry(self, parent, textvariable=None, width=20, state='normal'):
        frame = tk.Frame(parent, bg=self.theme_colors['card_bg'])
        
        entry_bg = self.theme_colors['entry_bg']
        entry_fg = self.theme_colors['entry_fg']
        
        entry = tk.Entry(
            frame,
            textvariable=textvariable,
            bg=entry_bg,
            fg=entry_fg,
            insertbackground=entry_fg,
            bd=0,
            highlightthickness=1,
            highlightcolor=self.theme_colors['entry_focus_border'],
            highlightbackground=self.theme_colors['entry_border'],
            selectbackground=self.theme_colors['select_bg'],
            selectforeground=self.theme_colors['select_fg'],
            disabledbackground=self.theme_colors['disabled_bg'],
            disabledforeground=self.theme_colors['disabled_fg'],
            width=width,
            font=('Consolas', 10),
            state=state
        )
        entry.pack(fill=tk.X, padx=8, pady=6)
        
        return frame, entry
    
    def create_modern_listbox(self, parent, **kwargs):
        listbox_bg = self.theme_colors['listbox_bg']
        listbox_fg = self.theme_colors['listbox_fg']
        select_bg = self.theme_colors['listbox_select_bg']
        select_fg = self.theme_colors['listbox_select_fg']
        
        listbox = tk.Listbox(
            parent,
            bg=listbox_bg,
            fg=listbox_fg,
            selectbackground=select_bg,
            selectforeground=select_fg,
            selectmode=tk.SINGLE,
            activestyle='none',
            bd=0,
            highlightthickness=1,
            highlightcolor=self.theme_colors['card_border'],
            highlightbackground=self.theme_colors['card_border'],
            font=('Consolas', 9),
            exportselection=False,
            **kwargs
        )
        
        return listbox
    
    def create_modern_text(self, parent, **kwargs):
        text_bg = self.theme_colors['text_bg']
        text_fg = self.theme_colors['text_fg']
        
        text_widget = tk.Text(
            parent,
            bg=text_bg,
            fg=text_fg,
            insertbackground=text_fg,
            selectbackground=self.theme_colors['select_bg'],
            selectforeground=self.theme_colors['select_fg'],
            bd=0,
            highlightthickness=1,
            highlightcolor=self.theme_colors['card_border'],
            highlightbackground=self.theme_colors['card_border'],
            font=('Consolas', 10),
            wrap=tk.NONE,
            **kwargs
        )
        
        return text_widget
    
    def create_modern_combobox(self, parent, textvariable=None, values=None, width=10, state='normal'):
        combo = ttk.Combobox(
            parent,
            textvariable=textvariable,
            values=values,
            width=width,
            state='readonly' if state == 'disabled' else 'readonly',
            font=('Consolas', 9)
        )
        
        return combo
    
    def create_modern_spinbox(self, parent, textvariable=None, from_=1, to=100, width=10, state='normal'):
        frame, entry = self.create_modern_entry(
            parent,
            textvariable=textvariable,
            width=width,
            state=state
        )
        
        return frame, entry
    
    def setup_ui(self):
        self.root.configure(bg=self.theme_colors['bg'])
        
        main_frame = tk.Frame(self.root, bg=self.theme_colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        top_bar = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        top_bar.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            top_bar,
            text="文本处理工具",
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 16, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        theme_frame = tk.Frame(top_bar, bg=self.theme_colors['bg'])
        theme_frame.pack(side=tk.RIGHT)
        
        theme_label = tk.Label(
            theme_frame,
            text="主题:",
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        )
        theme_label.pack(side=tk.LEFT, padx=(0, 8))
        
        self.theme_var = tk.StringVar(value="system")
        self.theme_light_btn = ModernButton(
            theme_frame, "浅色", command=lambda: self.set_theme("light"),
            style='secondary', width=60, height=28, corner_radius=4
        )
        self.theme_light_btn.pack(side=tk.LEFT, padx=2)
        
        self.theme_dark_btn = ModernButton(
            theme_frame, "深色", command=lambda: self.set_theme("dark"),
            style='secondary', width=60, height=28, corner_radius=4
        )
        self.theme_dark_btn.pack(side=tk.LEFT, padx=2)
        
        self.theme_system_btn = ModernButton(
            theme_frame, "跟随系统", command=lambda: self.set_theme("system"),
            style='secondary', width=80, height=28, corner_radius=4
        )
        self.theme_system_btn.pack(side=tk.LEFT, padx=2)
        
        content_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(content_frame, bg=self.theme_colors['bg'])
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        actions_card = ModernCard(left_panel, "操作", self.theme_colors)
        actions_card.pack(fill=tk.X, pady=(0, 10))
        
        actions_inner = tk.Frame(actions_card, bg=self.theme_colors['card_bg'], padx=15, pady=15)
        actions_inner.pack(fill=tk.BOTH, expand=True)
        
        self.import_btn = ModernButton(
            actions_inner, "📂 导入文件", command=self.import_file,
            style='primary', width=160, height=40, corner_radius=6
        )
        self.import_btn.pack(pady=(0, 10))
        
        self.process_btn = ModernButton(
            actions_inner, "🔄 去重处理", command=self.process_deduplication,
            style='primary', width=160, height=40, corner_radius=6
        )
        self.process_btn.pack(pady=(0, 5))
        
        tk.Frame(actions_inner, bg=self.theme_colors['separator'], height=1).pack(fill=tk.X, pady=10)
        
        self.open_folder_btn = ModernButton(
            actions_inner, "📁 打开目录", command=self.open_containing_folder,
            style='secondary', width=160, height=32, corner_radius=4
        )
        self.open_folder_btn.pack(pady=(0, 8))
        
        self.clear_history_btn = ModernButton(
            actions_inner, "🗑️ 清空历史", command=self.clear_history,
            style='danger', width=160, height=32, corner_radius=4
        )
        self.clear_history_btn.pack()
        
        history_card = ModernCard(left_panel, "历史记录", self.theme_colors)
        history_card.pack(fill=tk.BOTH, expand=True)
        
        history_inner = tk.Frame(history_card, bg=self.theme_colors['card_bg'])
        history_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        style = ttk.Style()
        style.configure('History.TNotebook', background=self.theme_colors['notebook_bg'])
        
        history_notebook = ttk.Notebook(history_inner, style='History.TNotebook')
        history_notebook.pack(fill=tk.BOTH, expand=True)
        
        import_tab = tk.Frame(history_notebook, bg=self.theme_colors['notebook_active_bg'])
        history_notebook.add(import_tab, text="  导入记录  ")
        
        self.import_listbox = self.create_modern_listbox(import_tab, height=8)
        self.import_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.import_listbox.bind('<<ListboxSelect>>', self.on_import_select)
        self.import_listbox.bind('<Double-1>', self.on_import_double_click)
        
        generated_tab = tk.Frame(history_notebook, bg=self.theme_colors['notebook_active_bg'])
        history_notebook.add(generated_tab, text="  生成记录  ")
        
        self.generated_listbox = self.create_modern_listbox(generated_tab, height=8)
        self.generated_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.generated_listbox.bind('<<ListboxSelect>>', self.on_generated_select)
        self.generated_listbox.bind('<Double-1>', self.on_generated_double_click)
        
        right_panel = tk.Frame(content_frame, bg=self.theme_colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        config_card = ModernCard(right_panel, "去重配置", self.theme_colors)
        config_card.pack(fill=tk.X, pady=(0, 10))
        
        config_inner = tk.Frame(config_card, bg=self.theme_colors['card_bg'], padx=15, pady=15)
        config_inner.pack(fill=tk.BOTH, expand=True)
        
        options_frame = tk.Frame(config_inner, bg=self.theme_colors['card_bg'])
        options_frame.pack(fill=tk.X)
        
        self.use_separator = tk.BooleanVar(value=False)
        separator_check = tk.Checkbutton(
            options_frame,
            text="使用分隔符分割行进行比较",
            variable=self.use_separator,
            command=self.toggle_separator_options,
            bg=self.theme_colors['checkbutton_bg'],
            fg=self.theme_colors['checkbutton_fg'],
            selectcolor=self.theme_colors['card_bg'],
            activebackground=self.theme_colors['card_bg'],
            activeforeground=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        )
        separator_check.pack(anchor=tk.W, pady=(0, 10))
        
        separator_row = tk.Frame(options_frame, bg=self.theme_colors['card_bg'])
        separator_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            separator_row,
            text="分隔符:",
            bg=self.theme_colors['card_bg'],
            fg=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        ).pack(side=tk.LEFT)
        
        self.separator_var = tk.StringVar(value=",")
        self.separator_combo = ttk.Combobox(
            separator_row,
            textvariable=self.separator_var,
            values=(',', ';', '\\t', '|', ' ', '其他'),
            width=8,
            state='disabled',
            font=('Consolas', 9)
        )
        self.separator_combo.pack(side=tk.LEFT, padx=8)
        
        tk.Label(
            separator_row,
            text="自定义:",
            bg=self.theme_colors['card_bg'],
            fg=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        ).pack(side=tk.LEFT, padx=(15, 0))
        
        self.custom_separator = tk.StringVar()
        self.custom_separator_frame, self.custom_separator_entry = self.create_modern_entry(
            separator_row,
            textvariable=self.custom_separator,
            width=8,
            state='disabled'
        )
        self.custom_separator_frame.pack(side=tk.LEFT, padx=8)
        
        self.use_specific_param = tk.BooleanVar(value=False)
        specific_param_check = tk.Checkbutton(
            options_frame,
            text="仅根据指定列参数去重",
            variable=self.use_specific_param,
            command=self.toggle_param_options,
            bg=self.theme_colors['checkbutton_bg'],
            fg=self.theme_colors['checkbutton_fg'],
            selectcolor=self.theme_colors['card_bg'],
            activebackground=self.theme_colors['card_bg'],
            activeforeground=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        )
        specific_param_check.pack(anchor=tk.W, pady=(0, 10))
        
        param_row = tk.Frame(options_frame, bg=self.theme_colors['card_bg'])
        param_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            param_row,
            text="参数位置 (从1开始):",
            bg=self.theme_colors['card_bg'],
            fg=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        ).pack(side=tk.LEFT)
        
        self.param_position = tk.StringVar(value="1")
        self.param_spinbox_frame, self.param_spinbox = self.create_modern_entry(
            param_row,
            textvariable=self.param_position,
            width=6,
            state='disabled'
        )
        self.param_spinbox_frame.pack(side=tk.LEFT, padx=8)
        
        suffix_row = tk.Frame(options_frame, bg=self.theme_colors['card_bg'])
        suffix_row.pack(fill=tk.X)
        
        tk.Label(
            suffix_row,
            text="输出文件名后缀:",
            bg=self.theme_colors['card_bg'],
            fg=self.theme_colors['fg'],
            font=('Microsoft YaHei UI', 9)
        ).pack(side=tk.LEFT)
        
        self.output_suffix = tk.StringVar(value="_去重复")
        self.suffix_frame, self.suffix_entry = self.create_modern_entry(
            suffix_row,
            textvariable=self.output_suffix,
            width=15
        )
        self.suffix_frame.pack(side=tk.LEFT, padx=8)
        
        preview_card = ModernCard(right_panel, "文件预览", self.theme_colors)
        preview_card.pack(fill=tk.BOTH, expand=True)
        
        preview_inner = tk.Frame(preview_card, bg=self.theme_colors['card_bg'])
        preview_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.preview_text = self.create_modern_text(preview_inner)
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        preview_scrollbar_y = tk.Scrollbar(
            preview_inner,
            orient=tk.VERTICAL,
            command=self.preview_text.yview,
            bg=self.theme_colors['scrollbar_bg'],
            troughcolor=self.theme_colors['scrollbar_bg'],
            activebackground=self.theme_colors['scrollbar_thumb']
        )
        preview_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=preview_scrollbar_y.set)
        
        preview_scrollbar_x = tk.Scrollbar(
            preview_inner,
            orient=tk.HORIZONTAL,
            command=self.preview_text.xview,
            bg=self.theme_colors['scrollbar_bg'],
            troughcolor=self.theme_colors['scrollbar_bg'],
            activebackground=self.theme_colors['scrollbar_thumb']
        )
        
        status_bar = tk.Frame(self.root, bg=self.theme_colors['statusbar_bg'], height=36)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_bar,
            text="就绪",
            bg=self.theme_colors['statusbar_bg'],
            fg=self.theme_colors['statusbar_fg'],
            font=('Microsoft YaHei UI', 9),
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
        
        self.line_count_label = tk.Label(
            status_bar,
            text="行数: 0",
            bg=self.theme_colors['statusbar_bg'],
            fg=self.theme_colors['statusbar_fg'],
            font=('Microsoft YaHei UI', 9),
            anchor=tk.W,
            width=12
        )
        self.line_count_label.pack(side=tk.LEFT, padx=5)
        
        self.newline_label = tk.Label(
            status_bar,
            text="换行符: 未知",
            bg=self.theme_colors['statusbar_bg'],
            fg=self.theme_colors['statusbar_fg'],
            font=('Microsoft YaHei UI', 9),
            anchor=tk.W,
            width=18
        )
        self.newline_label.pack(side=tk.LEFT, padx=5)
        
        self.update_history_display()
    
    def apply_theme(self, theme_name):
        if theme_name == "light":
            self.theme_colors = ThemeManager.LIGHT
        else:
            self.theme_colors = ThemeManager.DARK
        
        self.root.configure(bg=self.theme_colors['bg'])
        
        for widget in [self.import_btn, self.process_btn, self.open_folder_btn, 
                       self.clear_history_btn, self.theme_light_btn, self.theme_dark_btn, 
                       self.theme_system_btn]:
            widget.set_theme(self.theme_colors)
        
        self.update_theme_buttons()
        
        self.update_history_display()
    
    def update_theme_buttons(self):
        pass
    
    def set_theme(self, theme):
        self.current_theme = theme
        if theme == "system":
            self.actual_theme = ThemeManager.detect_system_theme()
        else:
            self.actual_theme = theme
        self.apply_theme(self.actual_theme)
    
    def toggle_separator_options(self):
        state = 'normal' if self.use_separator.get() else 'disabled'
        
        if self.use_separator.get():
            self.separator_combo.config(state='readonly')
            self.custom_separator_entry.config(state='normal')
        else:
            self.separator_combo.config(state='disabled')
            self.custom_separator_entry.config(state='disabled')
        
        if not self.use_separator.get():
            self.use_specific_param.set(False)
            self.toggle_param_options()
    
    def toggle_param_options(self):
        if self.use_specific_param.get():
            self.use_separator.set(True)
            self.toggle_separator_options()
        
        state = 'normal' if self.use_specific_param.get() else 'disabled'
        self.param_spinbox.config(state=state)
    
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
        self.import_listbox.delete(0, tk.END)
        for filepath in self.history["imported"]:
            self.import_listbox.insert(tk.END, Path(filepath).name)
        
        self.generated_listbox.delete(0, tk.END)
        for filepath in self.history["generated"]:
            self.generated_listbox.insert(tk.END, Path(filepath).name)
    
    def on_import_select(self, event):
        selection = self.import_listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.history["imported"]):
                filepath = self.history["imported"][idx]
                self._preview_file(filepath)
    
    def on_generated_select(self, event):
        selection = self.generated_listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.history["generated"]):
                filepath = self.history["generated"][idx]
                self._preview_file(filepath)
    
    def on_import_double_click(self, event):
        selection = self.import_listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < len(self.history["imported"]):
                filepath = self.history["imported"][idx]
                self.load_file(filepath)
    
    def on_generated_double_click(self, event):
        selection = self.generated_listbox.curselection()
        if selection:
            idx = selection[0]
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
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, newline_char.join(preview_lines))
            if len(lines) > 100:
                self.preview_text.insert(tk.END, f"\n\n... 共 {len(lines)} 行，仅显示前100行 ...")
            
            self.status_label.config(text=f"预览: {Path(filepath).name} ({len(lines)} 行)")
        except Exception as e:
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"预览失败: {str(e)}")
    
    def open_containing_folder(self):
        import_selection = self.import_listbox.curselection()
        generated_selection = self.generated_listbox.curselection()
        
        filepath = None
        
        if import_selection:
            idx = import_selection[0]
            if idx < len(self.history["imported"]):
                filepath = self.history["imported"][idx]
        elif generated_selection:
            idx = generated_selection[0]
            if idx < len(self.history["generated"]):
                filepath = self.history["generated"][idx]
        
        if filepath and os.path.exists(filepath):
            folder_path = os.path.dirname(filepath)
            os.startfile(folder_path)
        else:
            messagebox.showinfo("提示", "请先选择一个历史记录文件")
    
    def clear_history(self):
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？"):
            self.history = {"imported": [], "generated": []}
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("完成", "历史记录已清空")
    
    def open_file(self, filepath):
        if os.path.exists(filepath):
            os.startfile(filepath)
        else:
            messagebox.showerror("错误", f"文件不存在: {filepath}")
    
    def import_file(self):
        filetypes = [
            ("文本文件", "*.txt"),
            ("CSV文件", "*.csv"),
            ("所有文件", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="选择要处理的文件",
            filetypes=filetypes
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
            self.line_count_label.config(text=f"行数: {len(self.file_content)}")
            self.newline_label.config(text=f"换行符: {newline_name}")
            self.status_label.config(text=f"已加载: {Path(filepath).name}")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")
    
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
        if self.separator_var.get() == '其他':
            return self.custom_separator.get()
        elif self.separator_var.get() == '\\t':
            return '\t'
        else:
            return self.separator_var.get()
    
    def get_dedup_key(self, line):
        if not self.use_separator.get():
            return line.strip()
        
        separator = self.get_separator()
        if not separator:
            return line.strip()
        
        parts = line.split(separator)
        
        if not self.use_specific_param.get():
            return tuple(p.strip() for p in parts)
        
        try:
            pos = int(self.param_position.get()) - 1
            if 0 <= pos < len(parts):
                return parts[pos].strip()
            else:
                return line.strip()
        except:
            return line.strip()
    
    def process_deduplication(self):
        if not self.file_content:
            messagebox.showwarning("警告", "请先导入文件")
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
            messagebox.showinfo("提示", "没有发现重复行")
            return
        
        original_path = Path(self.current_file)
        suffix = self.output_suffix.get()
        new_filename = f"{original_path.stem}{suffix}{original_path.suffix}"
        new_filepath = original_path.parent / new_filename
        
        try:
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(self.newline_char.join(unique_lines))
                if unique_lines and not unique_lines[-1].endswith(self.newline_char):
                    f.write(self.newline_char)
            
            self.add_generated_history(str(new_filepath))
            
            msg = f"去重完成！\n\n原始行数: {len(self.file_content)}\n去重后行数: {len(unique_lines)}\n删除重复行: {duplicate_count}\n\n文件已保存至:\n{new_filepath}"
            messagebox.showinfo("完成", msg)
            
            self._preview_file(str(new_filepath))
            self.status_label.config(text=f"已生成: {new_filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")


def main():
    root = tk.Tk()
    
    try:
        root.tk.call('tk', 'scaling', 1.0)
    except:
        pass
    
    app = TextProcessor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
