import threading
from random import choice
from time import sleep
from typing import Tuple

import click
import os

from inputimeout import inputimeout, TimeoutOccurred


class LongInputException(Exception):
    pass


def choose_difficulty(difficulty: int) -> Tuple[str, int]:
    """Choose a difficulty and choose an random word from the words list file
        :param difficulty: The difficulty to choose 1 or 2 for easy or hard
        :return Tuple[str, int]: returns the random word chosen from set of files and timer
                                timer for the appropriate difficulty
    """

    hard_file_list = ["D:/HangmanCode/hardfruit.txt",
                      "D:/HangmanCode/hardMedical.txt",
                      "D:/HangmanCode/hardInsect.txt"]

    easy_file_list = ["D:/HangmanCode/normInsect.txt",
                      "D:/HangmanCode/normUanimal.txt"]
    vocabulary = []
    seconds = 120
    # Difficulty Level 1 Time 120
    if difficulty == 1:
        file_path = choice(easy_file_list)
        with open(file_path) as f:
            vocabulary = f.read().split("\n")
    # Difficulty Level 2 Time 360
    elif difficulty == 2:
        file_path = choice(hard_file_list)
        with open(file_path) as f:
            vocabulary = f.read().split("\n")
            seconds = 360
    return choice(vocabulary), seconds


def hangman():
    while True:
        os.system("cls")
        try:
            difficulty = click.prompt("Enter difficulty (1.Easy,2.Hard)", show_choices=True, type=int)
        except ValueError:
            difficulty = 1
        secret_word, seconds = choose_difficulty(difficulty)

        guessed_letters = set()

        if difficulty == 1:
            attempts = 6
        else:
            attempts = 10

        def write_score(score: int, level: int):
            """Fucnction write score to file
                :param score: score of the play
                :param level: difficulty level
            """
            if level == 1:
                with open("scoreboard_easy.txt", "r") as f:
                    temp = f.read().split("\n")
                    temp.remove("")
                    score_board = [int(x) for x in temp]

                score_board.append(score)
                score_board.sort(reverse=True)

                print(score_board)
                with open("scoreboard_easy.txt", "w") as f:
                    for x in score_board:
                        f.writelines(str(x) + "\n")
            # Difficulty Level 2 Time 360
            elif difficulty == 2:
                with open("scoreboard_hard.txt", "r") as f:
                    temp = f.read().split("\n")
                    temp.remove("")
                    score_board = [int(x) for x in temp]

                score_board.append(score)
                score_board.sort(reverse=True)

                print(score_board)
                with open("scoreboard_easy.txt", "w") as f:
                    for x in score_board:
                        f.writelines(str(x) + "\n")

        def is_game_over(interval, level):
            """Fucnction to stop the game if condition is meet and write score
                to file depending on difficulty and score is the time take to guess
                :param interval: starting time for different difficulty
                :param level: difficulty level
            """
            if set(secret_word) <= guessed_letters:
                click.echo("Congratulations! You guessed the word correctly!")
                write_score(interval, level)
                return True
            if attempts <= 0:
                render_losing_screen()
                print(f"Game over! The word was: {secret_word}")
                return True
            return False

        def timer_thread(interval, level):
            """Fucnction to create a timer using thread
                :param interval: starting time for different difficulty
                :param level: difficulty level
            """
            temp = interval
            for remaining_time in range(interval, 0, -1):
                sleep(1)
                temp = temp - 1
                if is_game_over(temp, level):
                    return
            render_losing_screen()
            print("Time's up! Game over.")
            print("Sorry, you ran out of attempts. The word was", secret_word)

        timer = threading.Thread(target=timer_thread, args=(seconds, difficulty))
        timer.start()

        # check attempts to continue reading input and displaying each turn value
        while attempts > 0 or set(secret_word) <= guessed_letters:
            display_word = ""
            for letter in secret_word:
                if letter in guessed_letters:
                    display_word += letter
                else:
                    display_word += "_"

            click.echo(display_word)
            print("Attempts left:", attempts)

            # Check input format and time allow for input
            try:
                guess = inputimeout(prompt="Guess a letter: ", timeout=20)

                if len(guess) >= 2:
                    raise LongInputException("Only one letter")

                if guess in guessed_letters:
                    os.system('cls')
                    print("You already guessed that letter. Try again!")
                    continue

                guessed_letters.add(guess)
                if guess not in secret_word:
                    os.system('cls')
                    attempts -= 1
                    print("Wrong guess!")
                    draw_hangman(attempts)

            except LongInputException:
                print("You can only write 1 character only")
                continue

            except TimeoutOccurred:
                if set(secret_word) <= guessed_letters:
                    break
                attempts -= 1

        # wait for threads to finish before continuing to stop create new thread
        timer.join()
        if not click.confirm('Do you want to continue?'):
            exit(0)


def render_losing_screen():
    """Render the moving hanging screen for 20 seconds"""
    hanged_pic = ["   ------------\n"
                  "   |         /\n"
                  "   |        O\n"
                  "   |       /|\\\n"
                  "   |       / \\\n"
                  "   |         \n"
                  "   |         \n"
                  "   |         \n"
                  "   |         \n"
                  "-------        ",
                  "   ------------\n"
                  "   |          |\n"
                  "   |          O\n"
                  "   |         /|\\\n"
                  "   |         / \\\n"
                  "   |           \n"
                  "   |           \n"
                  "   |           \n"
                  "   |           \n"
                  "-------        ",
                  "   ------------\n"
                  "   |           \\\n"
                  "   |            O\n"
                  "   |           /|\\\n"
                  "   |           / \\\n"
                  "   |             \n"
                  "   |             \n"
                  "   |             \n"
                  "   |             \n"
                  "-------        ",
                  "   ------------\n"
                  "   |          |\n"
                  "   |          O\n"
                  "   |         /|\\\n"
                  "   |         / \\\n"
                  "   |           \n"
                  "   |           \n"
                  "   |           \n"
                  "   |           \n"
                  "-------        "]
    n = 0
    for i in range(20, 0, -1):
        os.system('cls')
        click.echo(hanged_pic[n])
        n = (n + 1) % len(hanged_pic)
        sleep(0.1)
    os.system('cls')
    click.echo(hanged_pic[-1])
    click.echo("Game finished")


def draw_hangman(attempts):
    """Draw the hangman pattern in cli"""
    stages = [
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     /
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |
        """,
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |
        """,
        """
           --------
           |      |
           |      O
           |
           |
           |
        """,
        """
           --------
           |      |
           |
           |
           |
           |
        """
    ]

    print(stages[attempts])


# Run the game
if __name__ == "__main__":
    hangman()
