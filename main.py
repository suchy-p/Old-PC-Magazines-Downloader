import bs4
import requests
import os


# TODO refactor for objects

# loop for downloading all issues from given year
def download_whole_year(year):
    number = 1
    year = int(year)
    directory = os.path.expanduser("~") + "\\Desktop\\"

    while True:
        try:
            name = f"Gambler_{year}_{str(number).zfill(2)}"

            # url pattern for Gambler
            base_url = requests.get(
                f'https://archive.org/details/gambler_magazine-{year}'
                f'-{str(number).zfill(2)}')
            soup = bs4.BeautifulSoup(base_url.text, 'lxml')
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
                    os.path.join(directory, "Gambler\\"))
            except FileExistsError:
                pass
            finally:
                os.chdir(directory + "Gambler")

                # file exists check
                if os.path.isfile(
                        directory + "Gambler\\" + "{name}.pdf".format(
                            name=name)):
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
                        print(f"Issue {number} / {year} already downloaded")
                        number += 1
                # write file
                else:
                    with open("{name}.pdf".format(name=name), 'wb') as file:
                        file.write(requests.get(download_url).content)
                    print(f"Issue {number} / {year} downloaded")
                    number += 1

        except IndexError:
            # searching for first issue from first year <== change print()
            if number < 12:
                print("Searching for first issue...\n")
                number += 1
                continue
            # check for full year ==> number > 12 for monthly magazine
            else:
                print(f"All issues from year {year} downloaded")
                break


def download_all(years):
    all_years = years

    for year in all_years:
        download_whole_year(year)

    print("Download completed")


download_all([1993, 1994, 1995, 1996, 1997,
              1998, 1999])
