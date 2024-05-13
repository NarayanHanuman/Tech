
def get_sevenSegment_str(number, minWidth=0):
    """Return a seven-segment display string of number. The returned
      string will be padded with zeros if it is smaller than minWidth."""

    # Convert number to string in case it's an int or float:
    number = str(number).zfill(minWidth)

    rows = ['', '', '']
    for i, numeral in enumerate(number):
        if numeral == "0":
            rows[0] += " __ "
            rows[1] += "|  |"
            rows[2] += "|__|"
        elif numeral == "1":
            rows[0] += "    "
            rows[1] += "   |"
            rows[2] += "   |"
        elif numeral == "2":
            rows[0] += " __ "
            rows[1] += " __|"
            rows[2] += "|__ "
        elif numeral == "3":
            rows[0] += " __ "
            rows[1] += " __|"
            rows[2] += " __|"
        elif numeral == "4":
            rows[0] += "    "
            rows[1] += "|__|"
            rows[2] += "   |"
        elif numeral == "5":
            rows[0] += " __ "
            rows[1] += "|__ "
            rows[2] += " __|"
        elif numeral == "6":
            rows[0] += " __ "
            rows[1] += "|__ "
            rows[2] += "|__|"
        elif numeral == "7":
            rows[0] += " __ "
            rows[1] += "   |"
            rows[2] += "   |"
        elif numeral == "8":
            rows[0] += " __ "
            rows[1] += "|__|"
            rows[2] += "|__|"
        elif numeral == "9":
            rows[0] += " __ "
            rows[1] += "|__|"
            rows[2] += " __|"
        elif numeral == ".":
            rows[0] += " "
            rows[1] += " "
            rows[2] += "."
        elif numeral == "-":
            rows[0] += " "
            rows[1] += "-"
            rows[2] += " "

         # Add a space (for the space in between numerals) if this isn't the last numeral and the decimal point isn't next:
        if i != len(number) - 1 and number[i+1] != ".":
            rows[0] += " "
            rows[1] += " "
            rows[2] += " "
    return "\n".join(rows)


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    print('This module is meant to be imported rather than run.')
    print('For example, this code:')
    print('    import sevseg')
    print('    myNumber = sevseg.getSevSegStr(42, 3)')
    print('    print(myNumber)')
    print()
    print('...will print 42, zero-padded to three digits:')
    print(' __        __ ')
    print('|  | |__|  __|')
    print('|__|    | |__ ')
    width = 0
    while True:
        number = input("Please enter time you want to display: ")
        # width = int(input('pls enter the width(Numbers only): '))
        print(get_sevenSegment_str(number, width))
