# Album Bot

Queries the Spotify API and posts newly released albums in a given genre to Reddit.


# Installation

1. Install python 3.8+.
2. Install [Poetry](https://python-poetry.org/docs/#installation/)
3. `cd` into the project directory and run `poetry install` to install dependencies.
4. Edit the `.env` file
5. From the project root, run `poetry run python -m albumbot`.
6. If you want to run this automatically, set up hosting, do the first run to populate the database and then run with `cron` or similar.
