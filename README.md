# pacspin

A Pac-Man progress bar for `pacman` and `paru` on fish.

`ILoveCandy` is drawn by libalpm itself, so `pacman.conf` can't restyle it.
`pacspin` runs the command in a PTY and rewrites only the `[bar] NN%` part of the
output. A Pac-Man eats the dots as the real percentage grows, a ghost chases it,
and at 100% the bar fills solid. Prompts, the sudo password, errors and the
terminal width pass through untouched.

```text
core        130,2 KiB  1,2 MiB/s 00:00 [          ᗣ   ᗧ··●····]  42%
core        130,2 KiB  1,2 MiB/s 00:00 [━━━━━━━━━━━━━━━━━━━━━━] 100%
```

## Requirements

| Item | Notes |
|---|---|
| Arch-based distro | Arch, CachyOS, EndeavourOS, Manjaro. Needs `pacman`; `paru` is optional |
| `fish` 3.4+ | Uses `path`, which was added in 3.5, so 3.5+ is safest |
| `python3` | Standard library only, no pip packages |
| Font with `ᗧ ᗣ ● · ━` | Most Nerd Fonts and terminals render them. If you see boxes, change the font |
| `ILoveCandy` in `/etc/pacman.conf` | Keep it enabled. `pacspin` rewrites the bar that option generates |

Truecolor terminals show the intended palette. Others fall back to the nearest colors.

## Install

### Fisher

```fish
fisher install alepspizzetti/pacspin
```

### install.sh

```sh
git clone https://github.com/alepspizzetti/pacspin.git
cd pacspin
./install.sh
exec fish
```

The script copies 6 files into `${XDG_CONFIG_HOME:-~/.config}/fish` (`functions/` and `conf.d/`)
and checks for `fish` and `python3` first. It does not touch `pacman.conf`, `config.fish` or anything outside that folder.

## Usage

Nothing changes in how you work. Run the usual commands:

```fish
sudo pacman -Syu
paru -S some-package
sudo pacman -Rns some-package
```

The wrapper only kicks in when all of these hold:

| Condition | Why |
|---|---|
| First argument starts with `-S`, `-R` or `-U` | Query commands (`-Q`) have no progress bar |
| stdout is a terminal | Pipes and scripts get the original output |
| Called as `pacman`, `paru`, `sudo pacman` or `sudo paru` | Those are the functions defined |

Anything else runs the real command. To bypass the wrapper once: `command pacman -Syu`.

## Compatibility

| Case | Status |
|---|---|
| fish | Supported |
| bash / zsh | Not supported, the wrappers are fish functions. `pacspin.py` can be run directly: `python3 pacspin.py pacman -Syu` |
| Scripts, cron, CI | Unaffected, the wrapper only runs on an interactive terminal |
| `sudo -E`, `doas`, other privilege tools | Not wrapped |
| Other AUR helpers (`yay`, ...) | Not wrapped. Copy `functions/paru.fish` and rename it |
| Terminal resize during an operation | Supported |

## How it works

1. `pacspin.py` forks the command inside a PTY, so pacman still thinks it talks to a terminal.
2. Output is read in chunks and held back only while a bar might be split in two.
3. Each `[...] NN%` match is replaced by a bar of the same width, with the position taken from the real percentage.
4. Everything else, including prompts and your keystrokes, is forwarded as is. The exit code is preserved.

## Uninstall

```sh
./install.sh uninstall
```

or, with Fisher:

```fish
fisher remove alepspizzetti/pacspin
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Plain `ILoveCandy` bar, no Pac-Man | Open a new shell or `exec fish`. Check `type pacman` says `function` |
| Boxes instead of Pac-Man | Terminal font lacks the glyphs |
| Broken lines or stray `38;2;...m` text | Open an issue with the output of `pacman --version` and your terminal name |
| Installed by both Fisher and `install.sh` | Use only one. Remove the other with its uninstall |

## License

MIT
