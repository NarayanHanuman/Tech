import random


def display_text():
    """
    This will just explain game to user.
    :return: None
    """
    print('Welcome to a deductive logic game')
    print('I am thinking of a 3-digit number. Try to guess what it is.')
    print('''
    Here are some clues:
    When I say:    That means:
      Pico         One digit is correct but in the wrong position.
      Fermi        One digit is correct and in the right position.
      Bagels       No digit is correct.
    I have thought up a number.
    You have 10 guesses to get it.
    ''')
    print('You have 10 guesses to get it.')
    return None


def check_validity(guessed_str, correct_value):
    """
    This brain of whole game.
    :param guessed_str: User guessed number
    :param correct_value: computer guessed number
    :return: None
    """
    one_valid_num = False
    k = 0
    for i, char1 in enumerate(guessed_str):
        for j, char2 in enumerate(correct_value):
            if char1 in char2:
                k += 1
                one_valid_num = True
                if i == j:
                    print(f'{k}.Fermi')
                else:
                    print(f'{k}.pico')
    if one_valid_num == False:
        print('Bagels')
    return None


def main():
    """
    This is main orchestrator which controls the process.
    :return:
    """
    correct_value = random.randint(100, 999)
    correct_value = str(correct_value)

    display_text()

    for i in range(1,11):
        guessed_str = input(f'Guess # {i}: ')
        if guessed_str == correct_value:
            print('You got it, Shivansh!')
            break
        else:
            check_validity(guessed_str, correct_value)
    else:
        print(f'actual number: {correct_value}')
    if input('do you want to play again? ').lower().startswith('y'):
        main()
    return None


if __name__ == '__main__':
    main()
