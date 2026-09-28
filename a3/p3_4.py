import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import re
import os
import subprocess
import threading

# Premium Apple-inspired Color Palette
THEMES = {
    "Dark": {
        "bg": "#1E1E1E",               # Main editor background
        "fg": "#FFFFFF",               # Main text
        "toolbar_bg": "#282828",       # Toolbar & Status bar
        "toolbar_fg": "#E5E5EA",       # Toolbar text
        "btn_hover": "#3A3A3C",        # Button hover state
        "selection": "#264F78",        # Selection color
        "cursor": "#0A84FF",           # Apple Blue cursor
        "tab_bg": "#282828",           # Inactive tab
        "tab_selected": "#1E1E1E",     # Active tab
        "tab_fg": "#8E8E93",           # Inactive tab text
        "tab_selected_fg": "#FFFFFF",  # Active tab text
        "terminal_bg": "#151515",      # Terminal background
        "terminal_fg": "#32D74B",      # Terminal text (Green)
        "statusbar_bg": "#282828",     # Status bar
        "statusbar_fg": "#8E8E93",     # Status text
        "keyword": "#FF9F0A",          # Orange
        "builtin": "#0A84FF",          # Blue
        "string": "#32D74B",           # Green
        "comment": "#8E8E93",          # Gray
        "number": "#FFD60A",           # Yellow
        "border": "#38383A",           # Subtle border line
        "run_btn": "#0A84FF",          # Run button color
        "run_btn_fg": "#FFFFFF"
    },
    "Light": {
        "bg": "#FFFFFF",
        "fg": "#1C1C1E",
        "toolbar_bg": "#F5F5F7",
        "toolbar_fg": "#1C1C1E",
        "btn_hover": "#E5E5EA",
        "selection": "#B3D7FF",
        "cursor": "#0A84FF",
        "tab_bg": "#E5E5EA",
        "tab_selected": "#FFFFFF",
        "tab_fg": "#8E8E93",
        "tab_selected_fg": "#000000",
        "terminal_bg": "#F4F4F4",
        "terminal_fg": "#1C1C1E",
        "statusbar_bg": "#F5F5F7",
        "statusbar_fg": "#8E8E93",
        "keyword": "#FF9500",
        "builtin": "#007AFF",
        "string": "#34C759",
        "comment": "#8E8E93",
        "number": "#FFCC00",
        "border": "#D1D1D6",
        "run_btn": "#007AFF",
        "run_btn_fg": "#FFFFFF"
    }
}

class HoverButton(tk.Label):
    def __init__(self, master, text, command, theme_mode, bold=False, is_primary=False, **kwargs):
        self.is_primary = is_primary
        f = ("Helvetica Neue", 13, "bold") if bold else ("Helvetica Neue", 13)
        # Added nice padding to make buttons look premium and clickable
        super().__init__(master, text=text, padx=16, pady=8, font=f, cursor="hand2", **kwargs)
        self.command = command
        self.theme_mode = theme_mode
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.update_theme(theme_mode)

    def update_theme(self, theme_mode):
        self.theme_mode = theme_mode
        t = THEMES[self.theme_mode]
        if self.is_primary:
            self.configure(bg=t["run_btn"], fg=t["run_btn_fg"])
        else:
            self.configure(bg=t["toolbar_bg"], fg=t["toolbar_fg"])

    def on_enter(self, e):
        t = THEMES[self.theme_mode]
        if self.is_primary:
            self.configure(bg=t["selection"]) 
        else:
            self.configure(bg=t["btn_hover"])

    def on_leave(self, e):
        self.update_theme(self.theme_mode)

    def on_click(self, e):
        if self.command:
            self.command()

