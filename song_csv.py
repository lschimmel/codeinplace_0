#import libraries
import csv
from bs4 import BeautifulSoup
import requests
from lxml import html
N = 100
#scrapes top 100 songs from Billboard 100 music chart, and saves them as .csv file 'songs.csv.'


## Currently I'm working to bridge songs.csv into the lyrics.csv file I am using in my explicit.py program.
# Planning on using genius API to scrape for lyrics and match them against Billboard songs.


def main():
    song_title = get_top_billboard_songs()
    artist = get_top_billboard_artist()
    write_data(artist, song_title)

def write_data(artist, song_title):
    streams = 3
    lyrics_id = 4
    with open('songs.csv', "w", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(["number", "artist", "title", "streams", "lyrics_id"])
        for i in range(N):
            print(song_title[i])
            print(artist[i])
            html = 'TODO'
            writer.writerows([
                [i + 1, artist[i], song_title[i], streams, html]
            ])
    return artist

def get_top_billboard_songs():
    url = "https://www.billboard.com/charts/hot-100"
   # url = "The Hot 100 Chart _ Billboard.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.title.text)
    gdp_table = soup.find("ol", attrs={"class": "chart-list__elements"})
    gdp_table_data = gdp_table.text.replace('\n', ' ').strip()
    li = gdp_table.find_all("li")
    # print(li)
    songs = []
    for i in range(N):
        for sd in li[i].find_all("span",
                                 attrs={"class": "chart-element__information__song text--truncate color--primary"}):

            songs.append(sd.text)

    return songs

def get_top_billboard_artist():
    url = "https://www.billboard.com/charts/hot-100"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.title.text)
    gdp_table = soup.find("ol", attrs={"class": "chart-list__elements"})
    gdp_table_data = gdp_table.text.replace('\n', ' ').strip()
    li = gdp_table.find_all("li")
    # print(li)
    artist = []
    for i in range(N):
        for sd in li[i].find_all("span",
                                 attrs={"class": "chart-element__information__artist text--truncate color--secondary"}):
            artist.append(sd.text)

    return artist

if __name__ == "__main__":
    main()



