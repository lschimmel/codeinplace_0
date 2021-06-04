import csv


def read_csv():
    lyrics = []
    with open("lyrics.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lyrics.append(row)

    #print(lyrics[4])
'''
    with open("lyrics.csv", "r") as f:
        reader = csv.reader(f, delimiter= ' ', quotechar = '|')
        for row in reader:
            print(row)
'''


if __name__ == "__main__":
    main()