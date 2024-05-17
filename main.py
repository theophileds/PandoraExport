"""
PandoraExporter Usage: main.py --artist <artist> [--song <song>] [--limit <limit>] [--output <file>]

Options:
  -h, --help            Show this screen.
  -a, --artist <artist> Name of the artist (required). Enclose in quotes if it contains spaces.
  -s, --song <song>     Name of the song (optional). Enclose in quotes if it contains spaces.
  -l, --limit <limit>   Maximum number of songs [default: 100]
  -o, --output <file>   Output file name (optional) [default: <artist>.json]
"""

import json
import logging
from pick import pick
from collections import defaultdict

from docopt import docopt
from pandora.clientbuilder import APIClientBuilder
from pandora.errors import PandoraException

from pandora_settings import pandora_credentials

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

class PandoraExporter(APIClientBuilder):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.client = self.build_from_settings_dict(settings)
    
    def login(self):
        self.client.login(self.settings['USERNAME'], self.settings['PASSWORD'])
    
    def search_song(self, artist, song):
        search = self.client.search(artist + ' ' + song, include_near_matches=True)
        if search.songs:
            _, index = pick([song.song_name for song in search.songs], 'Select the song from {} you want to generate the playlist for:'.format(artist))
            return search.songs[index].token
        else:
            logging.warning('No Songs found for: {}'.format(artist))

    def search_artist(self, artist):
        search = self.client.search(artist, include_near_matches=True)
        if search.artists:
            _, index = pick([artist.artist for artist in search.artists], 'Select the artist you want to generate the playlist for:')
            return search.artists[index].token
        else:
            logging.warning('No artist found for: {}'.format(artist))

    def generate_playlist(self, token, limit):
        if token:
            playlist = defaultdict(list)
            # Each API call retrieve 4 songs
            for i in range(limit // 4):
                station = self.client.create_station(token)
                try:
                    songs = self.client.get_playlist(station.token)
                except PandoraException as e:
                    logging.info('Pandora exception error: {}'.format(e))
                    break
                for song in list(filter(lambda track: not track.is_ad, songs)):
                    if song.song_name not in playlist[song.artist_name]:
                        playlist[song.artist_name].append(song.song_name)
                    logging.info('Fetching new song: {} - {}'.format(song.artist_name, song.song_name))

                self.client.delete_station(station.token)
            return playlist
        else:
            logging.warning('No token provided')

    @classmethod
    def export_playlist_to_json(cls, playlist, filename):
        with open(filename, 'w') as output:
            output.writelines(json.dumps(playlist, sort_keys=True, ensure_ascii=False))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    artist = arguments.get('--artist')
    song = arguments.get('--song')
    limit = int(arguments.get('--limit'))
    output = arguments.get('--output').replace('<artist>', artist).replace(' ', '_')

    pandora_client = PandoraExporter(pandora_credentials)
    pandora_client.login()
    token = pandora_client.search_song(artist, song) if song else pandora_client.search_artist(artist)
    playlist = pandora_client.generate_playlist(token, limit)
    pandora_client.export_playlist_to_json(playlist, output)
