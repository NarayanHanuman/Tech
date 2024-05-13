import shelve


def main():
    message = 'Wkdqn#|rx#Nulvkqd#iru#wklv#juhdw#ydfdwlrq1'
    # Let the user specify the message to hack:
    # print('Enter the encrypted Caesar cipher message to hack.')
    # message = input('> ')

    for key in range(8):
        print(f"key {key}: ", end=" ")
        for char in message:
            print(chr(ord(char)-key), end="")
        print()

    return None



if __name__ == '__main__':
    main()
    # with shelve.open("message1.db") as SHELF:
    #     keys = list(SHELF.keys())
    #     for key in keys:
    #         print(key, SHELF[key])

