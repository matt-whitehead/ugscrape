# ugscrape

A simple Python library for scraping chords from https://www.ultimate-guitar.com/

## Requirements

* Python 3.6 or newer (has not been tested on older versions, will NOT work with Python 2.x)
* selenium
* chromedriver

## Installation 

* Clone the repo
* Install selenium with:
  * ``pip install selenium``
* Or, if you're using anaconda:
  * ``conda install -c conda-forge selenium``
* Download [chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=2.43/) for your OS and place it in the same directory as main.py
  
 ## Usage
  Full docs to come. But for now:
  * main.py contains the class and all its methods
    * they are explained in the docstrings
  * example.py shows you how to use the library
  * Don't run main.py, import it and run your own script
  
## A Note About chromedriver
* Sometimes chromedriver doesn't like to quit when selenium tells it to (ChordScraper.killDriver). If this happens, try running:
    * ``killall -9 chromedriver``
    * ``killall -9 "Google Chrome"``
* That will only work on a mac/unix-like system. If you're on Windows, you're on your own  ¯\_(ツ)_/¯.
