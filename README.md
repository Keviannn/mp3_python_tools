# mp3_sorter

A lightweight Python script designed for use with a Navidrome server, which organizes MP3 files based on their metadata tags. This script helps keep your music library clean and well-structured by sorting MP3 files into directories based on their artist and album tags.

## Features

- Extracts MP3 file metadata such as artist and album.
- Basic interface for adding basic tags if they do not exist.
- Automatically adds the `album_artist` tag if it doesn't already exist, using the first listed artist.
- Moves the MP3 file into a folder structure: `SORTED_DIR/artist/album/`.

## Requirements

- Python 3
- `eyed3` library for reading and modifying MP3 metadata.
  
```bash
apt install python3-eyed3
```

## mp3_sorter.py

This script does the following:

1. Reads the MP3 file metadata, extracting important tags like artist and album.
2. If `title`, `artist` or `album` tags do not exist, gives the user the option to add them.
3. If the `album_artist` tag is missing, it automatically adds the first listed artist as the album artist.
4. If the album name has non valid characters for a directory, changes them for valid ones.
5. Moves the MP3 file into a pre-defined folder structure: `SORTED_DIR/artist/album/`, where `SORTED_DIR` is a user-defined base directory for sorted files.
   
### Example Usage:

```bash
#Execute inside the directory of unsorted MP3 files
path/of/unsorted/files$ python3 /path/to/script/mp3_sorter.py
```

### Folder Structure

- **Original File:**  
  `/path/to/your/mp3/files/artist_album_song.mp3`
  
- **After Sorting:**  
  `/path/to/sorted/music/artist/album/song.mp3`

## Configuration

- **UNSORTED_DIR**: Define the base directory where original files are. Modify the script to set your preferred directory path.
- **SORTED_DIR**: Define the base directory where sorted files will be moved. Modify the script to set your preferred directory path.
- The script is designed to handle basic tagging scenarios. If additional or custom tags are needed, you can modify the script as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.