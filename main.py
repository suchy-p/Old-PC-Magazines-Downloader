import Magazines
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk


# tkinter object
class App(tk.Tk):
    def __init__(self, ):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.geometry("400x400")
        self.resizable(False, False)
        self.selected_magazine = tk.StringVar()
        self.selected_year = tk.StringVar()
        self.title("Retro PC Magazines Downloader", )

    def magazine_selection(self, event):
        view.combo_years.set("")
        self.selected_magazine.set(view.combo_magazines.get())
        view.combo_years.configure(values=([year for year in magazines.get(
            view.combo_magazines.get()).years]))

    def year_selection(self, event):
        self.selected_year.set(view.combo_years.get())

    def download_year(self, *args):
        magazine = self.selected_magazine.get()
        year = self.selected_year.get()

        if (len(magazine) != 0 and len(
                year) != 0):

            # disable all interactive ui elements except quit when starting
            # download
            view.btn_download_year.config(state="disabled")
            view.btn_download_all.config(state="disabled")
            view.combo_magazines.config(state="disabled")
            view.combo_years.config(state="disabled")

            magazines.get(magazine).create_file_list(
                year)
            magazines.get(magazine).check_existing_directory()

            for item in magazines.get(magazine).issues_index:
                try:
                    magazines.get(magazine).current_issue()
                    magazines.get(magazine).download_selected_year()

                    view.text_box.config(state="normal")
                    view.text_box.insert(1.0,
                                         f"{magazines.get(magazine).name} "
                                         f"downloaded\n")
                    view.text_box.config(state="disabled")

                except IndexError:
                    break

            # enable all interactive ui elements after finished download
            view.combo_years.set("")
            view.btn_download_year.config(state="normal")
            view.btn_download_all.config(state="normal")
            view.combo_magazines.config(state="normal")
            view.combo_years.config(state="normal")

        elif len(magazine) == 0:
            # check if magazine is selected
            view.text_box.config(state="normal")
            view.text_box.insert(1.0, "Select magazine\n")
            view.text_box.config(state="disabled")

        else:
            # check if year is selected
            view.text_box.config(state="normal")
            view.text_box.insert(1.0, "Select year\n")
            view.text_box.config(state="disabled")

    def download_all(self, ):
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


class View:
    def __init__(self):
        self.lbl1 = tk.Label(text="Select magazine")

        self.combo_magazines = ttk.Combobox(
            values=[cda.title, gambler.title,
                    reset.title],
            state="readonly",
            width=22
        )

        self.lbl2 = tk.Label(text="Select year", )

        self.combo_years = ttk.Combobox(state="readonly", width=22)

        self.combo_magazines.bind("<<ComboboxSelected>>",
                                  app.magazine_selection)
        self.combo_years.bind("<<ComboboxSelected>>", app.year_selection)

        self.btn_download_year = ttk.Button(text="Start Download", width=20)

        self.btn_download_all = ttk.Button(text="Download all years", width=20)

        self.lbl3 = tk.Label(height=10, width=50)

        self.text_box = tk.Text(
            self.lbl3,
            height=10,
            width=48,
            bd=4,
            state="disabled",
        )

        self.scrollbar = ttk.Scrollbar(
            self.lbl3,
            orient=tk.VERTICAL,
            command=self.text_box.yview,
        )

        self.lbl4 = ttk.Label()
        self.btn_close = ttk.Button(self.lbl4, text="Close")


cda = Magazines.CDAction()
gambler = Magazines.Gambler()
reset = Magazines.Reset()

magazines = {cda.title: cda, gambler.title: gambler, reset.title: reset}
app = App()
view = View()

view.lbl1.grid(column=0, row=0, pady=10)
view.combo_magazines.grid(column=1, row=0, padx=10, pady=15)

view.lbl2.grid(column=0, row=1, pady=5)
view.combo_years.grid(column=1, row=1, padx=10, pady=10)

view.btn_download_year.grid(column=1, row=2, padx=10, pady=10)
view.btn_download_year.bind("<Button-1>", app.thread1)

view.btn_download_all.grid(column=1, row=3, padx=10, pady=5)
view.btn_download_all.bind("<Button-1>", app.thread2)

view.lbl3.grid(columnspan=2, rowspan=20)
view.text_box.grid(column=0, columnspan=2, row=4, rowspan=10, pady=5)
view.scrollbar.grid(column=1, row=4, rowspan=10, pady=10, sticky=(tk.NE +
                                                                  tk.SE))
view.text_box.configure(yscrollcommand=view.scrollbar.set)

view.lbl4.grid(column=1)
view.btn_close.grid(column=2, row=5, padx=10, pady=5)
view.btn_close.bind("<Button-1>", app.quit)

if __name__ == "__main__":
    app.mainloop()
