def art_to_integer(ascii_art):
    integer = 0
    for row_index, row in enumerate(ascii_art):
        for col_index, char in enumerate(row):
            if char == "#":
                bit_position = row_index * 5 + col_index
                integer |= 1 << bit_position
    return integer


letters_art_dict = {
    "A": ["  #  ", " # # ", "#####", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#### ", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#####", "#    ", "#####"],
    "F": ["#####", "#    ", "#####", "#    ", "#    "],
    "G": [" ####", "#    ", "#  ##", "#   #", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["   ##", "    #", "    #", "#   #", " ### "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "O": ["#####", "#   #", "#   #", "#   #", "#####"],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "# # #", " ### ", "    #"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "S": ["#####", "#    ", "#####", "    #", "#####"],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#####"],
    "V": ["#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "X": ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "   # ", "  #  ", " #   ", "#####"],
    "{": [" ####", " #   ", "#    ", " #   ", " ####"],
    "}": ["#### ", "   # ", "    #", "   # ", "#### "],
    "_": ["     ", "     ", "     ", "     ", "#####"],
}

print("unsigned int ascii_art_map[] = {")
for letter, art in letters_art_dict.items():
    integer_value = art_to_integer(art)
    print(f"    {integer_value}, // {letter}")
print("};")