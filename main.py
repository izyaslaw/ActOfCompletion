from tkinter.messagebox import *
from tkinter.filedialog import *
from children.carriers import Carriers
from children.cities import Cities
from children.saves import Saves
from children.preview import Preview
from dbs.dbs import *
from textbuild import createAct
import tkinter as tk
import datetime as dt
from tkinter import ttk


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.db_carriers = DBCarriers()
        self.db_cities = DBCities()
        self.db_saves = DBSaves()
        self.init_main(root)

    def init_main(self, root):
        self.init_menu(root)
        self.init_body(root)

    def init_menu(self, root):
        def change_directory():
            dir_file = open('dir.txt', 'w')
            dir_file.write(askdirectory())
            dir_file.close()

        def saves():
            Saves(self, root, self.db_saves)

        def carriers():
            Carriers(self, root, self.db_carriers)

        def cities():
            Cities(root, self.db_cities)

        def close_win():
            """Close window and exit program"""
            if askyesno("Exit", "Do you want to quit?"):
                root.destroy()

        fm = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=fm)
        fm.add_command(label="Директория хранения актов", command=change_directory)
        fm.add_command(label="Акты", command=saves)
        fm.add_command(label="Выход", command=close_win)

        dm = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Данные", menu=dm)
        dm.add_command(label="Перевозчики", command=carriers)
        dm.add_command(label="Города", command=cities)

    def init_body(self, root):
        self.label_act = tk.Label(root, text='Акт №:')
        self.label_date = tk.Label(root, text='Дата:')
        self.label_carrier = tk.Label(root, text='Перевозчик:')
        self.label_from = tk.Label(root, text='Из:')
        self.label_to = tk.Label(root, text='В:')
        self.dates_of_trips = tk.Label(root, text='Дата доставки:')
        self.label_amount = tk.Label(root, text='Количество:')
        self.label_price = tk.Label(root, text='Цена услуги:')

        self.entry_act_number = ttk.Entry(root)
        self.db_saves.c.execute('''SELECT MAX(number) FROM saves''')
        self.last_act = self.db_saves.c.fetchall()
        if self.last_act[0] != (None,):
            last_act_number = int(self.last_act[0][0])
            self.entry_act_number.insert(END, last_act_number + 1)
        else:
            self.entry_act_number.insert(END, '1')

        self.entry_date = ttk.Entry(root)
        self.entry_date.insert(END, getCurrentDate())

        self.db_carriers.c.execute('''SELECT * FROM carriers''')
        self.carriers = self.db_carriers.c.fetchall()
        self.carriers_options = [carrier[1] for carrier in self.carriers]
        self.pick_carrier = ttk.Combobox(root, value=self.carriers_options)
        # self.pick_carrier.current(0)

        self.db_cities.c.execute('''SELECT * FROM cities''')
        self.cities = self.db_cities.c.fetchall()
        self.cities_options = [city[1] for city in self.cities]
        self.pick_cities_from = [ttk.Combobox(root, value=self.cities_options)]
        # self.pick_cities_from.current(0)
        self.btn_add_cities_from = ttk.Button(root, text='+', width=3)
        self.btn_add_cities_from.bind('<Button-1>', lambda event: self.addCityFrom(root))

        self.pick_cities_to = [ttk.Combobox(root, value=self.cities_options)]
        self.btn_add_cities_to = ttk.Button(root, text='+', width=3)
        self.btn_add_cities_to.bind('<Button-1>', lambda event: self.addCityTo(root))

        self.entry_dates_of_trips = [ttk.Entry(root)]
        self.entry_dates_of_trips[0].insert(END, getCurrentDate())
        self.entry_amount = ttk.Entry(root)
        self.entry_price = ttk.Entry(root)
        self.entry_price.insert(END, '0')

        self.btn_add_date = ttk.Button(root, text='+', width=3)
        self.btn_add_date.bind('<Button-1>', lambda event: self.addDate(root))

        self.btn_create_act = ttk.Button(root, text='Создать акт', width=20)
        self.btn_create_act.bind('<Button-1>', lambda event: self.createActAndReload(root))

        self.btn_reboot = ttk.Button(root, text='🔃', width=3)
        self.btn_reboot.bind('<Button-1>', lambda event: self.reboot(root))

        self.btn_preview = ttk.Button(root, text='Предпросмотр', width=20)
        self.btn_preview.bind('<Button-1>', lambda event: self.previewClick(root))

        self.packing()

    def previewClick(self, root):
        if self.checkForm():
            Preview(self, root)
        else:
            return

    def checkForm(self):
        empty_field = self.checkEmptyFields()
        print('1')
        if empty_field != '':
            showinfo(title='Ошибка', message=empty_field)
            return False
        return True

    def checkEmptyFields(self):
        try:
            int(self.entry_act_number.get())
        except BaseException:
            return 'Номер акта должен быть числом'
        if self.entry_act_number.get() == '': return 'Введите номер акта'
        if self.entry_date.get() == '': return 'Введите дату'
        if self.pick_carrier.get() == '': return 'Выберите перевозчика'
        for city in self.pick_cities_from:
            if city.get() == '': return 'Выберите город-из'
        for city in self.pick_cities_to:
            if city.get() == '': return 'Выберите город-в'
        if self.pick_cities_to == '': return 'Выберите город-в'

        return ''

    def createActAndReload(self, root):
        if self.checkForm():
            createAct(self)
            self.reboot(root)
        else:
            return

    def reboot(self, root):
        root.destroy()
        creatingMainApp()

    def packing(self):
        padding_y = 2.5
        padding_x = 25
        self.label_act.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky='nw')
        self.label_date.grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky='w')
        self.label_carrier.grid(row=2, column=0, padx=padding_x, pady=padding_y, sticky='nw')
        self.label_from.grid(row=3, column=0, padx=padding_x, pady=padding_y, sticky='w')
        self.label_to.grid(row=4, column=0, padx=padding_x, pady=padding_y, sticky='nw')
        self.dates_of_trips.grid(row=5, column=0, padx=padding_x, pady=padding_y, sticky='nw')
        self.label_amount.grid(row=6, column=0, padx=padding_x, pady=padding_y, sticky='w')
        self.label_price.grid(row=7, column=0, padx=padding_x, pady=padding_y, sticky='w')
        self.entry_act_number.grid(row=0, column=1)
        self.entry_date.grid(row=1, column=1)
        self.pick_carrier.grid(row=2, column=1)
        self.pick_cities_from[0].grid(row=3, column=1)
        self.btn_add_cities_from.grid(row=3, column=2, padx=padding_x)
        self.pick_cities_to[0].grid(row=4, column=1)
        self.btn_add_cities_to.grid(row=4, column=2, padx=padding_x)
        self.entry_dates_of_trips[0].grid(row=5, column=1)
        self.entry_amount.grid(row=6, column=1)
        self.entry_price.grid(row=7, column=1)
        self.btn_create_act.grid(row=8, column=1, pady=padding_y * 4)
        self.btn_add_date.grid(row=5, column=2, padx=padding_x)
        self.btn_reboot.grid(row=0, column=2)
        self.btn_preview.grid(row=8, column=0)

    def addDate(self, root):
        self.entry_dates_of_trips.append(ttk.Entry(root))
        len_dates_array = len(self.entry_dates_of_trips)
        self.entry_dates_of_trips[len_dates_array - 1].insert(END, getCurrentDate())
        self.entry_dates_of_trips[len_dates_array - 1].grid(row=5, column=len_dates_array, padx=10)
        self.btn_add_date.grid(row=5, column=len_dates_array + 1)

    def addCityFrom(self, root):
        self.pick_cities_from.append(ttk.Combobox(root, value=self.cities_options))
        len_cities_from_array = len(self.pick_cities_from)
        self.pick_cities_from[len_cities_from_array - 1].grid(row=3, column=len_cities_from_array, padx=10)
        self.btn_add_cities_from.grid(row=3, column=len_cities_from_array + 1)

    def addCityTo(self, root):
        self.pick_cities_to.append(ttk.Combobox(root, value=self.cities_options))
        len_cities_to_array = len(self.pick_cities_to)
        self.pick_cities_to[len_cities_to_array - 1].grid(row=4, column=len_cities_to_array, padx=10)
        self.btn_add_cities_to.grid(row=4, column=len_cities_to_array + 1)


def getCurrentDate():
    current_time = str(dt.datetime.today())
    current_date = current_time.split()[0]
    current_date = current_date.split('-')
    current_date.reverse()
    current_date = '.'.join(current_date)
    return current_date


def creatingMainApp():
    app_root = tk.Tk()
    db_carriers = DBCarriers()
    db_cities = DBCities()
    db_saves = DBSaves()
    app = Main(app_root)
    # app.pack()
    app_root.title("АКТ о выполненной работе")
    # appRoot.geometry("500x500")
    # appRoot.resizable(False, False)
    app_root.mainloop()


creatingMainApp()
