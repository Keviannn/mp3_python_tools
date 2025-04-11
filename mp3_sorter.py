import os
import eyed3
from pathlib import Path
import shutil

UNSORTED_DIR = Path("/path/to/unsorted/mp3")
SORTED_DIR = Path("/path/to/sorted/mp3")
tags_edited = 0
empty_tags = 0
empty_tags_arr = [1, 1, 1]
user_input = ""
first_artist = ""
artist = ""

def error_msg(msg):
    print(f"\n----- Error -----\nError: {msg}\n")

def exception_msg(msg, exception):
    print(f"\n----- Error -----\nError: {msg}")
    print(f"Exception Type: {type(exception).__name__}\nMessage: {exception}\n")

def add_tags(audio_file, empty_tags_arr):
    if empty_tags_arr[0] == 0:
        audio_file.tag.title = input("Write title: ")
    if empty_tags_arr[1] == 0:
        audio_file.tag.artist = input("Write artist (if more than one artist1/artist2/...): ")
    if empty_tags_arr[2] == 0:
        audio_file.tag.album = input("Write album: ")
    global tags_edited 
    tags_edited = 1

if __name__ == "__main__":
    print("mp3_sorter by Keviannn")
    print("Remember using \" / \" to differentiate artists.")
    for file in UNSORTED_DIR.iterdir():
        tags_edited = 0
        empty_tags = 0
        empty_tags_arr = [1, 1, 1]

        if file.is_file():
            audio_file = eyed3.load(file)
            if audio_file is None:
                error_msg(f"File \"{file.name}\" does not have ID3 tag or is not an mp3 file")
            else:
                print(f'\nProcesing \"{file.name}\"...')

                print(f"Name: {audio_file.tag.title} \nArtist: {audio_file.tag.artist} \nAlbum: {audio_file.tag.album}")
    
                if audio_file.tag.title is None:
                    empty_tags_arr[0] = 0
                if audio_file.tag.artist is None:
                    empty_tags_arr[1] = 0
                if audio_file.tag.album is None:
                    empty_tags_arr[2] = 0
                if 0 in empty_tags_arr:
                    error_msg(f"File \"{file.name}\" does not have values into some tags.")
                    while 1:
                        user_input = input("Do you want to input them? Y/N ")
                        if user_input.lower() == "y":
                            add_tags(audio_file, empty_tags_arr)
                            break
                        elif user_input.lower() == "n":
                            error_msg(f"File \"{file.name}\" won't be processed due to lack of information in tags")
                            break
                        else:
                            print("Non valid input")
                            continue

                if user_input.lower() == "n":
                    continue
                
                artist = audio_file.tag._getArtist()
                try:
                    if "/" in artist:
                        #Check if the name are various artists or just one to asign album_artist tag
                        first_artist = artist.split(' / ')[0]
                    elif "," in artist:
                        while 1:
                            answer = input(f"Are artist {artist} various artists? Y/N ").lower()
                            if answer == "y":
                                artist = artist.replace(",", " /")
                                while 1:
                                    answer = input(f"Is this artist tag ({artist}) now correct? Y/N ").lower()
                                    if answer == "y":
                                        audio_file.tag.artist = artist
                                        first_artist = artist.split(' / ')[0]
                                        print("New tag added")
                                    elif answer == "n":
                                        artist = input(f"Write the correct tag (now {artist}): ")
                                    else:
                                        print("Non valid input")
                            elif answer == "n":
                                break
                            else:
                                print("Non valid input")
                    else:
                        first_artist = artist
                except Exception as e:
                    exception_msg(f"Could not split artist tag", e)
                    break

                #Add album_artist tag for all music so multi-artist songs get in the same album
                if audio_file.tag.album_artist is None:
                    print("No album_artist tag, adding one...")
                    audio_file.tag.album_artist = first_artist
                    print(f'New album_artist: {audio_file.tag._getAlbumArtist()}')
                    tags_edited = 1
                    print("Tags edited: 1")
                else:
                    print(f'Existing album_artist tag is {audio_file.tag._getAlbumArtist()}')
                    print("Tags edited: 0")
                    
                #If trying to save without doing changes for ID3 v2.2 eyed3 launches an error
                #because it cant't handle it. But if edited changes to ID3 v2.3 and saves in that format
                if tags_edited:
                    try:
                        audio_file.tag.save()
                    except Exception as e:
                        exception_msg(f"Could not save tags, non compatible mp3 file \"{file.name}\"", e)
                        continue
                
                first_letter = audio_file.tag._getArtist()[0].upper()

                try:
                #Moves to SORTED_DIR + artist folder + album folder
                    album_dir = audio_file.tag._getAlbum()
                    if "/" in album_dir:
                        album_dir = album_dir.replace("/", "-")
                    if "\"" in album_dir:
                        album_dir = album_dir.replace("\"", "")
                    if ":" in album_dir:
                        album_dir = album_dir.replace(":", " -")
                    if first_artist.endswith('.'):
                        first_artist = first_artist.replace(".", "")
                    if album_dir.endswith('.'):
                        album_dir = album_dir.replace(".", "")
                except Exception as e:
                    exception_msg(f"Could not get album tag from file.", e)
                    continue
                        
                audio_file_dir = SORTED_DIR / first_letter / first_artist / album_dir / file.name
                print(f'Moving {audio_file} to {audio_file_dir}...')
                os.makedirs(os.path.dirname(audio_file_dir), exist_ok=True)
                shutil.move(file, audio_file_dir)
                print('Done\n')
        else:
            error_msg(f'Error: \"{file.name}\" is not a file')