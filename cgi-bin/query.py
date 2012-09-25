#!/usr/bin/env python
import cgitb
cgitb.enable()
import cgi
import sys
import result
import functions


#######################
# Initialization area #
#######################

dbname = "tompressor.sqlite"
form = cgi.FieldStorage()
shorturl = form.getvalue('shorturl')


###############
# Input check #
###############

#filter the code -> we cannot have more then 7 char code
#because 6 are enough to index all internet url
if len(shorturl) > 7:
    result.redirect_to_wrongcode(shorturl)

#filter the code -> the code must contain only alpha-numeric chars
if shorturl.isalnum() is False:
    result.redirect_to_wrongcode(shorturl)
    

#######################################
# Sqlite operation and output results #
#######################################

id = functions.base62decoding(shorturl, )
longurl = functions.sqlite3_output_url(dbname, id)

#if we have a result permanent redirect browser so it will be cached and not requested again
if longurl:
    print "Status: 301"
    print "Location: %s" %(longurl)
    print
else:
    result.redirect_to_wrongcode(shorturl)
sys.exit(0)
