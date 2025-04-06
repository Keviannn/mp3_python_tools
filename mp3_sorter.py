import os
import eyed3
from pathlib import Path
import shutil

UNSORTED_DIR = Path("/home/raid/catalogar")
SORTED_DIR = Path("/home/raid/music")
tags_edited = 0
empty_tags = 0
empty_tags_arr = [1, 1, 1]
user_input = ""

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
    
                try:
                    if "/" in audio_file.tag._getArtist():
                        #Get first artist only from artist tag (BadBunny/ABBA --> BadBunny)
                        first_artist = audio_file.tag._getArtist().split('/')[0]
                    else:
                        first_artist = audio_file.tag._getArtist()
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
                    print("Tags not edited: 0")
                    
                #If trying to save without doing changes for ID3 v2.2 eyed3 launches an error
                #because it cant't handle it. But if edited changes to ID3 v2.3 and saves in that format
                if tags_edited:
                    try:
                        audio_file.tag.save()
                    except Exception as e:
                        exception_msg(f"Could not save tags, non compatible mp3 file \"{file.name}\"", e)
                        continue

                #Moves to SORTED_DIR + artist folder + album folder
                if "/" in audio_file.tag._getAlbum():
                    audio_file.tag.album = audio_file.tag._getAlbum().replace("/", "-")
                if "\"" in audio_file.tag._getAlbum():
                    audio_file.tag.album = audio_file.tag._getAlbum().replace("\"", "")
                        
                audio_file_dir = SORTED_DIR / first_artist / audio_file.tag._getAlbum() / file.name
                print(f'Moving {audio_file} to {audio_file_dir}...')
                os.makedirs(os.path.dirname(audio_file_dir), exist_ok=True)
                shutil.move(file, audio_file_dir)
                print('Done\n')
        else:
            error_msg(f'Error: \"{file.name}\" is not a file')