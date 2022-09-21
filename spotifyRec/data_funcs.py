import pandas as pd

def extract_followers_from_col(followers):

    followers = followers['total']
    return followers


def extract_artist_from_col(artist_info):

    artists = [artist['name'] for artist in artist_info if artist['type'] == 'artist']
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
    tracks_df['artists'] = tracks_df['artists'].apply(extract_artist_from_col)

    tracks_df['album_id'] = tracks_df['album'].apply(lambda x: x['id'])
    tracks_df['album_name'] = tracks_df['album'].apply(lambda x: x['name'])
    tracks_df['album_release_date'] = tracks_df['album'].apply(lambda x: x['release_date'])
    tracks_df['album_uri'] =  tracks_df['album'].apply(lambda x: x['uri'])

    return tracks_df