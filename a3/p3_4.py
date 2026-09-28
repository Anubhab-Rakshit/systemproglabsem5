import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import re
import os

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        
        # Xcode Light Theme inspired colors for a premium feel
        self.text_widget.tag_configure("keyword", foreground="#9B2393", font=self.get_bold_font())
        self.text_widget.tag_configure("builtin", foreground="#326D74")
        self.text_widget.tag_configure("string", foreground="#C41A16")
        self.text_widget.tag_configure("comment", foreground="#5D6C79")
        self.text_widget.tag_configure("number", foreground="#1C00CF")
        
        # Regex patterns for Python/C-like syntax
        self.patterns = {
            "keyword": r'\b(def|class|if|else|elif|for|while|return|import|from|as|pass|break|continue|in|is|and|or|not|try|except|finally|with|void|int|char|double|float|long|struct|sizeof)\b',
            "builtin": r'\b(str|bool|list|dict|set|tuple|print|len|range|open|True|False|None|printf|scanf|malloc|free)\b',
            "number": r'\b\d+\b',
            "string": r'".*?"|\'.*?\'',
            "comment": r'#.*$|//.*$'
        }
        
    def get_bold_font(self):
        base_font = font.Font(font=self.text_widget['font'])
        return font.Font(family=base_font.actual('family'), size=base_font.actual('size'), weight='bold')

    def highlight(self, event=None):
        for tag in self.patterns.keys():
            self.text_widget.tag_remove(tag, "1.0", tk.END)
            
        text_content = self.text_widget.get("1.0", tk.END)
        
        for tag, pattern in self.patterns.items():
            for match in re.finditer(pattern, text_content, re.MULTILINE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_widget.tag_add(tag, start, end)


class EditorTab(tk.Frame):
    def __init__(self, parent, font_family, font_size, status_callback):
        super().__init__(parent, bg="#ffffff")
        self.filepath = None
        self.status_callback = status_callback
        
        self.text_font = font.Font(family=font_family, size=font_size)
        
        self.text_area = tk.Text(
            self,
            font=self.text_font,
            wrap='none',
            undo=True,
            padx=20,
            pady=20,
            bg="#ffffff",
            fg="#292929",
            insertbackground="#000000",
            selectbackground="#B5D5FF", # macOS selection blue
            relief="flat",
            highlightthickness=0
        )
        self.text_area.pack(expand=True, fill='both', side='left')
        
        self.scrollbar = tk.Scrollbar(self, command=self.text_area.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        self.highlighter = SyntaxHighlighter(self.text_area)
        
        self.text_area.bind('<KeyRelease>', self.on_key_release)
        self.text_area.bind('<ButtonRelease>', self.status_callback)
        
    def on_key_release(self, event=None):
        self.status_callback(event)
        self.highlighter.highlight(event)
        
    def get_text(self):
        return self.text_area.get(1.0, "end-1c")
        
    def set_text(self, content):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        self.highlighter.highlight()


class ModernNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F6F6F6")
        
        # Setup ttk styles for an Apple-like premium look
        self.style = ttk.Style()
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
            
        self.style.configure("TNotebook", background="#ECECEC", borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=[20, 8], font=('Helvetica', 12), background="#ECECEC", foreground="#555555", borderwidth=0)
        self.style.map("TNotebook.Tab", 
                       background=[("selected", "#FFFFFF")], 
                       foreground=[("selected", "#000000")])
                       
        self.style.configure("Flat.TButton", font=('Helvetica', 12), padding=4, background="#F6F6F6", borderwidth=0)
        self.style.map("Flat.TButton", background=[("active", "#EAEAEA"), ("pressed", "#DCDCDC")])
        self.style.configure("Toolbar.TFrame", background="#F6F6F6")

        # Menlo is the standard premium monospace font on macOS
        self.font_family = "Menlo"
        self.font_size = 14
        
        self.create_menu()
        self.create_toolbar()
        
        # Subtle separator line
        separator = tk.Frame(self.root, bg="#D1D1D1", height=1)
        separator.pack(fill="x")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=0, pady=0)
        self.notebook.bind("<<NotebookTabChanged>>", self.update_status_bar)
        
        self.create_status_bar()
        
        self.new_file()

        # Keyboard shortcuts
        self.root.bind('<Command-n>', lambda e: self.new_file())
        self.root.bind('<Command-o>', lambda e: self.open_file())
        self.root.bind('<Command-s>', lambda e: self.save_file())
        self.root.bind('<Command-w>', lambda e: self.close_current_tab())
        
    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Tab", command=self.new_file, accelerator="Cmd+N")
        self.file_menu.add_command(label="Open...", command=self.open_file, accelerator="Cmd+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Cmd+S")
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close Tab", command=self.close_current_tab, accelerator="Cmd+W")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo, accelerator="Cmd+Z")
        self.edit_menu.add_command(label="Redo", command=self.redo, accelerator="Cmd+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Cmd+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Cmd+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Cmd+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Cmd+A")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.format_menu.add_command(label="Increase Font", command=self.increase_font)
        self.format_menu.add_command(label="Decrease Font", command=self.decrease_font)
        self.menu_bar.add_cascade(label="View", menu=self.format_menu)
        
        self.root.config(menu=self.menu_bar)

    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.root, style="Toolbar.TFrame")
        self.toolbar.pack(side="top", fill="x", ipadx=5, ipady=3)
        
        # Professional flat text buttons (removed emojis)
        btn_new = ttk.Button(self.toolbar, text="New Tab", style="Flat.TButton", command=self.new_file)
        btn_new.pack(side="left", padx=5)
        
        btn_open = ttk.Button(self.toolbar, text="Open File", style="Flat.TButton", command=self.open_file)
        btn_open.pack(side="left", padx=5)
        
        btn_save = ttk.Button(self.toolbar, text="Save", style="Flat.TButton", command=self.save_file)
        btn_save.pack(side="left", padx=5)
        
        btn_save_as = ttk.Button(self.toolbar, text="Save As...", style="Flat.TButton", command=self.save_as_file)
        btn_save_as.pack(side="left", padx=5)
        
        btn_close = ttk.Button(self.toolbar, text="Close Tab", style="Flat.TButton", command=self.close_current_tab)
        btn_close.pack(side="right", padx=10)

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ln 1, Col 0")
        
        self.status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var,
            anchor='e', 
            bg="#F6F6F6", 
            fg="#737373",
            font=("Helvetica", 11),
            padx=15,
            pady=5
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

    def new_file(self):
        tab = EditorTab(self.notebook, self.font_family, self.font_size, self.update_status_bar)
        self.notebook.add(tab, text="Untitled")
        self.notebook.select(tab)
        tab.text_area.focus_set()
        self.update_status_bar()

    def open_file(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C Files", "*.c")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                tab = EditorTab(self.notebook, self.font_family, self.font_size, self.update_status_bar)
                tab.filepath = filepath
                tab.set_text(content)
                filename = os.path.basename(filepath)
                self.notebook.add(tab, text=filename)
                self.notebook.select(tab)
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        tab = self.get_current_tab()
        if not tab: return
        
        if tab.filepath:
            try:
                content = tab.get_text()
                with open(tab.filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                filename = os.path.basename(tab.filepath)
                self.notebook.tab(tab, text=filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        tab = self.get_current_tab()
        if not tab: return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C Files", "*.c")]
        )
        if filepath:
            tab.filepath = filepath
            filename = os.path.basename(filepath)
            self.notebook.tab(tab, text=filename)
            self.save_file()
            
    def close_current_tab(self):
        tab = self.get_current_tab()
        if tab:
            self.notebook.forget(tab)
            tab.destroy()
            if not self.notebook.tabs():
                self.new_file()

    def undo(self):
        tab = self.get_current_tab()
        if tab:
            try: tab.text_area.edit_undo()
            except: pass

    def redo(self):
        tab = self.get_current_tab()
        if tab:
            try: tab.text_area.edit_redo()
            except: pass

    def cut(self):
        tab = self.get_current_tab()
        if tab: tab.text_area.event_generate("<<Cut>>")

    def copy(self):
        tab = self.get_current_tab()
        if tab: tab.text_area.event_generate("<<Copy>>")

    def paste(self):
        tab = self.get_current_tab()
        if tab: tab.text_area.event_generate("<<Paste>>")
        
    def select_all(self):
        tab = self.get_current_tab()
        if tab:
            tab.text_area.tag_add('sel', '1.0', 'end')
        return 'break'

    def increase_font(self):
        self.font_size += 2
        for tab_id in self.notebook.tabs():
            tab = self.root.nametowidget(tab_id)
            tab.text_font.configure(size=self.font_size)

    def decrease_font(self):
        if self.font_size > 8:
            self.font_size -= 2
            for tab_id in self.notebook.tabs():
                tab = self.root.nametowidget(tab_id)
                tab.text_font.configure(size=self.font_size)

    def update_status_bar(self, event=None):
        tab = self.get_current_tab()
        if tab:
            cursor_pos = tab.text_area.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            self.status_var.set(f"Ln {line}, Col {col}")

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernNotepad(root)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()
