#!/usr/bin/python

# 
# Imports
#
import functions
import result
import httplib
import urlparse
import time
import sys
import hashlib
import cgi
import cgitb
cgitb.enable()

#######################
# Initialization area #
#######################


#database /path/name.sqlite
dbname = "tompressor.sqlite"

#read user input
form = cgi.FieldStorage()
longurl = form.getvalue("longurl")


##################################
# section 1: verify users' input #
##################################


#verify that the input is not null
if longurl is None:
  #handle the error
  result.redirect_to_error("BLANK")
  sys.exit(1)

#verify that the URL is not longer then 2083 chars. Following recommandations here http://www.boutell.com/newfaq/misc/urllength.html
if len(longurl) > 2083:
    #handle the error
    #print only first 50 chars...
    result.redirect_to_error(longurl[0:50]+"...")
    sys.exit(1)

#verify lazy user input without http:// substring
if longurl.startswith('http://', 0, 7) is False:
    longurl = "http://"+ longurl

#check after adding http:// if there is a valid port in the url
if functions.http_port_in_url(longurl) is False:
    result.redirect_to_error(longurl)
  


#check for active URL to avoid a database full of junk
if functions.check_url(longurl) is False:
    #handle the error
    result.redirect_to_error(longurl)
    sys.exit(1)




##################################
# section 2: database operations #
##################################


# Calculation of url's SHA1 
urlhash = hashlib.sha1()
urlhash.update(longurl)

# We check for duplicate entry (users might input url already in our DB)
id = functions.sqlite3_check_for_duplicate(dbname, urlhash.hexdigest())

if id:
  #if we already have an entry we give the result to the user
  shorturl=functions.base62encoding(id,)
  result.redirect_to_result(shorturl, longurl)
else:
   # We insert in DBNAME, the longurl and the sha1(longurl) 
   id = functions.sqlite3_insert_url(dbname, longurl, urlhash.hexdigest())
   #compute the shorturl
   shorturl = functions.base62encoding(id,)
   #send the result to the user
   result.redirect_to_result(shorturl, longurl)
