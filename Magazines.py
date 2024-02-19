import bs4
import os
import re
import requests


class CDAction:
    def __init__(self, ):
        self.current_year = str()
        self.download_url = None
        self.file_url = None
        self.issues = list()
        self.issues_index = list()
        self.name = str()
        self.page_url = "https://archive.org/download/CDA1996-2001/"
        # years available in this collection
        self.title = "CD-Action"
        self.years = (1996, 1997, 1998, 1999, 2000, 2001)

        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

    def check_existing_directory(self):
        # directory exists check
        try:
            os.mkdir(self.download_directory)

        except FileExistsError:
            pass
        finally:
            os.chdir(self.download_directory)

    def create_file_list(self, year):
        self.current_year = year

        soup = bs4.BeautifulSoup(requests.get(self.page_url).text, 'lxml')

        # [-\d{2}]* == [hyphen|digit*2] occurs zero or more times
        # searching for possible double issue like CD-Action_001_1996_04-05
        self.file_url = soup.find_all(href=re.compile(self.current_year +
                                                      r"_\d+[-\d{2}]*.pdf$"))

        # issues from all years on one list on archive org, creating list of
        # all urls
        self.issues = [str(item) for item in self.file_url]

        # indexing issues urls for self.current_year
        for index, item in enumerate(self.issues):
            if self.current_year in item:
                self.issues_index.append(index)

    def current_issue(self):
        self.download_url = f'{self.page_url}{self.file_url[0].get("href")}'
        self.name = self.file_url[0].getText()
        self.file_url.pop(0)

    def download_selected_year(self):
        # uncompleted download check
        try:
            if os.path.getsize(self.name) == 0:
                os.remove(self.name)

        except FileNotFoundError:
            pass

        # completed download check
        if not os.path.isfile(self.name):
            with open(self.name, 'wb') as file:
                file.write(requests.get(self.download_url).content)


class Gambler:

    def __init__(self, ):
        self.current_number = 1
        self.current_year = str()
        self.download_url = None
        self.file_url = None
        self.issues = list()
        self.issues_index = list()
        self.name = str()
        self.numbers = list()
        self.page_url = "https://archive.org/details/gambler_magazine"
        self.title = "Gambler"
        self.years = (1993, 1994, 1995, 1996, 1997, 1998, 1999)

        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

    def check_existing_directory(self):
        # directory exists check
        try:
            # existing directory check
            os.mkdir(self.download_directory)

        except FileExistsError:
            pass

        finally:
            os.chdir(self.download_directory)

    def create_file_list(self, year):
        self.current_year = str(year)
        self.numbers = [12] if year == "1993" else list(range(1, 13))

        # creating list of issues urls
        for number in self.numbers:
            soup = bs4.BeautifulSoup(
                requests.get(f"{self.page_url}-{self.current_year}-"
                             f"{str(number).zfill(2)}")
                .text, 'lxml')
            self.file_url = soup.find_all(href=re.compile(r"\d.pdf$"))

            self.issues.append(f"https://archive.org"
                               f"{(self.file_url[0].get('href'))}")

        # indexing issues urls for self.current_year
        for index, item in enumerate(self.issues):
            if self.current_year in item:
                self.issues_index.append(index)

    def current_issue(self):
        self.download_url = self.issues[0]
        self.name = (f"{self.title}_{self.current_year}"
                     f"_{str(self.current_number).zfill(2)}.pdf")
        self.issues.pop(0)

        if self.current_year != "1993":
            if self.current_number == 12:
                self.current_number = 1
            else:
                self.current_number += 1

    def download_selected_year(self, ):

        # existing file check
        if os.path.isfile(self.name):

            # uncompleted download check
            try:
                if os.path.getsize(self.name) == 0:
                    os.remove(self.name)

            except FileNotFoundError:
                pass

        if not os.path.isfile(self.name):
            with open(self.name, 'wb') as file:
                file.write(requests.get(self.download_url).content)


class Reset:
    def __init__(self, ):
        self.current_year = str()
        self.download_url = None
        self.file_url = None
        self.issues = list()
        self.issues_index = list()
        self.name = str()
        self.number = int()
        self.page_url = ("https://archive.org/download/reset-cd-1999-06"
                         "/Reset%201997-2001/")
        self.title = "Reset"
        self.years = (1997, 1998, 1999, 2000, 2001)

        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

    def check_existing_directory(self):
        # directory exists check
        try:
            os.mkdir(self.download_directory)

        except FileExistsError:
            pass
        finally:
            os.chdir(self.download_directory)

    def create_file_list(self, year):
        self.current_year = year

        soup = bs4.BeautifulSoup(requests.get(self.page_url +
                                              self.current_year).text,
                                 'lxml')
        self.file_url = soup.find_all(href=re.compile(".djvu$"))

        # issues from all years on one list on archive org, creating list of
        # all urls
        self.issues = [str(item) for item in self.file_url]

        # indexing issues urls for self.current_year
        for index, item in enumerate(self.issues):
            if self.current_year in item:
                self.issues_index.append(index)

    def current_issue(self):
        self.download_url = (f'{self.page_url}{self.current_year}'
                             f'/{self.file_url[self.number].get("href")}')
        #self.download_url = f'{self.page_url}{self.file_url[0].get("href")}'
        self.name = self.file_url[self.number].getText().capitalize()
        self.file_url.pop(0)

    def download_selected_year(self):
        # uncompleted download check
        try:
            if os.path.getsize(self.name) == 0:
                os.remove(self.name)

        except FileNotFoundError:
            pass

        # completed download check
        if not os.path.isfile(self.name):
            with open(self.name, 'wb') as file:
                file.write(requests.get(self.download_url).content)
