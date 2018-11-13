# imports
from selenium import webdriver
import os
from collections import OrderedDict
import json
import re

class WebDriver:
    """
    Base class for the selenium webdriver
    """
    def __init__(self):
        # Assume that the chromedriver file is in the same directory as this file
        driver_path = os.getcwd() + '/chromedriver'

        # Set the options for the chrome driver
        option = webdriver.ChromeOptions()
        option.add_argument('incognito')
        option.add_argument('headless')
        option.add_argument('no-proxy-server')

        # We start with this as False, any failures set it to True
        # Can be used as a while loop break condition if something goes wrong
        self.failed = False
        # Try to start the webdriver
        try:
            self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
        except:
            print("Couldn't start the webdriver. Did you place it in the same dir as the API file?")
            self.failed = True

    def closewindow(self):
        """
        DO NOT USE. This will break future calls to geturl. Probably will be removed.
        Closes the current webdriver window. Run this after you're done with a page.
        """
        self.driver.close()

    def killDriver(self):
        """
        Closes all the windows and quits the webdriver. Run this when you're done with the class instance.
        If you don't do this when you're finished the chrome processes will keep running even when the script stops.
        """
        self.driver.quit()


class ChordScraper(WebDriver):
    def __init__(self):
        super().__init__()
        self.span_start = re.compile(r'<span[^>]*>')

    def geturl(self, url):
        """
        Go to the URL and scrape the data

        Arguments:
            url – string, the url to fetch

        Returns:
            True - If we succeeded
            False – If something went wrong
        """
        # Grab the url from the argument
        self.url = url
        self.driver.get(url)

        # Try to grab the text and metadata
        try:
            self.meta = self.driver.find_elements_by_class_name('_3JgI9')
            self.body = self.driver.find_element_by_class_name('_1YgOS').get_attribute('innerHTML')
            self.body = self.span_start.sub('[CH]', self.body)
            self.body = self.body.replace('</span>', '[/CH]')
            self.dict = OrderedDict()
            # Not all songs have meta data
            if self.meta:
                for i in self.meta:
                    # This stops us from getting random text like "Do you like this song? (yes/no)"
                    # Which they have stored in the same div class as the metadata
                    if i.text.find(': ') == -1:
                        continue
                    element_list = i.text.split(': ')
                    self.dict[element_list[0]] = element_list[1]
                self.dict['text'] = self.body
            return True
        except Exception as e:
            print(e)
            print('!!!@@@ FAILURE AT: @@@!!!')
            print(self.url)
            self.failed = True
            return False

    def savejson(self, filename):
        """
        Save the scraped data to a file as JSON data

        Arguments:
            filename – string, the filename or filepath to save the data to

        Returns:
            True – If we succeeded
            False – If something went wrong
        """
        if not self.body:
            print('No data to save! Have you called getURL?')
            self.failed = True
            return False
        else:
            with open(filename, 'w') as f:
                json.dump(self.dict, f)
                print('Saved ' + filename)
            return True

    def savetext(self, filename):
        """
        Save the scraped data to a file as raw text data

        Arguments:
            filename – string, the filename or filepath to save the data to

        Returns:
            True – If we succeeded
            False – If something went wrong
        """
        if not self.body:
            print('No data to save! Have you called getURL?')
            self.failed = True
            return False
        else:
            with open(filename, 'w') as f:
                for k,v in self.dict.items():
                    if k == 'text':
                        f.write('Text:' + '\n\n')
                        f.write(v)
                    else:
                        f.write(k + ': ' + v + '\n')
                print('Saved ' + filename)
                return True
