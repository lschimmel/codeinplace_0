import explicit

#constant used to enable code to show first lettor when censoring expletives
TWO = 2

def main(text):
    lyrics = get_lyrics(text)
    expletives = explicit.get_explicit_list()
    check(lyrics, expletives)

def get_lyrics(text):
    txt_file = open(text, "r", errors="ignore", encoding="utf-8")
    lyrics = []
    line = txt_file.read().replace("\n", " ") ##puts whole lyrics into string
    ## remove punctuation from items in list, to allow for word comparisons
    line = line.replace('(', '')
    line = line.replace(')', '')
    line = line.replace('[', '[ ')
    line = line.replace(']', ' ]')
    line = line.replace('!', ' !')
    line = line.replace('?', ' ?')
    line = line.replace(';', ' ;')
    line = line.replace(',', ' ,')
    word = line.split(' ') ##split string into list, based on spaces
    lyrics.append(word)
    txt_file.close()
    # print(lyrics)
    return word

def check(lyrics, expletives):
    j = 0
    k = 0
    expletives_used = []
    censored_expletives_used = []
    for i in range(len(lyrics)):
        word = lyrics[i]
        if word in expletives:
            if word in expletives_used:
                pass
            else:
                expletives_used.append(word)
                ## censor word using *'s, and show only first char
                i = 0
                astrix = "*"
                for i in range(len(word)- TWO):
                    astrix = astrix + "*"
                censored_expletives = word[0:1] + astrix
                censored_expletives_used.append(censored_expletives)
                j += 1
            k+= 1
    if j == 0 and k == 0:
        print("This song is squeaky clean, and SFW!")
    print("This song uses", j, "explicit terms", k, "times.")
    # option to print either censored or uncensored terms
    # print("The terms are: ", expletives_used)
    print("The terms are: ", censored_expletives_used, "\n")


if __name__ == "__main__":
    main()