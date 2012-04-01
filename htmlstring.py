#!/usr/bin/env python

from urlparse import urlparse

class XMLString():

    def __init__(self):
        self.head='\
<?xml version="1.0" encoding="UTF-8"?>\n\
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n\
  <channel>\n\
    <title>favs</title>\n\
    <atom:link href="http://rythdev.com/social/favs.rss" rel="self" type="application/rss+xml"/>\n\
    <link>https://www.twitter.com</link>\n\
    <description>\n\
     favs of friends\n\
    </description>\n\
    <language>en-us</language>\n\
    <ttl>40</ttl>\n'
        self.bottom = '\
  </channel>\n\
</rss>\n'

    def XML_node(self, title, description, guid, link):
        node = '\
    <item>\n\
    <title>%s</title>\n\
    <description>\n\
    &lt;table&gt;\n\
    %s\n\
    &lt;/table&gt;\n\
    </description>\n\
    <guid>%s</guid>\n\
    <link>%s</link>\n\
    </item>\n' % (title, description, guid, link)

        return node

def MakeHTMLLink(link):

    link_text = urlparse(link).hostname.replace('www.','')

    html = '<a style="text-decoration: none" href="%s">[%s]</a>' % (link, link_text)

    return ConvertChar(html)

def MakeImage(pic_link, alt_text=''):

    return ConvertChar('<img src="%s" alt="%s"/>' % (pic_link, alt_text))

def MakeHTMLItem(pic, text, friend, user):
    html = '\
    <tr>\n\
    <td valign=top><img src="%s" width="48" height="48" /></td>\n\
    <td style="border-bottom:1px; border-bottom-style:solid; border-bottom-color:#C0C0C0;">\n\
    <b>%s</b><br />%s<br />\n\
    <font size="2" color="grey">faved by %s</font></td>\n\
    </tr>\n' % (pic, user, text, friend)

    return ConvertChar(html)

def MakeStyle():

    return '\
    .ext_link { text-decoration: none;}\n'

def ConvertChar(text):

    return text.replace('<', '&lt;').replace('>', '&gt;')


        


