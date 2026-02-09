# Keyboard Trainer 500

A typing trainer application for the Raspberry Pi 500 keyboard with RGB LED support.

## Overview

This project uses the Pi 500's programmable RGB LEDs to create an interactive typing training experience. The application lights up keys that need to be pressed and provides visual feedback when incorrect keys are pressed.

## Requirements

- Raspberry Pi 500 keyboard
- Python 3
- RPiKeyboardConfig library

## Usage

Run the trainer from a terminal:

```bash
python3 kb-trainer-v3.py
```

The program will display a sentence and light up each key that needs to be pressed. If you press the wrong key, nearby keys will blink to help you find the correct one.

## Versions

- `kb-trainer-v-01.py` - Initial version
- `kb-trainer-v-02.py` - Improved version
- `kb-trainer-v3.py` - Latest version with neighbor key hints

## Resources

- [Raspberry Pi Keyboard Documentation](https://www.raspberrypi.com/documentation/computers/keyboard-computers.html#advanced-led)
- [Pi Keyboard Config Tool](https://github.com/raspberrypi/rpi-keyboard-config)

## License

See LICENSE file for details. 
