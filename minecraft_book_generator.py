"""
Takes a text file and generates Minecraft commands to give written books with
that text parsed into it. If a body of text is too long to fit inside a single book,
multiple commands are generated to give multiple books.

ASSUMPTIONS ABOUT INPUT TEXT:
- Made up of exclusively ASCII characters 32-126
- No individual word is longer than a whole page
"""

# every book has a max of 100 pages
PAGE_LIMIT = 100

# every page has a width of 114 pixels
BOOK_WIDTH = 114

# every page has a height of 14 lines
BOOK_HEIGHT = 14

# dictionary of character pixel widths for ASCII characters 32-126
PIXEL_WIDTHS = {
    ' ': 3,
    '!': 1,
    '"': 3,
    '#': 5,
    '$': 5,
    '%': 5,
    '&': 5,
    '\'': 1,
    '(': 3,
    ')': 3,
    '*': 3,
    '+': 5,
    ',': 1,
    '-': 5,
    '.': 1,
    '/': 5,
    '0': 5,
    '1': 5,
    '2': 5,
    '3': 5,
    '4': 5,
    '5': 5,
    '6': 5,
    '7': 5,
    '8': 5,
    '9': 5,
    ':': 1,
    ';': 1,
    '<': 4,
    '=': 5,
    '>': 4,
    '?': 5,
    '@': 6,
    'A': 5,
    'B': 5,
    'C': 5,
    'D': 5,
    'E': 5,
    'F': 5,
    'G': 5,
    'H': 5,
    'I': 3,
    'J': 5,
    'K': 5,
    'L': 5,
    'M': 5,
    'N': 5,
    'O': 5,
    'P': 5,
    'Q': 5,
    'R': 5,
    'S': 5,
    'T': 5,
    'U': 5,
    'V': 5,
    'W': 5,
    'X': 5,
    'Y': 5,
    'Z': 5,
    '[': 3,
    '\\': 5,
    ']': 3,
    '^': 5,
    '_': 5,
    '`': 2,
    'a': 5,
    'b': 5,
    'c': 5,
    'd': 5,
    'e': 5,
    'f': 4,
    'g': 5,
    'h': 5,
    'i': 1,
    'j': 5,
    'k': 4,
    'l': 2,
    'm': 5,
    'n': 5,
    'o': 5,
    'p': 5,
    'q': 5,
    'r': 5,
    's': 5,
    't': 3,
    'u': 5,
    'v': 5,
    'w': 5,
    'x': 5,
    'y': 5,
    'z': 5,
    '{': 3,
    '|': 1,
    '}': 3,
    '~': 6,
}

# clear the output file
with open('output.txt', 'w') as file:
    file.write("")

words = []
filename = input("What is the full name of the file containing your text?: ")
with open(filename, 'r') as file:
    # replace tabs and newlines with spaces
    words = file.read().replace('\t', ' ').replace('\n', ' ').split(' ')

title = input("What is the title of the book?: ").replace('\"', '\\\"').strip()

author = input("What is the author of the book?: ").replace('\"', '\\\"').strip()

lore = input("What is the description of the book?: ").replace('\"', '\\\"').strip()

command = "/give @p written_book{pages:['{\"text\":\""

curr_book = 1 # what number book the program is on
curr_page = 1 # what number page of the current book the program is on
curr_line = 1 # what number line of the current page the program is on
curr_num_pixels = 0 # how many pixels on the current line the program is on

i = 0
while i < len(words):
    curr_word_num_pixels = 0
    new_word = ""
    for character in words[i].strip():
        curr_word_num_pixels += PIXEL_WIDTHS[character] + 1 # there is 1 pixel spacing between every character
        # if the character is a quote or apostrophe, escape it for command formatting
        if character == '\"':
            new_word += "\\\\\""
        elif character == '\'':
            new_word += "\\\'"
        else:   
            new_word += character
    # if the word was just made up of spaces, skip
    if len(new_word) == 0:
        i += 1
        continue

    curr_num_pixels += curr_word_num_pixels

    if curr_num_pixels > BOOK_WIDTH:
        # remove the space from the end of the last word, since this is the end of the line
        command.rstrip(command[-1])

        # increment the current line and set the number of pixels to start that line equal to its length
        curr_line += 1
        potential_num_pixels = curr_word_num_pixels

        # in the case that the word is longer than an entire line, continue incrementing lines for its whole length
        curr_num_pixels_in_word = 0
        for character in new_word:
            curr_num_pixels_in_word += PIXEL_WIDTHS[character] + 1
            if curr_num_pixels_in_word > BOOK_WIDTH:
                curr_line += 1
                potential_num_pixels -= (curr_num_pixels_in_word - PIXEL_WIDTHS[character] - 1)
                curr_num_pixels_in_word = PIXEL_WIDTHS[character] + 1

        # if the word pushes the book to the next page, don't add the next word, don't
        # increment to the next word, and don't reset the number of pixels
        if curr_line > BOOK_HEIGHT:
            # if the page limit has been reached, end this command, write it to the file, and start a new one
            if curr_page >= PAGE_LIMIT:
                # if this book is not the first, append its number to the end of the title
                if curr_book >= 2:
                    command += "\"}'],title:\"" + title + " " + str(curr_book) + "\",author:\"" + author + "\",display:{Lore:[\"" + lore + "\"]}}"
                else:
                    command += "\"}'],title:\"" + title + "\",author:\"" + author + "\",display:{Lore:[\"" + lore + "\"]}}"

                with open('output.txt', 'a') as file:
                    file.write(command)
                    file.write("\n\n")
                command = "/give @p written_book{pages:['{\"text\":\""
                curr_page = 1
                curr_book += 1
            # if the page limit hasn't been met, start a new page
            else:
                command += "\"}','{\"text\":\""
                curr_page += 1
            curr_line = 1
            curr_num_pixels = 0
            continue
        curr_num_pixels = potential_num_pixels
    
    # add a space at the end of the word
    new_word += ' '
    curr_num_pixels += PIXEL_WIDTHS[' '] + 1
    command += new_word
    i += 1

# end the current command and write it to the file
command += "\"}'],title:\"" + title + "\",author:\"" + author + "\",display:{Lore:[\"" + lore + "\"]}}"
with open('output.txt', 'a') as file:
    file.write(command)