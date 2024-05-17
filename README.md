
# PandoraExport

Hello and welcome to PandoraExport,  
  
This script allows you to take advantage of the Pandora AI search for songs and export them to Json. 

The benefit is that you can use the export file to automatically import songs from Pandora to another streaming platform like Soundcloud or Spotify, freeing you from listening restrictions and ads.
  
To use PandoraExport, you need a US IP address, so if you don't live in the US, you can still use a VPN.
  
## How to use it
First you need to install dependencies with Pipenv

    pipenv install

  Then activate the virtual environment
  

    pipenv shell

Before running the script, you will need to set environment variables to connect to Pandora services.

    export PANDORA_USER=<your_pandora_login>
    export PANDORA_PASSWORD=<your_pandora_password>

Run the script!

    python main.py --artist BADBADNOTGOOD
    python main.py --artist 'Kit Sebastian' --song Yeter --limit 50 --output kit_sebastian_playlist.json

## More information about the libraries used:
  
Pandora API: https://github.com/mcrute/pydora
  
Docopt: https://github.com/docopt/docopt

Pick: https://github.com/aisk/pick
