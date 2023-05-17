"""
Takes a text file and generates a Minecraft function file to be placed inside a
datapack folder. This bypasses the 32,500 character limit inside command blocks
and allows the generation of any (reasonable) length book. 

The output file can be placed inside the 'functions' folder of any data pack, or
it can be pasted right into a command block if it is fewer than 32,500 characters.

ASSUMPTIONS ABOUT INPUT TEXT:
- Made up of exclusively ASCII characters 32-126
"""

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
    '\n': 0
}

# clear the output file
with open('makebook.mcfunction', 'w') as file:
    file.write("")

words = []
filename = input("What is the full name of the file containing your text?: ")
with open(filename, 'r', encoding='utf-8') as file:
    # replace tabs with spaces and add a space after every newline, then split by spaces
    words = file.read().replace('\t', ' ').replace('\n', '\n ').split(' ')

title = input("What is the title of the book?: ").replace('\"', '\\\"').strip()

author = input("What is the author of the book?: ").replace('\"', '\\\"').strip()

lore = input("What is the description of the book?: ").replace('\"', '\\\"').strip()

command = "give @p written_book{pages:['{\"text\":\""

curr_book = 1 # what number book the program is on
curr_page = 1 # what number page of the current book the program is on
curr_line = 1 # what number line of the current page the program is on
curr_num_pixels = 0 # how many pixels on the current line the program is on

i = 0
last_word_ended_with_newline = False
while i < len(words):
    curr_word_num_pixels = 0
    new_word = ""
    for character in words[i]:
        curr_word_num_pixels += PIXEL_WIDTHS[character] + 1 # there is 1 pixel spacing between every character

        # if the character is a slash, quote, apostrophe, or newline, escape it for command formatting
        if character == "\\":
            new_word += "\\\\"
        elif character == '\"':
            new_word += "\\\\\""
        elif character == '\'':
            new_word += "\\\'"
        elif character == '\n':
            new_word += "\\\\n"
        else:   
            new_word += character

    # if the word was just made up of spaces, skip
    if len(new_word) == 0:
        i += 1
        continue

    curr_num_pixels += curr_word_num_pixels

    # if the number of pixels is greater than the limit for a single line or there is a newline
    if curr_num_pixels > BOOK_WIDTH or last_word_ended_with_newline:
        last_word_ended_with_newline = False # reset this

        # increment the current line and set the number of pixels at the start of that line equal to its length
        curr_line += 1
        potential_num_pixels = curr_word_num_pixels

        num_escape_characters = 0 # keep track of the number of characters that need escaping with the backslash in the word
        # in the case that the word is longer than an entire line, continue incrementing lines for its whole length
        if curr_word_num_pixels > BOOK_WIDTH:
            curr_num_pixels_in_word = 0
            j = 0
            while j < len(words[i]):
                if words[i][j] == '\\' or words[i][j] == '\"' or words[i][j] == '\'':
                    num_escape_characters += 1

                curr_num_pixels_in_word += PIXEL_WIDTHS[words[i][j]] + 1
                if curr_num_pixels_in_word > BOOK_WIDTH:
                    curr_line += 1
                    potential_num_pixels -= (curr_num_pixels_in_word - PIXEL_WIDTHS[words[i][j]] - 1)
                    curr_num_pixels_in_word = PIXEL_WIDTHS[words[i][j]] + 1

                # if the word goes over to the next page, break to save processing time
                if curr_line > BOOK_HEIGHT:
                    break

                j += 1

                # if this word takes up more than the rest of the page, write as much of it as will fit, and take that bit off
            if curr_line > BOOK_HEIGHT:
                # new_word is num_escape_characters longer than words[i] up until j
                command += new_word[:j + num_escape_characters] # don't include the current character, since that pushed the word onto the next page
                command += "\"}','{\"text\":\""
                words[i] = words[i][j:]
                curr_page += 1
                curr_line = 1
                curr_num_pixels = 0
                continue

        # if the word pushes the book to the next page, don't add the next word, don't
        # increment to the next word, and don't reset the number of pixels
        if curr_line > BOOK_HEIGHT:
            command += "\"}','{\"text\":\""
            curr_page += 1
            curr_line = 1
            curr_num_pixels = 0
            continue

        # only set the curr_num_pixels to the potential if the book isn't going to the next page
        curr_num_pixels = potential_num_pixels
    
    # add a space at the end of the word
    new_word += ' '
    curr_num_pixels += PIXEL_WIDTHS[' '] + 1
    command += new_word
    i += 1

    # whether there is a newline only matters if the book isn't going to the next page
    if new_word[-4:-1] == '\\\\n':
        last_word_ended_with_newline = True

# end the current command and write it to the file
command += "\"}'],title:\"" + title + "\",author:\"" + author + "\",display:{Lore:[\"" + lore + "\"]}}"
with open('makebook.mcfunction', 'a') as file:
    file.write(command)