"""
Takes a text file of Unicode characters and generates a Minecraft function file 
to be placed inside a datapack folder. This bypasses the 32,500 character limit 
inside command blocks and allows the generation of any (reasonable) length book. 

The output file can be placed inside the 'functions' folder of any data pack, or
it can be pasted right into a command block if it is fewer than 32,500 characters.

Updated as of Unicode version 15.0
Updated as of Minecraft version 1.21.1

Author: Aidan Dalgarno-Platt
"""

import argparse
from packaging.version import Version

from pixel_widths import PIXEL_WIDTHS
from CONSTANTS import (
    BOOK_END,
    BOOK_WIDTH,
    BOOK_HEIGHT,
    COMMAND_START,
    COMMAND_NEW_PAGE,
    COMMAND_END,
    DEFAULT_INPUT_FILE,
    DEFAULT_MC_VERSION,
    DEFAULT_OUTPUT_FILE,
    ESCAPE_CHARS,
    PAGE_END,
)


def get_command_by_version(command_dict: dict, mc_version: str) -> str:
    """
    Get the correct syntax for the Minecraft command depending on the Minecraft version.

    Parameters
    ----------
    command_dict: {COMMAND_START, COMMAND_NEW_PAGE, COMMAND_END}
        The dictionary containing the command portion corresponding to a specific Minecraft version.

    mc_version: str
        The version of Minecraft being used for the command.

    Returns
    -------
    str
        The correct command portion corresponding to `mc_version`.
    """

    return command_dict[
        max(
            ([version for version in command_dict if Version(version) <= Version(mc_version)]), key=lambda x: Version(x)
        )
    ]


def text_to_book(text: str, title: str, author: str, mc_version: str) -> str:
    """
    Takes a body of text and converts it to a command for a single Minecraft book.

    Parameters
    ----------
    text: str
        The text to convert to a Minecraft book.

    title: str
        The title to give the Minecraft book.

    author: str
        The author to give the Minecraft book.

    Returns
    -------
    str
        The command to generate a book with the input text written in it.
    """

    # add a space before and after every newline, then split by spaces
    words = text.replace("\n", " \n ").split(" ")

    command = get_command_by_version(COMMAND_START, mc_version)

    curr_line = 1  # what number line of the current page the program is on
    curr_num_pixels = 0  # how many pixels on the current line the program is on

    # add every word to the command string
    for i in range(len(words)):

        curr_word_num_pixels = 0
        new_word = ""

        # find the total pixel length of the word and generate the word to be added to the command string
        for character in words[i]:

            # if it's the very start of a new page, don't write any newlines
            if curr_line == 1 and curr_num_pixels == 0 and character == "\n":
                continue

            # if a character isn't in the dictionary, assume a pixel spacing of 9 (the max potential spacing of a character)
            # + 1 pixel because there is a 1 character spacing between characters (with a few but handleable exceptions)
            curr_word_num_pixels += PIXEL_WIDTHS.get(character, 9) + 1

            # if the character isn't in the dictionary, print which character wasn't recognized
            if character not in PIXEL_WIDTHS:
                print("Character currently unrecognized: " + character + ". Using default pixel width 9.")

            # if the character is a \, ", ', or \n, escape it for command formatting
            if character == "\\":
                new_word += f"{get_command_by_version(ESCAPE_CHARS, mc_version)}{get_command_by_version(ESCAPE_CHARS, mc_version)}"
            elif character == '"':
                new_word += f'{get_command_by_version(ESCAPE_CHARS, mc_version)}"'
            elif character == "'":
                new_word += "\\'"
            elif character == "\n":
                new_word += f"{get_command_by_version(ESCAPE_CHARS, mc_version)}n"
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

                            command += get_command_by_version(COMMAND_NEW_PAGE, mc_version)
                            curr_line = 1

                    # if the character is a slash, then it is the start of an escape sequence
                    if new_word[0] == "\\":

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
        if new_word == f"{get_command_by_version(ESCAPE_CHARS, mc_version)}n":

            # if the current line is the last line of the page
            if curr_line == BOOK_HEIGHT:

                # go the next page and don't write the newline
                command += get_command_by_version(COMMAND_NEW_PAGE, mc_version)
                curr_line = 1
                continue

            else:

                # go to the next line
                curr_line += 1

            curr_num_pixels = 0

        # if the current line is off the page,
        if curr_line > BOOK_HEIGHT or new_word == PAGE_END:

            # go the next page
            command += get_command_by_version(COMMAND_NEW_PAGE, mc_version)
            curr_line = 1
            curr_num_pixels = 0

        # add the current word to the page
        if new_word != PAGE_END:
            command += new_word
            curr_num_pixels += curr_word_num_pixels

            # if the word isn't made up of whitespace, add a space at the end of it
            if len(new_word.strip()) > 0:
                command += " "
                curr_num_pixels += PIXEL_WIDTHS[" "] + 1

    # end the command and return it
    command += get_command_by_version(COMMAND_END, mc_version).replace("{BOOK_TITLE}", title).replace("{BOOK_AUTHOR}", author)
    return command


def text_to_many_books(
    text: str, title: str = None, author: str = None, in_line_titles: bool = False, mc_version: str = DEFAULT_MC_VERSION
) -> list[str]:
    """
    Takes a body of text and converts it to many Minecraft books.

    Parameters
    ----------
    text: str
        The text to convert to a Minecraft books.

    Returns
    -------
    str
        The commands to generate books with the input text written in it.
    """

    commands: list[str] = []
    documents = text.split(BOOK_END)

    for document in documents:
        document = document.strip()
        if in_line_titles:
            title = document[: document.index("\n")].strip()
            document = document[document.index("\n") + 1 :]
        elif title is None:
            title = ""

        if author is None:
            author = ""

        commands.append(text_to_book(document, title, author, mc_version))

    return commands


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text into Minecraft books.")

    parser.add_argument(
        "-a",
        "--author",
        default=None,
        help="The author to give the book(s).",
        dest="author",
    )
    parser.add_argument(
        "-t",
        "--title",
        default=None,
        help="The title to name the book(s).",
        dest="title",
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        help="The name of the input file with the text to convert.",
        dest="input_file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="The name of the file to output the command(s) to.",
        dest="output_file",
    )
    parser.add_argument(
        "-mcv",
        "--minecraft-version",
        default=None,
        help="The version of Minecraft (ex. 1.20.5) to generate the commands for.",
        dest="mc_version",
    )
    parser.add_argument(
        "-ilt",
        "--in-line-titles",
        action="store_true",
        help="Read the first line of each text document as the book title. Overrides --title.",
        dest="in_line_titles",
    )
    args = parser.parse_args()

    if args.input_file is None:
        input_file = DEFAULT_INPUT_FILE
    else:
        input_file = args.input_file
    if args.input_file is None:
        output_file = DEFAULT_OUTPUT_FILE
    else:
        output_file = args.output_file
    if args.mc_version is None:
        mc_version = DEFAULT_MC_VERSION
    else:
        mc_version = args.mc_version

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()
    commands = text_to_many_books(text, args.title, args.author, args.in_line_titles, mc_version)
    with open(output_file, "w", encoding="utf-8") as file:
        for command in commands:
            file.write(f"{command}\n")
