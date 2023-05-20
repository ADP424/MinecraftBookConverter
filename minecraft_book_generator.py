"""
Takes a text file of Unicode characters and generates a Minecraft function file 
to be placed inside a datapack folder. This bypasses the 32,500 character limit 
inside command blocks and allows the generation of any (reasonable) length book. 

The output file can be placed inside the 'functions' folder of any data pack, or
it can be pasted right into a command block if it is fewer than 32,500 characters.

Updated as of Unicode version 15.0
Updated as of Minecraft version 1.19.4

Author: Aidan Dalgarno-Platt
"""

from pixel_widths import PIXEL_WIDTHS

# every Minecraft book page has a width of 114 pixels
BOOK_WIDTH = 114

# every Minecraft book page has a height of 14 lines
BOOK_HEIGHT = 14

# extract every space-separated word from a file given by the user
words = []
filename = input("What is the full name of the file containing your text?: ")
with open(filename, 'r', encoding='utf-8') as file:

    # add a space before and after every newline, then split by spaces
    words = file.read().replace('\n', ' \n ').split(' ')

# get the title and author of the book from the user
title = input("What is the title of the book?: ").replace('\"', '\\\"').strip()
author = input("What is the author of the book?: ").replace('\"', '\\\"').strip()

command = "give @p written_book{pages:['{\"text\":\""

curr_line = 1 # what number line of the current page the program is on
curr_num_pixels = 0 # how many pixels on the current line the program is on

# add every word to the command string
for i in range(len(words)):

    curr_word_num_pixels = 0
    new_word = ""

    # find the total pixel length of the word and generate the word to be added to the command string
    for character in words[i]:

        # if a character isn't in the dictionary, assume a pixel spacing of 9 (the max potential spacing of a character)
        # + 1 pixel because there is a 1 character spacing between characters (with a few but handleable exceptions)
        curr_word_num_pixels += PIXEL_WIDTHS.get(character, 9) + 1

        # if the character isn't in the dictionary, print which character wasn't recognized
        if character not in PIXEL_WIDTHS:
            print("Character currently unrecognized: " + character + ". Using default pixel width 9.")

        # if the character is a \, ", ', or \n, escape it for command formatting
        if character == "\\":
            new_word += "\\\\\\\\"
        elif character == '\"':
            new_word += "\\\\\""
        elif character == '\'':
            new_word += "\\\'"
        elif character == '\n':
            new_word += "\\\\n"
        else:
            new_word += character

    # if the addition of this word would make the line too long
    if curr_num_pixels + curr_word_num_pixels > BOOK_WIDTH:

        # if the word by itself is longer than a line, add it to the page piecemeal
        if curr_word_num_pixels > BOOK_WIDTH:

            # continue until every character from the word has been added
            while len(new_word) > 0:

                # if the next character will push the word onto the next line, go to the next line
                if curr_num_pixels + PIXEL_WIDTHS.get(new_word[0], 9) + 1 > BOOK_WIDTH:

                    curr_line += 1
                    curr_num_pixels = 0

                    # if the current line is off the page, go to the next page
                    if curr_line > BOOK_HEIGHT:

                        command += "\"}','{\"text\":\""
                        curr_line = 1

                # if the character is a slash, then it is the start of an escape sequence
                if new_word[0] == '\\':

                    # count the character after the slash but not the slash itself, then skip both
                    curr_num_pixels += PIXEL_WIDTHS.get(new_word[1], 9) + 1
                    command += new_word[0:2]
                    new_word = new_word[2:]

                else:

                    # add the first character from the remaining word to the command
                    curr_num_pixels += PIXEL_WIDTHS.get(new_word[0], 9) + 1
                    command += new_word[0]

                    # remove the first character from the word
                    new_word = new_word[1:]

        # go to the next line
        curr_line += 1
        curr_num_pixels = 0

    # if the current word is a newline
    if new_word == "\\\\n":

        # if the current line is the last line of the page,
        if curr_line == BOOK_HEIGHT:

            # go the next page and don't write the newline
            command += "\"}','{\"text\":\""
            curr_line = 1
            continue
        
        else:

            # go to the next line
            curr_line += 1
        
        curr_num_pixels = 0

    # if the current line is off the page,
    if curr_line > BOOK_HEIGHT:

        # go the next page
        command += "\"}','{\"text\":\""
        curr_line = 1
        curr_num_pixels = 0
        
    # add the current word to the page
    command += new_word
    curr_num_pixels += curr_word_num_pixels

    # if the word isn't made up of whitespace, add a space at the end of it
    if len(new_word.strip()) > 0:
        command += ' '
        curr_num_pixels += PIXEL_WIDTHS[' '] + 1

# end the command and write it to the file
command += "\"}'],title:\"" + title + "\",author:\"" + author + "\"}"
with open('makebook.mcfunction', 'w', encoding='utf-8') as file:
    file.write(command)