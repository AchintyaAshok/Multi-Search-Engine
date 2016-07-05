import urllib2
import os
import sys
import json
from bs4 import BeautifulSoup

class Scraper:

    searchEngineName = None
    searchEngineUrl = None
    queryBase = None
    query = None
    rawData = None
    results = {}
    numResults = 0
    numTimesPaged = 0

    def __init__(self, searchEngineName, searchEngineUrl, queryBase, query):
        self.searchEngineName = searchEngineName
        self.searchEngineUrl = searchEngineUrl
        self.queryBase = queryBase
        self.query = query
        self.numResults = self.numTimesPaged = 0

    def executeQuery(self):
        print "Executing Query: " + self.query
        fullUrlPath = self.searchEngineUrl + self.queryBase + self.query + "&num=100&hl=en&start=0"
        print "Full URL: " + fullUrlPath
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"}
        rawResponse = urllib2.urlopen(urllib2.Request(fullUrlPath, None, headers))
        self.processResults(rawResponse)

    def processResults(self, response):
        print "Parsing Raw Response"

    # overriden by derived class
    def getSearchResults(self):
        if len(self.results) > 0:
            return self.results
        else:
            return [
                {
                    "title": "SiteA",
                    "url": self.searchEngineUrl,
                    "searchEngine": self.searchEngineName
                },
                {
                    "title": "SiteB - Something Else!",
                    "url": self.searchEngineUrl,
                    "searchEngine": self.searchEngineName
                },
            ]
