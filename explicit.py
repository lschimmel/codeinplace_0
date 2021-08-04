# opens txt file containing explicit terms, "explicit.txt", sourced from: 'https://www.cs.cmu.edu/~biglou/resources/bad-words.txt'
# outputs explicit terms as a list

def get_explicit_list():
    a_file = open("txt_files/explicit.txt", "r")
    list_of_explicit_terms = []
    for line in a_file:
        stripped_line = line.strip("\n")
        list_of_explicit_terms.append(stripped_line)
    a_file.close()
    return list_of_explicit_terms



if __name__ == '__main__':
    main()