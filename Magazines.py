import bs4
import os
import re
import requests


class Gambler:

    def __init__(self, ):
        self.title = "Gambler"
        self.url = "https://archive.org/details/gambler_magazine"
        self.years = (1993, 1994, 1995, 1996, 1997, 1998, 1999)
        self.number = 1
        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

    def download_engine(self, year):

        y = str(year)

        """
        while loop because => searching for first issue; might be useful
        for some other magazine with similarly diffused files and structured 
        urls on archive.org
        """
        while True:
            try:
                # original file name: Gambler_issue_year, not great for
                # organizing files in folder by name
                name = f"{self.title}_{y}_{str(self.number).zfill(2)}.pdf"

                try:
                    # existing directory check
                    os.mkdir(self.download_directory)
                except FileExistsError:
                    pass
                finally:
                    os.chdir(self.download_directory)

                    # existing file check
                    if os.path.isfile(name):

                        # uncompleted download check
                        try:
                            if os.path.getsize(name) == 0:
                                os.remove(name)
                                continue
                        except FileNotFoundError:
                            pass
                        # completed download check
                        else:
                            print(f"{self.title} issue {self.number} / {y} "
                                  f"already downloaded")
                            self.number += 1

                    # write file
                    else:
                        base_url = requests.get(
                            f"{self.url}-{y}-{str(self.number).zfill(2)}")
                        soup = bs4.BeautifulSoup(base_url.text, "lxml")
                        # find pdf download link in soup
                        file_url = soup.find_all(href=re.compile(r"\d.pdf$"))
                        # pdf download link pattern, index of download link in
                        # file_url
                        download_url = (f"https://archive.org"
                                        f"{file_url[0].get('href')}")
                        print(download_url)
                        print(f"Downloading issue {self.title} {self.number} "
                              f"/ {y}")
                        with open(name, "wb") as file:
                            file.write(requests.get(download_url).content)
                        print(f"{self.title} issue {self.number} / {y} "
                              f"downloaded")
                        self.number += 1

            except IndexError:
                # searching for first issue from first year
                if self.number < 12:
                    print("Searching for first issue...\n")
                    self.number += 1
                    continue

                    # check for full year ==> number > 12 for monthly magazine
                else:
                    print(f"All issues from year {y} downloaded")
                    self.number = 1
                    break


class Reset:
    def __init__(self, ):
        self.title = "Reset"
        self.url = ("https://archive.org/download/reset-cd-1999-06/Reset"
                    "%201997-2001/")
        self.years = (1997, 1998, 1999, 2000, 2001)
        # self.number == index of url on download list, not actual issue number
        self.number = 0
        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

    def download_engine(self, year):

        y = str(year)

        # if base_url used (see Gambler) result == Response 200, no data (no
        # idea why)
        soup = bs4.BeautifulSoup(requests.get(self.url+y).text, 'lxml')
        file_url = soup.find_all(href=re.compile(".djvu$"))

        try:
            # directory exists check
            os.mkdir(self.download_directory)
        except FileExistsError:
            pass
        finally:
            os.chdir(self.download_directory)

        # for loop => file structure organized by years
        for issue in file_url:
            name = file_url[self.number].getText().capitalize()
            download_url = f'{self.url}{y}/{file_url[self.number].get("href")}'

            if os.path.isfile(name):
                # uncompleted download check
                try:
                    if os.path.getsize(name) == 0:
                        os.remove(name)
                        continue
                except FileNotFoundError:
                    pass
                else:
                    print(f"{name} already downloaded")
                    self.number += 1
                    continue
            else:
                # download file
                print(f'Downloading {name}')
                with open(name, 'wb') as file:
                    file.write(requests.get(download_url).content)
                self.number += 1
                print(f"{name} downloaded")

        self.number = 0
        print(f'All issues from {y} downloaded')


class CDAction:
    def __init__(self, ):
        self.title = "CD-Action"
        self.url = "https://archive.org/download/CDA1996-2001/"
        # not all years in history ofc
        self.years = (1996, 1997, 1998, 1999, 2000, 2001)
        # self.number == index of url on download list, not actual issue number
        self.number = 0
        self.download_directory = os.path.join((os.path.expanduser("~") +
                                                "\\Desktop\\"), self.title)

    def download_engine(self, year):

        y = str(year)
        issue_index = list()

        # base_url = requests.get(self.url)
        soup = bs4.BeautifulSoup(requests.get(self.url).text, 'lxml')
        file_url = soup.find_all(href=re.compile(y + r"_\d+.pdf$"))

        try:
            # directory exists check
            os.mkdir(self.download_directory)
        except FileExistsError:
            pass
        finally:
            os.chdir(self.download_directory)

        # issues from all years on one list on archive org, creating list of
        # all urls
        issues = [str(item) for item in file_url]

        # indexing issues urls for given year (y)
        for index, item in enumerate(issues):
            if y in item:
                issue_index.append(index)

        # loop for downloading all issues from given year
        for item in issue_index:
            name = file_url[item].getText()
            download_url = f'{self.url}{file_url[item].get("href")}'

            if os.path.isfile(name):
                # uncompleted download check
                try:
                    if os.path.getsize(name) == 0:
                        os.remove(name)
                        continue
                except FileNotFoundError:
                    pass
                    # completed download check
                else:
                    print(f"{name} already downloaded")
                    self.number += 1
                    continue

            else:
                # download file
                print(f'Downloading {name}')
                self.number = item
                with open(name, 'wb') as file:
                    file.write(requests.get(download_url).content)

                print(f"{name} downloaded")

        print(f'All issues from {y} downloaded')


