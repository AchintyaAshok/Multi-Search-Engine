from Scraper import *
import urllib2
import os
import sys
import json
import re
from bs4 import BeautifulSoup

class GoogleScraper(Scraper):

    def __init__(self, query):
        Scraper.__init__(self, "Google", "http://www.google.com", "/search?q=", query)
        print "Initializing Google Scraper!"

    def getAllResults(self):
        print "Returning all parsed results."

    def getMoreResults(self):
        print "Getting more results"

    def processResults(self, response):
        print "Processing Response"
        self.rawData = unicode(response.read(), errors='ignore')
        self.numTimesPaged = 1
        print "Response length: " + str(len(self.rawData))
        soup = BeautifulSoup(self.rawData, "html.parser")
        searchResults = soup.findAll("h3", {"class":'r'})
        parsedResults = []
        for elem in searchResults:
            parsedResults.append( {
                "url" : elem.a['href'],
                "pageName": elem.a.getText()
            } )
        self.results = parsedResults

class YahooScraper(Scraper):

    def __init__(self, query):
        Scraper.__init__(self, "Yahoo", "http://www.yahoo.com", "/search?q=", query)
        print "Initializing Yahoo Scraper!"

    def getAllResults(self):
        print "Returning all parsed results."

    def getMoreResults(self):
        print "Getting more results"

    def processResults(self, response):
        print "Processing Response"
        self.rawData = unicode(response.read(), errors='ignore')
        self.numTimesPaged = 1
        print "Response length: " + str(len(self.rawData))
        soup = BeautifulSoup(self.rawData, "html.parser")
        searchResults = soup.findAll("h3", {"class":'r'})
        parsedResults = []
        for elem in searchResults:
            parsedResults.append( {
                "url" : elem.a['href'],
                "pageName": elem.a.getText()
            } )
        print parsedResults
        # print response
        # print "Processing Response"
        # self.rawData = response.read()
        # self.rawData = unicode(self.rawData, errors='ignore')
        # self.numTimesPaged = 1
        # print "Response length: " + str(len(self.rawData))
        # DATA = "<div class='g'><div class='rc'>data</div></div>"
        # soup = BeautifulSoup(self.rawData, "lxml")
        # searchResults = soup.findAll("cite", {"class":"_Rm"})
        # print searchResults

class BingScraper(Scraper):

    def __init__(self, query):
        Scraper.__init__(self, "Bing", "http://www.bing.com", "/search?q=", query)
        print "Initializing Bing Scraper!"

    def getAllResults(self):
        print "Returning all parsed results."

    def getMoreResults(self):
        print "Getting more results"

    def processResults(self, response):
        print response
        print "Processing Response"
        self.rawData = response.read()
        self.numTimesPaged = 1
        print "Response length: " + str(len(self.rawData))
        DATA = "<div class='g'><div class='rc'>data</div></div>"
        soup = BeautifulSoup(self.rawData, "lxml")
        searchResults = soup.findAll("cite", {"class":"_Rm"})
        print searchResults
