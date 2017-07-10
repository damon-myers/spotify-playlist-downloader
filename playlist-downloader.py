import argparse
import requests
import json

class Spotify:
    """
    A simple wrapper for the spotify API in order to download a user's playlists
    """
    def __init__(self):
        """
        Retrieves a Spotify Authorization Token so we can use the API
        Stores the token as a member variable of the object
        """
        with open("config.json") as config_json:
            configs = json.load(config_json)
            client_id = configs["client_id"]
            secret = configs["secret"]

            self.access_token = self.get_access_token(client_id, secret)
            self.auth_header = {"Authorization": "Bearer " + self.access_token}


    def get_access_token(self, client_id, secret):
        """
        Gets a "Client Credentials" auth token using the provided
        client_id and secret. Such tokens are described at
        https://developer.spotify.com/web-api/authorization-guide/
	"""
        body_params = {"grant_type": "client_credentials"}
        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, data=body_params, auth=(client_id, secret))
        
        if response.status_code == requests.codes.ok:
            print("Successfully obtained access token.")
            return response.json()["access_token"]
        else:
            raise Exception("""Unable to acquire access token, please check that 
                            your client_id and secret are properly specified 
                            in config.json""")

    def get_user_playlists(self, username):
        """
        Gets all of a user's playlists and returns the json list as a dict
        """
        url = "https://api.spotify.com/v1/users/{0}/playlists".format(username) 
        response = requests.get(url, headers=self.auth_header)
        return response.json()

    def get_playlist_by_name(self, username, playlist_name):
        """
        First gets all of user's playlists and then searches the dict
        for a specific playlist by checking the playlist names
        """
        for playlist in self.get_user_playlists(username)["items"]:
            if playlist["name"] == playlist_name:
                return playlist

        return None

    def get_playlist_tracks(self, username, playlist):
        """
        Returns a list of tracks on a playlist using the playlist's tracks url
        """
        url = playlist["tracks"]["href"]
        response = requests.get(url, headers=self.auth_header)

        return response.json()

    def select_from_all_playlists(self, username):
        """
        List all of a user's playlists on the command-line, and then prompt the
        user to select one using numbers
        """
        playlists = self.get_user_playlists(username)

        print()
        print("Please indicate which playlist you would like to download:")
        print()

        for index, playlist in enumerate(playlists["items"]):
            print("[{0}] {1} : {2} song(s).".format(index, 
                                                    playlist["name"], playlist["tracks"]["total"]))
        print()

        selected_number = int(input("Playlist number: "))

        if 0 <= selected_number <= len(playlists["items"]) - 1:
            return playlists["items"][selected_number]
        else:
            print("Please select a valid playlist number!")
            return self.select_from_all_playlists(username)


def build_argument_parser():
    """
    Returns the argument parser for handling command-line options.https://stackoverflow.com/questions/13628791/how-do-i-check-whether-an-int-is-between-the-two-numbers
    Options are "--playlist" to specify a playlist name, and
    "--list" to specify that all playlists should be listed
    """
    parser = argparse.ArgumentParser(description="Convert spotify playlists to xml.")

    parser.add_argument("username", default=None, action="store", 
                        help="user whose playlists we will convert")

    parser.add_argument("--playlist", "-p", action="store", default="",
                        help="name of playlist to convert")

    parser.add_argument("--list", "-l", action="store_true", default=False, 
                        help="list all of the user's playlists and prompt for selection")

    return parser



if __name__ == "__main__":
    spotify = Spotify()

    # Gather command line arguments
    parser = build_argument_parser()
    args = parser.parse_args()

    # If no playlist name was entered, 
    # we simply list all choices and have the user pick one
    if not (args.playlist or args.list):
        print("No playlist name entered, so we will list all choices.")
        args.list = True

    playlist = None
    tracks = None

    # Either have the user select a playlist or get the specified one
    if args.list:
        playlist = spotify.select_from_all_playlists(args.username)
        tracks = spotify.get_playlist_tracks(args.username, playlist)
    else:
        playlist = spotify.get_playlist_by_name(args.username, args.playlist)
        tracks = spotify.get_playlist_tracks(args.username, playlist)

    # Write the playlist and tracks to files
    playlist_name = playlist["name"]
    playlist_filename = "{0}.json".format(playlist_name)
    tracks_filename = "{0}-tracks.json".format(playlist_name)

    with open(playlist_filename, "w") as outfile:
        json.dump(playlist, outfile, indent=4)

    with open(tracks_filename, "w") as outfile:
        json.dump(tracks, outfile, indent=4)

    print("Playlist written to {0} and tracks written to {1}".format(playlist_filename, tracks_filename))
    print()
