# lastfm-archiver

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


This is a script that creates json archives of [lastfm](https://last.fm) scrobbles. 

It's *your* listening data and, well, what happens if/when LastFM goes away?

This requires a LastFM api_key, you can request one [here](https://www.last.fm/api/authentication). Naturally, a LastFM account is required.

---

## Usage

```
Usage: lastfm-archiver [OPTIONS] COMMAND [ARGS]...

  LastFM Archiver

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  init  Initialize the archiver with a lastfm username, api key, and a path...
  run   Run archiving job.
```


## Commands:
### `init`
```
Usage: lastfm-archiver init [OPTIONS]

  Initialize the archiver with a lastfm username, api key, and a path to put
  archive json files. Also optionally specify the earliest year to look back
  (default 2010)

Options:
  --username TEXT
  --api-key TEXT
  --archive-path TEXT   (absolute) path to directory to store archive json
                        files  [default: /Users/damola/Library/Application
                        Support/lastfm-archiver/archive]

  --earliest-year TEXT  the earliest year to start fetching scrobbles from
                        [default: 2010]

  --help                Show this message and exit.
```
  
### run
```
  Usage: lastfm-archiver run [OPTIONS]

  Run archiving job. Will fetch all years, skipping already archived years.
  Scrobbles for current year will be merged into the json archive for the
  current year.

Options:
  --help  Show this message and exit.
```

Configuration:
- the script uses a `config.ini` file to store username and other settings (passed at `init`).
- `config.ini` file location is determined by [`typer`](https://typer.tiangolo.com/tutorial/app-dir/)


---
## Development

- Built with [typer](https://typer.tiangolo.com/). Thanks to it, I only write code and have messages, colors and everything else, for cheap.

- Package management with [poetry](https://python-poetry.org)

### Getting Started 
`poetry shell && poetry install` - this installs all depencies as well as the script as defined in the [pyproject.toml](pyproject.toml).
