from pathlib import Path
import configparser
import typer

APP_NAME = "lastfm-archiver"
app = typer.Typer()

@app.callback()
def callback():
    """
    LastFM Archiver
    """

@app.command()
def init(username = typer.Option(None, prompt=True), api_key=typer.Option(None, prompt=True)):
  """
  Initialize the archiver with a lastfm username and api key
  """
  typer.echo("Initializing the archiver...")
  app_dir = typer.get_app_dir(APP_NAME)
  Path(app_dir).mkdir(parents=True, exist_ok=True)
  config_path: Path = Path(app_dir) / "config.ini"
  config_path.touch(exist_ok=True)

  config = configparser.ConfigParser()
  config["LOCAL"] = {
    "username": username,
    "key": api_key
  }

  current_config = configparser.ConfigParser()
  current_config.read(config_path)
  if "LOCAL" in current_config:
    typer.confirm("Are you sure you want to overwrite existing configuration?", abort=True)

  with open(config_path, mode="w") as f:
    config.write(f)
  
  typer.echo("Confg file written")


@app.command()
def run():
  """
  Run archive job. Will start from  the last updated scrobble, if any.
  """
  typer.echo("Now running")


if __name__ == "__main__":
    app()