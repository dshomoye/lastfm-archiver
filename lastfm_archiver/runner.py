import requests
import json
import time
import typer
from pathlib import Path
from typing import Dict, Optional, List, Any
from datetime import datetime

LASTFM_ROOT = "http://ws.audioscrobbler.com/2.0"


def get_year(year: int, username: str, api_key: str) -> Optional[Dict[str, List[Any]]]:
    from_time = int(datetime(year, 1, 1).timestamp())
    to_time = int(datetime(year + 1, 1, 1).timestamp())
    page = 1
    year_scrobbles = {"scrobbles": []}
    RETRIES = 5
    while True:
        url = f"{LASTFM_ROOT}/?method=user.getRecentTracks&api_key={api_key}&format=json&user={username}&limit=1000&from={from_time}&to={to_time}&page={page}"
        res = requests.get(url)
        if res.status_code == 429:
            if RETRIES <= 0:
                return None
            RETRIES -= 1
            typer.echo("api calls rate limited.")
            for i in range(5, 1, -1):
                typer.echo(f"retying in {i}s...")
                time.sleep(1)
        if res.status_code == 200:
            res_data = res.json()
            total_pages = int(res_data["recenttracks"]["@attr"]["totalPages"])
            page = int(res_data["recenttracks"]["@attr"]["page"])
            if total_pages == 0:
                return year_scrobbles
            year_scrobbles["scrobbles"] += res_data["recenttracks"]["track"]
            if page >= total_pages:
                break
            page += 1
        else:
            error_msg = typer.style(
                f"\nerror occured for year {year}. status: {res.status_code}.\nresponse: {res.text}",
                fg=typer.colors.WHITE,
                bg=typer.colors.RED,
            )
            typer.echo(error_msg)
            return None
    return year_scrobbles


def write_json(path: Path, data: Dict[str, List[Any]]) -> None:
    if not len(data["scrobbles"]):
        return
    path.touch(exist_ok=True)
    with open(path, mode="w+") as f:
        json.dump(data, f)
