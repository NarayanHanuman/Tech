import datetime
import random

date_list = []
# Set up a tuple of month names in order:
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def take_user_input() -> int:
    """
    This will ask for user's input
    :return: valid number
    """
    num_dates = 0
    try:
        num_dates = int(input(f'How many birthdays shall I generate? : '))
    except ValueError:
        print("Invalid input. Please reenter a valid number.")
    return num_dates


def get_random_birthdates(num_dates):
    """
    Create a shuffled list
    :param num_dates: This number represent sample size.
    :return: selected_dates
    """

    global date_list
    # Step 1: Create a list of distinct dates
    date_list = [datetime.date(2020, j, i) for j in range(1, 12) for i in range(1, 29)]

    # Step 2: Shuffle the list randomly
    random.shuffle(date_list)

    # Step 3: slice the shuffled list to get the desired number of distinct dates
    selected_dates = date_list[:num_dates]

    return selected_dates


def get_birthdays_ai(number_of_birthdays):
    """
    This will calculate selected dates = first_day + delta
    :param number_of_birthdays: This number represent sample size.
    :return: selected_dates
    """

    first_day = datetime.date(2020, 1, 1)
    selected_dates = []
    for i in range(1, number_of_birthdays + 1):
        num = datetime.timedelta(random.randint(1, 364))
        next_date = first_day + num
        selected_dates.append(next_date)
    return selected_dates


def get_match_dates(selected_dates):
    """
    if there is a match in dates then add it to dict with counter
    :param selected_dates: whole list containing dates
    :return: dict {matched_date, cnt}
    """
    if len(selected_dates) == len(set(selected_dates)):
        # print('all dates are unique')
        return None
    matched_dates_cnt = {}
    for iA, birthdayA in enumerate(selected_dates):
        for iB, birthdayB in enumerate(selected_dates[(iA + 1):]):
            if birthdayB == birthdayA:
                birthday_A = birthdayA.strftime('%m-%d-%Y')
                matched_dates_cnt[birthday_A] = matched_dates_cnt.setdefault(birthday_A, 1) + 1
                return birthday_A
    # return matched_dates_cnt


def fetch_valid_user_input():
    number_of_birthdays = take_user_input()
    while number_of_birthdays < 0:
        print(f"Number of dates requested is out of range. Minimum:0")
        number_of_birthdays = take_user_input()
    return number_of_birthdays


def main_orchestrator():
    """
    Take input from customers & get the list.
    :return: None
    """
    global date_list
    sim_match = 0  # How many simulations had matching birthdays in them.

    # 1. Take user input
    # number_of_birthdays = fetch_valid_user_input()
    number_of_birthdays = random.randint(26, 80)

    # 2. Get the random number_of_birthdays
    # selected_dates = get_random_birthdates(number_of_birthdays)
    selected_dates = get_birthdays_ai(number_of_birthdays)

    # 3. check if you have duplicate in your sample size
    matched_dates_result = get_match_dates(selected_dates)
    if matched_dates_result is not None:
        sim_match = 1

    # print('Here are selected list of dates')
    # print([date.strftime('%Y-%m-%d') for date in selected_dates])

    return sim_match


if __name__ == '__main__':
    # Display the intro:
    print('''Birthday Paradox, by Kalpan Dalal 
  
     The birthday paradox shows us that in a group of N people, the odds
     that two of them have matching birthdays is surprisingly large.
     This program does a Monte Carlo simulation (that is, repeated random
     simulations) to explore this concept.
     
     (It's not actually a paradox, it's just a surprising result.)
    ''')

    print('Let us run simulation 100,000 times')
    simulation_match = 0
    num_of_simulation = 100_001
    divisior = num_of_simulation // 5
    for i in range(1, num_of_simulation):
        if i % divisior == 0:
            print(f'{i:,} simulation ran...')
        simulation_match += main_orchestrator()
    print(f'Out of {num_of_simulation-1:,} simulations, matched is found in {simulation_match:,} runs.')
    probability_calc = round(simulation_match/num_of_simulation * 100, 2)
    print('people have a', probability_calc, '% chance of')
