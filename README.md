# MinecraftBookConverter

Converts a body of text into a Minecraft command to add a correctly-formatted book to your inventory and adds it to a .mcfunction file to be used in datapacks. Supports both pre and post-1.20.5 syntax for Minecraft commands.

## Using the Book Generator

### Installing Requirements

Run `pip install -r requirements.txt` in base or a virtual environment.

### Defining Your Book's Text

Create a blank text file and paste the body of text you want to convert to a Minecraft book inside.

### Defining the Parameters

Open `PARAMETERS.py`.
Set `TEXT_FILE` to the name of the text file you created in the previous step.
Set `OUTPUT_FILE` to the name of the file you want the program to create and output the command to (typically a .mcfunction file).
Set `MC_VERSION` to the version of Minecraft you want to use the command in (in the form 1.x.x).
Set `BOOK_TITLE` to the title you want your book to have.
Set `BOOK_AUTHOR` to the name of the author you want your book to have.

### Run the Conversion

Run `python minecraft_book_converter.py`.
Copy-and-paste your command from your output file (`makebook.mcfunction` by default) or copy the .mcfunction file into your datapack.
