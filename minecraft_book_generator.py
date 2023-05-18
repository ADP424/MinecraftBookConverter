"""
Takes a text file and generates a Minecraft function file to be placed inside a
datapack folder. This bypasses the 32,500 character limit inside command blocks
and allows the generation of any (reasonable) length book. 

The output file can be placed inside the 'functions' folder of any data pack, or
it can be pasted right into a command block if it is fewer than 32,500 characters.

ASSUMPTIONS ABOUT INPUT TEXT:
- Made up of standard unicode characters
"""

# every page has a width of 114 pixels
BOOK_WIDTH = 114

# every page has a height of 14 lines
BOOK_HEIGHT = 14

# dictionary of character pixel widths for unicode characters
# an entry with an asterisk * next to it is not recognized by Minecraft and appears as a 5 pixel wide box
PIXEL_WIDTHS = {
    # formatting characters
    '\n': -1,
    '§': -1,

    # Basic Latin
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

    # Latin-1 Supplement
    ' ': 3,
    '¡': 1,
    '¢': 5,
    '£': 5,
    '¤': 7,
    '¥': 5,
    '¦': 1,
    '¨': 3,
    '©': 7,
    'ª': 4,
    '«': 6,
    '¬': 5,
    '­' : 3, # soft hyphen
    '®': 7,
    '¯': 5,
    '°': 4,
    '±': 5,
    '²': 4,
    '³': 4,
    '´': 2,
    'µ': 5,
    '¶': 6,
    '·': 1,
    '¸': 1,
    '¹': 3,
    'º': 4,
    '»': 6,
    '¼': 7,
    '½': 7,
    '¾': 7,
    '¿': 5,
    'À': 5,
    'Á': 5,
    'Â': 5,
    'Ã': 5,
    'Ä': 5,
    'Å': 5,
    'Æ': 9,
    'Ç': 5,
    'È': 5,
    'É': 5,
    'Ê': 5,
    'Ë': 5,
    'Ì': 3,
    'Í': 3,
    'Î': 3,
    'Ï': 3,
    'Ð': 6,
    'Ñ': 5,
    'Ò': 5,
    'Ó': 5,
    'Ô': 5,
    'Õ': 5,
    'Ö': 5,
    '×': 5,
    'Ù': 5,
    'Ú': 5,
    'Û': 5,
    'Ü': 5,
    'Ý': 5,
    'Þ': 5,
    'ß': 5,
    'à': 5,
    'á': 5,
    'â': 5,
    'ã': 5,
    'ä': 5,
    'å': 5,
    'æ': 9,
    'ç': 5,
    'è': 5,
    'é': 5,
    'ê': 5,
    'ë': 5,
    'ì': 2,
    'í': 2,
    'î': 3,
    'ï': 3,
    'ð': 5,
    'ñ': 5,
    'ò': 5,
    'ó': 5,
    'ô': 5,
    'õ': 5,
    'ö': 5,
    '÷': 5,
    'Ø': 5,
    'ù': 5,
    'ú': 5,
    'û': 5,
    'ü': 5,
    'ý': 5,
    'þ': 5,
    'ÿ': 5,

    # Latin Extended-A
    'Ā': 5,
    'ā': 5,
    'Ă': 5,
    'ă': 5,
    'Ą': 5,
    'ą': 5,
    'Ć': 5,
    'ć': 5,
    'Ĉ': 5,
    'ĉ': 5,
    'Ċ': 5,
    'ċ': 5,
    'Č': 5,
    'č': 5,
    'Ď': 5,
    'ď': 7,
    'Đ': 6,
    'đ': 6,
    'Ē': 5,
    'ē': 5,
    'Ĕ': 5,
    'ĕ': 5,
    'Ė': 5,
    'ė': 5,
    'Ę': 5,
    'ę': 5,
    'Ě': 5,
    'ě': 5,
    'Ĝ': 5,
    'ĝ': 5,
    'Ğ': 5,
    'ğ': 5,
    'Ġ': 5,
    'ġ': 5,
    'Ģ': 5,
    'ģ': 5,
    'Ĥ': 5,
    'ĥ': 5,
    'Ħ': 7,
    'ħ': 6,
    'Ĩ': 4,
    'ĩ': 4,
    'Ī': 3,
    'ī': 3,
    'Ĭ': 4,
    'ĭ': 4,
    'Į': 3,
    'į': 2,
    'İ': 3,
    'ı': 1,
    'Ĳ': 5,
    'ĳ': 4,
    'Ĵ': 5,
    'ĵ': 5,
    'Ķ': 5,
    'ķ': 4,
    'ĸ': 4,
    'Ĺ': 5,
    'ĺ': 3,
    'Ļ': 5,
    'ļ': 2,
    'Ľ': 5,
    'ľ': 3,
    'Ŀ': 5,
    'ŀ': 3,
    'Ł': 6,
    'ł': 4,
    'Ń': 5,
    'ń': 5,
    'Ņ': 5,
    'ņ': 5,
    'Ň': 5,
    'ň': 5,
    'ŉ': 7,
    'Ŋ': 5,
    'ŋ': 5,
    'Ō': 5,
    'ō': 5,
    'Ŏ': 5,
    'ŏ': 5,
    'Ő': 5,
    'ő': 5,
    'Œ': 9,
    'œ': 9,
    'Ŕ': 5,
    'ŕ': 5,
    'Ŗ': 5,
    'ŗ': 5,
    'Ř': 5,
    'ř': 5,
    'Ś': 5,
    'ś': 5,
    'Ŝ': 5,
    'ŝ': 5,
    'Ş': 5,
    'ş': 5,
    'Š': 5,
    'š': 5,
    'Ţ': 5,
    'ţ': 3,
    'Ť': 5,
    'ť': 4,
    'Ŧ': 5,
    'ŧ': 3,
    'Ũ': 5,
    'ũ': 5,
    'Ū': 5,
    'ū': 5,
    'Ŭ': 5,
    'ŭ': 5,
    'Ů': 5,
    'ů': 5,
    'Ű': 5,
    'ű': 5,
    'Ų': 5,
    'ų': 5,
    'Ŵ': 5,
    'ŵ': 5,
    'Ŷ': 5,
    'ŷ': 5,
    'Ÿ': 5,
    'Ź': 5,
    'ź': 5,
    'Ż': 5,
    'ż': 5,
    'Ž': 5,
    'ž': 5,
    'ſ': 3,

    # Latin Extended-B
    'ƀ': 6,
    'Ɓ': 7,
    'Ƃ': 5,
    'ƃ': 5,
    'Ƅ': 6,
    'ƅ': 6,
    'Ɔ': 5,
    'Ƈ': 6,
    'ƈ': 6,
    'Ɖ': 6,
    'Ɗ': 7,
    'Ƌ': 5,
    'ƌ': 5,
    'ƍ': 5,
    'Ǝ': 5,
    'Ə': 5,
    'Ɛ': 5,
    'Ƒ': 6,
    'ƒ': 5,
    'Ɠ': 6,
    'Ɣ': 5,
    'ƕ': 8,
    'Ɩ': 3,
    'Ɨ': 3,
    'Ƙ': 5,
    'ƙ': 4,
    'ƚ': 3,
    'ƛ': 5,
    'Ɯ': 5,
    'Ɲ': 6,
    'ƞ': 5,
    'Ɵ': 5,
    'Ơ': 7,
    'ơ': 7,
    'Ƣ': 7,
    'ƣ': 7,
    'Ƥ': 7,
    'ƥ': 5,
    'Ʀ': 5,
    'Ƨ': 5,
    'ƨ': 5,
    'Ʃ': 5,
    'ƪ': 5,
    'ƫ': 3,
    'Ƭ': 6,
    'ƭ': 3,
    'Ʈ': 5,
    'Ư': 7,
    'ư': 7,
    'Ʊ': 5,
    'Ʋ': 5,
    'Ƴ': 6,
    'ƴ': 7,
    'Ƶ': 5,
    'ƶ': 5,
    'Ʒ': 5,
    'Ƹ': 5,
    'ƹ': 5,
    'ƺ': 5,
    'ƻ': 5,
    'Ƽ': 5,
    'ƽ': 5,
    'ƾ': 5,
    'ƿ': 5,
    'ǀ': 5,
    'ǁ': 3,
    'ǂ': 5,
    'ǃ': 1,
    'Ǆ': 9,
    'ǅ': 9,
    'ǆ': 9,
    'Ǉ': 9,
    'ǈ': 9,
    'ǉ': 7,
    'Ǌ': 9,
    'ǋ': 9,
    'ǌ': 9,
    'Ǎ': 5,
    'ǎ': 5,
    'Ǐ': 3,
    'ǐ': 3,
    'Ǒ': 5,
    'ǒ': 5,
    'Ǔ': 5,
    'ǔ': 5,
    'Ǖ': 5,
    'ǖ': 5,
    'Ǘ': 5,
    'ǘ': 5,
    'Ǚ': 5,
    'ǚ': 5,
    'Ǜ': 5,
    'ǜ': 5,
    'ǝ': 5,
    'Ǟ': 5,
    'ǟ': 5,
    'Ǡ': 5,
    'ǡ': 5,
    'Ǣ': 9,
    'ǣ': 9,
    'Ǥ': 6,
    'ǥ': 6,
    'Ǧ': 5,
    'ǧ': 5,
    'Ǩ': 5,
    'ǩ': 4,
    'Ǫ': 5,
    'ǫ': 5,
    'Ǭ': 5,
    'ǭ': 5,
    'Ǯ': 5,
    'ǯ': 5,
    'ǰ': 5,
    'Ǳ': 9,
    'ǲ': 9,
    'ǳ': 9,
    'Ǵ': 5,
    'ǵ': 5,
    'Ƕ': 8,
    'Ƿ': 5,
    'Ǹ': 5,
    'ǹ': 5,
    'Ǻ': 5,
    'ǻ': 5,
    'Ǽ': 9,
    'ǽ': 9,
    'Ǿ': 5,
    'ǿ': 5,
    'Ȁ': 5,
    'ȁ': 5,
    'Ȃ': 5,
    'ȃ': 5,
    'Ȅ': 5,
    'ȅ': 5,
    'Ȇ': 5,
    'ȇ': 5,
    'Ȉ': 5,
    'ȉ': 5,
    'Ȋ': 4,
    'ȋ': 4,
    'Ȍ': 5,
    'ȍ': 5,
    'Ȏ': 5,
    'ȏ': 5,
    'Ȑ': 5,
    'ȑ': 5,
    'Ȓ': 5,
    'ȓ': 5,
    'Ȕ': 5,
    'ȕ': 5,
    'Ȗ': 5,
    'ȗ': 5,
    'Ș': 5,
    'ș': 5,
    'Ț': 5,
    'ț': 3,
    'Ȝ': 5,
    'ȝ': 5,
    'Ȟ': 5,
    'ȟ': 5,
    'Ƞ': 5,
    'ȡ': 7,
    'Ȣ': 5,
    'ȣ': 5,
    'Ȥ': 5,
    'ȥ': 5,
    'Ȧ': 5,
    'ȧ': 5,
    'Ȩ': 5,
    'ȩ': 5,
    'Ȫ': 5,
    'ȫ': 5,
    'Ȭ': 5,
    'ȭ': 5,
    'Ȯ': 5,
    'ȯ': 5,
    'Ȱ': 5,
    'ȱ': 5,
    'Ȳ': 5,
    'ȳ': 5,
    'ȴ': 3,
    'ȵ': 7,
    'ȶ': 4,
    'ȷ': 5,
    'ȸ': 9,
    'ȹ': 9,
    'Ⱥ': 5,
    'Ȼ': 5,
    'ȼ': 5,
    'Ƚ': 6,
    'Ⱦ': 5,
    'ȿ': 5,
    'ɀ': 5,
    'Ɂ': 5,
    'ɂ': 5,
    'Ƀ': 6,
    'Ʉ': 7,
    'Ʌ': 5,
    'Ɇ': 5,
    'ɇ': 6,
    'Ɉ': 6,
    'ɉ': 6,
    'Ɋ': 6,
    'ɋ': 6,
    'Ɍ': 6,
    'ɍ': 6,
    'Ɏ': 7,
    'ɏ': 7,

    # Latin Extended Additional
    'Ḁ': 5,
    'ḁ': 5,
    'Ḃ': 5,
    'ḃ': 5,
    'Ḅ': 5,
    'ḅ': 5,
    'Ḇ': 5,
    'ḇ': 5,
    'Ḉ': 5,
    'ḉ': 5,
    'Ḋ': 5,
    'ḋ': 5,
    'Ḍ': 5,
    'ḍ': 5,
    'Ḏ': 5,
    'ḏ': 5,
    'Ḑ': 5,
    'ḑ': 5,
    'Ḓ': 5,
    'ḓ': 5,
    'Ḕ': 5,
    'ḕ': 5,
    'Ḗ': 5,
    'ḗ': 5,
    'Ḙ': 5,
    'ḙ': 5,
    'Ḛ': 5,
    'ḛ': 5,
    'Ḝ': 5,
    'ḝ': 5,
    'Ḟ': 5,
    'ḟ': 4,
    'Ḡ': 5,
    'ḡ': 5,
    'Ḣ': 5,
    'ḣ': 5,
    'Ḥ': 5,
    'ḥ': 5,
    'Ḧ': 5,
    'ḧ': 5,
    'Ḩ': 5,
    'ḩ': 5,
    'Ḫ': 5,
    'ḫ': 5,
    'Ḭ': 4,
    'ḭ': 4,
    'Ḯ': 3,
    'ḯ': 3,
    'Ḱ': 5,
    'ḱ': 4,
    'Ḳ': 5,
    'ḳ': 4,
    'Ḵ': 5,
    'ḵ': 4,
    'Ḷ': 5,
    'ḷ': 2,
    'Ḹ': 5,
    'ḹ': 3,
    'Ḻ': 5,
    'ḻ': 3,
    'Ḽ': 5,
    'ḽ': 3,
    'Ḿ': 5,
    'ḿ': 5,
    'Ṁ': 5,
    'ṁ': 5,
    'Ṃ': 5,
    'ṃ': 5,
    'Ṅ': 5,
    'ṅ': 5,
    'Ṇ': 5,
    'ṇ': 5,
    'Ṉ': 5,
    'ṉ': 5,
    'Ṋ': 5,
    'ṋ': 5,
    'Ṍ': 5,
    'ṍ': 5,
    'Ṏ': 5,
    'ṏ': 5,
    'Ṑ': 5,
    'ṑ': 5,
    'Ṓ': 5,
    'ṓ': 5,
    'Ṕ': 5,
    'ṕ': 5,
    'Ṗ': 5,
    'ṗ': 5,
    'Ṙ': 5,
    'ṙ': 5,
    'Ṛ': 5,
    'ṛ': 5,
    'Ṝ': 5,
    'ṝ': 5,
    'Ṟ': 5,
    'ṟ': 5,
    'Ṡ': 5,
    'ṡ': 5,
    'Ṣ': 5,
    'ṣ': 5,
    'Ṥ': 5,
    'ṥ': 5,
    'Ṧ': 5,
    'ṧ': 5,
    'Ṩ': 5,
    'ṩ': 5,
    'Ṫ': 5,
    'ṫ': 3,
    'Ṭ': 5,
    'ṭ': 3,
    'Ṯ': 5,
    'ṯ': 3,
    'Ṱ': 5,
    'ṱ': 3,
    'Ṳ': 5,
    'ṳ': 5,
    'Ṵ': 5,
    'ṵ': 5,
    'Ṷ': 5,
    'ṷ': 5,
    'Ṹ': 5,
    'ṹ': 5,
    'Ṻ': 5,
    'ṻ': 5,
    'Ṽ': 5,
    'ṽ': 5,
    'Ṿ': 5,
    'ṿ': 5,
    'Ẁ': 5,
    'ẁ': 5,
    'Ẃ': 5,
    'ẃ': 5,
    'Ẅ': 5,
    'ẅ': 5,
    'Ẇ': 5,
    'ẇ': 5,
    'Ẉ': 5,
    'ẉ': 5,
    'Ẋ': 5,
    'ẋ': 5,
    'Ẍ': 5,
    'ẍ': 5,
    'Ẏ': 5,
    'ẏ': 5,
    'Ẑ': 5,
    'ẑ': 5,
    'Ẓ': 5,
    'ẓ': 5,
    'Ẕ': 5,
    'ẕ': 5,
    'ẖ': 5,
    'ẗ': 3,
    'ẘ': 5,
    'ẙ': 5,
    'ẚ': 5,
    'ẛ': 3,
    'ẜ': 4,
    'ẝ': 4,
    'ẞ': 5,
    'ẟ': 5,
    'Ạ': 5,
    'ạ': 5,
    'Ả': 5,
    'ả': 5,
    'Ấ': 5,
    'ấ': 5,
    'Ầ': 5,
    'ầ': 5,
    'Ẩ': 5,
    'ẩ': 5,
    'Ẫ': 5,
    'ẫ': 5,
    'Ậ': 5,
    'ậ': 5,
    'Ắ': 5,
    'ắ': 5,
    'Ằ': 5,
    'ằ': 5,
    'Ẳ': 5,
    'ẳ': 5,
    'Ẵ': 5,
    'ẵ': 5,
    'Ặ': 5,
    'ặ': 5,
    'Ẹ': 5,
    'ẹ': 5,
    'Ẻ': 5,
    'ẻ': 5,
    'Ẽ': 5,
    'ẽ': 5,
    'Ế': 5,
    'ế': 5,
    'Ề': 5,
    'ề': 5,
    'Ể': 5,
    'ể': 5,
    'Ễ': 5,
    'ễ': 5,
    'Ệ': 5,
    'ệ': 5,
    'Ỉ': 3,
    'ỉ': 3,
    'Ị': 3,
    'ị': 1,
    'Ọ': 5,
    'ọ': 5,
    'Ỏ': 5,
    'ỏ': 5,
    'Ố': 5,
    'ố': 5,
    'Ồ': 5,
    'ồ': 5,
    'Ổ': 5,
    'ổ': 5,
    'Ỗ': 5,
    'ỗ': 5,
    'Ộ': 5,
    'ộ': 5,
    'Ớ': 7,
    'ớ': 7,
    'Ờ': 7,
    'ờ': 7,
    'Ở': 7,
    'ở': 7,
    'Ỡ': 7,
    'ỡ': 7,
    'Ợ': 7,
    'ợ': 7,
    'Ụ': 5,
    'ụ': 5,
    'Ủ': 5,
    'ủ': 5,
    'Ứ': 7,
    'ứ': 7,
    'Ừ': 7,
    'ừ': 7,
    'Ử': 7,
    'ử': 7,
    'Ữ': 7,
    'ữ': 7,
    'Ự': 7,
    'ự': 7,
    'Ỳ': 5,
    'ỳ': 5,
    'Ỵ': 5,
    'ỵ': 5,
    'Ỷ': 5,
    'ỷ': 5,
    'Ỹ': 5,
    'ỹ': 5,
    'Ỻ': 7,
    'ỻ': 6,
    'Ỽ': 5,
    'ỽ': 4,
    'Ỿ': 5,
    'ỿ': 6,
    
    # Latin Extended-C
    'Ⱡ': 3,
    'ⱡ': 2,
    'Ɫ': 7,
    'Ᵽ': 3,
    'Ɽ': 3,
    'ⱥ': 6,
    'ⱦ': 5,
    'Ⱨ': 3,
    'ⱨ': 3,
    'Ⱪ': 3,
    'ⱪ': 3,
    'Ⱬ': 3,
    'ⱬ': 3,
    'Ɑ': 5,
    'Ɱ': 3,
    'Ɐ': 5,
    'Ɒ': 5,
    'ⱱ': 7,
    'Ⱳ': 3,
    'ⱳ': 3,
    'ⱴ': 3,
    'Ⱶ': 2,
    'ⱶ': 2,
    'ⱷ': 3,
    'ⱸ': 3,
    'ⱹ': 3,
    'ⱺ': 3,
    'ⱻ': 3,
    'ⱼ': 1,
    'ⱽ': 2,
    'Ȿ': 5,
    'Ɀ': 5,

    # Latin Extended-D
    '꜠': 3,
    '꜡': 3,
    'Ꜣ': 2,
    'ꜣ': 2,
    'Ꜥ': 3,
    'ꜥ': 2,
    'Ꜧ': 5,
    'ꜧ': 5,
    'Ꜩ': 7,
    'ꜩ': 6,
    'Ꜫ': 3,
    'ꜫ': 2,
    'Ꜭ': 2,
    'ꜭ': 2,
    'Ꜯ': 4,
    'ꜯ': 4,
    'ꜰ': 5,
    'ꜱ': 5,
    'Ꜳ': 9,
    'ꜳ': 9,
    'Ꜵ': 9,
    'ꜵ': 9,
    'Ꜷ': 9,
    'ꜷ': 9,
    'Ꜹ': 9,
    'ꜹ': 8,
    'Ꜻ': 9,
    'ꜻ': 8,
    'Ꜽ': 9,
    'ꜽ': 8,
    'Ꜿ': 5,
    'ꜿ': 5,
    'Ꝁ': 3,
    'ꝁ': 3,
    'Ꝃ': 3,
    'ꝃ': 3,
    'Ꝅ': 3,
    'ꝅ': 3,
    'Ꝇ': 3,
    'ꝇ': 2,
    'Ꝉ': 2,
    'ꝉ': 2,
    'Ꝋ': 4,
    'ꝋ': 4,
    'Ꝍ': 4,
    'ꝍ': 4,
    'Ꝏ': 9,
    'ꝏ': 9,
    'Ꝑ': 3,
    'ꝑ': 3,
    'Ꝓ': 4,
    'ꝓ': 4,
    'Ꝕ': 4,
    'ꝕ': 4,
    'Ꝗ': 3,
    'ꝗ': 3,
    'Ꝙ': 5,
    'ꝙ': 5,
    'Ꝛ': 5,
    'ꝛ': 4,
    'Ꝝ': 3,
    'ꝝ': 3,
    'Ꝟ': 4,
    'ꝟ': 3,
    'Ꝡ': 5,
    'ꝡ': 5,
    'Ꝣ': 3,
    'ꝣ': 2,
    'Ꝥ': 3,
    'ꝥ': 3,
    'Ꝧ': 3,
    'ꝧ': 3,
    'Ꝩ': 2,
    'ꝩ': 2,
    'Ꝫ': 2,
    'ꝫ': 2,
    'Ꝭ': 3,
    'ꝭ': 3,
    'Ꝯ': 3,
    'ꝯ': 3,
    'ꝰ': 3,
    'ꝱ': 6,
    'ꝲ': 5,
    'ꝳ': 6,
    'ꝴ': 6,
    'ꝵ': 4,
    'ꝶ': 6,
    'ꝷ': 5,
    'ꝸ': 3,
    'Ꝺ': 5,
    'ꝺ': 3,
    'Ꝼ': 3,
    'ꝼ': 2,
    'Ᵹ': 3,
    'Ꝿ': 3,
    'ꝿ': 3,
    'Ꞁ': 5,
    'ꞁ': 2,
    'Ꞃ': 3,
    'ꞃ': 3,
    'Ꞅ': 2,
    'ꞅ': 2,
    'Ꞇ': 3,
    'ꞇ': 3,
    'ꞈ': 3,
    '꞉': 1,
    '꞊': 2,
    'Ꞌ': 0,
    'ꞌ': 0,
    'Ɥ': 5, # *
    'ꞎ': 5, # *
    'ꞏ': 5, # *
    'Ꞑ': 5, # *
    'ꞑ': 5, # *
    'Ꞓ': 5, # *
    'ꞓ': 5, # *
    'ꞔ': 5,
    'ꞕ': 6,
    'Ꞗ': 5, # *
    'ꞗ': 5, # *
    'Ꞙ': 5, # *
    'ꞙ': 5, # *
    'Ꞛ': 5, # *
    'ꞛ': 5, # *
    'Ꞝ': 5, # *
    'ꞝ': 5, # *
    'Ꞟ': 5, # *
    'ꞟ': 5, # *
    'Ꞡ': 5, # *
    'ꞡ': 5, # *
    'Ꞣ': 5, # *
    'ꞣ': 5, # *
    'Ꞥ': 5, # *
    'ꞥ': 5, # *
    'Ꞧ': 5, # *
    'ꞧ': 5, # *
    'Ꞩ': 6,
    'ꞩ': 5,
    'Ɦ': 5, # *
    'Ɜ': 5, # *
    'Ɡ': 5, # *
    'Ɬ': 5, # *
    'Ɪ': 5, # *
    'ꞯ': 5,
    'Ʞ': 3,
    'Ʇ': 5, # *
    'Ʝ': 5, # *
    'Ꭓ': 5, # *
    'Ꞵ': 5, # *
    'ꞵ': 5, # *
    'Ꞷ': 5, # *
    'ꞷ': 5, # *
    'Ꞹ': 5, # *
    'ꞹ': 5, # *
    'Ꞻ': 5, # *
    'ꞻ': 5, # *
    'Ꞽ': 5, # *
    'ꞽ': 5, # *
    'Ꞿ': 5, # *
    'ꞿ': 5, # *
    'Ꟁ': 5, # *
    'ꟁ': 5, # *
    'Ꟃ': 5, # *
    'ꟃ': 5, # *
    'Ꞔ': 5,
    'Ʂ': 5, # *
    'Ᶎ': 6,
    'Ꟈ': 5, # *
    'ꟈ': 5, # *
    'Ꟊ': 5, # *
    'ꟊ': 5, # *
    'Ꟑ': 5, # *
    'ꟑ': 5, # *
    'ꟓ': 5, # *
    'ꟕ': 5, # *
    'Ꟗ': 5, # *
    'ꟗ': 5, # *
    'Ꟙ': 5, # *
    'ꟙ': 5, # *
    'ꟲ': 5, # *
    'ꟳ': 5, # *
    'ꟴ': 5, # *
    'Ꟶ': 5, # *
    'ꟶ': 5, # *
    'ꟷ': 5, # *
    'ꟸ': 5, # *
    'ꟹ': 5, # *
    'ꟺ': 5, # *
    'ꟻ': 3,
    'ꟼ': 3,
    'ꟽ': 3,
    'ꟾ': 2,
    'ꟿ': 8,

    # Latin Extended-E
    'ꬰ': 5, # *
    'ꬱ': 5, # *
    'ꬲ': 5, # *
    'ꬳ': 5, # *
    'ꬴ': 5, # *
    'ꬵ': 5, # *
    'ꬶ': 5, # *
    'ꬷ': 5, # *
    'ꬸ': 5, # *
    'ꬹ': 5, # *
    'ꬺ': 5, # *
    'ꬻ': 5, # *
    'ꬼ': 5, # *
    'ꬽ': 5, # *
    'ꬾ': 5, # *
    'ꬿ': 5, # *
    'ꭀ': 5, # *
    'ꭁ': 5, # *
    'ꭂ': 5, # *
    'ꭃ': 5, # *
    'ꭄ': 5, # *
    'ꭅ': 5, # *
    'ꭆ': 5, # *
    'ꭇ': 5, # *
    'ꭈ': 5, # *
    'ꭉ': 5, # *
    'ꭊ': 5, # *
    'ꭋ': 5, # *
    'ꭌ': 5, # *
    'ꭍ': 5, # *
    'ꭎ': 5, # *
    'ꭏ': 5, # *
    'ꭐ': 5,
    'ꭑ': 5,
    'ꭒ': 5, # *
    'ꭓ': 5, # *
    'ꭔ': 5, # *
    'ꭕ': 5, # *
    'ꭖ': 5, # *
    'ꭗ': 5, # *
    'ꭘ': 5, # *
    'ꭙ': 5, # *
    'ꭚ': 5, # *
    '꭛': 5, # *
    'ꭜ': 5, # *
    'ꭝ': 5, # *
    'ꭞ': 5, # *
    'ꭟ': 5, # *
    'ꭠ': 5, # *
    'ꭡ': 5, # *
    'ꭢ': 5, # *
    'ꭣ': 9,
    'ꭤ': 5, # *
    'ꭥ': 5, # *
    'ꭦ': 5, # *
    'ꭧ': 5, # *
    'ꭨ': 5, # *
    'ꭩ': 5, # *
    '꭪': 5, # *
    '꭫': 5, # *

    # Latin Extended-F
    '𐞀': 5, # *
    '𐞁': 5, # *
    '𐞂': 5, # *
    '𐞃': 5, # *
    '𐞄': 5, # *
    '𐞅': 5, # *
    '𐞇': 5, # *
    '𐞈': 5, # *
    '𐞉': 5, # *
    '𐞊': 5, # *
    '𐞋': 5, # *
    '𐞌': 5, # *
    '𐞍': 5, # *
    '𐞎': 5, # *
    '𐞏': 5, # *
    '𐞐': 5, # *
    '𐞑': 5, # *
    '𐞒': 5, # *
    '𐞓': 5, # *
    '𐞔': 5, # *
    '𐞕': 5, # *
    '𐞖': 5, # *
    '𐞗': 5, # *
    '𐞘': 5, # *
    '𐞙': 5, # *
    '𐞚': 5, # *
    '𐞛': 5, # *
    '𐞜': 5, # *
    '𐞝': 5, # *
    '𐞞': 5, # *
    '𐞟': 5, # *
    '𐞠': 5, # *
    '𐞡': 5, # *
    '𐞢': 5, # *
    '𐞣': 5, # *
    '𐞤': 5, # *
    '𐞥': 5, # *
    '𐞦': 5, # *
    '𐞧': 5, # *
    '𐞨': 5, # *
    '𐞩': 5, # *
    '𐞪': 5, # *
    '𐞫': 5, # *
    '𐞬': 5, # *
    '𐞭': 5, # *
    '𐞮': 5, # *
    '𐞯': 5, # *
    '𐞰': 5, # *
    '𐞲': 5, # *
    '𐞳': 5, # *
    '𐞴': 5, # *
    '𐞵': 5, # *
    '𐞶': 5, # *
    '𐞷': 5, # *
    '𐞸': 5, # *
    '𐞹': 5, # *
    '𐞺': 5, # *

    # Latin Extended-G
    '𝼀': 5, # *
    '𝼁': 5, # *
    '𝼂': 5, # *
    '𝼃': 5, # *
    '𝼄': 5, # *
    '𝼅': 5, # *
    '𝼆': 5, # *
    '𝼇': 5, # *
    '𝼈': 5, # *
    '𝼉': 5, # *
    '𝼊': 5, # *
    '𝼋': 5, # *
    '𝼌': 5, # *
    '𝼍': 5, # *
    '𝼎': 5, # *
    '𝼏': 5, # *
    '𝼐': 5, # *
    '𝼑': 5, # *
    '𝼒': 5, # *
    '𝼓': 5, # *
    '𝼔': 5, # *
    '𝼕': 5, # *
    '𝼖': 5, # *
    '𝼗': 5, # *
    '𝼘': 5, # *
    '𝼙': 5, # *
    '𝼚': 5, # *
    '𝼛': 5, # *
    '𝼜': 5, # *
    '𝼝': 5, # *
    '𝼞': 5, # *
    '𝼥': 5, # *
    '𝼦': 5, # *
    '𝼧': 5, # *
    '𝼨': 5, # *
    '𝼩': 5, # *
    '𝼪': 5, # *

    # IPA (International Phonetic Alphabet) Extensions
    'ɐ': 5,
    'ɑ': 5,
    'ɒ': 5,
    'ɓ': 5,
    'ɔ': 5,
    'ɕ': 5,
    'ɖ': 6,
    'ɗ': 6,
    'ɘ': 5,
    'ə': 5,
    'ɚ': 7,
    'ɛ': 5,
    'ɜ': 5,
    'ɝ': 7,
    'ɞ': 5,
    'ɟ': 4,
    'ɠ': 6,
    'ɡ': 5,
    'ɢ': 5,
    'ɣ': 5,
    'ɤ': 5,
    'ɥ': 5,
    'ɦ': 5,
    'ɧ': 5,
    'ɨ': 3,
    'ɩ': 2,
    'ɪ': 3,
    'ɫ': 5,
    'ɬ': 4,
    'ɭ': 2,
    'ɮ': 5,
    'ɯ': 5,
    'ɰ': 5,
    'ɱ': 5,
    'ɲ': 6,
    'ɴ': 5,
    'ɵ': 5,
    'ɶ': 9,
    'ɷ': 7,
    'ɸ': 5,
    'ɹ': 5,
    'ɺ': 5,
    'ɻ': 6,
    'ɼ': 5,
    'ɽ': 5,
    'ɾ': 5,
    'ɿ': 5,
    'ʀ': 5,
    'ʁ': 5,
    'ʂ': 5,
    'ʃ': 5,
    'ʄ': 6,
    'ʅ': 5,
    'ʆ': 6,
    'ʇ': 3,
    'ʈ': 3,
    'ʉ': 7,
    'ʊ': 5,
    'ʋ': 5,
    'ʌ': 5,
    'ʍ': 5,
    'ʎ': 5,
    'ʏ': 5,
    'ʐ': 6,
    'ʑ': 5,
    'ʒ': 5,
    'ʓ': 5,
    'ʔ': 5,
    'ʕ': 5,
    'ʖ': 5,
    'ʗ': 5,
    'ʘ': 5,
    'ʙ': 5,
    'ʚ': 5,
    'ʛ': 6,
    'ʜ': 5,
    'ʝ': 5,
    'ʞ': 4,
    'ʟ': 5,
    'ʠ': 6,
    'ʡ': 5,
    'ʢ': 5,
    'ʣ': 9,
    'ʤ': 9,
    'ʥ': 9,
    'ʦ': 8,
    'ʧ': 7,
    'ʨ': 8,
    'ʩ': 9,
    'ʪ': 7,
    'ʫ': 7,
    'ʬ': 5,
    'ʭ': 5,
    'ʮ': 6,
    'ʯ': 7,

    # Spacing Modifier Letters
    'ʰ': 2,
    'ʱ': 2,
    'ʲ': 2,
    'ʳ': 2,
    'ʴ': 2,
    'ʵ': 3,
    'ʶ': 2,
    'ʷ': 2,
    'ʸ': 2,
    'ʹ': 1,
    'ʺ': 3,
    'ʻ': 1,
    'ʼ': 1,
    'ʽ': 1,
    'ʾ': 2,
    'ʿ': 2,
    'ˀ': 3,
    'ˁ': 3,
    '˂': 2,
    '˃': 2,
    '˄': 3,
    '˅': 3,
    'ˆ': 2,
    'ˇ': 2,
    'ˈ': 0,
    'ˉ': 2,
    'ˊ': 2,
    'ˋ': 2,
    'ˌ': 1,
    'ˍ': 2,
    'ˎ': 2,
    'ˏ': 2,
    'ː': 1,
    'ˑ': 1,
    '˒': 2,
    '˓': 2,
    '˔': 2,
    '˕': 2,
    '˖': 2,
    '˗': 2,
    '˘': 3,
    '˙': 1,
    '˚': 2,
    '˛': 1,
    '˜': 3,
    '˝': 3,
    '˞' : 3,
    '˟': 3,
    'ˠ': 2,
    'ˡ': 1,
    'ˢ': 2,
    'ˣ': 2,
    'ˤ': 2,
    '˥': 2,
    '˦': 2,
    '˧': 2,
    '˨': 2,
    '˩': 2,
    '˪': 2,
    '˫': 2,
    'ˬ': 2,
    '˭': 3,
    'ˮ': 3,
    '˯': 2,
    '˰': 2,
    '˱': 1,
    '˲': 1,
    '˳': 2,
    '˴': 1,
    '˵': 3,
    '˶': 3,
    '˷': 3,
    '˸': 1,
    '˹': 1,
    '˺': 1,
    '˻': 1,
    '˼': 1,
    '˽': 3,
    '˾': 3,
    '˿': 3,

    # Phonetic Extensions
    'ᴀ': 5,
    'ᴁ': 3,
    'ᴂ': 9,
    'ᴃ': 3,
    'ᴄ': 5,
    'ᴅ': 5,
    'ᴆ': 3,
    'ᴇ': 5,
    'ᴈ': 3,
    'ᴉ': 1,
    'ᴊ': 5,
    'ᴋ': 5,
    'ᴌ': 3,
    'ᴍ': 5,
    'ᴎ': 2,
    'ᴏ': 5,
    'ᴐ': 3,
    'ᴑ': 3,
    'ᴒ': 3,
    'ᴓ': 3,
    'ᴔ': 9,
    'ᴕ': 2,
    'ᴖ': 2,
    'ᴗ': 2,
    'ᴘ': 5,
    'ᴙ': 3,
    'ᴚ': 5,
    'ᴛ': 5,
    'ᴜ': 5,
    'ᴝ': 3,
    'ᴞ': 3,
    'ᴟ': 3,
    'ᴠ': 5,
    'ᴡ': 5,
    'ᴢ': 5,
    'ᴣ': 3,
    'ᴤ': 3,
    'ᴥ': 3,
    'ᴦ': 3,
    'ᴧ': 3,
    'ᴨ': 3,
    'ᴩ': 3,
    'ᴪ': 3,
    'ᴫ': 3,
    'ᴬ': 2,
    'ᴭ': 3,
    'ᴮ': 2,
    'ᴯ': 3,
    'ᴰ': 2,
    'ᴱ': 2,
    'ᴲ': 2,
    'ᴳ': 3,
    'ᴴ': 3,
    'ᴵ': 2,
    'ᴶ': 2,
    'ᴷ': 2,
    'ᴸ': 2,
    'ᴹ': 2,
    'ᴺ': 2,
    'ᴻ': 2,
    'ᴼ': 3,
    'ᴽ': 2,
    'ᴾ': 3,
    'ᴿ': 3,
    'ᵀ': 3,
    'ᵁ': 3,
    'ᵂ': 3,
    'ᵃ': 3,
    'ᵄ': 3,
    'ᵅ': 3,
    'ᵆ': 3,
    'ᵇ': 2,
    'ᵈ': 2,
    'ᵉ': 3,
    'ᵊ': 3,
    'ᵋ': 3,
    'ᵌ': 3,
    'ᵍ': 3,
    'ᵎ': 2,
    'ᵏ': 2,
    'ᵐ': 3,
    'ᵑ': 3,
    'ᵒ': 3,
    'ᵓ': 3,
    'ᵔ': 2,
    'ᵕ': 2,
    'ᵖ': 3,
    'ᵗ': 2,
    'ᵘ': 3,
    'ᵙ': 3,
    'ᵚ': 3,
    'ᵛ': 3,
    'ᵜ': 3,
    'ᵝ': 3,
    'ᵞ': 3,
    'ᵟ': 3,
    'ᵠ': 3,
    'ᵡ': 3,
    'ᵢ': 2,
    'ᵣ': 3,
    'ᵤ': 3,
    'ᵥ': 3,
    'ᵦ': 3,
    'ᵧ': 3,
    'ᵨ': 2,
    'ᵩ': 3,
    'ᵪ': 3,
    'ᵫ': 9,
    'ᵬ': 7,
    'ᵭ': 7,
    'ᵮ': 5,
    'ᵯ': 7,
    'ᵰ': 7,
    'ᵱ': 7,
    'ᵲ': 7,
    'ᵳ': 7,
    'ᵴ': 7,
    'ᵵ': 5,
    'ᵶ': 5,
    'ᵷ': 5,
    'ᵸ': 3,
    'ᵹ': 3,
    'ᵺ': 8,
    'ᵻ': 2,
    'ᵼ': 2,
    'ᵽ': 3,
    'ᵾ': 3,
    'ᵿ': 3,

    # Phonetic Extensions Supplement
    'ᶀ': 5,
    'ᶁ': 6,
    'ᶂ': 4,
    'ᶃ': 6,
    'ᶄ': 5,
    'ᶅ': 2,
    'ᶆ': 6,
    'ᶇ': 6,
    'ᶈ': 5,
    'ᶉ': 5,
    'ᶊ': 5,
    'ᶋ': 5,
    'ᶌ': 5,
    'ᶍ': 6,
    'ᶎ': 6,
    'ᶏ': 6,
    'ᶐ': 6,
    'ᶑ': 6,
    'ᶒ': 6,
    'ᶓ': 6,
    'ᶔ': 5,
    'ᶕ': 6,
    'ᶖ': 2,
    'ᶗ': 6,
    'ᶘ': 5,
    'ᶙ': 6,
    'ᶚ': 5,
    'ᶛ': 3,
    'ᶜ': 2,
    'ᶝ': 2,
    'ᶞ': 2,
    'ᶟ': 2,
    'ᶠ': 2,
    'ᶡ': 2,
    'ᶢ': 2,
    'ᶣ': 2,
    'ᶤ': 2,
    'ᶥ': 2,
    'ᶦ': 2,
    'ᶧ': 2,
    'ᶨ': 3,
    'ᶩ': 2,
    'ᶪ': 1,
    'ᶫ': 2,
    'ᶬ': 3,
    'ᶭ': 3,
    'ᶮ': 3,
    'ᶯ': 3,
    'ᶰ': 2,
    'ᶱ': 3,
    'ᶲ': 2,
    'ᶳ': 2,
    'ᶴ': 2,
    'ᶵ': 3,
    'ᶶ': 3,
    'ᶷ': 3,
    'ᶸ': 2,
    'ᶹ': 3,
    'ᶺ': 2,
    'ᶻ': 2,
    'ᶼ': 3,
    'ᶽ': 3,
    'ᶾ': 3,
    'ᶿ': 2,

    # Combining Marks
    '̀' : 3,
    '́' : 3,
    '̂' : 3,
    '̃' : 3,
    '̄' : 3,
    '̅' : 4,
    '̆' : 3,
    '̇' : 3,
    '̈' : 3,
    '̉' : 3,
    '̊' : 3,
    '̋' : 3,
    '̌' : 3,
    '̍' : 3,
    '̎' : 3,
    '̏' : 3,
    '̐' : 3,
    '̑' : 3,
    '̒': 3,
    '̓' : 3,
    '' : 3,
    '̔' : 3,
    '̕' : 3,
    '̖' : 3,
    '̗' : 3,
    '̘' : 3,
    '̙' : 3,
    '̚' : 3,
    '̛' : 3,
    '̜' : 3,
    '̝' : 3,
    '̞' : 3,
    '̟' : 3,
    '̠' : 3,
    '̡' : 3,
    '̢' : 3,
    '̣' : 3,
    '̤' : 3,
    '̥' : 3,
    '̦' : 3,
    '̧' : 2,
    '̨' : 3,
    '̩' : 3,
    '̪' : 3,
    '̫' : 3,
    '̬' : 3,
    '̭' : 3,
    '̮' : 3,
    '̯' : 3,
    '̰' : 3,
    '̱' : 3,
    '̲' : 4,
    '̳' : 4,
    '̴' : 3,
    '̵' : 3,
    '̶' : 4,
    '̷' : 3,
    '̸' : 4,
    '̹' : 3,
    '̺' : 3,
    '̻' : 3,
    '̼' : 3,
    '̽' : 3,
    '̾' : 3,
    '̿' : 4,
    '̀' : 3,
    '́' : 3,
    '͂' : 3,
    '̓' : 3,
    '̈́' : 3,
    'ͅ' : 3,
    '͆' : 3,
    '͇' : 3,
    '͈' : 3,
    '͉' : 3,
    '͊' : 3,
    '͋' : 3,
    '͌' : 3,
    '͍' : 3,
    '͎' : 3,
    '͏' : 8, # combining grapheme joiner
    '͐' : 3,
    '͑' : 3,
    '͒' : 3,
    '͓' : 3,
    '͔' : 3,
    '͕' : 3,
    '͖' : 4,
    '͗' : 3,
    '͘' : 3,
    '͙' : 3,
    '͚' : 3,
    '͛' : 3,
    '͜' : 4,
    '͝' : 4,
    '͞' : 4,
    '͟' : 4,
    '͠' : 4,
    '͡' : 4,
    '͢' : 4,
    'ͣ' : 3,
    'ͤ' : 3,
    'ͥ' : 3,
    'ͦ' : 3,
    'ͧ' : 3,
    'ͨ' : 3,
    'ͩ' : 3,
    'ͪ' : 3,
    'ͫ' : 3,
    'ͬ' : 3,
    'ͭ' : 3,
    'ͮ' : 3,
    'ͯ' : 3,

    # Greek and Coptic
    'Ͱ': 2,
    'ͱ': 3,
    'Ͳ': 3,
    'ͳ': 2,
    'ʹ': 1,
    '͵': 2,
    'Ͷ': 3,
    'ͷ': 3,
    'ͺ': 1,
    'ͻ': 3,
    'ͼ': 3,
    'ͽ': 3,
    ';': 1,
    'Ϳ': 5, # *
    '΄': 0,
    '΅': 2,
    'Ά': 7,
    '·': 1,
    'Έ': 7,
    'Ή': 7,
    'Ί': 5,
    'Ό': 7,
    'Ύ': 7,
    'Ώ': 7,
    'ΐ': 5,
    'Α': 5,
    'Β': 5,
    'Γ': 5,
    'Δ': 5,
    'Ε': 5,
    'Ζ': 5,
    'Η': 5,
    'Θ': 5,
    'Ι': 3,
    'Κ': 5,
    'Λ': 5,
    'Μ': 5,
    'Ν': 5,
    'Ξ': 5,
    'Ο': 5,
    'Π': 5,
    'Ρ': 5,
    'Σ': 5,
    'Τ': 5,
    'Υ': 5,
    'Φ': 5,
    'Χ': 5,
    'Ψ': 5,
    'Ω': 5,
    'Ϊ': 3,
    'Ϋ': 5,
    'ά': 5,
    'έ': 5,
    'ή': 5,
    'ί': 2,
    'ΰ': 5,
    'α': 5,
    'β': 5,
    'γ': 5,
    'δ': 5,
    'ε': 5,
    'ζ': 5,
    'η': 5,
    'θ': 5,
    'ι': 2,
    'κ': 4,
    'λ': 5,
    'μ': 5,
    'ν': 5,
    'ξ': 5,
    'ο': 5,
    'π': 5,
    'ρ': 5,
    'ς': 5,
    'σ': 6,
    'τ': 5,
    'υ': 5,
    'φ': 5,
    'χ': 5,
    'ψ': 5,
    'ω': 7,
    'ϊ': 3,
    'ϋ': 5,
    'ό': 5,
    'ύ': 5,
    'ώ': 7,
    'Ϗ': 3,
    'ϐ': 3,
    'ϑ': 3,
    'ϒ': 3,
    'ϓ': 9,
    'ϔ': 6,
    'ϕ': 3,
    'ϖ': 3,
    'ϗ': 3,
    'Ϙ': 3,
    'ϙ': 3,
    'Ϛ': 3,
    'ϛ': 5,
    'Ϝ': 3,
    'ϝ': 2,
    'Ϟ': 3,
    'ϟ': 2,
    'Ϡ': 3,
    'ϡ': 2,
    'Ϣ': 4,
    'ϣ': 3,
    'Ϥ': 3,
    'ϥ': 2,
    'Ϧ': 3,
    'ϧ': 3,
    'Ϩ': 3,
    'ϩ': 3,
    'Ϫ': 4,
    'ϫ': 3,
    'Ϭ': 3,
    'ϭ': 3,
    'Ϯ': 3,
    'ϯ': 3,
    'ϰ': 3,
    'ϱ': 3,
    'ϲ': 3,
    'ϳ': 2,
    'ϴ': 3,
    'ϵ': 2,
    '϶': 2,
    'Ϸ': 3,
    'ϸ': 3,
    'Ϲ': 3,
    'Ϻ': 3,
    'ϻ': 3,
    'ϼ': 3,
    'Ͻ': 3,
    'Ͼ': 3,
    'Ͽ': 3,

    # Greek Extended
    ''

    # others I haven't categorized yet
    '┐': 5,
    '€': 6,
    '“': 4,
    '”': 4,
    '‘': 2,
    '’': 2,
    '„': 4,
    '‚': 2,
    '‹': 3,
    '›': 3,
    '•': 2,
    '–': 6,
    '˜': 3,
    '™': 8,
    'š': 5,
    'œ': 9,
    'ÿ': 5,
    'ž': 5,
    'Æ': 9,
    'æ': 9,
    '░': 7,
    '▒': 8,
    '▓': 8,
    '│': 5,
    '┫': 2,
    '─': 8,
    '┌': 8,
    '┘': 5,
    '└': 8,
    'π': 5,
    '√': 6,
    '∑': 5,
    '∞': 7,
    '≡': 6,
}

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
    last_char_was_section_sign = False
    curr_word_num_pixels = 0
    new_word = ""
    for character in words[i]:
        # if the character was a §, skip counting the next character's pixels, since that is used for Minecraft formatting
        if not last_char_was_section_sign:
            curr_word_num_pixels += PIXEL_WIDTHS[character] + 1 # there is 1 pixel spacing between every character
        else:
            last_char_was_section_sign = False

        # if the character is a \, ", ', or \n, escape it for command formatting
        if character == "\\":
            new_word += "\\\\"
        elif character == '\"':
            new_word += "\\\\\""
        elif character == '\'':
            new_word += "\\\'"
        elif character == '\n':
            new_word += "\\\\n"
        elif character == '§':
            last_char_was_section_sign = True
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
with open('makebook.mcfunction', 'w', encoding='utf-8') as file:
    file.write(command)