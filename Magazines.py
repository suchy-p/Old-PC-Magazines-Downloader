import bs4
import os
import re
import requests


class ParentMagazine:
    def __init__(self):
        self.current_year = str()
        self.download_directory = str()
        self.download_url = str()
        self.file_url = list()
        self.issues = list()
        self.issues_index = list()
        self.name = str()
        self.page_url = str()
        self.title = str()
        self.years = str()


    def check_existing_directory(self):
        # check if download dir was already created with previous run
        try:
            os.mkdir(self.download_directory)
        except FileExistsError:
            pass
        finally:
            os.chdir(self.download_directory)

    def create_file_list(self, year):
        # creates list of files for download from selected year
        # exact Parent ver of this method isn't used in children: CDAction,
        # Gambler, Reset in ver. 1.00
        self.current_year = year

        soup = bs4.BeautifulSoup(requests.get(self.page_url +
                                              self.current_year).text,
                                 'lxml')
        self.file_url = soup.find_all(href=re.compile(".pdf$"))

        # list of all issue urls
        self.issues = [item for item in self.file_url]

        # indexing issues urls for self.current_year
        # used in main in for download loop for selected year
        for index, item in enumerate(self.issues):
            if self.current_year in item:
                self.issues_index.append(index)

            
    def current_issue(self):
        # creating download link for issues in download loop in main,
        # output file name, removing used issue from url list
        self.download_url = f'{self.page_url}{self.file_url[0].get("href")}'
        self.name = self.file_url[0].getText()
        self.file_url.pop(0)
        
    def download_selected_year(self):
        # check for uncompleted download
        try:
            if os.path.getsize(self.name) == 0:
                os.remove(self.name)
        except FileNotFoundError:
            pass

        # check for completed download, skip file download if true
        if not os.path.isfile(self.name):
            with open(self.name, 'wb') as file:
                file.write(requests.get(self.download_url).content)
        
    
class CDAction(ParentMagazine):
    def __init__(self, ):
        super().__init__()
        self.page_url = 'https://archive.org/download/CDA1996-2001/'
        self.title = "CD-Action"
        # years available in this collection
        self.years = (1996, 1997, 1998, 1999, 2000, 2001)

        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)



    def create_file_list(self, year):
        self.current_year = year

        soup = bs4.BeautifulSoup(requests.get(self.page_url).text, 'lxml')

        # [-\d{2}]* == [hyphen|digit*2] occurs zero or more times
        # searching for possible double issue like CD-Action_001_1996_04-05
        self.file_url = soup.find_all(href=re.compile(self.current_year +
                                                      r"_\d+[-\d{2}]*.pdf$"))

        # issues from all years on one list on archive org, creating list of
        # all urls
        self.issues = [item for item in self.file_url]

        # indexing issues urls for self.current_year
        # issues_index for CDAction differs from others bcs all download
        # links are on one page, not separate ones
        self.issues_index = [num for num in range(len(self.issues))]


    def current_issue(self):
        self.name = self.file_url[0].getText()
        self.download_url = (f'{self.page_url}'
                             f'{self.file_url.pop(0).get("href")}')



class Gambler(ParentMagazine):

    def __init__(self, ):
        super().__init__()
        self.current_number = 1
        self.page_url = "https://archive.org/details/gambler_magazine"
        self.title = "Gambler"
        self.years = (1993, 1994, 1995, 1996, 1997, 1998, 1999)

        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)


    def create_file_list(self, year):
        self.current_year = str(year)
        # first issue ever of Gambler was published in december 1993,
        # hence 12 in self.numbers for this year
        self.numbers = [12] if year == "1993" else list(range(1, 13))

        # creating list of issues urls;
        # they have consecutive issue nums from 1 to 12 and year
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


class Reset(ParentMagazine):
    def __init__(self, ):
        super().__init__()
        self.number = int()
        self.page_url = ("https://archive.org/download/reset-cd-1999-06"
                         "/Reset%201997-2001/")
        self.title = "Reset"
        self.years = (1997, 1998, 1999, 2000, 2001)

        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

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
        self.name = self.file_url[self.number].getText().capitalize()
        self.file_url.pop(0)

if __name__ == "__main__":
    main()