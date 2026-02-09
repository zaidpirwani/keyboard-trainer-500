import sys
import termios
import tty
import time
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
        # Clear previous LED
        keyboard.rgb_clear()

        # Determine LED index
        if expected_char == " ":
            led_idx = 78
        else:
            led_idx = letter_to_led(expected_char)

        # Light expected key
        keyboard.set_led_by_idx(
            idx=led_idx,
            colour=(0, 255, 255)
        )
        keyboard.send_leds()

        # Wait for correct keypress
        while True:
            key = get_single_key()

            if key == expected_char:
                print(key, end="", flush=True)
                break
            # wrong key: ignored completely

    keyboard.rgb_clear()
    keyboard.send_leds()




# Using the special variable 
# __name__
if __name__=="__main__":
    main()




# Initialise the keyboard
#keyboard = RPiKeyboardConfig()

# Set LED direct control mode
#keyboard.set_led_direct_effect()

# Set individual LED by index (HSV format: hue, saturation, value)
# keyboard.set_led_by_idx(idx=5, colour=(0, 255, 255))      # Red
# keyboard.set_led_by_idx(idx=6, colour=(85, 255, 255))     # Green
# keyboard.set_led_by_idx(idx=7, colour=(170, 255, 255))    # Cyan

# Set LED by matrix position
#keyboard.set_led_by_matrix(matrix=[2, 3], colour=(42, 255, 255))  # Orange

# Send LED updates to keyboard (required after setting colours)
# keyboard.send_leds()

# Clear all LEDs
# keyboard.rgb_clear()

# 32 is q
# 47 is a
# 62 is z


