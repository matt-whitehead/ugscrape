from main import ChordScraper

# set up the scraper and start the webdriver
scrape = ChordScraper()

# initialize a list for all the failed URLs to go
failed = []

# read in the links from a file
with open('examples/chord_links.txt', 'r') as f:
    links = f.read().splitlines()
    # loop through the list of links and call the API
    for i,v in enumerate(links):
        # The if statements are error handlers
        # If the API fails it will return False which will cause the link to be added to the failed list
        # Otherwise the API will return True and nothing special happens
        if scrape.geturl(v) == False:
            failed.append(v)
            continue
        if scrape.savetext('data/text/song_' + str(i) + '.txt') == False:
            failed.append(v)
        if scrape.savejson('data/json/song_' + str(i) + '.json') == False:
            failed.append(v)

# kill the webdriver, otherwise the processes will keep running when the script ends
scrape.killDriver()

# write a list of failed links to file
with open('failed_links.txt', 'w') as f:
    for link in failed:
        f.write(link + '\n')
