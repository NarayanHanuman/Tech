import shelve
SHELF = shelve.open("message1.db")
print('shelve file open')


def main():
    """
    This is main orchestrator. It will take all user input
    :return:
    """
    global SHELF
    action = input('Do you want to (e)ncrypt or (d)ecrypt? ')

    try:
        if action.lower().startswith('e'):
            key = int(input('Please enter the key (0 to 25) to use: '))
            # key = 3
            message = input('Enter the message to encrypt: ')
            encrypt_message(key, message)
            print('Full encrypted text copied to shelve!')
        elif action.lower().startswith('d'):
            key = int(input('Please enter the key (0 to 25) to use: '))
            # key = 3
            message = input('Enter the message to encrypt: ')
            dencrypt_message(key, message)

        else:
            print('Incorrect choice. Bye!')
            print()
    except Exception as e:
        print(f"Here is the exception: {e}")
    finally:
        SHELF.close()
        print('shelve file close')
    return None


def encrypt_message(key, message):
    global SHELF
    encrypted_message = []
    ascii_val = 0
    print(f"Your encrypted message is as follows")
    for char in message:
        # if char.isalpha():
        ascii_val = ord(char)
        ascii_val += key
        encrypted_message.append(ascii_val)
        print(chr(ascii_val), end="")
    print()
    SHELF["encrypted_message_num"] = encrypted_message
    SHELF["key"] = key
    return None


def dencrypt_message(key, message):
    global SHELF
    decrypted_message = encrypted_message = ''
    if int(key) == SHELF["key"]:
        for num in SHELF["encrypted_message_num"]:
            encrypted_message += chr(num)
            num -= key
            decrypted_message += chr(num)

    if encrypted_message == message:
        print(f"You have deciphered the message as follows: {decrypted_message}")
        print('Congratuation!')
    else:
        print("No such message exists")
    return None


if __name__ == '__main__':
    print('I am in main{} location ')
    main()
