import tkinter as tk
import tkinter.ttk as ttk
import Magazines
import sys


cda = Magazines.CDAction()
gambler = Magazines.Gambler()
reset = Magazines.Reset()

magazines = {cda.title: cda, gambler.title: gambler, reset.title: reset}


# tkinter object
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.minsize(width=300, height=200)
        self.title("Retro PC Magazines Downloader", )
        self.selected_magazine = tk.StringVar()
        self.selected_year = tk.StringVar()
        self.text_box = tk.Text(#app,
                                height=10,
                                width=50,
                                pady=10,
                                padx=10,
                                bd=4,
                                state="disabled",
                                )

    def magazine_selection(self, event):
        combo_years.set("")
        self.selected_magazine.set(combo_magazines.get())
        combo_years.configure(values=([year for year in magazines.get(
            combo_magazines.get()).years]))

    def year_selection(self, event):
        self.selected_year.set(combo_years.get())

    def download_year(self, event):
        if (len(self.selected_magazine.get()) != 0 and len(
                self.selected_year.get()) != 0):
            magazines.get(self.selected_magazine.get()).download_engine(
                self.selected_year.get())
            combo_years.set("")

        elif len(self.selected_magazine.get()) == 0:
            app.text_box.config(state="normal")
            app.text_box.insert(1.0, "Select magazine\n")
            app.text_box.config(state="disabled")

        else:
            app.text_box.config(state="normal")
            app.text_box.insert(1.0, "Select year\n")
            app.text_box.config(state="disabled")

    def download_all(self, event):
        if len(self.selected_magazine.get()) != 0:
            all_years = magazines.get(self.selected_magazine.get()).years
            app.text_box.config(state="normal")
            for year in all_years:
                magazines.get(self.selected_magazine.get()).download_engine(
                    year)

            app.text_box.insert(1.0, "Download completed\n")
            app.text_box.config(state="disabled")

        else:
            app.text_box.config(state="normal")
            app.text_box.insert(1.0, "Select magazine\n")
            app.text_box.config(state="disabled")

    def quit(self, event):
        self.destroy()


app = App()

lbl1 = tk.Label(text="Select magazine")
lbl1.pack(pady=5)

combo_magazines = ttk.Combobox(values=[cda.title, gambler.title,
                                       reset.title], state="readonly", )
combo_magazines.pack(padx=10, pady=10)

lbl2 = tk.Label(text="Select year")
lbl2.pack(pady=5)

combo_years = ttk.Combobox(
    state="readonly")
combo_years.pack(padx=10, pady=10)

combo_magazines.bind("<<ComboboxSelected>>", app.magazine_selection)
combo_years.bind("<<ComboboxSelected>>", app.year_selection)

btn_download_year = ttk.Button(text="Start Download", )
btn_download_year.pack(padx=10, pady=10)

btn_download_all = ttk.Button(text="Download all years")
btn_download_all.pack(padx=10, pady=15)

app.text_box.pack()

btn_download_year.bind("<Button-1>", app.download_year)
btn_download_all.bind("<Button-1>", app.download_all)


btn_close = ttk.Button(text="Close")
btn_close.pack(pady=10)
btn_close.bind("<Button-1>", app.quit)

app.text_box.config(state="normal")
# set variables in constructor, modify in constructor? then for loop in gui?
app.text_box.insert(1.0, f"{gambler.title} {gambler.years} issue "
                         f"{gambler.number}")

app.mainloop()
