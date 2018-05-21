# Project Title

Let's Fly

## The project in short

Simple Google App Engine Web Application example with minimal style, written in Python 2.7, using Mashape Market API
site (see references in "Built With" section).
The app is able to find all the airports in a city and to give information about the Time Zone.

## Specifications

* A form is used to retrieve the city name.
* The app response shows: airport name, airport code, time zone info.
* City name is saved automatically in the Datastore.
* An API GET is given to show the 3 most popular requested cities, in JSON format.
* An API POST is given: it allows inserting a new city in the Datastore; if the city is already present,
an error is returned.

## Before starting
* Add a lib folder to the project, in which you have to install the libraries listed in "requirements.txt" file.
* You must be logged in Mashape Market site in order to use its API; the site, also, provide you with an API key: 
paste it in the variable named "MASHAPE_KEY", before you run this project.

## Built With

* [Google App Engine](https://cloud.google.com/appengine) - Platform used
* [Flask](http://flask.pocoo.org/) - The microframework for Python used
* [Airports Finder](https://market.mashape.com/cometari/airportsfinder) - API used
* [Time Zone info](https://market.mashape.com/tehuano/time-zone-info) - API used

## Author

**Marcella Tincani** - [Marcella](https://github.com/tmarcy)
