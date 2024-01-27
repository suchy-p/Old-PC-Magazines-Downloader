import flet as ft
import requests
import Magazines

magazine = Magazines.CDAction()


def download_all(years):
    all_years = years

    for year in all_years:
        magazine.download_engine(year)

    print("Download completed")


try:
    check = requests.get(magazine.url, timeout=5)
except requests.RequestException as err:
    print(f"Error occurred:\n{err}")
else:
    download_all(magazine.years)
