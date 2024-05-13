import random
# import pprint

# Global variables
SPADE = chr(9824)
CLUB = chr(9827)
HEART = chr(9829)
DIAMOND = chr(9830)
DISPLAY_MODE = 'On'

BLANK_CARD = 'blank'
NUM_OF_SPLITS = 0
NUM_OF_PLAYERS = 0
DECK = []  # this will be in format [(,),(,)]
MONEY = BET = []
PLAYER_HAND = PLAYED_HAND_VAL = []
DEALER_HAND = []
DEALER_HAND_VAL = 0
HAS_PLAYER_GOT_BLACKJACK = HAS_PLAYER_SURRENDERED = HAS_PLAYER_BUSTED = []


def get_shuffled_deck():
    """
    This will calculate teh deck & shuffled it.
    :return: whole new, freshly shuffled & minted deck
    """
    global DECK
    for suite in (SPADE, CLUB, HEART, DIAMOND):
        for i in range(2, 11):
            DECK.append((i, suite))
        for _ in ('J', 'Q', 'K'):
            DECK.append((10, suite))
        for rank in 'A':
            DECK.append((rank, suite))
    random.shuffle(DECK)
    return DECK


def make_bet(player):
    """
    This function checks if bet placed is within the range
    :param player: Player index
    :return: none
    """
    global MONEY, BET
    while True:
        # placed_bet = input('how much you are betting? ')
        placed_bet = '8'
        if placed_bet.isdecimal():
            placed_bet = int(placed_bet.strip())
            if 1 <= placed_bet <= MONEY[player]:
                BET[player] = placed_bet
                return None
            else:
                print(f"invalid amount. Please retry")
        else:
            print('not decimal, please retry')


def calculate_hand_value(player, is_it_dealer):
    """
    This function calculates hand value of player & dealer
    :param player: player index
    :param is_it_dealer: True or False
    :return: total hand value
    """
    global PLAYER_HAND, PLAYED_HAND_VAL, DEALER_HAND, DEALER_HAND_VAL
    number_of_aces = total_hand_val = 0
    if is_it_dealer:
        set_of_cards = DEALER_HAND
    else:
        set_of_cards = PLAYER_HAND[player]

    for card in set_of_cards:
        rank, suite = card
        if rank == 'A':
            number_of_aces += 1
        else:
            total_hand_val += rank
    for i in range(number_of_aces):
        if (total_hand_val + 11) > 21:
            total_hand_val += 1
        else:
            total_hand_val += 11

    if is_it_dealer:
        DEALER_HAND_VAL = total_hand_val
    else:
        PLAYED_HAND_VAL[player] = total_hand_val

    return total_hand_val


def show_player_card(player):
    """
    This function display card
    :param player: player index
    :return: None
    """
    global PLAYER_HAND, DEALER_HAND
    rows = [''] * 5

    for card in PLAYER_HAND[player]:
        rank, suite = card
        rows[0] += ' ____  '
        rows[1] += '|{}  | '.format(str(rank).ljust(2))
        rows[2] += '| {}  | '.format(suite)
        rows[3] += '|  {}| '.format(str(rank).rjust(2, '_'))
        rows[4] += ' ----  '
    for row in rows:
        print(row)

    return None


def show_value_and_display_cards(player):
    """
    This function calls two functions:
     1. calculate value of card
     2. show card
    :param player: player index
    :return: None
    """
    global PLAYER_HAND, PLAYED_HAND_VAL
    calculate_hand_value(player, False)

    print(f"Player {player+1}: Hand value- {PLAYED_HAND_VAL[player]:2d} player hand- {PLAYER_HAND[player]}")
    if DISPLAY_MODE == 'On':
        show_player_card(player)

    return None


def show_dealer_card(cards):
    """
    This function shows dealer's card
    :param cards: dealer's card
    :return: None
    """
    global BLANK_CARD
    rows = ['', '', '', '', '']
    for card in cards:
        if card == BLANK_CARD:
            rows[0] += ' ____  '
            rows[1] += '|##  | '
            rows[2] += '|### | '
            rows[3] += '|_## | '
            rows[4] += ' ----  '
        else:
            rank, suite = card
            rows[0] += ' ____  '
            rows[1] += '|{}  | '.format(str(rank).ljust(2))
            rows[2] += '| {}  | '.format(suite)
            rows[3] += '|  {}| '.format(str(rank).rjust(2, '_'))
            rows[4] += ' ----  '
    for row in rows:
        print(row)
    return


