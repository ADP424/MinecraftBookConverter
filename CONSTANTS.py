from PARAMETERS import (
    BOOK_TITLE,
    BOOK_AUTHOR
)

# every Minecraft book page has a width of 114 pixels
BOOK_WIDTH = 114

# every Minecraft book page has a height of 14 lines
BOOK_HEIGHT = 14

# the beginning of the give command, depending on Minecraft version
COMMAND_START = {
    "1.21.0": "give @p written_book[written_book_content={pages:['",
    "1.20.5": "give @p written_book[written_book_content={pages:['[[\"",
    "1.4.2" : "give @p written_book{pages:['{\"text\":\""
}

COMMAND_NEW_PAGE = {
    "1.21.0": "','",
    "1.20.5": "\"]]','[[\"",
    "1.4.2" : "\"}','{\"text\":\""
}

COMMAND_END = {
    "1.21.0": "'],title:\"" + BOOK_TITLE + "\",author:\"" + BOOK_AUTHOR + "\"}]",
    "1.20.5": "\"]]'],title:\"" + BOOK_TITLE + "\",author:\"" + BOOK_AUTHOR + "\"}]",
    "1.4.2" : "\"}'],title:\"" + BOOK_TITLE + "\",author:\"" + BOOK_AUTHOR + "\"}"
}

ESCAPE_CHARS = {
    "1.21.0": "\\",
    "1.4.2": "\\\\",
}

PAGE_END = "{END}"