import tkinter as tk
from tkinter import ttk


class Saves(tk.Toplevel):
    def __init__(self, app, root, db):
        super().__init__(root)
        self.init_child(app)
        self.root = root
        self.db = db
        self.view_records()

    def init_child(self, main_app):
        self.title('Акты')
        self.geometry("%dx%d+%d+%d" % (650, 260, 400, 300))
        self.resizable(False, False)

        self.tree = ttk.Treeview(self, columns=('number', 'date', 'carrier', 'price'), height=10, show='headings')

        self.tree.column('number', width=30, anchor=tk.CENTER)
        self.tree.column('date', width=230, anchor=tk.CENTER)
        self.tree.column('carrier', width=230, anchor=tk.CENTER)
        self.tree.column('price', width=140, anchor=tk.CENTER)

        self.tree.heading('number', text='№')
        self.tree.heading('date', text='Дата')
        self.tree.heading('carrier', text='Водитель')
        self.tree.heading('price', text='Цена услуги')

        self.tree.place(x=10, y=10)
        self.tree.pack()

        # btn_add = ttk.Button(self, text='Загрузить', width=15)
        # btn_add.place(x=432, y=230)
        # btn_add.bind('<Button-1>', lambda event: self.load_act())

        btn_delete = ttk.Button(self, text='Удалить', width=15)
        btn_delete.place(x=542, y=230)
        btn_delete.bind('<Button-1>', lambda event: self.delete_rec())

        self.grab_set()
        self.focus_set()

    def delete_rec(self):
        for item in self.tree.selection():
            item_value = self.tree.item(item, "values")
        self.db.delete_data(item_value[0])
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT number, date, carrier, price FROM saves''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def load_act(self, ):
        for item in self.tree.selection():
            item_value = self.tree.item(item, "values")
        self.db.c.execute('''SELECT * FROM saves WHERE number == ?''', (item_value[0],))
        pass
