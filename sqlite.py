__version__ = "1.0.0"

"""
SQLite GUI App
© 2025 KCoder Programming

Licensed under Creative Commons BY-NC 4.0
You may use, modify, and share this app, but not for commercial purposes.
More info: https://creativecommons.org/licenses/by-nc/4.0/
"""

import traceback
from os import startfile, path, getenv, makedirs
import sys
from tkinter.messagebox import askyesnocancel, showinfo

try:
    import sqlite3
    from tabulate import tabulate
    from tkinter import Scrollbar, filedialog, Button, Toplevel
    from ttkbootstrap import Window, Label, Entry, StringVar, Menu, Frame, BooleanVar, Text

    if getattr(sys, 'frozen', False):
        import pyi_splash

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = path.dirname(path.abspath(__file__))
        return path.join(base_path, relative_path)

    '''def run_cmd_file(cmd_name):
        cmd_path = resource_path(path.join("files", cmd_name))
        system(f'start cmd /k "{cmd_path}"')

    if __name__ == '__main__' and len(sys.argv) > 1:
        if sys.argv[1] in ['--version', '-v']:
            run_cmd_file("version.cmd")
            sys.exit()
        elif sys.argv[1] in ['--help', '-h']:
            run_cmd_file("help.cmd")
            sys.exit()'''

    IS_PORTABLE = '--portable' in sys.argv

    class Notepad(Toplevel):
        def __init__(self, master, *args, **kwargs):
            super().__init__(master=master, *args, **kwargs)
            self.geometry(f"{root.winfo_width()-20}x{root.winfo_height()-20}+{root.winfo_x()+10}+{root.winfo_y()+10}")
            self.title("Untitled")
            self.wm_protocol("WM_DELETE_WINDOW", self.on_close)
            self.bind("<Control-s>", lambda event: self.save_file())
            self.bind("<Control-S>", lambda event: self.save_file())
            self.bind("<Control-n>", lambda event: new_file())
            self.bind("<Control-N>", lambda event: new_file())
            self.bind("<Control-O>", lambda event: open_file())
            self.bind("<Control-o>", lambda event: open_file())

            self.m3 = Menu(self, tearoff=0)
            self.m3.add_command(label="Run", command=self.run)
            self.m3.add_separator()
            self.m3.add_command(label="Cut", command=lambda: cut(self.text))
            self.m3.add_command(label="Copy", command=lambda: copy(self.text))
            self.m3.add_command(label="Paste", command=lambda: paste(self.text))

            self.text = Text(self, wrap="word", font=("Consolas", 13))
            self.text.pack(side="top", fill="both", expand=True)
            self.text.bind("<MouseWheel>", lambda event: zoom(event, self.text))
            self.text.bind("<Control-+>", lambda event: inc(self.text))
            self.text.bind("<Control-minus>", lambda event: dec(self.text))
            self.text.bind("<Control-=>", lambda event: self.text.config(font=('Consolas', 13)))
            self.text.bind("<Control-BackSpace>", lambda event: on_backspace(self.text))
            self.bind("<F5>", lambda event: self.run())
            self.text.bind("<Button-3>", lambda event: do_popup(event, self.m3))

            self.menu = Menu(self)
            self.config(menu=self.menu)

            file_menu = Menu(self.menu)
            self.menu.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="New", command=new_file)
            file_menu.add_command(label="Open", command=open_file)
            file_menu.add_separator()
            file_menu.add_command(label="Save", command=self.save_file)
            file_menu.add_command(label="Save As", command=self.save_as)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.destroy)

            edit_menu = Menu(self.menu)
            self.menu.add_cascade(label="Edit", menu=edit_menu)
            edit_menu.add_command(label="Cut", command=lambda: cut(self.text))
            edit_menu.add_command(label="Copy", command=lambda: copy(self.text))
            edit_menu.add_command(label="Paste", command=lambda: paste(self.text))

            self.menu.add_command(label="Run", command=self.run)

        def save_as(self):
            file = filedialog.asksaveasfilename(parent=self, title="Save as", defaultextension=".nbdb", filetypes=[("SQL notebook", "*.nbdb")])
            if file:
                contents = self.text.get("1.0", "end")
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(contents)
                self.wm_title(str(file))
                self.text.focus_set()
                return True
            else: 
                self.text.focus_set()
                return False

        def save_file(self):
            file = self.wm_title()
            if file[-5:] == ".nbdb":
                contents = self.text.get("1.0", "end")
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(contents)
                return True
            else:
                return self.save_as()

        def run(self):
            content = self.text.get('1.0', 'end')
            content2 = commd.get('1.0', 'end')
            commd.delete('1.0', 'end')
            commd.insert('end', content)
            command()
            commd.delete('1.0', 'end')
            commd.insert('end', content2)
            if commd.get('end-1c', 'end') == '\n':
                commd.delete('end-1c', 'end')
            root.focus_set()

        def on_close(self):
            if self.wm_title()[-5:] == '.nbdb':
                contents = self.text.get('1.0', 'end')
                with open(self.wm_title(), 'r', encoding='utf-8') as f:
                    content = f.read()
                if content == contents:
                    self.destroy()
                    commd.focus_set()
                    return
            elif not self.text.get('1.0', 'end').strip():
                self.destroy()
                commd.focus_set()
                return
            result = askyesnocancel("Save", "Do you want to save the changes?", master = self)
            if result == True:
                if self.save_file():
                    self.destroy()
                    commd.focus_set()
            elif result == False:
                self.destroy()
                commd.focus_set()
            else:
                self.text.focus_set()

    def cut(commd):
        commd.event_generate("<<Cut>>")

    def copy(commd):
        commd.event_generate("<<Copy>>")

    def paste(commd):
        commd.event_generate("<<Paste>>")

    def on_backspace(text):
        content = text.get('1.0', 'end-1c').rstrip()
        idx = content.rfind(' ')
        text.delete('1.0' if idx == -1 else f'1.0+{idx+1}c', 'end')
        return 'break'

    def clear_box():
        box.config(state='normal')
        box.delete('1.0','end')
        box.config(state='disabled')

    def inc(widget):
        family,size = widget.cget('font').split()
        if int(size)<100:
            widget.config(font=(family,int(size)+3))
    def dec(widget):
        family,size = widget.cget('font').split()
        if int(size)>1:
            widget.config(font=(family,int(size)-3))
    def zoom(event,widget):
        if event.state & 0x4: 
            if event.delta > 0: 
                inc(widget)
            else: 
                dec(widget)

    def show_about():
        showinfo("About", "SQLite GUI App\n© 2025 KCoder Programming\nLicensed under CC BY-NC 4.0\nhttps://creativecommons.org/licenses/by-nc/4.0/")

    def show_license():
        showinfo("License", """Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

Copyright © 2025 KCoder Programming

You are free to:
✔ Share — copy and redistribute the material in any medium or format
✔ Adapt — remix, transform, and build upon the material

Under the following terms:
❗ Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
❗ NonCommercial — You may not use the material for commercial purposes.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

License Link: https://creativecommons.org/licenses/by-nc/4.0/
    """)

    def new_database():
        directory = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".db", filetypes=[("database file", "*.db"), 
    ("SQLite file", "*.sqlite"), ("database3 file", "*.db3"), ("SQLite3 file", "*.sqlite3")])
        if directory:
            database.delete('0','end')
            database.insert('end', directory)

    def select_database():
        name = filedialog.askopenfilename(filetypes= [("database file", "*.db"), ("SQLite file", "*.sqlite"), 
    ("SQLite file", "*.sqlite3"), ("database file", "*.db3")])
        if name:
            database.delete('0','end')
            database.insert('end', name)

    def new_file():
        notepad = Notepad(master = root)
        notepad.text.focus_set()
        notepad.mainloop()

    def open_file():
        file = filedialog.askopenfilename(parent=root, title="Open a file", defaultextension=".nbdb", filetypes=[("SQL notebook", "*.nbdb")])
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            notepad = Notepad(master=root)
            notepad.text.focus_set()
            notepad.text.insert("1.0", content)
            if notepad.text.get('end-1c', 'end') == '\n':
                notepad.text.delete('end-1c', 'end')
            notepad.title(file)

    def command():
        def format_row(row):
            return ["<BLOB>" if isinstance(col, (bytes, bytearray)) else col for col in row]
        
        query = commd.get('1.0', 'end').strip()
        database_name = database.get().strip()
        box.config(state='normal')
        query_list = [i.replace('\n', '') for i in query.split(';') if i.strip()]
        if not query_list:
            box.insert('end', '>>>\n')
            return
        elif 'exit' in query_list or 'exit()' in query_list:
            sys.exit()
        
        with sqlite3.connect(database_name, autocommit=True) as conn:
            cursor = conn.cursor()
            return_string = ""
            for query in query_list:
                try:
                    cursor.execute(query)
                    data1 = [format_row(row) for row in cursor.fetchall()]
                    header1 = [desc[0] for desc in cursor.description if desc[0]]
                    if data1:
                        if header1 and len(header1) == len(data1[0]):
                            return_string = return_string + f">>> {query}\n{tabulate(data1, header1, tablefmt=table_format1.get())}\n\n"
                        else:
                            return_string = return_string + f">>> {query}\n{tabulate(data1, tablefmt=table_format1.get())}\n\n"
                    else:
                        return_string = return_string + f">>> {query}\nEmpty Data[]\nQuery Executed Successfully\n\n"
                    
                except Exception as e:
                    return_string = return_string + f">>> {query}\n{e}\n\n"
            
        box.insert('end', return_string)
        box.config(state='disabled')

    def do_popup(event, menu):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def save_info(info, value, key, folder):
        if info[key] != value:
            info[key] = value
            with open(path.join(folder, "info.config"), "w") as f:
                for k, v in info.items():
                    f.write(f"{k}={v}\n")

    def reset1(folder):
        save_info(info, "simple_outline", 'tablefmt', folder)
        save_info(info, 'pulse', 'themename', folder)
        root.style.theme_use("pulse")
        table_format1.set('simple_outline')
        theme1.set('pulse')

    if IS_PORTABLE:
        folder = path.dirname(sys.executable)  # or use "" for current dir
    else:
        base = getenv('LOCALAPPDATA')
        folder = path.join(base, 'KCoder SQLite App')
    makedirs(folder, exist_ok=True)

    try:
        with open(path.join(folder, "info.config")) as f:
            info = dict(line.strip().split('=') for line in f if line.strip())
    except FileNotFoundError:
        with open(path.join(folder, "info.config"), "w") as f:
            info = {"themename":"pulse", "tablefmt":"simple_outline", "maximised":'0', 'height':'600', 'width':'950'}
            f.write("themename=pulse\ntablefmt=simple_outline\nmaximised=0\nheight=600\nwidth=950")

    root  = Window(title="SQLite",themename=info['themename'])
    if IS_PORTABLE:
        root.wm_title("SQLite [Portable Mode]")
    root.iconbitmap(resource_path(r'files\icon1.ico'))
    root.iconbitmap(default=resource_path(r'files\icon1.ico'))
    if info.get('maximised', '0') == '1':
        root.wm_state("zoomed")
    else:
        height = info.get('height', '600')
        width = info.get('width', '950')
        x = root.winfo_screenwidth()//2 - int(width)//2
        y = root.winfo_screenheight()//2 - int(height)//2
        root.geometry(f"{width}x{height}+{x}+{y}")

    m = Menu(root, tearoff=0)
    m.add_command(label="Run", command=command)
    m.add_separator()
    m.add_command(label="Cut", command=lambda: cut(commd))
    m.add_command(label="Copy", command=lambda: copy(commd))
    m.add_command(label="Paste", command=lambda: paste(commd))

    m1 = Menu(root, tearoff=0)
    m1.add_command(label="Copy", command=lambda: copy(box))

    menubar = Menu(root)
    root.config(menu=menubar)
    file = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="File",menu=file)
    file.add_command(label="New Database", command=new_database)
    file.add_command(label="Open Database", command=select_database)
    file.add_separator()
    file.add_command(label='New File', command=new_file)
    file.add_command(label='Open File', command=open_file)
    file.add_separator()
    file.add_command(label="exit",command=root.destroy)
    edit = Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Edit',menu=edit)
    edit.add_command(label="Clear Output",command= clear_box)
    yes = BooleanVar(value=False)
    edit.add_checkbutton(label="Clear Input",variable=yes,onvalue=True,offvalue=False,command=lambda: commd.delete('1.0','end'))
    edit.add_separator()
    edit.add_command(label="Inc output size",command= lambda :inc(box))
    edit.add_command(label="Dec output size",command= lambda :dec(box))
    edit.add_command(label="Reset output size",command=lambda:box.config(font=('Consolas',13)))
    edit.add_separator()
    edit.add_command(label="Inc editor size",command= lambda :inc(commd))
    edit.add_command(label="Dec editor size",command= lambda :dec(commd))
    edit.add_command(label="Reset editor size",command=lambda:commd.config(font=('Consolas',13)))
    style = Menu(menubar, tearoff=0)
    theme = Menu(menubar,tearoff=0)
    theme1 = StringVar(root, info['themename'])
    themes = ['flatly', 'litera', 'minty', 'pulse' , 'united', 'cerculean', 'morph', 'superhero', 'solar', 'vapor', 'darkly', 'cyborg']
    for value in themes:
        theme.add_radiobutton(label = value, variable = theme1, value = value,command = lambda: (root.style.theme_use(theme1.get()), save_info(info, theme1.get(), 'themename', folder)))
    table_format = Menu(menubar, tearoff=0)
    tabulate_formats = ['double_grid', 'double_outline', 'fancy_grid', 'fancy_outline', 'github', 'html', 'latex', 'mediawiki', 'moinmoin', 'orgtbl', 'grid', 'outline', 'pipe', 'plain', 'presto', 'pretty', 'psql', 'rst', 'simple', 'simple_grid', 'simple_outline', 'textile']
    table_format1 = StringVar(root, info['tablefmt'])
    for value in tabulate_formats:
        table_format.add_radiobutton(label=value, variable=table_format1, value=value, command=lambda: save_info(info, table_format1.get(), 'tablefmt', folder))
    style.add_cascade(label="Format", menu=table_format)
    style.add_cascade(label="Themes", menu=theme)
    style.add_command(label="Reset", command=lambda: reset1(folder))
    menubar.add_cascade(label="Style",menu=style)
    help = Menu(menubar,tearoff=0)
    menubar.add_cascade(label='help',menu=help)
    help.add_command(label="Help", command= lambda: startfile(resource_path(r"files\help2.html")))
    help.add_command(label="SQLite", command= lambda: startfile(resource_path(r"files\help1.html")))
    help.add_command(label="About", command=show_about)
    help.add_command(label="License", command=show_license)
    menubar.add_command(label="Run (F5)", command=command)

    frame1 = Frame(root)
    frame1.grid(row= 1,column= 1,sticky= 'nsew',columnspan= 2)
    Label(frame1, text="SQLite", font= ('Halveta', 15, 'bold')).grid(column= 1,row= 1,pady= 2,sticky= 'nsew', columnspan=2)
    Label(frame1,text="\t\tDatabase: ", font=('Consolas',11,'bold')).grid(column=3,row=1,pady=2,sticky='nsew')
    database = Entry(frame1,font=('Consolas',11))
    database.grid(row=1, column=4, sticky='nsew', pady=2, padx=4)
    database.insert("end", "unknown.db")
    Button(frame1, text='Run', font=("Consolas", 13), command=command).grid(row=2, column=4, sticky='nse', padx=4, pady=2)
    frame1.columnconfigure(4, weight=1)
    commd = Text(root, font=("Consolas",13), height=5)
    commd.grid(row=2,column=0,pady=5,sticky='nsew',padx=5, columnspan=2)
    commd.bind("<F5>",func= lambda event: command())
    commd.bind("<Control-BackSpace>", lambda event: on_backspace(commd))
    commd.bind
    y_scroll1 = Scrollbar(root, orient='vertical', command=commd.yview)
    y_scroll1.grid(row=2,column=3,sticky='ns', pady=5)
    commd['yscrollcommand'] = y_scroll1.set
    box = Text(root,font = ("Consolas",13), wrap = 'none')
    box.grid(row=3,column=0,columnspan=2,sticky='nsew', ipadx=2, ipady=2)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(1, weight=1)
    box.config(state='disabled')
    h_scroll = Scrollbar(root, orient='horizontal', command=box.xview)
    h_scroll.grid(row=4, column=0, columnspan=2, sticky='ew')
    y_scroll = Scrollbar(root, orient='vertical', command=box.yview)
    y_scroll.grid(row=3,column=3,sticky='ns')
    box['yscrollcommand'] = y_scroll.set
    box['xscrollcommand'] = h_scroll.set
    box.bind("<Left>", lambda event: box.xview_scroll(-3, "units"))
    box.bind("<Right>", lambda event: box.xview_scroll(3, "units"))

    box.bind("<MouseWheel>", lambda event:zoom(event,box), add="+")
    box.bind("<Button-3>", lambda event: do_popup(event, m1))
    root.bind("<Control-n>", lambda event: new_database())
    root.bind("<Control-o>", lambda event: select_database())
    box.bind("<Control-+>", lambda event: inc(box))
    box.bind("<Control-minus>", lambda event: dec(box))
    box.bind("<Control-=>", lambda event: box.config(font=('Consolas', 13)))
    commd.bind("<MouseWheel>", lambda event:zoom(event,commd), add="+")
    commd.bind("<Button-3>", lambda event: do_popup(event, m))
    commd.bind("<Control-+>", lambda event: inc(commd))
    commd.bind("<Control-minus>", lambda event: dec(commd))
    commd.bind("<Control-=>", lambda event: commd.config(font=('Consolas', 13)))
    def on_close():
        if root.wm_state() == 'zoomed':
            val = '1'
        else:
            val = '0'
            save_info(info, root.winfo_height(), 'height', folder)
            save_info(info, root.winfo_width(), 'width', folder)
        save_info(info, val, 'maximised', folder)
        sys.exit()
    root.protocol("WM_DELETE_WINDOW", on_close)
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    root.mainloop()

except Exception as e:
    error_path = path.join(path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "error.log")
    with open(error_path, "w", encoding="utf-8") as f:
        f.write("Unexpected error occurred:\n\n")
        f.write(traceback.format_exc())
    
    try:
        showinfo("Application Crashed", f"An unexpected error occurred.\nA log file has been saved:\n{error_path}")
        startfile(error_path)
    except:
        pass
    sys.exit(1)