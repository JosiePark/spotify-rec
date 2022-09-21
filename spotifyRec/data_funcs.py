import pandas as pd

def extract_followers_from_col(followers):

    followers = followers['total']
    return followers


def extract_artist_from_col(artist_info):

    artists = [artist['name'] for artist in artist_info if artist['type'] == 'artist']
    return artists

def extract_artist_id_from_col(artist_info):
    artists = [artist['id'] for artist in artist_info if artist['type'] == 'artist']
    return artists


def process_artists(artists_data):

    artists_df = pd.DataFrame(artists_data)
    artists_df['followers'] = artists_df['followers'].apply(extract_followers_from_col)
    cols_to_keep = [
        'id',
        'uri',
        'type',
        'name',
        'genres',
        'followers'
    ]
    artists_df = artists_df[cols_to_keep]

    return artists_df

def process_tracks(tracks_data):

    tracks_df = pd.DataFrame(tracks_data)
    
    # artist data
    tracks_df['artists_id'] = tracks_df['artists'].apply(extract_artist_id_from_col)
    tracks_df['artist_names'] = tracks_df['artists'].apply(extract_artist_from_col)
    
    # album data
    tracks_df['album_id'] = tracks_df['album'].apply(lambda x: x['id'])
    tracks_df['album_name'] = tracks_df['album'].apply(lambda x: x['name'])
    tracks_df['album_release_date'] = tracks_df['album'].apply(lambda x: x['release_date'])
    tracks_df['album_uri'] =  tracks_df['album'].apply(lambda x: x['uri'])
    tracks_df['album_type'] =  tracks_df['album'].apply(lambda x: x['type'])

    cols_to_keep = [
        'artists_id',
        'artist_names',
        'album_id',
        'album_name',
        'album_release_date',
        'album_uri',
        'album_type'
    ]

    tracks_df = tracks_df[cols_to_keep]

    return tracks_df