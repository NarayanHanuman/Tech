import random

winning_bet = None

"connneted code inside while loop"
# dice1 = [1, 2, 3, 4, 5, 6]
# dice2 = [1, 2, 3, 4, 5, 6]

while True:
    p1_choice = input('Player 1, enter your choice(odd/even): ').lower()
    while True:
        p2_choice = input('Player 2, enter your choice(odd/even): ').lower()
        if p2_choice != p1_choice:
            break

    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    result = dice1 + dice2
    # print(f"here is dice1: {dice1} dice2: {dice2} and result: {result}")
    print(f"Result: {result}")

    "connneted code above while loop"
    # # Shuffle both dice
    # random.shuffle(dice1)
    # random.shuffle(dice2)
    # result += dice1.pop()
    # result += dice2.pop()

    if result % 2 == 0:
        winning_bet = 'e'  # for even
    else:
        winning_bet = 'o'  # for odd

    if p1_choice.startswith(winning_bet):
        print('Player 1 wins')
    else:
        print('Player 2 wins')

    if input('do you want to continue(y/n)? ').lower().startswith('n'):
        print('Thank you for playing')
        break
