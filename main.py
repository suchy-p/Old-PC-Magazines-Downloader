import requests
import Magazines

magazine = Magazines.Gambler()


def download_all(years):
    all_years = years

    for year in all_years:
        magazine.download_selected_year()

    print("Download completed")

magazine.create_file_list(1994)
print(magazine.issues)
print(magazine.issues_index)
print(magazine.download_url)



"""try:
    check = requests.get(magazine.url, timeout=5)
except requests.RequestException as err:
    print(f"Error occurred:\n{err}")
else:
    download_all(magazine.years)"""
