# MAKE BEER GREAT AGAIN (MBGA)
## Description
This Project was started initially in context of the module "Prozess- und Anlagenautomatisierung einer Microbrauanlage" of TU Berlin.
Goal of it was to control and supervise the mashing process in beer production. The used platform is an RPI 3 with some extra Hardware (e.g. Thermosensor, Servomotor, IR-Socket).

For the usability and to observe the brewing process a webinterface is provided.

## Setup
In this guide we assume you have a clean installation of [raspian](https://www.raspbian.org/) running on RPI rev. 3.
Following dependencies are required to run the program:
* python
* nodejs
* ...

To get the sourcecode you've to clone this git-project. 

## Usage
To run the webserver you've to navigate into the web directory and run `npm start`
The webinterface is accessible through your prefered webbrowser over the URL: `http://localhost:4000`
