import sys, time
from sevenSegmentStr import get_sevenSegment_str


def main():
    # seconds_left = int(input('pls enter how many seconds are left(numbers only): '))
    seconds_left = 60
    try:
        while True:  # Main program loop.
            # Clear the screen by printing several newlines:
            # print('\n' * 60)

            # Get the hours/minutes/seconds from secondsLeft:
            # For example: 7265 is 2 hours, 1 minute, 5 seconds.
            # So 7265 // 3600 is 2 hours:
            hours = str(seconds_left//3600)
            # And 7265 % 3600 is 65, and 65 // 60 is 1 minute:
            minutes = str((seconds_left % 3600) // 60)
            # And 7265 % 60 is 5 seconds:
            seconds = str(seconds_left % 60)

            hstr = get_sevenSegment_str(hours,2)
            mstr = get_sevenSegment_str(minutes,2)
            sstr = get_sevenSegment_str(seconds,2)
            # print(hstr)
            # print(mstr)
            # print(sstr)
            # print("$" * 80)
            # print(hstr, mstr, sstr, sep="$")

            hTopRow, hMiddleRow, hBottomRow = hstr.splitlines()

            mTopRow, mMiddleRow, mBottomRow = mstr.splitlines()

            sTopRow, sMiddleRow, sBottomRow = sstr.splitlines()

            # print(hTopRow, hMiddleRow, hBottomRow)
            # print(mTopRow, mMiddleRow, mBottomRow)
            # print(sTopRow, sMiddleRow, sBottomRow)

            print(hTopRow + '     ' + mTopRow + '     ' +sTopRow)
            print(hMiddleRow + '  *  ' + mMiddleRow + '  *  ' +sMiddleRow)
            print(hBottomRow + '  *  ' + mBottomRow + '  *  ' +sBottomRow)

            if seconds_left == 0:
                print()
                print('    * * * * BOOM * * * *')
                break

            print()
            print('Press Ctrl-C to quit.')

            time.sleep(1)  # Insert a one-second pause.
            seconds_left -= 1

    except KeyboardInterrupt:
        print('thank you for playing')
        sys.exit()

if __name__ == '__main__':
    print("Welcome to Kalpan's countdown")
    main()


