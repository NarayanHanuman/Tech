import calendar
import datetime

while True:
    res = input('Enter the year for the calendar: ')
    if not res.isdecimal():
        print('only decimal is allowed')
        continue

    YEAR = int(res)

    if 999 < YEAR < 2080:
        break
    else:
        print('please only key-in 4 digit decimal values for year, like 2022, 2023, etc. ')


while True:
    res = input('Enter the month number (1-12): ')
    if not res.isdecimal():
        print('only decimal is allowed')
        continue

    MONTH = int(res)
    if 1 <= MONTH <= 12:
        break
    else:
        print('please enter numeric month number, like 3 for March ')


# for testing, you can comment above and uncomment below lines
# YEAR = '2016'
# MONTH = '2'

DAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday')
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December')

def convert_decimal_year_to_str(dec_year: str) -> str:
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    if not dec_year.isdecimal():
        return "Invalid month"
    else:
        dec_year = int(dec_year)

    if dec_year < 1 or dec_year > 12:
        return "Invalid month"
    else:
        return months[dec_year - 1]

    return None


def main():
    global YEAR, MONTH
    yr, mon = int(YEAR), int(MONTH)
    # line_break = "+----------+----------+----------+----------+----------+----------+----------+"
    line_break = "+----------" * 7 + "+"
    day_one = 1
    day1_one, num_of_days = calendar.monthrange(yr, mon)
    has_new_week_started = True
    rows = [''] * 31
    sr = 1

    print(F"\t\t\t\t\t\t\t  {convert_decimal_year_to_str(MONTH)} {YEAR}")
    print("...Sunday.....Monday....Tuesday...Wednesday...Thursday....Friday....Saturday..")
    # print(line_break)
    rows[0] = line_break
    last_day = False
    for dt in range(day_one, (num_of_days + 1)):
        week_day = datetime.date(yr, mon, dt).strftime("%A")

        if dt == num_of_days:
            last_day = True
            
        for day in DAYS:
            
            if day == week_day:
                rows[sr] += "|{}        ".format(str(dt).rjust(2))
                has_new_week_started = False
                if last_day:
                    rows[sr] += F"|          " * (len(DAYS) - (DAYS.index(day)+1))
                break
            elif has_new_week_started:
                rows[sr] += F"|          "

        if week_day == 'Saturday' or last_day:
            has_new_week_started = True
            rows[sr] += r'|'  # this is for ending current line

            for i in range(3):
                sr += 1  # this is for new line
                # rows[sr] +='|          |          |          |          |          |          |          |'
                rows[sr] += '|          ' * 7 + r'|'

            sr += 1  # this is for Week separator
            rows[sr] += line_break

            sr += 1  # this is for next Week


    for row in rows:
        if row != '':
           print(row)

    return None


if __name__ == '__main__':
    print('Welcome to Calendar Maker!\n\t\t\tby Kalpan Dalal')
    main()