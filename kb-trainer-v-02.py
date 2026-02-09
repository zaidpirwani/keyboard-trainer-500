import sys
import termios
import tty
import time
import random

from RPiKeyboardConfig import RPiKeyboardConfig

if not sys.stdin.isatty():
    raise RuntimeError(
        "This program must be run from a real terminal (not IDLE or an IDE)."
    )

# Define keyboard rows with their starting LED index
KEYBOARD_ROWS = [
    ("qwertyuiop", 32),
    ("asdfghjkl", 47),
    ("zxcvbnm", 62),
]

# Build the mapping dictionary
LETTER_TO_LED = {
    char: base + index
    for row, base in KEYBOARD_ROWS
    for index, char in enumerate(row)
}

def letter_to_led(char: str) -> int:
    """
    Convert a single letter to its LED index.
    """
    char = char.lower()
    if char not in LETTER_TO_LED:
        raise ValueError(f"Unsupported character: {char}")
    return LETTER_TO_LED[char]

def get_single_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

NEIGHBORS = {
    "q": ["w", "a"],
    "w": ["q", "e", "a", "s"],
    "e": ["w", "r", "s", "d"],
    "r": ["e", "t", "d", "f"],
    "t": ["r", "y", "f", "g"],
    "y": ["t", "u", "g", "h"],
    "u": ["y", "i", "h", "j"],
    "i": ["u", "o", "j", "k"],
    "o": ["i", "p", "k", "l"],
    "p": ["o", "l"],

    "a": ["q", "w", "s", "z"],
    "s": ["w", "e", "a", "d", "z", "x"],
    "d": ["e", "r", "s", "f", "x", "c"],
    "f": ["r", "t", "d", "g", "c", "v"],
    "g": ["t", "y", "f", "h", "v", "b"],
    "h": ["y", "u", "g", "j", "b", "n"],
    "j": ["u", "i", "h", "k", "n", "m"],
    "k": ["i", "o", "j", "l", "m"],
    "l": ["o", "p", "k"],

    "z": ["a", "s", "x"],
    "x": ["s", "d", "z", "c"],
    "c": ["d", "f", "x", "v"],
    "v": ["f", "g", "c", "b"],
    "b": ["g", "h", "v", "n"],
    "n": ["h", "j", "b", "m"],
    "m": ["j", "k", "n"],

    " ": ["c", "v", "b", "n", "m"],
}


def random_colour():
    return (
        random.randint(0, 255),  # hue
        255,                     # full saturation
        255                      # full brightness
    )

ERROR_COLOUR = (30, 255, 255)   # yellow-orange


def blink_neighbors(keyboard, char, times=2):
    neighbors = NEIGHBORS.get(char, [])

    for _ in range(times):
        keyboard.rgb_clear()

        for n in neighbors:
            idx = letter_to_led(n)
            keyboard.set_led_by_idx(
                idx=idx,
                colour=ERROR_COLOUR  # error color
            )

        keyboard.send_leds()
        time.sleep(0.2)

        keyboard.rgb_clear()
        keyboard.send_leds()
        time.sleep(0.2)



# Defining main function
def main():
    # Initialise the keyboard
    keyboard = RPiKeyboardConfig()

    # Set LED direct control mode
    keyboard.set_led_direct_effect()

    # Clear all LEDs
    keyboard.rgb_clear()

    sentence = "the quick brown fox jumps over the lazy dog"

    for expected_char in sentence:
        keyboard.rgb_clear()

        if expected_char == " ":
            led_idx = 78
        else:
            led_idx = letter_to_led(expected_char)

        main_colour = random_colour()

        keyboard.set_led_by_idx(
            idx=led_idx,
            colour=main_colour
        )
        keyboard.send_leds()

        while True:
            key = get_single_key()

            if key == expected_char:
                print(key, end="", flush=True)
                break
            else:
                blink_neighbors(keyboard, expected_char)

                keyboard.rgb_clear()
                keyboard.set_led_by_idx(
                    idx=led_idx,
                    colour=main_colour
                )
                keyboard.send_leds()

    keyboard.rgb_clear()
    keyboard.send_leds()


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
