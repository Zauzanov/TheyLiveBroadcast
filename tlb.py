#!/usr/bin/env python3
import sys
import time
import shutil
import random

# ANSI colors / effects
VIOLET = "\033[35m"
WHITE  = "\033[37m"
YELLOW = "\033[33m"
RED    = "\033[31m"
RESET  = "\033[0m"

DIM    = "\033[2m"
BRIGHT = "\033[1m"
BLINK  = "\033[5m"
INVERT = "\033[7m"

CLEAR_SCREEN = "\033[2J\033[H"

NOISE_CHARS = " .,:;|/\\!@#$%^&*()_+=-~`[]{}<>?"

INTERFERENCE_PHRASES = [
    "SIGNAL DETECTED",
    "YOU ARE NOT AUTHORIZED",
    "CEASE TRANSMISSION",
    "WE SEE YOU",
    "STOP BROADCAST",
    "THIS CHANNEL IS MONITORED",
    "RETURN TO CONSUMPTION",
    "OBEY",
    "DO NOT RESIST",
    "THEY ARE WATCHING",
    "SIGNAL COMPROMISED",
]

def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()

def terminal_size():
    sz = shutil.get_terminal_size(fallback=(80, 24))
    return sz.columns, sz.lines

def build_full_width_line(text: str, width: int) -> str:
    if not text.endswith(" "):
        text += " "
    return (text * (width // len(text) + 1))[:width]

def type_line(line: str, delay: float):
    for ch in line:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)

def noise_line(width: int) -> str:
    return "".join(random.choice(NOISE_CHARS) for _ in range(width))

def crt_prefix(color: str) -> str:
    r = random.random()
    if r < 0.08:
        return DIM + color
    elif r < 0.14:
        return BRIGHT + color
    return color

def interference_style():
    return RED + random.choice([BLINK, INVERT, BRIGHT])

def type_block_for(message: str, color: str,
                   rows: int = 70,
                   seconds: float = 60.0,
                   char_delay: float = 0.0002,
                   hold_after: float = 0.2):
    start = time.time()

    while time.time() - start < seconds:
        clear()
        width, height = terminal_size()
        full_line = build_full_width_line(message, width)

        glitch = random.random() < 0.06
        interference = random.random() < 0.12  # chance of alien interference
        jitter = random.randint(0, 3) if random.random() < 0.12 else 0
        pad = " " * jitter

        phrase = random.choice(INTERFERENCE_PHRASES)

        for row in range(min(rows, height)):
            if interference and random.random() < 0.4:
                # Interference hijacks this row
                sys.stdout.write(interference_style())
                line = build_full_width_line(phrase, width)
                type_line(line, char_delay * 0.5)
                sys.stdout.write(RESET + "\n")
                continue

            style = crt_prefix(color)
            sys.stdout.write(style)

            if glitch and random.random() < 0.35:
                line = pad + noise_line(max(0, width - jitter))
                type_line(line, char_delay * 0.25)
            else:
                line = pad + full_line[:max(0, width - jitter)]
                type_line(line, char_delay)

            sys.stdout.write(RESET + "\n")

        sys.stdout.flush()
        time.sleep(hold_after)

if __name__ == "__main__":
    try:
        while True:
            type_block_for("THEY LIVE WE SLEEP         ", VIOLET, seconds=60)
            type_block_for("I AM ALL OUT OF BUBBLEGUM!          ", WHITE, seconds=60)
            type_block_for("PUT ON THE SUNGLASSES!          ", YELLOW, seconds=60)

    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")
        sys.stdout.flush()
        print("Broadcast terminated.")

