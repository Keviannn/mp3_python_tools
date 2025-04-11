import eyed3
from pathlib import Path

UNSORTED_DIR = Path("/path/to/unsorted/mp3")

print("artist_tag_format by Keviannn")
for file in UNSORTED_DIR.iterdir():
    if file.is_file():
        try:
            audio_file = eyed3.load(file)
            if " / " in audio_file.tag._getArtist():
                print(f"Already has \" / \" {audio_file.tag._getArtist()}")
            elif "/" in audio_file.tag._getArtist():
                print(f"Adding / to file {file.name}...")
                audio_file.tag.artist = audio_file.tag._getArtist().replace("/"," / ")
                print(f"new tag: {audio_file.tag._getArtist()}")
                audio_file.tag.save()
            else: 
                print(f"No / in {audio_file.tag._getArtist()}")
            print("Done\n")
        except:
            print(f"File {file.name} failed")
            continue