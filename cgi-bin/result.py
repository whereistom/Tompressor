#!/usr/bin/python
import cgi
import sys
import os

#######################
# Outout result pages #
#######################

#
#initialize HTML common code for every page. Below personalize the output
#
html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <html>

    <head>
    <title>Tompressor</title>
    <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
    <meta name="generator" content="HAPedit 3.1">
    <link rel="shortcut icon" type="image/x-icon" href="http://www.tomjournal.net/jobagenda/favicon.ico">

    </head>
    <style>
       a:link{
           color: black;
       }
       a:hover{
           color: blue;
       }
       a:active{
           color: black;
       }
    </style>
    <body>
    <div id="header"><center><h1>Tompressor</h1></center>
    <br>
    <div id="form">
     <form  name="form" method="post" action="/cgi-bin/tompressor.py" >
            <LABEL for="url">Long URL: </LABEL>
            <input type="text" name="longurl" placeholder="http://www.averylongurl.com" title="Insert URL"/ style="width: 450px;"><br>

            <INPUT type="submit" value="Compress!" />
            <input type="reset" value="Clear form" />
     </form>
    </div><!-- close div form -->
    </div><!-- close div header -->
    <br>
    <br>
    <br>
"""


################################
#                              #
# Generate CORRECT result page #
#                              #
################################

def redirect_to_result(shorturl, longurl):

    #computer the difference between the long and the short url - 
    #NOTE(1) not counting the leading http:// - 
    #NOTE(2) the domain of shorturl is not considered since can be much shorter then tompressor.no-ip.org this is just a test   
    charnum = (len(longurl)-7) - len(shorturl)
    
    #...i know that tompressor is not short name for this kind of service, but just T was not available :) a real service should be call "sho.rt" or similar
    result = "http://tompressor.no-ip.org/" + shorturl
    print "Content-Type: text/html\n\n"
    print
    print html
    print "<div id=\"result\"><b><font size=\"6\">Tom</font><font size=\"3\" color=\"red\">pressed!</font></b><br>" 
    print "<p> The compressed url is <b><a href=\"%s\">%s</a></b> </p>" %(result,result)
    print "<p> You original url was <i>%s</i> </p>" %(longurl)
    print "<p> Your URL is now <b>%s</b> characters shorter!<br><font size=\"2\"><i>(domain is not counted!)</i></font> </p>" %(charnum)
    print "</div></body></html>"
    sys.exit(0)
########## END OF VALID RESULTS WEBPAGE ###########



##############################
#                            #
# Generate WRONG result page #
#                            #
##############################
#
# we generate this page when the shorturl CODE is INVALID or NOT in our Database
#
def redirect_to_wrongcode(shorturl):
    print "Content-Type: text/html\n\n"
    print
    print html
    print "<div id=\"result\"><b><font size=\"6\">Tom</font><font size=\"3\" color=\"red\">error!</font></b><br>"
    print "<br><p> The url <i>http://tompressor.no-ip.org/%s</i> you have submited is <b>INVALID</b></p>"%(shorturl)
    print "<p>This may be caused by several reasons: malformed url, inactive link or never compressed url.</p>"
    print "</div></body></html>"
    sys.exit(0)
########## END OF WRONG RESULTS WEBPAGE ###########



###############################
#                             #
# Redirect to a generic ERROR #
#                             #
##############################
#
# We dont want the user to know what kind of checks we perform so we redirect them to a generic error page telling them to double check their input.
#
def redirect_to_error(url):
    print "Content-Type: text/html\n\n"
    print
    print html
    print "<div id=\"result\"><b><font size=\"6\">Tom</font><font size=\"3\" color=\"red\">error!</font></b><br>"
    print "<br><p> The url <i>%s</i> you have submited is <b>INVALID</b></p>"%(url)
    print "<p>This may be caused by several reasons usually a malformed url or inactive link.</p>"
    print "</div></body></html>"
    sys.exit(0)
########## ENF OF HTTP URL FUNCTIONS ##########
