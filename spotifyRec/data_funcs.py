import pandas as pd
import logging
import os
from bs4 import BeautifulSoup

from spotifyRec.api_funcs import authenticate_spotify, read_from_api

logger = logging.getLogger(__name__)


def extract_artist_from_col(artist_info):
    """Extracts a list of artist names associated with a track

    Args:
        artist_info (dict): Artist metadata associated with a track

    Returns:
        list (str): list of artist names
    """
    artists = [
        artist["name"] for artist in artist_info if artist["type"] == "artist"
    ]
    return artists


def extract_artist_id_from_col(artist_info):
    """Extracts a list of artist IDs associated with a track

    Args:
        artist_info (dict): Artist metadata associated with a track

    Returns:
        list (str): list of artist IDs
    """
    artists = [
        artist["id"] for artist in artist_info if artist["type"] == "artist"
    ]
    return artists


def process_artists(artists_data):
    """Converts JSON object containing information on a users top artists into
    a pandas dataframe, while processing the followers column to extract
    the total number of followers

    Args:
        artists_data (dict): list of JSON objects returned by spotify api call

    Returns:
        pandas DataFrame: dataframe with processed artist data
    """

    artists_df = pd.DataFrame(artists_data)
    artists_df["followers"] = artists_df["followers"].apply(
        lambda x: x["total"]
    )
    cols_to_keep = ["id", "uri", "type", "name", "genres", "followers"]
    artists_df = artists_df[cols_to_keep]

    return artists_df


def process_tracks(tracks_data):
    """Converts JSON object containing information on a user top tracks
    into a pandas dataframe while extracting data on individual 
    artists featuring on the track and the album that the track is feature in.

    Args:
        tracks_data (dict): list of JSON objects returned by spotify API call

    Returns:
        pandas dataframe: processesed dataframe
    """

    tracks_df = pd.DataFrame(tracks_data)

    # artist data
    tracks_df["artists_id"] = tracks_df["artists"].apply(
        extract_artist_id_from_col
    )
    tracks_df["artist_names"] = tracks_df["artists"].apply(
        extract_artist_from_col
    )

    # album data
    tracks_df["album_id"] = tracks_df["album"].apply(lambda x: x["id"])
    tracks_df["album_name"] = tracks_df["album"].apply(lambda x: x["name"])
    tracks_df["album_release_date"] = tracks_df["album"].apply(
        lambda x: x["release_date"]
    )
    tracks_df["album_uri"] = tracks_df["album"].apply(lambda x: x["uri"])
    tracks_df["album_type"] = tracks_df["album"].apply(lambda x: x["type"])

    cols_to_keep = [
        "artists_id",
        "artist_names",
        "album_id",
        "album_name",
        "album_release_date",
        "album_uri",
        "album_type",
        "duration_ms",
        "explicit",
        "href",
        "id",
        "name",
        "popularity",
        "uri",
    ]

    tracks_df = tracks_df[cols_to_keep]

    return tracks_df


def add_audio_features(sp, tracks_df):
    """Reads audio features from the spotify API using the id column
    in the tracks dataframe and adds these columns to the tracks dataframe

    Args:
        sp : Spotify OAuth
        tracks_df (pandas DataFrame): dataframe with procesed tracks

    Returns:
        pandas DataFrame: dataframe containing the original tracks data 
                          plus associated audio features
    """

    audio_feature_data = sp.audio_features(tracks_df.id)
    audio_feature_df = pd.DataFrame(audio_feature_data)

    cols_to_keep = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "time_signature",
        "id",
    ]

    audio_feature_df = audio_feature_df[cols_to_keep]

    merged_df = tracks_df.merge(audio_feature_df, on="id", how="left")

    return merged_df


def get_user_data(to_save=True, save_dir="data"):

    """Reads your top artists and tracks played on spotify,
    converts and processes into a dataframe, and optionally saves to file

    Args:
        to_save (bool, optional): Whether to save the data to file. Defaults to True.
        save_dir (str, optional): Directory in which to save the data. Defaults to "data".

    Returns:
        tuple containing
        - tracks_df (pandas dataframe) : dataframe containing processed top tracks
        - artists_df (pandas dataframe) : dataframe containing processed top artists
    """

    sp = authenticate_spotify()

    logger.info("Reading Top Artists from API")
    artist_api_call = sp.current_user_top_artists()
    top_artists = read_from_api(sp, artist_api_call)
    artists_df = process_artists(top_artists)

    logger.info("Reading top Tracks from API")
    track_api_call = sp.current_user_top_tracks()
    top_tracks = read_from_api(sp, track_api_call)
    tracks_df = process_tracks(top_tracks)

    logger.info("Reading audio features for users favourite tracks")
    tracks_df = add_audio_features(sp, tracks_df)

    if to_save:
        logger.info("Writing user data to file")
        artists_df.to_csv(os.path.join(save_dir, "artists_data.csv"))
        tracks_df.to_csv(os.path.join(save_dir, "tracks_data.csv"))

    return tracks_df, artists_df

def get_song_lyrics(track_name, track_artist):

    base_url = 'https://api.genius.com'


    return
