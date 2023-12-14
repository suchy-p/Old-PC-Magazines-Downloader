import bs4
import os
import requests

from Mags import Mags



# loop for downloading all issues from given year
def download_whole_year(magazine, year):
    number = 1
    year = year
    directory = os.path.expanduser("~") + "\\Desktop\\"

    while True:
        #TODO refactor as method in Mags.Mags
        try:
            name = f"{magazine.title}_{year}_{str(number).zfill(2)}"

            # url pattern for chosen magazine
            base_url = requests.get(
                f"{magazine.url}-{year}-{str(number).zfill(2)}")
            soup = bs4.BeautifulSoup(base_url.text, "lxml")
            # find pdf download link in soup
            pdf_url = soup.find_all("a",
                                    {"class": "format-summary download-pill"})
            # pdf download link pattern, 3rd index in download links
            download_url = 'https://archive.org{}'.format(
                pdf_url[3].get('href'))

            # save as .pdf
            try:
                # directory exists check
                download_directory = os.mkdir(
                    os.path.join(directory, magazine.title))
            except FileExistsError:
                pass
            finally:
                os.chdir(directory + magazine.title)

                # file exists check
                if os.path.isfile(
                        directory + magazine.title + "\\" + f"{name}.pdf"):
                    # uncompleted download check
                    try:
                        if os.path.getsize(
                                os.path.join(os.getcwd(), name + ".pdf")) == 0:
                            os.remove(os.path.join(os.getcwd(), name + ".pdf"))
                            continue
                    except FileNotFoundError:
                        pass
                    # completed download check
                    else:
                        print(f"{magazine.title} issue "
                              f"{number} / {year} already downloaded")
                        number += 1
                # write file
                else:
                    with open(f"{name}.pdf", 'wb') as file:
                        file.write(requests.get(download_url).content)
                    print(f"Issue {number} / {year} downloaded")
                    number += 1

        except IndexError:
            # searching for first issue from first year <== change print()
            if year == magazine.years[0] and number < 12:
                print("Searching for first issue...\n")
                number += 1
                continue
            # check for full year ==> number > 12 for monthly magazine
            else:
                print(f"All issues from year {year} downloaded")
                number = 1
                break


def download_all(magazine):
    all_years = magazine.years

    for year in all_years:
        download_whole_year(magazine, year)

    print("Download completed")


gambler = Mags.Gambler()

download_all(gambler)

#download_whole_year(gambler, 1997)