def display_dealer_hand_and_val(should_I_show_blank_cards):
    """
        This function shows dealer's hand value & card
    :param should_I_show_blank_cards: True or False
    :return: None
    """
    global DEALER_HAND, BLANK_CARD, DEALER_HAND_VAL
    cards = []
    calculate_hand_value(1, True)
    print(f"Dealer    Hand value- {DEALER_HAND_VAL:2d} Dealer hand- {DEALER_HAND}")
    print()

    if DISPLAY_MODE == 'On':
        if should_I_show_blank_cards:
            cards.append(BLANK_CARD)
            cards.append(DEALER_HAND[1])
        else:
            cards = DEALER_HAND
        show_dealer_card(cards)
    return None


def process_newly_appended_element():
    """
        This function process newly appended element in 3 steps:
        1. initializes variables
        2. make bet
        3. show hand value and display cards
    :return: None
    """
    global NUM_OF_PLAYERS, MONEY, BET, PLAYED_HAND_VAL, HAS_PLAYER_GOT_BLACKJACK, HAS_PLAYER_SURRENDERED
    NUM_OF_PLAYERS += 1

    # Initialization of variable
    MONEY.append(5000)
    BET.append(0)
    # player_hand = [[(1, '♠'), (1, '♠')]]  # THis is already done before calling this function
    PLAYED_HAND_VAL.append(0)
    HAS_PLAYER_GOT_BLACKJACK.append(False)
    HAS_PLAYER_BUSTED.append(False)
    HAS_PLAYER_SURRENDERED.append(False)

    index = len(MONEY) - 1  # calculating correct index = length - 1 because index starts with 0

    # ensuring that bet value is made
    make_bet(index)

    # display hand & value
    show_value_and_display_cards(index)

    return None


def your_move_player(player):
    """
    This function allows player to make move.
    This function also implement Double down rules using already_doubled_flg.
    It lets user append new card at the end for the Split process.
    :param player: player index
    :return: None
    """
    global PLAYER_HAND, PLAYED_HAND_VAL, HAS_PLAYER_SURRENDERED, NUM_OF_SPLITS, DEALER_HAND, HAS_PLAYER_BUSTED
    already_doubled_flg = False  # this flag is used to automatically hit after double
    while True:
        if already_doubled_flg:
            print("Since you have doubled in the last game, you automatically get a new hit!")
            player_move = "hit"
        else:
            player_move = input(f"Player-{player + 1} move(q for quit): ").lower().strip()
            if player_move.startswith("q"):
                return None

        if player_move.lower().startswith("d"):
            original_amt = MONEY[player]
            bet = BET[player]

            if len(PLAYER_HAND[player]) == 2 and original_amt > 0:
                pass
            else:
                print('You can no longer Double down. Please choose form h, st, sp or su.')
                your_move_player(player)

            # if there is valid double, then control will come till here.
            already_doubled_flg = True  # Hence, I am setting up this flag.
            if (original_amt - bet) > (bet * 2):
                bet *= 2
            else:
                bet += (original_amt - bet)

            BET[player] = bet

            if DISPLAY_MODE == 'On':
                print(F"Player's total bet: {bet} and balance is {original_amt - bet}")

        if player_move.lower().startswith("h") and already_doubled_flg is True:
            already_doubled_flg = False  # reset the flag here because this hit is after double

        if player_move.lower().startswith("h") or player_move.lower().startswith("d"):
            rank, suite = new_card = DECK.pop()
            print('You got {} of a {}'.format(rank, suite))
            PLAYER_HAND[player].append(new_card)
            show_value_and_display_cards(player)
            if PLAYED_HAND_VAL[player] > 21:
                print(f'It is a bust for Player {player+1}.')
                HAS_PLAYER_BUSTED[player] = True
                break
        elif player_move.lower().startswith("sp"):
            if PLAYER_HAND[player][0][0] != PLAYER_HAND[player][1][0] and NUM_OF_SPLITS == 0:
                print('since both values are not same, you cannot split')
                print('Please choose from one of valid values only h, st, su')
                continue
            else:
                print(f'before split player hand {PLAYER_HAND}\tdealer hand {DEALER_HAND}')
                PLAYER_HAND.append([PLAYER_HAND[player][1]])
                PLAYER_HAND[player].pop(1)
                print(f'after split player hand {PLAYER_HAND}\tdealer hand {DEALER_HAND}')
                print('You have successfully appended new hand & popped it in original place')
                NUM_OF_SPLITS += 1
                print('New player processing...')
                process_newly_appended_element()
                print('Continue original player....')
                continue
        elif player_move.lower().startswith("st"):
            print('Player has chosen to stand')
            break
        elif player_move.lower().startswith("su"):
            HAS_PLAYER_SURRENDERED[player] = True
            break
        else:
            print('Please choose from: h, d, st, sp, su')
    return None


