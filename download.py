import pandas as pd
import requests
import time
import os

# Read the CSV file with track IDs
df = pd.read_csv('top10s_with_track_ids.csv')

# RapidAPI credentials
rapidapi_key = 'a0ea16deb4msh92c0c8ebfd23113p1003b0jsn18b8b59efea1'
rapidapi_host = 'spotify-downloader6.p.rapidapi.com'

def get_download_url(track_id):
    url = "https://spotify-downloader6.p.rapidapi.com/spotify"
    spotify_url = f"https://open.spotify.com/track/{track_id}"
    querystring = {"spotifyUrl": spotify_url}
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": rapidapi_host
    }

    response = requests.get(url, headers=headers, params=querystring)
    result = response.json()
    print(result)  # Debugging line to inspect the response
    if 'download_link' in result:
        return result['download_link']
    else:
        return None

def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def main():
    download_dir = 'downloads'
    os.makedirs(download_dir, exist_ok=True)

    for index, row in df.iterrows():
        track_id = row['track_id']
        title = row['title']
        artist = row['artist']
        
        if track_id:
            print(f"Getting download URL for {title} by {artist} (ID: {track_id})...")
            download_url = get_download_url(track_id)
            
            if download_url:
                print(f"Downloading {title} by {artist}...")
                filename = os.path.join(download_dir, f"{title} - {artist}.mp3")
                download_file(download_url, filename)
                print(f"Downloaded {title} by {artist} to {filename}")
            else:
                print(f"Failed to get download URL for {title} by {artist}")
            
            # Sleep to avoid hitting rate limits
            time.sleep(0.1)

if __name__ == "__main__":
    main()
