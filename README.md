# spotify-rec

WIP

## Installation and set-up instructions

This package has been built with poetry. Therefore, you will need to:

1. Install poetry
2. Install package

using the commands below

```bash
pip install poetry
poetry install
```

In order to run the package yourself, you will need to add your Spotify credentials to configs/settings.ini. These can be found from ... You also need to authenticate the Genius API.

```bash
[api_settings]
client_id =
client_secret =
redirect_uri =

[genius_settings]
client_id = 
client_secret = 
client_access_token = 
```



## How to run

```bash
python spotifyRec/run.py (--read_data)
```

Include the --read_data argument if you haven't already read data from the spotify API and stored locally.
