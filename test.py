
import pandas as pd
import requests
import base64
import time

client_id = 'fa9e11477a0d432a98c5547fe16a1d5d'
client_secret = '57ac6468ed5348d6abe7875c3f4ba1e6'

def get_access_token(client_id, client_secret):
    # Encode the client ID and client secret
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    # Get the access token
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = r.json()
    return token_response_data["access_token"]

def get_track_id(access_token, title, artist):
    search_url = "https://api.spotify.com/v1/search"
    search_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    search_params = {
        "q": f"track:{title} artist:{artist}",
        "type": "track",
        "limit": 1
    }

    response = requests.get(search_url, headers=search_headers, params=search_params)
    search_results = response.json()

    if search_results['tracks']['items']:
        return search_results['tracks']['items'][0]['id']
    else:
        return None

def main():
    # Read the CSV file
    df = pd.read_csv('top10s.csv', encoding='latin1')  # You can also try 'utf-16' or 'ISO-8859-1' if 'latin1' does not work

    # Get access token
    access_token = get_access_token(client_id, client_secret)

    # Prepare the new data
    new_data = {
        "track_id": [],
        "title": [],
        "artist": []
    }

    # Loop through each song in the DataFrame
    for index, row in df.iterrows():
        title = row['title']
        artist = row['artist']
        
        # Get the track ID
        track_id = get_track_id(access_token, title, artist)
        
        # Append the data
        new_data['track_id'].append(track_id)
        new_data['title'].append(title)
        new_data['artist'].append(artist)
        
        # Sleep to avoid hitting rate limits
        time.sleep(0.1)

    # Create a new DataFrame
    new_df = pd.DataFrame(new_data)

    # Save the new DataFrame to a CSV file
    new_df.to_csv('top10s_with_track_ids.csv', index=False)

if __name__ == "__main__":
    main()