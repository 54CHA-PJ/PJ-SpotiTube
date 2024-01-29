import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import urllib.request
import re
import configparser

# Read the API data from the config file
config = configparser.ConfigParser()
config.read('APIDATA.cfg')
CLIENT_ID = config.get('DEFAULT', 'client_id', fallback='')
CLIENT_SECRET = config.get('DEFAULT', 'client_secret', fallback='')
REDIRECT_URI = config.get('DEFAULT', 'redirect_uri', fallback='')

# Define the scope for the request
SCOPE = 'user-read-playback-state'
# Initialize the Spotipy client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))
# Get the currently playing track
current_track = sp.current_playback()

# Extract the song details
if current_track is not None:
    song_name = current_track['item']['name']
    artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
    print("\n-----------------------------")
    print(f"The currently playing song is '{song_name}' by {artists}.")
    print("-----------------------------\n")
    # Define the name of the video
    name = song_name + " " + artists + " Music Video"
    # Format the name for the search query
    query = name.replace(" ", "+")
    # Get the HTML of the search results page
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
    # Find the first video URL using regular expressions
    video_url = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
    # Open the video in the web browser
    webbrowser.open("https://www.youtube.com/watch?v=" + video_url)

else:
    print("\n-----------------------------")
    print("No song is currently playing.")
    print("-----------------------------\n")
