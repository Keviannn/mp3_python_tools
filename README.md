# mp3_python_tools

A collection of lightweight Python scripts designed to be used with a Navidrome server to keep your MP3 files organized and with coherent tags. This collection helps keep your music library clean and well-structured by sorting MP3 files into directories based on their metadata while giving them the correct tag and its correct format. **Please note that these scripts are intended for educational purposes only, and it is important to use them with legally acquired music files. The project does not promote piracy or the use of illegal content. Always ensure that you have the right to manage and modify the MP3 files you work with.**

## Requirements

- Python 3
- `eyed3` library for reading and modifying MP3 metadata.
- `spotipy` library for searching with the Spotify API.

  <br>

  ```bash
  apt install python3-eyed3 
  pip install spotipy
  ```

## Scripts

### mp3_sorter.py
Even though it's not needed for Navidrome to work correctly, I like to have a clear folder structure so I can easily find my music files manually if needed.

**The script is designed to handle basic tagging scenarios. If you need additional functionality, feel free to ask or modify the script as necessary.**

This script does the following:

1. Reads the MP3 file metadata, extracting important tags like artist and album.
2. If `title`, `artist` or `album` tags do not exist, gives the user the option to add them.
3. If the `album_artist` tag is missing, it automatically adds the first listed artist as the album artist.
4. Sometimes, different artists are separated by commas, so it asks whether that's the case to format it properly.
5. If the album name has non valid characters for a directory, changes them for valid ones.
6. Moves the MP3 file into a pre-defined folder structure: `SORTED_DIR/FIRST_LETTER/artist/album/`, where `SORTED_DIR` is a user-defined base directory for sorted files and `FIRST_LETTER` is the first letter of the artist name.
   
- ### Example Usage:

  ```bash
  $ python3 /path/to/script/mp3_sorter.py
  ```

- ### Configuration

  - **UNSORTED_DIR**: Defines the base directory where original files are located. Modify the script to set your preferred directory path.
  - **SORTED_DIR**: Defines the base directory where sorted files will be moved. Modify the script to set your preferred directory path.

<br>

---
### artist_tag_format.py
Sometimes, artists are separated by a "/" like this: artist1/artist2. This is incorrect for Navidrome, as it sees them as a single artist (like AC/DC).

The correct way is: artist1 / artist2. This way, Navidrome recognizes them as two separate artists.

**The script is designed to handle basic scenarios. If you need additional functionality, feel free to ask or modify the script as necessary.**

This script does the following:

1. Reads the MP3 file metadata, extracting the artist tag.
2. If `artist` already has " / " as a separator, does nothing.
3. If `artist` has "/" as a separator, changes it for the correct one.

- ### Example Usage:

  ```bash
  $ python3 /path/to/script/artist_tag_format.py
  ```

- ### Configuration

  - **UNSORTED_DIR**: Defines the base directory where original files are located. Modify the script to set your preferred directory path.

<br>

---

### artists_from_spotify.py
Sometimes, MP3 files don't have the correct artist tags, and as your music library grows, going through them one by one to check the artist tags becomes too tedious.

**The script is designed for files with a single artist tag that should contain multiple artists. If you need additional functionality, feel free to ask or modify the script as necessary.**

This script does the following:

1. Connects to the Spotify API based on ID and secret.
2. Goes through the sorted path checking for artists without a "/" separator.
3. Searches for that song in Spotify.
4. Displays mismatches to the user and offers the option to accept or reject the changes.

- ### Example Usage:

  ```bash
  $ python3 /path/to/script/artists_from_spotify.py
  ```

- ### Configuration

  - **SORTED_DIR**: Defines the base directory where original files are located. Modify the script to set your preferred directory path.
  - **SEARCH_WILDCARD**: Defines the file type to search for. The script is built for MP3 files but allows for modularity.
  - **client_id**: Enter your Spotify API client ID here.
  - **client_secret**: Enter your Spotify API client secret here.

<br>

---
<br>

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
