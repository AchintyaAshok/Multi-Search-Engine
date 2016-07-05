from socket import *
import json
import threading
import re
from allScrapers import *

SERVER_HOST = 'localhost' 	# server host name
SERVER_PORT = 8000			# server port

VALID_ENDPOINTS = {
	"/search" : {
		"GET": True
	}
}

# We can modularly add search engines to search from. Use Factory Method to create engines
POSSIBLE_ENGINES = {
	"google": 	"GoogleScraper",
	"yahoo":	"YahooScraper",
	"bing":		"BingScraper",
}

def search(query):
	print "Performing search across multiple engines"

	# this will be replaced by a generic factory to create search engines and
	# extract results
	# search engines can be used via the name to class mapping in POSSIBLE_ENGINES

	results = {}

	g = GoogleScraper(query)
	g.executeQuery()
	results[g.searchEngineName] = g.getSearchResults()

	yahoo = YahooScraper(query)
	yahoo.executeQuery()
	results[yahoo.searchEngineName] = yahoo.getSearchResults()

	bing = BingScraper(query)
	bing.executeQuery()
	results[bing.searchEngineName] = bing.getSearchResults()

	# remove duplicate results from three lists by doing a dictionary union
	# duplicate results can be checked via the urls
	# dictionary update does a union

	return results



def handleRequest(message):
	print "handling request message"
	print "Raw message: " + str(message)
	messageMainHeader = message[0].split(' ')
	requestMethod = messageMainHeader[0]
	requestEndpoint = messageMainHeader[1]

	# Determine if we have query params, in this case let's limit it to one for simplicity
	endpointPieces = requestEndpoint.split("?")
	query = None
	if len(endpointPieces) > 1:
		requestEndpoint = endpointPieces[0]
		query = endpointPieces[1][2:]
	print "Method: " + requestMethod
	print "Endpoint: " + requestEndpoint
	print "Query:" + query

	# Eventually, use the VALID_ENDPOINTS dictionary to validate endpoint
	if(requestMethod == "GET" and requestEndpoint == "/search"):
		print "Routing to search endpoint"
		return search(query)

def main():
	serverSocket = socket(AF_INET, SOCK_STREAM)
	try:
		serverSocket.bind((SERVER_HOST, SERVER_PORT))  # set the host name and the port
		serverSocket.listen(1)                         # the number of backlogged connections, we only handly 1 at a time
		print 'Ready to serve...'
		serverName = serverSocket.getsockname()
		print "Listening on address: " + str(serverName[0]) + ", port: " + str(serverName[1])
		while True: # keep listening on this port
			incomingConnection, address = serverSocket.accept()
			print "Connected to: " + str(address)
			message = incomingConnection.recv(1024) # get the message from the client
			try:
				message = message.splitlines()	# separate into a list of lines
				results = handleRequest(message)
				print "All Results -> " + str(results)
				incomingConnection.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + json.dumps(results))
			except Exception as excep:
				print str(excep)
				print "Unable to process the message. Check Logs."
				incomingConnection.send("HTTP/1.1 404 Not Found")
			finally:
				incomingConnection.close() # break the client connection
	except Exception as e:
		print str(e) # if there was something wrong while instantiating the server, print the error to std out
	finally:
		serverSocket.close()
main()
