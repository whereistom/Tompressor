#!/usr/bin/python

import httplib
import urlparse
import os
import urllib
import time
import sqlite3 as lite
import sys
import hashlib
import result



###############################
#                             #
# HTTP/URL checking functions #
#                             #
###############################

#
# Check for a valid port in the URL. http://www.google.com:80 -> strip off initial http://.
# URL such as test:password@mydomain.com:80  we ignore them since we dont want to store usernames and password in our service to avoid legal problems.
#
def http_port_in_url(url):
    cuttedurl = url[7:]
    if cuttedurl.count(':') > 1:
        return False
    
    #get port number   
    if cuttedurl.count(':') == 1:
        array=cuttedurl.partition(':')
        port=array[2]
        #test if it is a valid number port http
        if port.isdigit() and 1 <= int(port) <= 65535:
            return True
        else:
            return False
           
    return True

#
# Retrive the server status code i.e. 200!ok
#
def get_server_status_code(url):
    host, path = urlparse.urlparse(url)[1:3]
    try:
        conn=httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return False
#
# Test if the header code is one of a active website ::: input url in the form http://www.mydomain.com
#
def check_url(url):
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes



#################################################
#                                               #
# ENCODING / DECODING FUNCTIONS TO/FROM BASE XX #
#                                               #
#################################################

#Personalize the alphabet in this script
# in the format: ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#this can be customized romving confusing chars like "0Ol1" 
#
# Encode to base62
#
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62encoding(number, alphabet=ALPHABET): 

    if (number == 0):
        return alphabet[0]
    array = []
    base = len(alphabet)
    while number:
        rem = number % base
        number = number // base
        array.append(alphabet[rem])
    array.reverse()
    return ''.join(array)

#
# Decode from base62
#
def base62decoding(string, alphabet=ALPHABET):
 
    base = len(alphabet)
    strlen = len(string)
    number = 0

    current = 0
    for char in string:
        power = (strlen - (current + 1))
        number += alphabet.index(char) * (base ** power)
        current += 1

    return number
########## END OF ENCODING/DECODING FUNCTIONS ##########




####################
#                  #
# Sqlite Functions #
#                  #
####################

#
# Sqlite3 version - returns db version
#
def sqlite3_version(dbname):
   con = None
   try:
    con = lite.connect(dbname)
    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    
    data = cur.fetchone()
    
    print "SQLite version: %s" % data                
    
   except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
   finally:
    
    if con:
        con.close()
    
    return


#
# Insert url and url's hash inside the database
#
def sqlite3_insert_url(dbname, longurl, urlhash):
 
  #connect to the database 
  connection = None
  try:
    connection = lite.connect(dbname)
    #generate a tuple that we will insert in our database
    t = (longurl, urlhash)
    
    #create a cursor to point our database
    cursor = connection.cursor()
    cursor.execute("INSERT INTO urlist ('url','hash') VALUES (?,?)", t)
    connection.commit()
    
    #we handle the error 
  except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
  finally:
    #read the the ID of the new value
    result=cursor.lastrowid
    #close connection to db
    if connection:
        connection.close()
    #return the ID of the newly insert url
    return result


#
#  Check for duplicates in the database using the HASH
#
def sqlite3_check_for_duplicate(dbname, urlhash):
    
    #connect to db
    connection = None
    connection = lite.connect(dbname)
    
    #generate tuple that we need to check
    t = (urlhash,)
    
    #create cursos
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM urlist WHERE hash=(?)", t)
    
    #check the results for duplicate
    result=cursor.fetchone()
    
    if connection:
        connection.close()
    if result:
        #return the ID of the result
        return result[0]
    else:
        #no results
        return None


#
# Retrive a database entry from the ID and output the long url (if one)
#
def sqlite3_output_url(dbname, id):
    
    #connect to db
    connection = None
    connection = lite.connect(dbname)
    
    #generate tuple that we need to check
    t = (id,)
    
    #create cursos
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM urlist WHERE id=(?)", t)
    
    #check the results for duplicate
    result=cursor.fetchone()
    
    if connection:
        connection.close()
    if result:
        #return the ID of the result
        return result[1]
    else:
        #no results
        return False
########## END OF SQLITE FUNCTIONS ##########
