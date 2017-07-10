# playlist-downloader

A python program that uses the Spotify Web API to download a user's public playlists as JSON.

# Usage

Before using this program, you must first obtain a Spotify API client id and secret.
You can do so by following the instructions [here](https://developer.spotify.com/web-api/tutorial/#registering-your-application).

Once you have obtained your client id and secret, create a file named "config.json" in the project directory and enter your "client_id" and "secret" as values in JSON notation. The "sample-config.json" is an example of how to properly do this.

Now install the program's dependencies with `pip` by running `pip install -r requirements.txt` in the project directory.

You can now run the program using `python playlist-downloader.py <username>`

## Options and usage explanations

```
python playlist-downloader.py <username>
```
will list all of <username>'s public playlists and allow you to pick one to download.

```
python playlist-downloader.py <username> -l
```
will do the same thing, but without the line saying you missed adding a playlist name

If you know the name of the playlist you want to download, you can do so with:
```
python playlist-downloader.py <username> -p <playlist-name>
```

# Issues

If you have any issues with usage, or would like additional features added, please let me know by reporting it here on GitHub.

# Licensing

This software is licensed under the MIT License, so do with it what you will. :)

