"""PandoraExporter

Usage:
  main.py [--output result.json] [--limit 100] [--artist Echo_Delta]
  main.py [-h | --help]

Options:
  -h --help          Show this screen.
  --output=filename  Output file name [default: output.json]
  --limit=100        Maximum number of songs [default: 100]
  --artist=name      Name of the artist with _ instead of space [default: Echo_Delta]

"""

import json
import logging
from collections import defaultdict

from docopt import docopt
from pandora.clientbuilder import APIClientBuilder
from pandora.errors import PandoraException

from pandora_settings import pandora_credentials

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

class PandoraExporter(APIClientBuilder):
    def __init__(self, settings, **kwargs):
        self.settings = settings
        super().__init__(**kwargs)

    def _build_client(self):
        return self.build_from_settings_dict(self.settings)

    def generate_playlist(self, artist, limit):
        client = self._build_client()
        client.login(self.settings['USERNAME'], self.settings['PASSWORD'])

        search_result = client.search(artist)
        if search_result.artists:
            songs_batch = defaultdict(list)
            # Each API call retrieve 4 songs
            for i in range(limit // 4):
                station_result = client.create_station(search_result.artists[0].token)
                try:
                    playlist_result = client.get_playlist(station_result.token)
                except PandoraException as e:
                    logging.info('Pandora exception error: {}'.format(e))
                    break
                for song in list(filter(lambda track: not track.is_ad, playlist_result)):
                    if song.song_name not in songs_batch[song.artist_name]:
                        songs_batch[song.artist_name].append(song.song_name)
                    logging.info('Fetching new song: {} - {}'.format(song.artist_name, song.song_name))

                client.delete_station(station_result.token)
            return songs_batch
        else:
            logging.warning('No artist found for: {}'.format(artist))

    @classmethod
    def export_playlist(cls, playlist, output):
        with open(output, 'w') as output:
            output.writelines(json.dumps(playlist, sort_keys=True, ensure_ascii=False))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    artist_name = ' '.join(arguments.get('--artist').split('_'))
    songs_limit = int(arguments.get('--limit'))
    output_filename = arguments.get('--output')

    pandora_client = PandoraExporter(pandora_credentials)
    pandora_playlist = pandora_client.generate_playlist(artist_name, songs_limit)
    pandora_client.export_playlist(pandora_playlist, output_filename)
