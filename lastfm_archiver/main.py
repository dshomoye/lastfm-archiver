import configparser
import typer
from datetime import datetime
from datetime import datetime
from pathlib import Path

from lastfm_archiver.runner import get_year, write_json

APP_NAME = "lastfm-archiver"
METADATA_KEY = "METADATA"
SETTINGS_KEY = "SETTINGS"

app = typer.Typer()
app_dir = typer.get_app_dir(APP_NAME)

Path(app_dir).mkdir(parents=True, exist_ok=True)
config_path: Path = Path(app_dir) / "config.ini"
config_path.touch(exist_ok=True)
current_config = configparser.ConfigParser()
current_config.read(config_path)

default_archive_dir = Path(app_dir) / "archive"
default_archive_dir = str(default_archive_dir)


@app.callback()
def callback():
    """
    LastFM Archiver
    """


@app.command()
def init(
    username=typer.Option(None, prompt=True),
    api_key=typer.Option(None, prompt=True),
    archive_path=typer.Option(
        default_archive_dir,
        prompt=True,
        help="(absolute) path to directory to store archive json files",
    ),
    earliest_year=typer.Option(
        default=2010, help="the earliest year to start fetching scrobbles from"
    ),
):
    """
    Initialize the archiver with a lastfm username, api key, and a path to put archive json files.
    Also optionally specify the earliest year to look back (default 2010)
    """
    typer.echo("Initializing the archiver...")
    if SETTINGS_KEY in current_config:
        typer.confirm(
            f"Are you sure you want to overwrite existing configuration at {str(config_path)}?", abort=True
        )
    new_config = configparser.ConfigParser()
    new_config[SETTINGS_KEY] = {
        "username": username,
        "api_key": api_key,
        "archive_path": archive_path,
        "earliest_year": earliest_year,
    }
    with open(config_path, mode="w") as f:
        new_config.write(f)

    typer.echo(typer.style(f"Config file written to {str(config_path)}", fg=typer.colors.GREEN))


@app.command()
def run():
    """
    Run archiving job. Will fetch all years, skipping already archived years.
    Scrobbles for current year will be merged into the json archive for the current year.
    """
    start_time = datetime.now()
    if SETTINGS_KEY in current_config:
        typer.echo(typer.style("starting run...", fg=typer.colors.YELLOW))
        settings = current_config[SETTINGS_KEY]
        earliest_year = int(settings["earliest_year"])
        username = settings["username"]
        api_key = settings["api_key"]
        archive_path = settings["archive_path"]
        meta = {}
        Path(archive_path).mkdir(parents=True, exist_ok=True)

        if METADATA_KEY in current_config:
            meta = dict(current_config[METADATA_KEY])

        current_year = datetime.now().year
        with typer.progressbar(range(earliest_year, current_year + 1)) as years:
            for year in years:
                y_str = str(year)
                if y_str in meta and meta[y_str] is "1" and year is not current_year:
                    continue
                year_scrobbles = get_year(year=year, username=username, api_key=api_key)
                p = Path(archive_path) / f"{year}.json"
                if not year_scrobbles:
                    continue
                write_json(p, year_scrobbles)
                meta[str(year)] = "1"
                current_config[METADATA_KEY] = dict(meta)
                with open(config_path, mode="w") as f:
                    current_config.write(f)
        typer.echo(
            typer.style(
                f"🚀 updated in {(datetime.now() - start_time).total_seconds()}s 🚀",
                fg=typer.colors.GREEN,
            )
        )
    else:
        typer.echo(
            typer.style(
                "archiver has not been initialized.",
                fg=typer.colors.WHITE,
                bg=typer.colors.RED,
            )
        )
        typer.Exit(code=1)


if __name__ == "__main__":
    app()
