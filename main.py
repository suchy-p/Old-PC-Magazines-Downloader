import bs4
import os
import requests

from Mags import Mags


def download_all(years):
    all_years = years

    for year in all_years:
        magazine.download_engine(year)

    print("Download completed")


#magazine = Mags.Gambler()
#magazine.download_engine(1998)

#magazine = Mags.Reset()
#magazine.download_engine(1999)

magazine = Mags.CDAction()
#magazine.download_engine(1996)

download_all(magazine.years)
