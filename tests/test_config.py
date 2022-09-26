import spotifyRec.config

def test_load_config():
    config_file = 'tests/test_config.ini'
    config = spotifyRec.config.load_config(config_file=config_file)
    test_client_id = config.get("api_settings", "client_id")
    assert test_client_id == "abc"
