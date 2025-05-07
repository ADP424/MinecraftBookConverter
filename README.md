# MinecraftBookConverter

Converts a body of text into a Minecraft command to add a correctly-formatted book to your inventory and adds it to a .mcfunction file to be used in datapacks. Supports both pre and post-1.21.5 syntax for Minecraft commands.

## Using the Book Generator

### Installing Requirements
Run `pip install -r requirements.txt` in base or a virtual environment.


### Defining Your Book's Text
Create a blank text file and paste the body of text you want to convert to Minecraft books inside.<br>
Add `{PAGE_END}` into your text whenever you want to force the text to the next page.<br>
Add `{BOOK_END}` into your text whenever you want to start a new book.


### Defining the Parameters
This program has a number of optional command line parameters you can pass.

#### Author
- `--author`
- `-a`
- The name of the author you want the book to have.

#### Title
- `--title`
- `-t`
- The title you want the book to have.

#### Input File
- `--input`
- `-i`
- The name of the file with the document to convert (including the file extension, like `.txt`).

#### Output File
- `--output`
- `-o`
- The name of the file to output the commands to (including the file extension, like `.mcfunction`).

#### Minecraft Version
- `--minecraft-version`
- `-mcv`
- The Minecraft version to generate the commands for (like `1.21.5`)

#### In Line Titles
- `--in-line-titles`
- `-ilt`
- Pass this flag if you want the first line of each document to be considered the book title. Overrides `--title`.


### Run the Conversion
Run `python minecraft_book_converter.py` with any chosen parameters.
Copy-and-paste your command from your output file (`makebook.mcfunction` by default) or copy the .mcfunction file into your datapack.
