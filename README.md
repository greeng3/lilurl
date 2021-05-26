# lilurl

A service for shortening urls, as described in [URL Shortening](https://en.wikipedia.org/wiki/URL_shortening), and embodied in [bitly](https://bitly.com/).

## Installation

This is intended to be run under python3.  Dependencies are managed with poetry.

> pip install poetry
> 
> poetry install

## Running the app

### Unix

> export FLASK_APP=lilurl
> 
> export FLASK_ENV=development
> 
> poetry run flask run

### Windows

> set FLASK_APP=lilurl
> 
> set FLASK_ENV=development
> 
> poetry run flask run

## Connecting to the app

Connect a browser to http://127.0.0.1:5000/


## NOTES

Many things were elided or dummies provided in the interest of time.

The database used to store the mapping of URL to short version is an in-memory dummy.  In practice, we'd use a real database so that:
* It would scale.
* Multiple instances of the server wouldn't end up with short URL collisions.
* It would be resilient to a server failure.

The function used to convert long URLs to their short forms should be given real consideration so that:
* A given long URL should get the same short form, no matter which server may happen to shorten it.
* The short form should be reasonable short.  Certainly, short enough to make it worthwhile to use a URL shortener.
* This one is just python hash() base-62 encoded, which seems to be what other URL shortening services like.  That also has the benefit of ensuring that a short-form URL can't be confused with a .txt or .html file, or with a path that has an underscore in it, such as I use to hit the _shorten path.

In the real world, we would have spent money on a domain name that is actually short, e.g. bit.ly.  I noticed from a cursory search that people with deep pockets have already squatted most of the desirably short domain names in the universe.
Alas.

The HTML and CSS are rudimentary, and the robots.txt is just a placeholder.  On a real service, more time would be devoted to making those look nice, and making space for advertising to pay for this service.  :-)

This is a single-threaded, single-server demo.  It isn't containerized, though I considered it.  That would be one simple way to scale it, after all, and to keep its db mangageable, say with kubernetes or something similar.

I confess I got a little carried away, and spent more like 2.5 hours, but I wanted a working demo that had basic, if ugly functionality.