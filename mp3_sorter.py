import os
import eyed3
from pathlib import Path
import shutil

UNSORTED_DIR = Path("/home/raid/catalogar")
SORTED_DIR = Path("/home/raid/music")
tags_edited = 0

def error_msg(msg):
    print(f"\n----- Error -----\nError: {msg}\n")

def exception_msg(msg, exception):
    print(f"\n----- Error -----\nError: {msg}")
    print(f"Exception Type: {type(exception).__name__}\nMessage: {exception}\n")

if __name__ == "__main__":
    print("mp3_sorter by Keviannn")
    for file in UNSORTED_DIR.iterdir():
            if file.is_file():
                audio_file = eyed3.load(file)
                if audio_file is None:
                    error_msg(f"File {file} does not have ID3 tag or is not an mp3 file")
                else:
                    print(f'\nProcesing {audio_file}...')

                    print(f"Name: {audio_file.tag.title} \nArtist: {audio_file.tag.artist} \nAlbum: {audio_file.tag.album}")

                    #Get first artist only from artist tag (BadBunny/ABBA --> BadBunny)
                    first_artist = audio_file.tag._getArtist().split('/')[0]

                    #Add album_artist tag for all music so multi-artist songs get in the same album
                    if audio_file.tag.album_artist is None:
                        print("No album_artist tag, adding one...")
                        audio_file.tag.album_artist = first_artist
                        print(f'New album_artist: {audio_file.tag._getAlbumArtist()}')
                        tags_edited = 1
                        print("Tags edited: 1")
                    else:
                        print(f'Existing album_artist tag is {audio_file.tag._getAlbumArtist()}')
                        tags_edited = 0
                        print("Tags not edited: 0")
                    
                    #If trying to save without doing changes for ID3 v2.2 eyed3 launches an error
                    #because it cant't handle it. But if edited changes to ID3 v2.3 and saves in that format
                    if tags_edited:
                        try:
                            audio_file.tag.save()
                        except Exception as e:
                            exception_msg(f"could not save tags, non compatible mp3 file {file}", e)
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
                print(f'Error: {file} is not a file')

