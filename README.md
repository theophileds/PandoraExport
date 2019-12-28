
# PandoraExport

Hi and Welcome to PandoraExport,  
  
This script allows you to take advantage of Pandora AI searching song and export them into Json. 

The advantage is that you can use the export file to automatically import songs from Pandora to another streaming platform such as Soundcloud or Spotify, freeing you from listening restrictions and ads.
  
To use PandoraExport, you need a US IP address, so unless you don't live in the US, you can still use it via a VPN connection or by running it on another machine in US/NZ/AU. 
  
## How to use it
First you need to install dependencies with Pipenv

    pipenv install

  Then activate the virtual environment
  

    pipenv shell

Before running the script you will probable need to set enviroment variables to connect use Pandora services

    export PANDORA_USER=<your_pandora_login>
    export PANDORA_PASSWORD=<your_pandora_password>

Then you can run the script with (*recommended*) or without parameters.

> For argument parsing reasons you need to replace **space** with **_** instead

    python main.py --output export.json --limit 200 --artist echo_delta

## More information about API :  
  
Pandora API: https://github.com/mcrute/pydora
  
Docopt: https://github.com/docopt/docopt
