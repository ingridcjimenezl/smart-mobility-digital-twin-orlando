import requests
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

#Public Bird GBFS feed for Orlando
BIRD_URL = "https://mds.bird.co/gbfs/v2/public/orlando/free_bike_status.json"

#Historical data file
OUTPUT_FILE = Path ("data/bird_orlando_history.csv")

def collect_bird_data ():
    cutoff = datetime (2026, 11, 23, 2, 0, tzinfo=timezone.utc)
    if datetime.now(timezone.utc)> cutoff:
        print ("Collection period ended. No more data will be collected.")
        return
    response = requests.get (BIRD_URL, timeout=30)
    response.raise_for_status()

    data = response.json ()
    vehicles = data.get ("data", {}).get ("bikes",[])

    if not vehicles:
        raise ValueError ("No vehicles returned by bird")
    df = pd.DataFrame (vehicles)

    # Record the collection date and local time
    df ["collection_time"] = datetime.now (timezone.utc).isoformat()

    # Create folder if it does not exist
    OUTPUT_FILE.parent.mkdir (parents=True, exist_ok=True)

    #Append this snapshot to the historical CSV
    df.to_csv (
      OUTPUT_FILE,
      mode ="a",
      header = not OUTPUT_FILE.exists (),
      index=False
    )
    print(f"Collection successful: {len(df)} vehicles")
    print(f"Saved to: {OUTPUT_FILE}")
if __name__ == "__main__":
    collect_bird_data ()
