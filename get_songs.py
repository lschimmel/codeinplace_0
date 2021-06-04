
import csv
import bs4

def main():
    write_data()


def write_data():
    position = 0
    artist = 1
    title = 2
    streams = 3
    lyrics_id = 4
    with open('songs.csv', "w", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(["number", "artist", "title", "streams", "lyrics_id"])
        writer.writerows([
            [position, artist, title, streams, lyrics_id]


        ])

if __name__ == "__main__":
    main()