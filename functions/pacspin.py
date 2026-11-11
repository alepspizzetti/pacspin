#!/usr/bin/env python3
import fcntl
import os
import pty
import re
import select
import signal
import struct
import sys
import termios
import tty

CYAN = "\x1b[38;2;139;233;253m"
YELLOW = "\x1b[38;2;241;250;140m"
MUTED = "\x1b[38;2;98;114;164m"
GHOST = "\x1b[38;2;255;184;255m"
RESET = "\x1b[0m"

ANSI = r"\x1b\[[0-9;]*m"
CELL = rf"(?:{ANSI}|[^\[\]\r\n\x1b])"
BAR = re.compile(rf"(?<!\x1b)\[((?:{CELL}){{4,}})\]( +)(\d{{1,3}})%")
PARTIAL = re.compile(rf"(?<!\x1b)\[{CELL}*(?:\x1b\[?[0-9;]*)?\]? *\d{{0,3}}$")
ANSI_RE = re.compile(ANSI)
TERMINATORS = re.compile(r".*[\r\n]", re.S)


class Candy:
    def __init__(self):
        self.chomp = 0

    def render(self, width, percent):
        if percent >= 100:
            return f"{CYAN}{'━' * width}{RESET}"
        pos = round(percent / 100 * (width - 1))
        self.chomp += 1
        pac = "ᗧ" if self.chomp % 2 else "●"
        ghost_pos = pos - 4
        cells = []
        for i in range(width):
            if i == pos:
                cells.append(f"{CYAN}{pac}{RESET}")
            elif i == ghost_pos:
                cells.append(f"{GHOST}ᗣ{RESET}")
            elif i < pos:
                cells.append(" ")
            elif i % 5 == 0:
                cells.append(f"{YELLOW}●{RESET}")
            else:
                cells.append(f"{MUTED}·{RESET}")
        return "".join(cells)

    def rewrite(self, text):
        def swap(match):
            width = len(ANSI_RE.sub("", match.group(1)))
            return f"[{self.render(width, int(match.group(3)))}]{match.group(2)}{match.group(3)}%"

        return BAR.sub(swap, text)


def copy_window_size(source_fd, target_fd):
    try:
        size = fcntl.ioctl(source_fd, termios.TIOCGWINSZ, b"\0" * 8)
        fcntl.ioctl(target_fd, termios.TIOCSWINSZ, size)
    except OSError:
        pass


def split_pending(text):
    last = None
    for match in TERMINATORS.finditer(text):
        last = match.end()
    if last is None:
        head, tail = "", text
    else:
        head, tail = text[:last], text[last:]
    if tail and not PARTIAL.search(tail):
        head, tail = head + tail, ""
    return head, tail


def run(command):
    stdin_fd = sys.stdin.fileno()
    stdout_fd = sys.stdout.fileno()
    pid, master = pty.fork()
    if pid == 0:
        os.execvp(command[0], command)

    copy_window_size(stdout_fd, master)
    signal.signal(signal.SIGWINCH, lambda *_: copy_window_size(stdout_fd, master))

    interactive = os.isatty(stdin_fd)
    saved = termios.tcgetattr(stdin_fd) if interactive else None
    if interactive:
        tty.setraw(stdin_fd)

    candy = Candy()
    pending = ""
    decoder_tail = b""
    try:
        while True:
            try:
                ready, _, _ = select.select([master, stdin_fd], [], [])
            except InterruptedError:
                continue
            if stdin_fd in ready:
                data = os.read(stdin_fd, 1024)
                if data:
                    os.write(master, data)
            if master in ready:
                try:
                    data = os.read(master, 4096)
                except OSError:
                    break
                if not data:
                    break
                raw = decoder_tail + data
                text = raw.decode("utf-8", errors="ignore")
                decoder_tail = b""
                head, pending = split_pending(pending + text)
                if head:
                    os.write(stdout_fd, candy.rewrite(head).encode())
        if pending:
            os.write(stdout_fd, candy.rewrite(pending).encode())
    finally:
        if saved is not None:
            termios.tcsetattr(stdin_fd, termios.TCSADRAIN, saved)

    _, status = os.waitpid(pid, 0)
    return os.waitstatus_to_exitcode(status)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("uso: pacspin <comando> [args...]")
    sys.exit(run(sys.argv[1:]))
