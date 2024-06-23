from flask import Flask
import requests
import base64

app = Flask(__name__)



client_id = 'fa9e11477a0d432a98c5547fe16a1d5d'
client_secret = '57ac6468ed5348d6abe7875c3f4ba1e6'

@app.route('/main')
def main():
    # Encode client_id and client_secret to base64
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')

    # Prepare the authentication request
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_headers = {
        'Authorization': f'Basic {auth_header}'
    }

    # Send the authentication request
    response = requests.post(auth_url, data=auth_data, headers=auth_headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"Access Token: {token}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    
    # Replace 'YOUR_ACCESS_TOKEN' with your actual Spotify access token
    access_token = token
    # id = '11dFghVXANMlKmJXsNCbNl'
    # API endpoint URL
    url = 'https://api.spotify.com/v1/audio-analysis/11dFghVXANMlKmJXsNCbNl'

    # Headers with Authorization
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send GET request to the Spotify API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Extract pitches from segments
        pitches = []
        for segment in data['segments']:
            pitches.extend(segment['pitches'])
        
        # Write pitches to a file
        with open('pitches.txt', 'w') as file:
            for pitch in pitches:
                file.write(f"{pitch}\n")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return data

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
