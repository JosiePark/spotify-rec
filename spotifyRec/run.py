import argparse
import logging
from datetime import datetime

import spotifyRec.data_funcs

run_time = datetime.now().strftime("%Y-%m-%d")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"logs/spotify_app_{run_time}.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--read_data", action="store_true")
    args = parser.parse_args()

    if args.read_data:
        logger.info("Reading data")
        tracks_df, artists_df = spotifyRec.data_funcs.get_user_data()
