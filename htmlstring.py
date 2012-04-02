#!/usr/bin/env python

from urlparse import urlparse

class XMLString():

    def __init__(self, title, atom, link, description, pubDate):
        self.head='\
<?xml version="1.0" encoding="utf-8"?>\n\
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n\
  <channel>\n\
    <title>%s</title>\n\
    <atom:link href="%s" rel="self" type="application/rss+xml"/>\n\
    <link>%s</link>\n\
    <description>\n\
     %s\n\
    </description>\n\
    <language>en-us</language>\n\
    <pubDate>%s</pubDate>\n\
    <lastBuildDate>%s</lastBuildDate>\n\
    <ttl>40</ttl>\n' % (title, atom, link, description, pubDate, pubDate)
        self.bottom = '\
  </channel>\n\
</rss>\n'

    def XML_node(self, title, description, date, guid, link):
        node = '\
    <item>\n\
    <title>%s</title>\n\
    <description>\n\
    &lt;table CELLPADDING="5" CELLSPACING="0" &gt;\n\
    %s\n\
    &lt;/table&gt;\n\
    </description>\n\
    <pubDate>%s</pubDate>\n\
    <guid>%s</guid>\n\
    <link>%s</link>\n\
    </item>\n' % (title, description, date, guid, link)

        return node

def MakeHTMLLink(link):

    link_text = urlparse(link).hostname.replace('www.','')

    html = '<a style="text-decoration: none" href="%s">[%s]</a>' % (link, link_text)

    return html

def MakeImage(pic_link, alt_text=''):

    return '<img src="%s" alt="%s"/>' % (pic_link, alt_text)

def MakeHTMLItem(pic, text, friend, user, bg_color=['#ffffff', '#eeeeee']):

    bg_color.append(bg_color.pop(0))

    html = '\
    <tr bgcolor="%s";>\n\
    <td valign=top><img src="%s" width="48" height="48" /></td>\n\
    <td>\n\
    <b>%s</b><br />%s<br />\n\
    <font size="2" color="grey">faved by %s</font></td>\n\
    </tr>\n' % (bg_color[0], pic, user, text, friend)

    return ConvertChar(html)

def MakeStyle():

    return '\
    .ext_link { text-decoration: none;}\n'

def ConvertChar(text):

    return text.replace('<', '&lt;').replace('>', '&gt;')


        


