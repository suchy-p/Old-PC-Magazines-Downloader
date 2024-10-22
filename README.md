# Old PC-Magazines Downloader
## Overview
This is pure hobby project. I'm interested in PC games from 90's and early 00's. Some time ago, there was a site called retroreaders, which aggregated many, if not all retro PC magazines published in Poland. 
Sadly, it doesn't exist anymore, but it turned out, that archivechive.org has many collections of these. Unfortunately, they are in disarray. These app was created to automate downloading of my three favorite magazines:
CD-Action (years 1996–2001), Gambler (1993–1999) and Reset (1997–2001).
>[!NOTE]
>Unfortunately, Cd-Action was removed from Archive.org late August 2024. From those three it's only one still being published, so it seems that for some reason publisher doesn't wan't anyone reading thei old issues, no matter how old.
## Technologies
- Python 3.12
- Beautiful Soup 4.12.3
- Requests 2.32.3
## How does it work
All of aforementioned magazines are aggregated in some sort of collection, either they are listed, have consecutive urls. Download links are scrapped either from list page or issue page, then written to disk.
CD-Action and Gambler are saved as pdfs. Reset pdfs are horribly compressed, so issues are saved as djvu, which in this case are much better quality, for the most part at least. GUI created in tkinter.
## How to handle it
Select magazone from dropdown, then either select desired year from another dropdown and click 'Start download', or click 'Download all' to download all issues from available years.
When starting a download there will be created folder on desktop named after chosen magazine. 

For Reset you will need something to open djvu files. For example this [Chrome extension](https://chromewebstore.google.com/detail/djvujs-viewer/bpnedgjmphmmdgecmklcopblfcbhpefm?pli=1) is ok, works with Opera as well.
## Deployment
Nuitka works fine (ver. 2.4.8), haven't tried PyInstaller.

Nuitka command line:
```
python -m nuitka --enable-plugin=tk-inter --windows-console-mode=disable --standalone main.py
```
## Known bugs
None that I am aware of right now.

## Upcoming changes
When I was writing this app I wasn't aware of existence of [The Internet Archive Python Library](https://archive.org/developers/internetarchive/) until almost finished.
I intend to use it in next version, try to get more magazines available.  
