"""Simple Typing Speech Tester in Python"""

# importing important modules
import curses
from curses import wrapper
from random import randint
import time

def TypingTest():
    """The main function to start the typing test"""

    # function to get the text from the website
    def getText():
        with open("texts.txt", "r") as file:
            text = file.readlines()
        return text[randint(0, len(text) - 1)].strip()

    # function to start the terminal for typing test
    def start(stdscr):
        stdscr.clear()
        stdscr.addstr("Welcome to the Speed Typing Test!")
        stdscr.addstr("\nPress enter to start...")
        stdscr.refresh()
        stdscr.getkey()

    # function to display text as the user type
    # It also display the speed in words per minutes
    def displayText(stdscr, targetText, currentText, wpm=0, accuracy=100):
        stdscr.addstr(targetText)
        stdscr.addstr(1, 0, f'Your speed is {wpm} words/min')
        stdscr.addstr(2, 0, f'Your accuracy is {accuracy} %.')

        for i, char in enumerate(currentText):
            correctChar = targetText[i]
            color = curses.color_pair(1)
            if char != correctChar:
                color = curses.color_pair(2)

            stdscr.addstr(0, i, char, color)

    # function to count the speed
    def test(stdscr):
        targetText = getText()
        currentText = []
        wpm = 0
        errors = 0

        # count the starting time
        startTime = time.time()
        words = 0
        stdscr.nodelay(True)

        while True:
            # calculate the speed
            timeElapsed = max(time.time() - startTime, 1)
            wpm = round(words / (timeElapsed / 60))
            accuracy = round(((len(targetText) - errors) / len(targetText)) * 100)
            stdscr.clear()
            displayText(stdscr, targetText, currentText, wpm, accuracy)
            stdscr.refresh()

            # if user finish typing break the loop
            if "".join(currentText) == targetText:
                stdscr.nodelay(False)
                break

            try:
                key = stdscr.getkey()
            except Exception:
                continue

            # if user press ESC leave the test
            if ord(key) == 27:
                break

            # if user press backspace last character will be removed
            if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                errors += 0.5
                if len(currentText) > 0:
                    currentText.pop()

            # if user press space increment the word by 1
            elif key == " ":
                words += 1
                currentText.append(key)

            # else add to current text
            elif len(currentText) < len(targetText):
                currentText.append(key)

    def run(stdscr):
        # creating color pair for different text
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # start the screen
        start(stdscr)

        # run the loop until user press ESC
        while True:
            test(stdscr)

            stdscr.addstr(4, 0, "You completed the test!\nPress enter to continue..."
                                "\nPress ESC to exit.")
            key = stdscr.getkey()

            # if user press ESC break the loop
            if ord(key) == 27:
                break

    wrapper(run)

# the main driver function
def main():
    TypingTest()


# call the main driver function
if __name__ == "__main__":
    main()
