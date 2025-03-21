import os
import eyed3
from pathlib import Path
import shutil

UNSORTED_DIR = Path("/home/raid/catalogar")
SORTED_DIR = Path("/home/raid/music")

for file in UNSORTED_DIR.iterdir():
        if file.is_file():
            audio_file = eyed3.load(file)
            try:
                if audio_file.tag is None:
                    print("Error: File does not have ID3 tag")
                else:
                    print(f'Procesing {audio_file}...')

                    print(f"Name: {audio_file.tag.title} \nArtist: {audio_file.tag.artist} \nAlbum: {audio_file.tag.album}")

                    #Get first artist only from artist tag (BadBunny/ABBA --> BadBunny)
                    first_artist = audio_file.tag._getArtist().split('/')[0]

                    #Add album_artist tag for all music so multi-artist songs get in the same album
                    if audio_file.tag.album_artist is None:
                        print("No album_artist tag, adding one...")
                        audio_file.tag.album_artist = first_artist
                        print(f'New album_artist: {audio_file.tag._getAlbumArtist()}')
                    else:
                        print(f'Existing album_artist tag is {audio_file.tag._getAlbumArtist()}')
                    
                    audio_file.tag.save()

                    #Moves to SORTED_DIR + artist folder + album folder
                    audio_file_dir = SORTED_DIR / first_artist / audio_file.tag._getAlbum() / file.name
                    print(f'Moving {audio_file} to {audio_file_dir}...')
                    os.makedirs(os.path.dirname(audio_file_dir), exist_ok=True)
                    shutil.move(file, audio_file_dir)
                    print('Done\n')
            except:
                print(f"Error: non mp3 file {file}\n")
                continue
        else:
            print(f'Error: {file} is not a file')

