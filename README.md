# pacspin

A Pac-Man progress bar for `pacman` and `paru` on fish.

`ILoveCandy` is drawn by libalpm itself, so it can't be restyled from `pacman.conf`.
`pacspin` runs the command in a PTY and rewrites only the `[bar] NN%` part of the
output: a Pac-Man eats the dots as the real percentage grows, a ghost chases it,
and at 100% the bar fills solid. Prompts, sudo password, errors and the terminal
width pass through untouched.

## Install

```fish
fisher install alepspizzetti/pacspin
```

Requires `fish`, `python3` and a font that renders `ᗧ` `ᗣ` `●` `·` `━`.
Keep `ILoveCandy` enabled in `/etc/pacman.conf`; `pacspin` rewrites the bar it generates.

## What it wraps

| Command | Wrapped when |
|---|---|
| `pacman`, `paru` | first argument starts with `-S`, `-R` or `-U`, and stdout is a terminal |
| `sudo pacman`, `sudo paru` | same condition on the inner command |

Anything else falls through to the real command. Scripts and pipes are not affected.

## Uninstall

```fish
fisher remove alepspizzetti/pacspin
```

## License

MIT
