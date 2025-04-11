import time
import eyed3
import spotipy
from pathlib import Path
from spotipy.oauth2 import SpotifyClientCredentials

SORTED_DIR = Path("/path/to/sorted/mp3")
SEARCH_WILDCARD = "*.mp3"
count = 0

#SPOTIFY APPY CONFIG
client_id = 'client-id'
client_secret = 'client-secret'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

print("artists_from_spotify by Keviannn")

#MAIN FUNCTIONALITY
for file in SORTED_DIR.rglob(SEARCH_WILDCARD): 
    count += 1
    if file.is_file():
        audio_file = eyed3.load(file)
        local_name = audio_file.tag._getTitle()
        local_artist = audio_file.tag._getArtist()
        local_album = audio_file.tag._getAlbum()

        if "/" not in local_artist:
            search_string = f'"{local_name}" {local_artist} {local_album}'
            song_search = sp.search(q=search_string, type='track', limit=1)
            song_result = song_search['tracks']['items']
            if song_result:
                song_result_first = song_result[0]
                song_result_name = song_result_first['name']
                song_result_artists = ' / '.join([artist['name'] for artist in song_result_first['artists']])
                song_result_album = song_result_first['album']['name']
                if "/" in song_result_artists:
                    print(f"\nMATCH IN FILE {count}:\n Local:\n   Artist: {local_artist}\n   Album: {local_album}\n   Name: {local_name}\n Search: \n   Artist: {song_result_artists}\n   Album: {song_result_album}\n   Name: {song_result_name}")
                    while 1:
                        answer = input("Do you want to update the artist tag with the artist found? Y/N ").lower()
                        if answer == "y":
                            print(f"Adding new artist tag ({local_artist}) --> ({song_result_artists})")
                            audio_file.tag.artist = song_result_artists
                            print(f"Done, new artist tag is {audio_file.tag._getArtist()}")
                            audio_file.tag.save()
                            break
                        elif answer == "n":
                            print("Tag not updated")
                            break
                        else:
                            print("Non valid input")
            else:
                print(f"FAILED: {search_string}")
    time.sleep(0.25)
print("---- END OF SEARCH ----")
