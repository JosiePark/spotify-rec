import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

from spotifyRec.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

logger = logging.getLogger(__name__)


def authenticate_spotify():
    """Authenticates the spotify API using you client credentials
    It requires client_id and client_secret to be stored as global variables

    Returns:
       spotipy.client.Spotify object
    """

    logger.info("Authenticating the Spotify API")
    scope = "user-library-read user-follow-read user-top-read playlist-read-private"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
        )
    )

    return sp


def read_from_api(sp, api_call):
    """Get all artists/tracks from a Spotify API call

    Args:
        sp : Spotify OAuth
        api_call : API function call

    Returns:
        list of artists or tracks
    """

    results = api_call
    if "items" not in results.keys():
        results = results["artists"]
    data = results["items"]

    while results["next"]:
        results = sp.next(results)
        if "items" not in results.keys():
            results = results["artists"]
        data.extend(results["items"])

    return data