class HoverMenuButton(tk.Menubutton):
    def __init__(self, master, text, theme_mode, **kwargs):
        super().__init__(master, text=text, padx=16, pady=8, font=("Helvetica Neue", 13), cursor="hand2", relief="flat", bd=0, highlightthickness=0, **kwargs)
        self.theme_mode = theme_mode
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.update_theme(theme_mode)

    def update_theme(self, theme_mode):
        self.theme_mode = theme_mode
        t = THEMES[self.theme_mode]
        self.configure(bg=t["toolbar_bg"], fg=t["toolbar_fg"])

    def on_enter(self, e):
        t = THEMES[self.theme_mode]
        self.configure(bg=t["btn_hover"])

    def on_leave(self, e):
        self.update_theme(self.theme_mode)

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.language = "Plain Text"
        
        self.patterns = {
            "keyword": r'\b(def|class|if|else|elif|for|while|return|import|from|as|pass|break|continue|in|is|and|or|not|try|except|finally|with|void|int|char|double|float|long|struct|sizeof|public|private|protected|interface|extends|implements|new|this|super|namespace|using|template)\b',
            "builtin": r'\b(str|bool|list|dict|set|tuple|print|len|range|open|True|False|None|printf|scanf|malloc|free|cout|cin|System|out|println|String)\b',
            "number": r'\b\d+\b',
            "string": r'".*?"|\'.*?\'',
            "comment": r'#.*$|//.*$'
        }

    def get_bold_font(self):
        base_font = font.Font(font=self.text_widget['font'])
        return font.Font(family=base_font.actual('family'), size=base_font.actual('size'), weight='bold')

    def update_theme(self, theme_mode):
        t = THEMES[theme_mode]
        self.text_widget.tag_configure("keyword", foreground=t["keyword"], font=self.get_bold_font())
        self.text_widget.tag_configure("builtin", foreground=t["builtin"])
        self.text_widget.tag_configure("string", foreground=t["string"])
        self.text_widget.tag_configure("comment", foreground=t["comment"])
        self.text_widget.tag_configure("number", foreground=t["number"])

    def highlight(self, event=None):
        for tag in self.patterns.keys():
            self.text_widget.tag_remove(tag, "1.0", tk.END)
            
        if self.language == "Plain Text":
            return
            
        text_content = self.text_widget.get("1.0", tk.END)
        for tag, pattern in self.patterns.items():
            for match in re.finditer(pattern, text_content, re.MULTILINE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_widget.tag_add(tag, start, end)

class PseudoTerminal:
    def __init__(self, text_widget, get_cwd_callback):
        self.text_widget = text_widget
        self.get_cwd_callback = get_cwd_callback
        
        self.text_widget.bind("<Return>", self.on_return)
        self.text_widget.bind("<BackSpace>", self.on_backspace)
        self.text_widget.bind("<Key>", self.on_key)
        
        for modifier in ['<Control-', '<Command-']:
            self.text_widget.bind(f"{modifier}c>", lambda e: self.text_widget.event_generate("<<Copy>>"))
            self.text_widget.bind(f"{modifier}v>", lambda e: self.text_widget.event_generate("<<Paste>>"))
        
        self.prompt_end_index = "1.0"
        self.is_executing = False
        self.write_prompt()

    def get_dir(self):
        cwd = self.get_cwd_callback()
        if cwd and os.path.exists(cwd):
            return cwd
        return os.getcwd()

    def write_prompt(self):
        prompt = f"{self.get_dir()} $ "
        if self.text_widget.index("end-1c") != "1.0":
            prompt = f"\n{prompt}"
            
        self.text_widget.insert("end", prompt)
        self.text_widget.see("end")
        self.prompt_end_index = self.text_widget.index("end-1c")
        self.text_widget.mark_set("insert", "end")

    def on_backspace(self, event):
        if self.is_executing: return "break"
        if self.text_widget.compare("insert", "<=", self.prompt_end_index):
            return "break"

    def on_key(self, event):
        if self.is_executing: return "break"
        if event.keysym in ("Left", "Up") and self.text_widget.compare("insert", "<=", self.prompt_end_index):
            return "break"
        if event.char and self.text_widget.compare("insert", "<", self.prompt_end_index):
            self.text_widget.mark_set("insert", "end")

    def on_return(self, event):
        if self.is_executing: return "break"
        cmd = self.text_widget.get(self.prompt_end_index, "end-1c").strip()
        self.text_widget.insert("end", "\n")
        
        if not cmd:
            self.write_prompt()
            return "break"
            
        if cmd.startswith("cd "):
            target = cmd[3:].strip()
            try:
                os.chdir(target)
            except Exception as e:
                self.text_widget.insert("end", f"cd: {e}\n")
            self.write_prompt()
            return "break"
            
        self.is_executing = True
        cwd = self.get_dir()
        
        def execute():
            try:
                process = subprocess.Popen(
                    cmd, shell=True, cwd=cwd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                stdout, stderr = process.communicate()
                
                def write_out():
                    if stdout: self.text_widget.insert("end", stdout)
                    if stderr: self.text_widget.insert("end", stderr)
                    self.text_widget.see("end")
                    self.is_executing = False
                    self.write_prompt()
                    
                self.text_widget.after(0, write_out)
            except Exception as e:
                def write_err():
                    self.text_widget.insert("end", f"Error: {e}\n")
                    self.text_widget.see("end")
                    self.is_executing = False
                    self.write_prompt()
                self.text_widget.after(0, write_err)

        threading.Thread(target=execute, daemon=True).start()
        return "break"

class EditorTab(tk.Frame):
    def __init__(self, parent, font_family, font_size, status_callback, initial_theme):
        super().__init__(parent)
        self.filepath = None
        self.status_callback = status_callback
        self.language = "Plain Text"
        
        self.text_font = font.Font(family=font_family, size=font_size)
        
        # PanedWindow with 0 border for flat UI
        self.paned_window = tk.PanedWindow(self, orient=tk.VERTICAL, bd=0, sashwidth=4, bg="#38383A")
        self.paned_window.pack(expand=True, fill='both')
        
        # --- Editor Area ---
        self.editor_frame = tk.Frame(self.paned_window, bd=0)
        
        self.find_bar = tk.Frame(self.editor_frame, height=40)
        self.find_lbl = tk.Label(self.find_bar, text="Find:", font=("Helvetica Neue", 12))
        self.find_lbl.pack(side="left", padx=(15, 5), pady=5)
        self.find_entry = tk.Entry(self.find_bar, width=20, relief="flat", highlightthickness=1, font=("Helvetica Neue", 12))
        self.find_entry.pack(side="left", padx=5, pady=5)
        self.find_entry.bind("<Return>", lambda e: self.find_next())
        self.rep_lbl = tk.Label(self.find_bar, text="Replace:", font=("Helvetica Neue", 12))
        self.rep_lbl.pack(side="left", padx=5, pady=5)
        self.rep_entry = tk.Entry(self.find_bar, width=20, relief="flat", highlightthickness=1, font=("Helvetica Neue", 12))
        self.rep_entry.pack(side="left", padx=5, pady=5)
        self.rep_entry.bind("<Return>", lambda e: self.replace_text())
        HoverButton(self.find_bar, text="Next", command=self.find_next, theme_mode=initial_theme).pack(side="left", padx=5)
        HoverButton(self.find_bar, text="Replace", command=self.replace_text, theme_mode=initial_theme).pack(side="left", padx=5)
        HoverButton(self.find_bar, text="✕", command=self.hide_find_bar, theme_mode=initial_theme).pack(side="right", padx=10)
        self.find_visible = False
        
        # Fluid padding (padx=30, pady=25) for a premium text editing experience
        self.text_area = tk.Text(
            self.editor_frame,
            font=self.text_font, wrap='none', undo=True,
            padx=30, pady=25, relief="flat", bd=0, highlightthickness=0,
            insertwidth=2, spacing1=4, spacing3=4
        )
        self.text_area.pack(expand=True, fill='both', side='left')
        
        self.editor_scrollbar = ttk.Scrollbar(self.editor_frame, command=self.text_area.yview)
        self.editor_scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.editor_scrollbar.set)
        
        for modifier in ['<Control-', '<Command-']:
            self.text_area.bind(f"{modifier}c>", lambda e: self.text_area.event_generate("<<Copy>>"))
            self.text_area.bind(f"{modifier}v>", lambda e: self.text_area.event_generate("<<Paste>>"))
            self.text_area.bind(f"{modifier}x>", lambda e: self.text_area.event_generate("<<Cut>>"))
            self.text_area.bind(f"{modifier}z>", lambda e: self.text_area.event_generate("<<Undo>>"))
        
        self.paned_window.add(self.editor_frame, stretch="always")
        
        # --- Terminal Area ---
        self.terminal_frame = tk.Frame(self.paned_window, bd=0)
        self.term_header = tk.Frame(self.terminal_frame, height=35)
        self.term_header.pack(fill='x', side='top')
        self.term_label = tk.Label(self.term_header, text="  TERMINAL", font=("Helvetica Neue", 11, "bold"))
        self.term_label.pack(side="left", padx=15, pady=8)
        HoverButton(self.term_header, text="✕", command=self.hide_terminal, theme_mode=initial_theme).pack(side="right")
        
        self.terminal_area = tk.Text(
            self.terminal_frame,
            font=font.Font(family=font_family, size=font_size-2),
            wrap='word', relief="flat", bd=0, highlightthickness=0,
            height=12, padx=20, pady=15, insertwidth=2
        )
        self.terminal_area.pack(expand=True, fill='both', side='left')
        
        self.term_scrollbar = ttk.Scrollbar(self.terminal_frame, command=self.terminal_area.yview)
        self.term_scrollbar.pack(side='right', fill='y')
        self.terminal_area.config(yscrollcommand=self.term_scrollbar.set)
        
        self.terminal_visible = False
        self.terminal = PseudoTerminal(self.terminal_area, self.get_working_dir)
        
        self.highlighter = SyntaxHighlighter(self.text_area)
        self.text_area.bind('<KeyRelease>', self.on_key_release)
        self.text_area.bind('<ButtonRelease>', self.status_callback)
        self.update_theme(initial_theme)

    def get_working_dir(self):
        if self.filepath:
            return os.path.dirname(self.filepath)
        return None

    def update_theme(self, theme_mode):
        t = THEMES[theme_mode]
        self.configure(bg=t["bg"])
        self.paned_window.configure(bg=t["border"])
        self.editor_frame.configure(bg=t["bg"])
        
        self.find_bar.configure(bg=t["toolbar_bg"])
        self.find_lbl.configure(bg=t["toolbar_bg"], fg=t["toolbar_fg"])
        self.rep_lbl.configure(bg=t["toolbar_bg"], fg=t["toolbar_fg"])
        self.find_entry.configure(bg=t["bg"], fg=t["fg"], insertbackground=t["cursor"], highlightcolor=t["border"])
        self.rep_entry.configure(bg=t["bg"], fg=t["fg"], insertbackground=t["cursor"], highlightcolor=t["border"])
        
        for btn in self.find_bar.winfo_children():
            if isinstance(btn, HoverButton): btn.update_theme(theme_mode)
            
        self.text_area.configure(bg=t["bg"], fg=t["fg"], insertbackground=t["cursor"], selectbackground=t["selection"])
        
        self.terminal_frame.configure(bg=t["terminal_bg"])
        self.term_header.configure(bg=t["toolbar_bg"])
        self.term_label.configure(bg=t["toolbar_bg"], fg=t["toolbar_fg"])
        for btn in self.term_header.winfo_children():
            if isinstance(btn, HoverButton): btn.update_theme(theme_mode)
            
        self.terminal_area.configure(bg=t["terminal_bg"], fg=t["terminal_fg"], insertbackground=t["cursor"])
        self.highlighter.update_theme(theme_mode)
        self.highlighter.highlight()

    def toggle_find_bar(self):
        if self.find_visible:
            self.hide_find_bar()
        else:
            self.show_find_bar()

    def show_find_bar(self):
        self.find_bar.pack(fill='x', side='top', before=self.text_area)
        self.find_visible = True
        self.find_entry.focus_set()

    def hide_find_bar(self):
        self.find_bar.pack_forget()
        self.find_visible = False
        self.text_area.tag_remove("found", '1.0', tk.END)

    def find_next(self):
        self.text_area.tag_remove("found", '1.0', tk.END)
        s = self.find_entry.get()
        if s:
            idx = self.text_area.search(s, tk.INSERT, nocase=1, stopindex=tk.END)
            if not idx:
                idx = self.text_area.search(s, "1.0", nocase=1, stopindex=tk.INSERT)
                
            if idx:
                lastidx = f"{idx}+{len(s)}c"
                self.text_area.tag_add("found", idx, lastidx)
                self.text_area.tag_config("found", background="#FFFF00", foreground="#000000")
                self.text_area.mark_set(tk.INSERT, lastidx)
                self.text_area.see(tk.INSERT)

    def replace_text(self):
        if self.text_area.tag_ranges("found"):
            idx = self.text_area.index("found.first")
            self.text_area.delete("found.first", "found.last")
            self.text_area.insert(idx, self.rep_entry.get())
            self.find_next()
        else:
            self.find_next()
            if self.text_area.tag_ranges("found"):
                idx = self.text_area.index("found.first")
                self.text_area.delete("found.first", "found.last")
                self.text_area.insert(idx, self.rep_entry.get())
                self.find_next()

    def on_key_release(self, event=None):
        self.status_callback(event)
        self.highlighter.highlight(event)
        
    def get_text(self):
        return self.text_area.get(1.0, "end-1c")
        
    def set_text(self, content):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        self.highlighter.highlight()
        
    def show_terminal(self):
        if not self.terminal_visible:
            self.paned_window.add(self.terminal_frame)
            self.terminal_visible = True
            
    def hide_terminal(self):
        if self.terminal_visible:
            self.paned_window.remove(self.terminal_frame)
            self.terminal_visible = False

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("1280x850")
        self.current_theme = "Dark"
        
        self.style = ttk.Style()
        # Clam theme enables flat borderless notebooks
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
            
        self.font_family = "Menlo" # Apple native monospace
        self.font_size = 15
        
        self.create_menu()
        self.create_toolbar()
        
        # Separator line under toolbar
        self.toolbar_sep = tk.Frame(self.root, height=1)
        self.toolbar_sep.pack(fill='x', side='top')
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # Separator line above status bar
        self.status_sep = tk.Frame(self.root, height=1)
        self.status_sep.pack(fill='x', side='bottom')
        
        self.create_status_bar()
        self.setup_theme_styles()
        self.new_file()

        for mod in ['<Command-', '<Control-']:
            self.root.bind(f'{mod}n>', lambda e: self.new_file())
            self.root.bind(f'{mod}o>', lambda e: self.open_file())
            self.root.bind(f'{mod}s>', lambda e: self.save_file())
            self.root.bind(f'{mod}w>', lambda e: self.close_current_tab())
            self.root.bind(f'{mod}r>', lambda e: self.run_code())
            self.root.bind(f'{mod}f>', lambda e: self.toggle_find())
        
    def toggle_find(self):
        tab = self.get_current_tab()
        if tab: tab.toggle_find_bar()

    def set_language(self, lang):
        tab = self.get_current_tab()
        if tab:
            tab.language = lang
            tab.highlighter.language = lang
            tab.highlighter.highlight()
            self.lang_btn.config(text=f"{lang} ▼")
            self.update_status_bar()

    def on_tab_change(self, event=None):
        tab = self.get_current_tab()
        if tab:
            self.lang_btn.config(text=f"{tab.language} ▼")
            self.update_status_bar()
        
    def setup_theme_styles(self):
        t = THEMES[self.current_theme]
        self.root.configure(bg=t["bg"])
        
        # Style flat premium tabs
        self.style.configure("TNotebook", background=t["toolbar_bg"], borderwidth=0, padding=0)
        self.style.configure("TNotebook.Tab", 
                             padding=[20, 10], font=('Helvetica Neue', 13), 
                             background=t["tab_bg"], foreground=t["tab_fg"], 
                             borderwidth=0, focuscolor=t["tab_selected"])
        
        self.style.map("TNotebook.Tab", 
                       background=[("selected", t["tab_selected"])], 
                       foreground=[("selected", t["tab_selected_fg"])])
                       
        self.toolbar_sep.configure(bg=t["border"])
        self.status_sep.configure(bg=t["border"])
                       
        if hasattr(self, 'toolbar'):
            self.toolbar.configure(bg=t["toolbar_bg"])
            for child in self.toolbar.winfo_children():
                if isinstance(child, HoverButton):
                    child.update_theme(self.current_theme)
                elif isinstance(child, HoverMenuButton):
                    child.update_theme(self.current_theme)
                    
        if hasattr(self, 'status_bar'):
            self.status_bar.configure(bg=t["statusbar_bg"], fg=t["statusbar_fg"])
            
        if hasattr(self, 'notebook'):
            for tab_id in self.notebook.tabs():
                tab = self.root.nametowidget(tab_id)
                tab.update_theme(self.current_theme)

    def switch_theme(self):
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        self.theme_btn.config(text=self.current_theme)
        self.setup_theme_styles()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Tab", command=self.new_file, accelerator="Cmd+N")
        self.file_menu.add_command(label="Open...", command=self.open_file, accelerator="Cmd+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Cmd+S")
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close Tab", command=self.close_current_tab, accelerator="Cmd+W")
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Find / Replace", command=self.toggle_find, accelerator="Cmd+F")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.lang_menu.add_command(label="Plain Text", command=lambda: self.set_language("Plain Text"))
        self.lang_menu.add_command(label="Python", command=lambda: self.set_language("Python"))
        self.lang_menu.add_command(label="C", command=lambda: self.set_language("C"))
        self.lang_menu.add_command(label="C++", command=lambda: self.set_language("C++"))
        self.lang_menu.add_command(label="Java", command=lambda: self.set_language("Java"))
        self.menu_bar.add_cascade(label="Language", menu=self.lang_menu)
        
        self.root.config(menu=self.menu_bar)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, bd=0, padx=15, pady=8)
        self.toolbar.pack(side="top", fill="x")
        
        # Left Group
        HoverButton(self.toolbar, "New", self.new_file, self.current_theme).pack(side="left", padx=2)
        HoverButton(self.toolbar, "Open", self.open_file, self.current_theme).pack(side="left", padx=2)
        HoverButton(self.toolbar, "Save", self.save_file, self.current_theme).pack(side="left", padx=2)
        HoverButton(self.toolbar, "Close Tab", self.close_current_tab, self.current_theme).pack(side="left", padx=2)
        
        # Right Group
        self.theme_btn = HoverButton(self.toolbar, self.current_theme, self.switch_theme, self.current_theme)
        self.theme_btn.pack(side="right", padx=2)
        
        HoverButton(self.toolbar, "Run Code", self.run_code, self.current_theme, bold=True, is_primary=True).pack(side="right", padx=10)
        HoverButton(self.toolbar, "Terminal", self.toggle_terminal_btn, self.current_theme).pack(side="right", padx=2)

        # Premium Language Selector Dropdown
        self.lang_btn = HoverMenuButton(self.toolbar, text="Plain Text ▼", theme_mode=self.current_theme)
        self.lang_menu_tb = tk.Menu(self.lang_btn, tearoff=0)
        self.lang_menu_tb.add_command(label="Plain Text", command=lambda: self.set_language("Plain Text"))
        self.lang_menu_tb.add_command(label="Python", command=lambda: self.set_language("Python"))
        self.lang_menu_tb.add_command(label="C", command=lambda: self.set_language("C"))
        self.lang_menu_tb.add_command(label="C++", command=lambda: self.set_language("C++"))
        self.lang_menu_tb.add_command(label="Java", command=lambda: self.set_language("Java"))
        self.lang_btn.config(menu=self.lang_menu_tb)
        self.lang_btn.pack(side="right", padx=10)

    def toggle_terminal_btn(self):
        tab = self.get_current_tab()
        if tab:
            if tab.terminal_visible:
                tab.hide_terminal()
            else:
                tab.show_terminal()

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ln 1, Col 0")
        
        self.status_bar = tk.Label(
            self.root, textvariable=self.status_var, anchor='e', 
            font=("Helvetica Neue", 12), padx=25, pady=8
        )
        self.status_bar.pack(side='bottom', fill='x')

    def get_current_tab(self):
        try:
            current_tab_id = self.notebook.select()
            if current_tab_id:
                return self.root.nametowidget(current_tab_id)
        except:
            pass
        return None

    def auto_detect_language(self, filepath):
        if filepath.endswith(".py"): return "Python"
        if filepath.endswith(".c"): return "C"
        if filepath.endswith((".cpp", ".cc", ".cxx")): return "C++"
        if filepath.endswith(".java"): return "Java"
        return "Plain Text"

    def new_file(self):
        tab = EditorTab(self.notebook, self.font_family, self.font_size, self.update_status_bar, self.current_theme)
        self.notebook.add(tab, text="Untitled")
        self.notebook.select(tab)
        tab.text_area.focus_set()
        self.set_language("Plain Text")

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                tab = EditorTab(self.notebook, self.font_family, self.font_size, self.update_status_bar, self.current_theme)
                tab.filepath = filepath
                tab.set_text(content)
                self.notebook.add(tab, text=os.path.basename(filepath))
                self.notebook.select(tab)
                
                lang = self.auto_detect_language(filepath)
                self.set_language(lang)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        tab = self.get_current_tab()
        if not tab: return False
        if tab.filepath:
            try:
                with open(tab.filepath, 'w', encoding='utf-8') as f:
                    f.write(tab.get_text())
                self.notebook.tab(tab, text=os.path.basename(tab.filepath))
                lang = self.auto_detect_language(tab.filepath)
                self.set_language(lang)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
                return False
        else:
            return self.save_as_file()

    def save_as_file(self):
        tab = self.get_current_tab()
        if not tab: return False
        filepath = filedialog.asksaveasfilename()
        if filepath:
            tab.filepath = filepath
            self.notebook.tab(tab, text=os.path.basename(filepath))
            return self.save_file()
        return False
            
    def close_current_tab(self):
        tab = self.get_current_tab()
        if tab:
            self.notebook.forget(tab)
            tab.destroy()
            if not self.notebook.tabs():
                self.new_file()

    def update_status_bar(self, event=None):
        tab = self.get_current_tab()
        if tab:
            cursor_pos = tab.text_area.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            self.status_var.set(f"Ln {line}, Col {col}")

    def run_code(self):
        tab = self.get_current_tab()
        if not tab: return
        
        if not tab.filepath:
            messagebox.showinfo("Save Required", "Please save the file before compiling/running.")
            if not self.save_file():
                return
        else:
            self.save_file()
            
        filepath = tab.filepath
        cwd = os.path.dirname(filepath)
        lang = tab.language
        
        tab.show_terminal()
        tab.terminal.is_executing = True
        
        def execute():
            try:
                if lang == 'Python':
                    process = subprocess.Popen(['python3', filepath], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                elif lang == 'C':
                    out_exe = filepath[:-2] if filepath.endswith('.c') else filepath + "_out"
                    compile_proc = subprocess.Popen(['gcc', filepath, '-o', out_exe], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    c_stdout, c_stderr = compile_proc.communicate()
                    if compile_proc.returncode != 0:
                        tab.terminal.text_widget.after(0, lambda: write_res(f"[COMPILATION ERROR]\n{c_stderr}\n"))
                        return
                    process = subprocess.Popen([f"./{os.path.basename(out_exe)}"], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                elif lang == 'C++':
                    out_exe = filepath[:filepath.rfind('.')] if '.' in filepath else filepath + "_out"
                    compile_proc = subprocess.Popen(['g++', filepath, '-o', out_exe], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    cpp_stdout, cpp_stderr = compile_proc.communicate()
                    if compile_proc.returncode != 0:
                        tab.terminal.text_widget.after(0, lambda: write_res(f"[COMPILATION ERROR]\n{cpp_stderr}\n"))
                        return
                    process = subprocess.Popen([f"./{os.path.basename(out_exe)}"], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                elif lang == 'Java':
                    compile_proc = subprocess.Popen(['javac', filepath], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    j_stdout, j_stderr = compile_proc.communicate()
                    if compile_proc.returncode != 0:
                        tab.terminal.text_widget.after(0, lambda: write_res(f"[COMPILATION ERROR]\n{j_stderr}\n"))
                        return
                    class_name = os.path.splitext(os.path.basename(filepath))[0]
                    process = subprocess.Popen(['java', class_name], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                else:
                    tab.terminal.text_widget.after(0, lambda: write_res(f"[ERROR] Cannot run files of Language Type: {lang}.\n"))
                    return
                
                stdout, stderr = process.communicate()
                out_text = ""
                if stdout: out_text += stdout
                if stderr: out_text += stderr
                
                tab.terminal.text_widget.after(0, lambda: write_res(out_text))
            except Exception as e:
                tab.terminal.text_widget.after(0, lambda: write_res(f"[RUNTIME ERROR]\n{str(e)}\n"))

        def write_res(text):
            tab.terminal.text_widget.insert("end", text)
            tab.terminal.is_executing = False
            tab.terminal.write_prompt()
            
        threading.Thread(target=execute, daemon=True).start()

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()
