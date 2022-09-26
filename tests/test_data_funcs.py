import spotifyRec.data_funcs

def test_extract_artist_from_col():

    artist_info = [
        {"name": "a", "type" : "artist", "info" :"a1"},
        {"name": "b", "type" : "not_artist", "info" : "b1"},
        {"name": "c", "type" : "artist", "info" : "c1"}
    ]

    print(artist for artist in artist_info)

    artists = spotifyRec.data_funcs.extract_artist_from_col(artist_info)

    assert artists[0] == "a"
    assert artists[1] == "c"