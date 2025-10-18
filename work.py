#!/usr/bin/env python
import os
import sys
import time
import shutil
import random
import re
from datetime import datetime, timedelta

# ---------------- ANSI colors ----------------
class bcolors:
    black      = '\033[38;5;234m'
    dark1      = '\033[38;5;235m'
    dark2      = '\033[38;5;236m'
    dark3      = '\033[38;5;237m'
    dark4      = '\033[38;5;239m'
    gray       = '\033[38;5;244m'
    light0     = '\033[38;5;223m'
    light1     = '\033[38;5;230m'
    light2     = '\033[38;5;229m'
    light3     = '\033[38;5;180m'
    red        = '\033[38;5;167m'
    green      = '\033[38;5;142m'
    yellow     = '\033[38;5;214m'
    blue       = '\033[38;5;109m'
    purple     = '\033[38;5;175m'
    aqua       = '\033[38;5;108m'
    orange     = '\033[38;5;208m'

    ENDC       = '\033[0m'
    BOLD       = '\033[1m'
    UNDERLINE  = '\033[4m'


ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


# ---------------- Terminal helpers ----------------
def clear_terminal():
    os.system('cls' if sys.platform.startswith('win') else 'clear')


def restore():
    print(f'{bcolors.ENDC}')
    print('\033[?25h', end="")


def print_centered_text(text):
    """Print a single text block centered vertically and horizontally."""
    size = shutil.get_terminal_size()
    term_width, term_height = size.columns, size.lines

    lines = text.splitlines()
    top_padding = max(0, (term_height - len(lines)) // 2)

    centered_lines = []
    for line in lines:
        visual_len = len(ANSI_ESCAPE.sub('', line))
        left_padding = max(0, (term_width - visual_len) // 2)
        centered_lines.append(" " * left_padding + line)

    print("\n" * top_padding + "\n".join(centered_lines))


# ---------------- Classes ----------------
class Art:
    def __init__(self, template):
        self.lines = template.splitlines()
        self.max_art_width = max(len(ANSI_ESCAPE.sub('', line)) for line in self.lines)

    def center(self, term_width):
        centered_lines = []
        for line in self.lines:
            visual_len = len(ANSI_ESCAPE.sub('', line))
            # Center relative to terminal but preserve shape
            left_padding = max(0, (term_width - self.max_art_width) // 2)
            centered_lines.append(" " * left_padding + line)
        return "\n".join(centered_lines)

class Quote:
    def __init__(self, text, color=bcolors.green):
        self.text = f"{color}{text}{bcolors.ENDC}"

    def center(self, term_width):
        visual_len = len(ANSI_ESCAPE.sub('', self.text))
        left_padding = max(0, (term_width - visual_len) // 2)
        return " " * left_padding + self.text

class TimeLine:
    def __init__(self, left_time, countdown, right_time):
        self.left_time = left_time
        self.countdown = countdown
        self.right_time = right_time

    def center(self, term_width):
        line = f"{bcolors.purple}{bcolors.UNDERLINE}{self.left_time}{bcolors.ENDC} | goal pending {self.countdown} | {bcolors.purple}{self.right_time}{bcolors.ENDC}"
        visual_len = len(ANSI_ESCAPE.sub('', line))
        left_padding = max(0, (term_width - visual_len) // 2)
        return " " * left_padding + line

# ---------------- Display function ----------------
def display_block(art, quote, time_line):
    size = shutil.get_terminal_size()
    term_width, term_height = size.columns, size.lines

    art_block = art.center(term_width).splitlines()
    quote_line = quote.center(term_width)
    time_line_line = time_line.center(term_width)

    block_lines = art_block + [quote_line] + [time_line_line]

    # Vertical centering
    top_padding = max(0, (term_height - len(block_lines)) // 2)

    print("\n" * top_padding + "\n".join(block_lines))

# ---------------- Live display ----------------
def live_display(duration):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration)

    art_template = r'''         .        .            |       .        .        .
              *        .       |   .        .
        .                     /-\     .           .   .
 .               .    .      |"""|              :        .
         .                  /"""""\  .      *       |>.
                           | # # # |     .        /\|  ___
    __     ___   ___   .   |# # # #| ___      ___/<>\ |:::|
  / ""|  __|~~| |"""|      |# # # #||"""|  __|"""|^^| |:::|
 /""""| |::|''|~~~~||_____ |# # # #||"""|-|::|"""|''|_|   |
 |""""| |::|''|""""|:::::| |# # # #||"""|t|::|"""|''|"""""|
 |""""|_|  |''|""""|:::::| |# # # #||"""|||::|"""|''""""""|
 |""""|::::|''|""""|:::::| |# # # #||"""|||::|"""|''""""""|

{quote}
{time_line}'''

    art = Art(art_template.replace("{quote}", "").replace("{time_line}", ""))

    quotes = [
        "Keep going — small steps add up.",
        "Stay focused. Time is your ally.",
        "You're building momentum.",
        "Progress > perfection.",
        "Discipline beats motivation."
    ]

    left_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    right_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    quote_text = random.choice(quotes)
    next_quote_time = time.time() + random.randint(900, 1800)

    try:
        while True:
            now = datetime.now()
            remaining = end_time - now
            if remaining.total_seconds() <= 0:
                break

            total_seconds = int(remaining.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown = f"{hours}h {minutes}m {seconds}s"

            if time.time() >= next_quote_time:
                quote_text = random.choice(quotes)
                next_quote_time = time.time() + random.randint(900, 1800)

            clear_terminal()
            quote = Quote(quote_text)
            time_line = TimeLine(left_time, countdown, right_time)
            display_block(art, quote, time_line)

            time.sleep(1)

    except KeyboardInterrupt:
        elapsed = datetime.now() - start_time
        clear_terminal()
        print_centered_text(f"{bcolors.yellow}⚠️  Timer interrupted! ⚠️\nElapsed: {str(elapsed).split('.')[0]}\nRemaining: {str(end_time - datetime.now()).split('.')[0]}{bcolors.ENDC}")
        sys.exit(0)

    clear_terminal()
    print_centered_text(f"{left_time} | ✅ goal complete | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ---------------- Main ----------------
if __name__ == "__main__":
    try:
        print('\033[?25l', end="")  # hide cursor
        live_display(duration=14400)  # 4 hours
    finally:
        restore()
