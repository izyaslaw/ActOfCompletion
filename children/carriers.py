import tkinter as tk
from tkinter import ttk


class Carriers(tk.Toplevel):
    def __init__(self, app, root, db):
        super().__init__(root)
        self.init_child(app)
        self.root = root
        self.db = db
        self.view_records()

    def init_child(self, main_app):
        self.title('Перевозчики')
        self.geometry("%dx%d+%d+%d" % (650, 260, 400, 300))
        self.resizable(False, False)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'genitive', 'number'), height=10, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=230, anchor=tk.CENTER)
        self.tree.column('genitive', width=230, anchor=tk.CENTER)
        self.tree.column('number', width=140, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Ф.И.О.')
        self.tree.heading('genitive', text='Родительный')
        self.tree.heading('number', text='Номер')

        self.tree.place(x=10, y=10)
        self.tree.pack()

        btn_add = ttk.Button(self, text='Добавить', width=15)
        btn_add.place(x=432, y=230)
        btn_add.bind('<Button-1>', lambda event: AddCarriers(self.root, self, main_app))

        btn_delete = ttk.Button(self, text='Удалить', width=15)
        btn_delete.place(x=542, y=230)
        btn_delete.bind('<Button-1>', lambda event: self.delete_rec())

        self.grab_set()
        self.focus_set()

    def records(self, name, genitive, number):
        self.db.insert_data(name, genitive, number)
        self.view_records()

    def delete_rec(self):
        for item in self.tree.selection():
            item_value = self.tree.item(item, "values")
        self.db.delete_data(item_value[0])
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM carriers''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


class AddCarriers(tk.Toplevel):
    def __init__(self, root, app, main_app):
        super().__init__(root)
        self.view = app
        self.init_child(main_app)

    def init_child(self, main_app):
        self.title('Добавить перевозчика')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Ф.И.О.:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Родительный:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Номер:')
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_genitive = ttk.Entry(self)
        self.entry_genitive.place(x=200, y=80)

        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Добавить', command=self.destroy)
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                  self.entry_genitive.get(),
                                                                  self.entry_number.get()))

        self.grab_set()
        self.focus_set()
