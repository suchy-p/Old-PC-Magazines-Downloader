#import threading
import Magazines
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk


cda = Magazines.CDAction()
gambler = Magazines.Gambler()
reset = Magazines.Reset()

magazines = {cda.title: cda, gambler.title: gambler, reset.title: reset}


# tkinter object
class App(tk.Tk):
    def __init__(self,):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.geometry("400x400")
        self.resizable(False, False)
        self.selected_magazine = tk.StringVar()
        self.selected_year = tk.StringVar()
        self.title("Retro PC Magazines Downloader", )

    def magazine_selection(self, event):
        combo_years.set("")
        self.selected_magazine.set(combo_magazines.get())
        combo_years.configure(values=([year for year in magazines.get(
            combo_magazines.get()).years]))

    def year_selection(self, event):
        self.selected_year.set(combo_years.get())

    def download_year(self, *args):
        magazine = self.selected_magazine.get()
        year = self.selected_year.get()

        if (len(magazine) != 0 and len(
                year) != 0):

            btn_download_year.config(state="disabled")
            btn_download_all.config(state="disabled")
            combo_magazines.config(state="disabled")
            combo_years.config(state="disabled")

            magazines.get(magazine).create_file_list(
                year)
            magazines.get(magazine).check_existing_directory()

            for item in magazines.get(magazine).issues_index:
                try:
                    magazines.get(magazine).current_issue()
                    magazines.get(magazine).download_selected_year()

                    text_box.config(state="normal")
                    text_box.insert(1.0,
                                    f"{magazines.get(magazine).name} "
                                    f"downloaded\n")
                    text_box.config(state="disabled")

                except IndexError:
                    break

            combo_years.set("")
            btn_download_year.config(state="normal")
            btn_download_all.config(state="normal")
            combo_magazines.config(state="normal")
            combo_years.config(state="normal")

        elif len(magazine) == 0:
            text_box.config(state="normal")
            text_box.insert(1.0, "Select magazine\n")
            text_box.config(state="disabled")

        else:
            text_box.config(state="normal")
            text_box.insert(1.0, "Select year\n")
            text_box.config(state="disabled")

    def download_all(self,):
        magazine = self.selected_magazine.get()
        all_years = magazines.get(self.selected_magazine.get()).years

        if len(magazine) != 0:

            for year in all_years:
                self.selected_year = tk.StringVar(value=year)
                self.download_year()

    def thread1(self, func):
        t1 = Thread(target=self.download_year)
        t1.start()

    def thread2(self, func):
        t2 = Thread(target=self.download_all)
        t2.start()

    def quit(self, event):
        self.destroy()


app = App()

lbl1 = tk.Label(text="Select magazine")
lbl1.grid(column=0, row=0, pady=10)

combo_magazines = ttk.Combobox(values=[cda.title, gambler.title,
                                       reset.title],
                               state="readonly", width=22)
combo_magazines.grid(column=1, row=0, padx=10, pady=15)

lbl2 = tk.Label(text="Select year", )
lbl2.grid(column=0, row=1, pady=5)

combo_years = ttk.Combobox(
    state="readonly", width=22)
combo_years.grid(column=1, row=1, padx=10, pady=10)

combo_magazines.bind("<<ComboboxSelected>>", app.magazine_selection)
combo_years.bind("<<ComboboxSelected>>", app.year_selection)

lbl3 = tk.Label()

btn_download_year = ttk.Button(text="Start Download", width=20)
btn_download_year.grid(column=1, row=2, padx=10, pady=10)

btn_download_all = ttk.Button(text="Download all years", width=20)
btn_download_all.grid(column=1, row=3, padx=10, pady=5)

lbl4 = tk.Label(height=10,
                width=50,
                )
lbl4.grid(columnspan=2, rowspan=20)

text_box = tk.Text(
                                lbl4,
                                height=10,
                                width=48,
                                bd=4,
                                state="disabled",
                                )
text_box.grid(column=0, columnspan=2, row=4, rowspan=10, pady=5)

scrollbar = ttk.Scrollbar(
    lbl4,
    orient=tk.VERTICAL,
    command=text_box.yview,
                            )
scrollbar.grid(column=1, row=4, rowspan=10, pady=10, sticky=(tk.NE + tk.SE))

text_box.configure(yscrollcommand=scrollbar.set)

btn_download_year.bind("<Button-1>", app.thread1)
btn_download_all.bind("<Button-1>", app.thread2)

lbl5 = ttk.Label()
lbl5.grid(column=1)

btn_close = ttk.Button(lbl5, text="Close")
btn_close.grid(column=2, row=5, padx=10, pady=5)
btn_close.bind("<Button-1>", app.quit)

app.mainloop()

