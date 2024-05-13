import random
import sys

# Set up the constants:
HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.
# (A list of chr codes is at https://inventwithpython.com/charactermap)
BACKSIDE = 'backside'
DECK = None

def get_legit_bet(maxBet):
    """
    Allows customers to enter bet value
    :param maxBet: money
    :return: placed bet
    """
    while True:
        placed_bet = input(f'How much do you want to wager? (1-{maxBet}, or [Q]UIT): ').upper().strip()
        # placed_bet = '1000'
        if placed_bet.upper().startswith('Q'):
            print('Thanks for playing!')
            exit(1)
        if placed_bet.isalpha() or placed_bet.isspace() or placed_bet.istitle():
            print('only numbers are allowed') # If the player didn't enter a number, ask again.
        elif placed_bet.isdigit():
            placed_bet = int(placed_bet)
            if 1 <= placed_bet <= maxBet:
                return placed_bet


def get_fresh_shuffled_deck():
    """Return a list of (rank, suit) tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((rank, suit))
        for rank in ('J', 'Q', 'K'):
            deck.append((10, suit))
        for rank in ('A'):
            deck.append((rank,suit))
    random.shuffle(deck)
    return deck


def display_hands(playerHand, dealerHand, showDealerHand):
    """Show the player's and dealer's cards & values.
    Hide the dealer's first card if showDealerHand is False."""
    print(playerHand, dealerHand)

    if showDealerHand:
        print('Dealer overall value:', calculate_total_hand_value(dealerHand))
        display_cards(dealerHand)
    else:
        print('DEALER:')
        # Hide the dealer's first card:
        display_cards([BACKSIDE] + dealerHand[1:])

    print()
    print('Player overall value:', calculate_total_hand_value(playerHand))
    display_cards(playerHand)
    return None


def calculate_total_hand_value(cards):
    """Returns the value of the cards. Face cards are worth 10, aces are
    worth 11 or 1 (this function picks the most suitable ace value)."""
    value = 0
    numberOfAces = []
    for card in cards:
        if card[0] == 'A':
            numberOfAces.append(1)
        else:
            value += card[0]
    if len(numberOfAces) > 0:
        for i in numberOfAces:
            if (value + 11) > 21:
                value += 1
            else:
                value += 11
    return value


