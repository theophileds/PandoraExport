
# PandoraExport

Hi and Welcome to PandoraExport,  
  
This script allows you to take advantage of Pandora AI searching song and export them into Json. 

The advantage is that you can use the export file to automatically import songs from Pandora to another streaming platform such as Soundcloud or Spotify, freeing you from listening restrictions and ads.
  
To use PandoraExport, you need a US IP address, so unless you don't live in the US, you can still a VPN.
  
## How to use it
First you need to install dependencies with Pipenv

    pipenv install

  Then activate the virtual environment
  

    pipenv shell

Before running the script you will probable need to set enviroment variables to connect use Pandora services

    export PANDORA_USER=<your_pandora_login>
    export PANDORA_PASSWORD=<your_pandora_password>

Then you can run the script with (*recommended*) or without parameters.

    python main.py --artist BADBADNOTGOOD
    python main.py --artist 'Kit Sebastian' --song Yeter --limit 50 --output kit_sebastian_playlist.json

## More information about API :  
  
Pandora API: https://github.com/mcrute/pydora
  
Docopt: https://github.com/docopt/docopt
