import tkinter as tk
from tkinter import ttk
import textbuild as tb


class Preview(tk.Toplevel):
    def __init__(self, app, root):
        super().__init__(root)
        self.init_child(app)
        self.root = root

    def init_child(self, main_app):
        data = {
            'number': main_app.entry_act_number.get(),
            'date': main_app.entry_date.get(),
            'carrier': main_app.pick_carrier.get(),
            'carrier_gen': tb.getGenitive(main_app.carriers, main_app.pick_carrier.get()),
            'series': tb.getSeries(main_app.carriers, main_app.pick_carrier.get()),
            'cities_from': tb.createCitiesFromString(main_app.pick_cities_from, main_app),
            'cities_to': tb.createCitiesToString(main_app.pick_cities_to),
            'dates': tb.createDatesString(main_app.entry_dates_of_trips),
            'amount': main_app.entry_amount.get(),
            'price': main_app.entry_price.get(),
            'price_trans': tb.createPriceTrans(main_app.entry_price.get())
        }
        spaces = ' ' * (80 - (len(data['carrier']) - 6) * 2)

        self.title('Предпросмотр')
        self.geometry("%dx%d+%d+%d" % (1150, 600, 400, 300))
        self.resizable(False, False)
        text = '\n'.join(
            [tb.head, tb.beginning_of_act, tb.services, tb.signatures, tb.signatures_place, tb.explanations])
        text_format = text.format(
            number=data['number'],
            date=data['date'],
            carrier=data['carrier'],
            carrier_gen=data['carrier_gen'],
            series=data['series'],
            city_from=data['cities_from'],
            cities_to=data['cities_to'],
            dates=data['dates'],
            amount=data['amount'],
            price=data['price'],
            price_trans=data['price_trans'],
            spaces=spaces
        )
        self.text = tk.Text(self, width=1000, height=35)
        self.text.insert(1.0, text_format)
        self.text.pack()

        btn_add = ttk.Button(self, text='Закрыть', width=15)
        btn_add.pack()
        btn_add.bind('<Button-1>', lambda event: self.destroy())

        self.grab_set()
        self.focus_set()