def tally_score(player):
    """
    This function is final arbitrator who tally the score. it compares player hand against dealer hand.
    :param player: Player index
    :return: None
    """
    # print("========================== Final Score ==========================")
    global PLAYED_HAND_VAL, HAS_PLAYER_SURRENDERED
    if HAS_PLAYER_SURRENDERED[player] == True:
        MONEY[player] -= (BET[player] // 2)
        print(f"Since player {player+1} has surrendered, his/her remaining amount: {MONEY[player]}")
    elif PLAYED_HAND_VAL[player] > 21:
        '''
        If both player & dealer got busted, then player plays first so player looses the bet
        '''
        MONEY[player] -= BET[player]
        print(f"Since player {player+1} is busted. remaining amount: {MONEY[player]}")
    elif PLAYED_HAND_VAL[player] > DEALER_HAND_VAL:
        MONEY[player] += (BET[player] * 2)
        print(f"Player {player+1} win. New amount: {MONEY[player]}")
    elif (PLAYED_HAND_VAL[player] < DEALER_HAND_VAL) and (DEALER_HAND_VAL > 21):
        MONEY[player] += BET[player]
        print(f"Since dealer is busted, player's new amount: {MONEY[player]}")
    elif (PLAYED_HAND_VAL[player] < DEALER_HAND_VAL) and (DEALER_HAND_VAL <= 21):
        MONEY[player] -= BET[player]
        print(f"Dealer win. Player {player+1} remaining amount: {MONEY[player]}")
    elif PLAYED_HAND_VAL[player] == DEALER_HAND_VAL:
        print(f"It is a Tie for Player {player+1}. No change in the amount.")

    return None


def main_orchestrator():
    """
    This is main orchestrator which orchestrate whole blackjack functionality.
    Execution of this function is one iteration of game.
    :return: Nothing
    """
    global NUM_OF_PLAYERS, MONEY, BET, PLAYER_HAND, PLAYED_HAND_VAL, DEALER_HAND, HAS_PLAYER_BUSTED
    global DEALER_HAND_VAL, DECK, HAS_PLAYER_SURRENDERED
    # number_of_players = 2
    try:
        NUM_OF_PLAYERS = int(input('how many players want to play this game? '))
    except Exception as e:
        print(f'here is the exception {e}')

    # get the shuffled deck
    DECK = get_shuffled_deck()

    # Initialization of variable
    MONEY = [5000] * NUM_OF_PLAYERS  # [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
    BET = [0] * NUM_OF_PLAYERS  # [0, 0, 0, 0, 0, 0, 0, 0]

    PLAYER_HAND = [[(1, '♠'), (1, '♠')]] * NUM_OF_PLAYERS
    PLAYED_HAND_VAL = [0] * NUM_OF_PLAYERS
    HAS_PLAYER_GOT_BLACKJACK = [False] * NUM_OF_PLAYERS
    HAS_PLAYER_SURRENDERED = [False] * NUM_OF_PLAYERS
    HAS_PLAYER_BUSTED = [False] * NUM_OF_PLAYERS

    DEALER_HAND = [(1, '♠'), (1, '♠')]
    DEALER_HAND_VAL = 0

    for player in range(NUM_OF_PLAYERS):
        # each player put his bet
        make_bet(player)

        # deal cards to each player
        # print('before', player_hand[player], end=" After: ")
        PLAYER_HAND[player] = [DECK.pop(), DECK.pop()]  # before [(1, '♠'), (1, '♠')] After: [(3, '♠'), (10, '♥')]
        # pprint.pprint(player_hand[player])

        # show cards & hand_val
        show_value_and_display_cards(player)

    # deal dealer's cards, show cards & hand_val
    DEALER_HAND = [DECK.pop(), DECK.pop()]  # before: [(1, '♠'), (1, '♠')] after: [(10, '♥'), (3, '♥')]
    display_dealer_hand_and_val(True)

    # if dealer has blackjack or players get blackjack
    if DEALER_HAND_VAL == 21:
        for player in range(NUM_OF_PLAYERS):
            if PLAYED_HAND_VAL[player] != 21:
                MONEY[player] -= BET[player]

        print("all players without blackjack looses their amount")
        print("Players' new value are:", PLAYED_HAND_VAL)
        return None
    else:
        for player in range(NUM_OF_PLAYERS):
            if PLAYED_HAND_VAL[player] == 21:
                MONEY[player] += (BET[player] * 1.5)
                print(f"Player {player + 1} got the blackjack. New amount: {MONEY[player]}")
                HAS_PLAYER_GOT_BLACKJACK[player] = True

        # below teo methods are to check if list contains True value
        if any(boolean for boolean in HAS_PLAYER_GOT_BLACKJACK):  # at least one is true
            print("Here are tally of players getting blackjack", HAS_PLAYER_GOT_BLACKJACK)
            print("At this stage, players' seed amount are:", MONEY)
        if HAS_PLAYER_GOT_BLACKJACK.count(True) > 0:
            return None

    # Player move
    for player in range(NUM_OF_PLAYERS):
        print("""Please choose among these values: h, st, sp, su, d
            (H)it to take another card.
            (St)and to stop taking cards.
            (Sp)lit to split your cards
            (Su)rrender to get half of your bet back  
            (D)ouble down to increase your bet, on your 1st play only but must hit exactly one more time before standing.
        """)
        print(f'your hand value: {PLAYED_HAND_VAL[player]}')
        your_move_player(player)

    if NUM_OF_SPLITS > 0:
        print('-' * 80)
        print('Newly split player processing...')
        print('-' * 80)
        indx = len(MONEY) - 1
        print(f'your hand value: {PLAYED_HAND_VAL[indx]}')
        your_move_player(indx)

        # after moving, we need to check if split-player got the blackjack
        if PLAYED_HAND_VAL[indx] == 21:
            MONEY[indx] += (BET[indx] * 1.5)
            print(f"Split Player {indx + 1} got the blackjack. New amount: {MONEY[indx]}")
            HAS_PLAYER_GOT_BLACKJACK[indx] = True
            return None

    # Dealer move
    if DEALER_HAND_VAL > 17:
        print('since dealer_hand_val > 17, dealer is standing')
    else:
        print('dealer is hitting..')
        DEALER_HAND.append((DECK.pop()))
        display_dealer_hand_and_val(False)

    # tally the result for each player
    for player in range(NUM_OF_PLAYERS):
        if DEALER_HAND_VAL > 21:
            if not HAS_PLAYER_BUSTED[player]:
                print(f"Haha! It is Dealer's bust. Player {player+1} wins!")
                MONEY[player] += (BET[player] * 2)
                print(f"0)Since dealer receive a bust, new amount for player {player}: ${MONEY[player]}")
        else:
            tally_score(player)

    return None


if __name__ == '__main__':
    print(''' Welcome to Blackjack, by Kalpan Dalal

      Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.

        (H)it to take another card.
        (St)and to stop taking cards.
        (Sp)lit to split your cards
        (Su)rrender to get half of your bet back  
        (D)ouble down to increase your bet, on your first play only
        but must hit exactly one more time before standing.

        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.''')
    i = 1
    while True:
        print(f'----------------------------------------------------- Welcome to Round: {i} '
              f'-----------------------------------------------------')
        main_orchestrator()
        if input("\nDo you want to stop playing?(y/n): ").upper().startswith('Y'):
            break
        else:
            i += 1