def display_cards(cards):
    """Display all the cards in the cards list."""
    rows = ['', '', '', '', '']  # The text to display on each row.
    for card in cards:
        rows[0] += ' ___  '
        if card != BACKSIDE:
            rank, suit = card
            rows[1] += '|{} | '.format(str(rank).ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '| {}| '.format(str(rank).rjust(2, '_'))
        else:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        rows[4] += ' ---  '

    for row in rows:
        print(row)

    return None


def get_move(player1_hand, remaining_money) -> str:
    """
    This will ensure user is only selecting right moves
    :param player1_hand:
    :param remaining_money:
    :return: player's move
    """
    if len(player1_hand) == 2 and remaining_money > 0:
        allowed_moves = ['(H)it', '(S)tand', '(D)ouble down']
    else:
        allowed_moves = ['(H)it', '(S)tand']

    move_prompt = ", ".join(allowed_moves)
    while True:
        move = input("Player move: " + move_prompt + "> ")
        if move.lower().startswith('h') or move.lower().startswith('s'):
            return move
        elif move.lower().startswith('d') and '(D)ouble down' in allowed_moves:
            return move
        elif move.lower().startswith('d') and '(D)ouble down' not in allowed_moves:
            print("You can't double down at this stage, please retry")
        else:
            print("please choose from h, s or d")

def main():
    """
    This is a main orchestrator
    :return: None
    """
    global DECK
    print(''' Welcome to Blackjack, by Kalpan Dalal

      Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.

        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.

        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.''')
    money = 5000
    while True:  # Main game loop.
        # Check if the player has run out of money:
        if money <= 0:
            print("You're broke!")
            print("Good thing you weren't playing with real money.")
            print('Thanks for playing!')
            sys.exit()

        # Let the player enter their bet for this round:
        print(f"Player's balance: ${money}")
        bet = get_legit_bet(money)

        # Give the dealer and player two cards from the deck each:
        deck = get_fresh_shuffled_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player1_hand = [deck.pop(), deck.pop()]

        # 'Handle player actions:'
        print('Player has wagered :', bet)
        player1_val = calculate_total_hand_value(player1_hand)
        print(f"Player's initial balance: {player1_val}")
        if player1_val == 21:
            print('Congratulation Player 1! You hit the blackjack!')
            display_hands(player1_hand, dealer_hand, True)
            print('################################################################')
            print(f"@@@@@ you get to earn {bet* 2} to player's initial seed amount {money}")
            money += (bet * 2)
            print(f"after winnings your balance is {money}")
            continue

        dealer_val = calculate_total_hand_value(dealer_hand)
        print(f"Dealer's initial balance: {dealer_val}")
        if dealer_val == 21:
            print('Congratulation Dealer! You hit the blackjack!')
            print('################################################################')
            print(f"1. $$$$$$$$ you get to earn {bet* 2} from player's seed amount {money}")
            money -= (bet * 2)
            print(f"after subtraction amount left is {money}")
            continue

        player_busted = False
        while True:  # Keep looping until player stands or busts.
        # Get the player's move, either H, S, or D:
            remaining_money = money - bet
            move = get_move(player1_hand, remaining_money)
            display_hands(player1_hand, dealer_hand, False)
            print()
            if move.upper().startswith('D'):  # Player is doubling down:
                new_bet = bet * 2
                if remaining_money < new_bet:
                    new_bet = bet + remaining_money

                remaining_money = money - new_bet
                bet = new_bet
                print(F"Player's total bet: {bet} and remaining balance is {remaining_money}")

            if move.upper().startswith('H') or move.upper().startswith('D'):
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                player1_hand.append(newCard)
                display_hands(player1_hand, dealer_hand, False)
                player1_val = calculate_total_hand_value(player1_hand)
                if player1_val > 21:
                    print("oopsy! It is bust for payer 1. Dealer won!")
                    player_busted = True
                    break
            elif move.upper().startswith('S'):
                print("Player has decided to stand")
                break

        "Dealer's actions:"
        if not player_busted:
            # print("It is Dealer's turn.")
            if dealer_val <= 21:
                if dealer_val <= 17:
                    dealer_move = input("Dealer's move: '(H)it' or '(S)tand' ")
                    if dealer_move.lower().startswith('h'):
                        print('Dealer hits...')
                        dealer_new_card = deck.pop()
                        rank, suit = dealer_new_card
                        print(F"Your have drawn {rank} of {suit}")
                        dealer_hand.append(dealer_new_card)
                        # check if dealer is busted or not
                        dealer_val = calculate_total_hand_value(dealer_hand)
                        if dealer_val > 21:
                            print("oopsy! It is bust for dealer. Payer 1 won!")
                    elif dealer_move.lower().startswith('s'):
                        print('You have decided to not take additional cards')
                else:
                    print('Dealer can only (s)tand!')

        'Show the final hands'
        display_hands(player1_hand, dealer_hand, True)
        print('@' * 80)
        print('@                                 Final score                                  @')
        print('@' * 80)
        if player1_val > 21:
            print("It is bust for payer 1. Dealer won!", end=" ")
            print(f"Player has lost his wager of {bet}!")
            print(f"3. $$$$$$$$ you get to earn {bet} from player's seed amount {money}")
            money -= bet
            print(f"after subtraction amount left is {money}")
        elif dealer_val > 21:
            print("It is bust for Dealer. Player 1 won")
            print(f"4. $$$$$$$$ you get to earn {bet} to player's initial seed amount {money}")
            money += bet
            print(f"after winnings your balance is {money}")
        elif player1_val > dealer_val:
            print(F'Player won by {player1_val-dealer_val} points')
            print(f"5. $$$$$$$$ you get to earn {bet} to player's initial seed amount {money}")
            money += bet
            print(f"after winnings your balance is {money}")
        elif player1_val == dealer_val:
            # NOTHING HAPPEND WITH money
            print('it is a tie, the bet is returned to you.')
        elif player1_val < dealer_val:
            print(F'Dealer won by {dealer_val-player1_val} points')
            print(f"6. $$$$$$$$ you get to earn {bet} from player's seed amount {money}")
            money -= bet
            print(f"after subtraction amount left is {money}")
        if input('enter Q for quiting:').strip().upper().startswith('Q'):
            print('Thank you for playing!')
            break

    return None


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
