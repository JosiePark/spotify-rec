import requests
from bs4 import BeautifulSoup
import logging

from spotifyRec.config import GENIUS_CLIENT_ACCESS_TOKEN

logger = logging.getLogger(__name__)

def format_track_title(track_title):
    """Processes the spotify returned track name to a format used
    by the genius api

    Args:
        artist_name (str): name of track returned by spotify

    Returns:
        str: formatted track name
    """
    if type(track_title) is int:
        track_title = str(track_title)

    track_title = track_title.strip().replace(' ','-').lower()

    return track_title

def format_artist_name(artist_name):
    """Processes the spotify returned artist name to a format used
    by the genius api

    Args:
        artist_name (str): name of artist returned by spotify

    Returns:
        str: formatted artist name
    """
    artist_name = artist_name.strip().replace(' ','-').lower().capitalize()

    return artist_name

def make_genius_url(track_title, artist_name):
    """Given the artist name and track title, the necessary url
    to call from the genius api is return

    Args:
        track_title (str): name of track
        artist_name (str): name of artist

    Returns:
        str: genius url for the track
    """
    song_url = '{}-{}-lyrics'.format(
        format_artist_name(artist_name),
        format_track_title(track_title)
    )
        
    base_url = 'genius.com'
    genius_url = f"https://{base_url}/{song_url}"

    return genius_url

def get_lyrics(genius_url):
    """Reads lyrics from the genius API given the relevant url

    Args:
        genius_url (str): The url of the track on genius.com

    Returns:
        str: lyrics of the song where \n is used to denote a new line
    """
    request = requests.get(genius_url)
    soup = BeautifulSoup(request.content, 'lxml')

    lyrics = ''
    for tag in soup.select('div[class^="Lyrics__Container"], .song_body-lyrics p'):
        t = tag.get_text(strip=True, separator='\n')
        if t:
            lyrics += t

    return lyrics

def add_lyrics_to_data(tracks_df):
    """Functuion that adds lyrics extracted from genius for each song
    in the tracks dataframe

    Args:
        tracks_df (pandas DataFrame): processed dataframe with track data

    Returns:
        pandas DataFrame: the tracks_df with an added column containing the lyrics
    """

    logger.info("Adding lyrics to tracks data frame")

    tracks_df['genius_url'] = tracks_df.apply(
        lambda x: make_genius_url(x.name, x.main_artist), 
        axis=1
        )
    
    tracks_df['lyrics'] = tracks_df['genius_url'].apply(get_lyrics)

    tracks_df.drop(
        columns = ['genius_url'], 
        inplace = True
        )

    return tracks_df