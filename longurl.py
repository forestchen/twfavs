#!/usr/bin/env python

import re, httplib, urlparse
from htmlstring import MakeHTMLLink

# text='there is two links http://t.cn/zOtKv90 , http://t.cn/zOt4xFM in this text'

url_loc = ['t.co','tr.im','is.gd','tinyurl.com','bit.ly',]

def MakeText(text):

    links = CheckLinks(text)
    if links != []:
        long_links = ExpandLinks(links)
        # print long_links

        for link in links:
            # print link, long_links
            text = text.replace(link, MakeHTMLLink(long_links[link]))

    return text.replace('&', '&amp;')

def CheckLinks(text):

    return re.findall(r'(https?://[\x21-\x7f]+)', text)

def ExpandLinks(links):

    link_dict = {}
    for link in links:
        com = urlparse.urlparse(link)
        if com.netloc in url_loc:
            c = httplib.HTTPConnection(com.netloc)
            c.request("GET", com.path)
            r = c.getresponse()
            long_link = r.getheader('Location')
        else:
            long_link = None

        link_dict[link] = long_link if long_link != None else link

    return link_dict

# print MakeText(text)
