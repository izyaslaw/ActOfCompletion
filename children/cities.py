import tkinter as tk
from tkinter import ttk


class Cities(tk.Toplevel):
    def __init__(self, root, db):
        super().__init__(root)
        self.init_child()
        self.root = root
        self.db = db
        self.view_records()

    def init_child(self):
        self.title('Города')
        self.geometry("%dx%d+%d+%d" % (650, 260, 400, 300))
        self.resizable(False, False)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'genitive'), height=10, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('genitive', width=300, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Название')
        self.tree.heading('genitive', text='Родительный')

        self.tree.place(x=10, y=10)
        self.tree.pack()

        btn_add = ttk.Button(self, text='Добавить', width=15)
        btn_add.place(x=432, y=230)
        btn_add.bind('<Button-1>', lambda event: AddCities(self.root, self))

        btn_delete = ttk.Button(self, text='Удалить', width=15)
        btn_delete.place(x=542, y=230)
        btn_delete.bind('<Button-1>', lambda event: self.delete_rec())

        self.grab_set()
        self.focus_set()

    def records(self, name, genitive):
        self.db.insert_data(name, genitive)
        self.view_records()

    def delete_rec(self):
        for item in self.tree.selection():
            item_value = self.tree.item(item, "values")
        id = item_value[0]
        self.db.delete_data(id)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM cities''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


class AddCities(tk.Toplevel):
    def __init__(self, root, app):
        super().__init__(root)
        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Добавить город')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Название:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Родительный:')
        label_select.place(x=50, y=80)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_genitive = ttk.Entry(self)
        self.entry_genitive.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                  self.entry_genitive.get()))

        self.grab_set()
        self.focus_set()
