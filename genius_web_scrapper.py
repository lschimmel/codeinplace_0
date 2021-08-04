from bs4 import BeautifulSoup
import requests
from datetime import date
import csv
import lyricsgenius
import open_lyrics_txt
import client_access

N = 3

# scrapes the top 100 songs from the Billboard top music, and outputs the number of explicit terms, and their frequency usage.
# lyrics are pulled using genius.com's API
# explicit words are sourced from: 'https://www.cs.cmu.edu/~biglou/resources/bad-words.txt'




def main():
    url = get_url()
    song_dict = get_top_billboard_songs(url)
    artist_song_dict = get_top_billboard_artist(url, song_dict)
    txt_file = analyze_lyrics(artist_song_dict)

def get_url():
    # url for Billboard top 100
    url = "https://www.billboard.com/charts/hot-100"
    return url

def get_top_billboard_songs(url):
    #scrapes the Billboard top 100 page for song names
    # songs are identified by their json class (chart-element__information__song text)
    # creates a song dictionary of key value pairs 0 - N. Appends a list containing the song title to each key value.
    #Use case for BTS's #1 song, Butter: {0: ['Butter']}
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    gdp_table = soup.find("ol", attrs={"class": "chart-list__elements"})
    li = gdp_table.find_all("li")
    # print(li)
    song_dict = {}
    for i in range(N):
        song = []
        for sd in li[i].find_all("span",
                                 attrs={"class": "chart-element__information__song text--truncate color--primary"}):
            song.append(sd.text)
            song_dict[i] = song
    # print(song_dict)
    return song_dict

def get_top_billboard_artist(url, song_dict):
    #scrapes the Billboard top 100 page for artist names
    #artist names are identified by their json class (chart-element__information__artist text)
    #Appends each artist name to the list of each key value.
    #Use case for BTS's #1 song, Butter: {0: ['Butter','BTS']}
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.title.text)
    hit_songs = soup.find("ol", attrs={"class": "chart-list__elements"})
    gdp_table_data = hit_songs.text.replace('\n', ' ').strip()
    li = hit_songs.find_all("li")
    # print(li)
    for i in range(N):
        for sd in li[i].find_all("span",
                                 attrs={"class": "chart-element__information__artist text--truncate color--secondary"}):
            song_dict[i].append(sd.text)
    # print(song_dict)
    return song_dict

def analyze_lyrics(artist_song_dict):
    #iterates over each song in the artist_song_dict,
    # calls function get_lyrics to query genius.com's API using song title and artist name, and
    # calls open_lyrics_txt to analyze the lyrics
    print("The analysis of this week's top 100 songs has begun.")
    i = 0
    for elem in (artist_song_dict):
        artist_name = str(artist_song_dict[elem][1])
        #clean billboard data to conform with genius.com's data requirements
        if '&' in artist_name or '+' in artist_name:
            artist_name = artist_name.replace('&' or '+', 'and')
        if 'Duet' in artist_name:
            artist_name = artist_name.replace('Duet With' or 'Duet With', 'and')
        if ' X ' in artist_name:
            artist_name = artist_name.replace(' X ', ' and ')
        if 'Featuring' in artist_name:
            head, sep, tail = artist_name.partition('Featuring')
            # print(head)
            artist_name = head
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", artist_name)
        song_title = str(artist_song_dict[elem][0])
        lyrics = get_lyrics(artist_name, song_title)
        name = str(i) + ".txt"
        i += 1
        lyrics.save_lyrics(filename= name, overwrite=True, ensure_ascii=True, sanitize=True, verbose=True, extension='txt',)
        artist_song_dict[elem].append(name)
        print(artist_song_dict[elem])
        lyrics_analysis = open_lyrics_txt.main(name)

    return name

def get_lyrics(artist_name, song_title):
    #returns lyrics given artist name and song title
    client_access_token = client_access.main()
    LyricsGenius = lyricsgenius.Genius(client_access_token)
    # artist = LyricsGenius.search_artist(search_term, max_songs= 5)
    song_lyrics = LyricsGenius.search_song(song_title, artist_name)
    if song_lyrics is None:
        song_lyrics_mod = ''
        for elem in song_title:
            song_lyrics_mod += elem + ' '
        # print(song_lyrics_mod)
        song_title = song_lyrics_mod[:len(song_lyrics_mod) - 1]
        print(song_title)
        print("yo")
        song_lyrics = LyricsGenius.search_song(song_title, artist_name)
    # text_file = song_lyrics.save_lyrics(extension='txt')
    # song_lyrics.save_lyrics(extension='json')
    # print(song_lyrics)
    return song_lyrics

# def get_lyrics_text(text):
#     # text = "lyrics_missyelliott_imbetter.txt"
#     txt_file = open(text, "r", errors="ignore", encoding="utf-8")
#     # words = list(txt_file)
#     # print(words)
#     lyrics = []
#     line = txt_file.read().replace("\n", " ") ##puts whole lyrics into string
#     ## remove punctuation from items in list, to allow for word comparisons
#     line = line.replace('(', '')
#     line = line.replace(')', '')
#     line = line.replace('[', '[ ')
#     line = line.replace(']', ' ]')
#     line = line.replace('!', ' !')
#     line = line.replace('?', ' ?')
#     line = line.replace(';', ' ;')
#     line = line.replace(',', ' ,')
#
#     word = line.split(' ') ##split string into list, based on spaces
#     lyrics.append(word)
#     txt_file.close()


# def get_today_date():
#     today = date.today()
#     d1 = today.strftime('%d%m%Y')
#     return d1

# def write_csv(artist_song_dict, date, lyrics):
#     csv_name = 'songs' + str(date) + '.csv'
#     print(csv_name)
#     with open(csv_name, "w", newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(["rank", "title", "artist", "genius_url", "lyrics"])
#         for i in range(len(artist_song_dict)):
#             writer.writerows([
#                 # [genius_url[elem][0], genius_url[elem][1], genius_url[elem][2], genius_url[elem][3], html]
#                  [i + 1,artist_song_dict[i][0], artist_song_dict[i][1], artist_song_dict[i][2], lyrics]
#             ])



if __name__ == "__main__":
    main()

