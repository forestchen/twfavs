#!/usr/bin/env python

import twitter
import pickle
import os
import sys
import time
import string
from xml.etree import ElementTree
from xml.dom import minidom

from longurl import MakeText
from htmlstring import MakeImage, MakeStyle, XMLString, MakeHTMLItem

def FormatString (raw_struc):
    raw_string = ElementTree.tostring(raw_struc)
    reparsed = minidom.parseString(raw_string)
    return reparsed.toprettyxml(indent='  ')

def ImplementApi():

    path = os.path.dirname(sys.argv[0])
    keys=[]
    with open(path+'/account','rb') as account_file:
        for i in range(4):
            line = account_file.readline().strip()
            key_value = string.split(line,'=')[1]
            keys.append(key_value)

    return twitter.Api(
        consumer_key=keys[0],
        consumer_secret=keys[1],
        access_token_key=keys[2],
        access_token_secret=keys[3])

def SetTimeZone():
    os.environ['TZ'] = 'Asia/Shanghai'
    if sys.platform != 'win32' :
        time.tzset()


def MakeDailyTweets(text):

    text = XMLString.XML_node('%s daily tweets' % time.strftime('%b %d'), text, \
                              'http://rythdev.com/favs/' + str(time.time()), \
                              'http://www.twitter.com')
    
    return text


def MakeItemList(items_list):
    text = ''
    for item in items_list:
        text =  text + MakeHTMLItem(item['avatar'], MakeText(item['text']),
                item['friend'], item['user'])

    return text

    
def MakeStatusLink(status):
    return 'https://twitter.com/'+status.user.screen_name+'/status/'+str(status.id)


def GenerateXML ():

    path = os.path.dirname(sys.argv[0])

    api = ImplementApi()
    if api.VerifyCredentials() == None:
        return

    # xml_struc = MakeXMLBody()
    xml_doc = XMLString()
    tree = xml_doc.head

    try:
        with open(path+'/title_id','r') as title_store:
            id_existed = pickle.load(title_store)
    except IOError:
        id_existed = []
    try:
        with open(path+'/cache_list','r') as cache_file:
            cache_list = pickle.load(cache_file)
    except IOError:
        cache_list = []
    try:
        with open(path+'/old_list','r') as old_file:
            old_list = pickle.load(old_file)
    except IOError:
        old_list = []

    title_id = []
    instant_id = []
    friends_list = api.GetFriends()[:]
    text_list = []
    for friend in friends_list:
        title_list = api.GetFavorites(friend.screen_name)
        if len(title_list)>5: title_list=title_list[0:4]
        for fav_title in title_list:
            instant_id.append(fav_title.id)
            if fav_title.id not in id_existed:
                link = MakeStatusLink(fav_title)
                text_list.append({'text':fav_title.text, 'friend':friend.screen_name,
                        'link':link, 'avatar':fav_title.user.profile_image_url,
                        'user':fav_title.user.screen_name})
                title_id.append(fav_title.id)
                cache_list.insert(0,[fav_title.text,friend.screen_name,link])
                if len(cache_list) > 20: cache_list = cache_list[0:19]
    if text_list != []:
        daily_text = MakeItemList(text_list)
        daily_item = xml_doc.XML_node('%s daily tweets' % time.strftime('%b %d'), \
            daily_text, 'http://rythdev.com/favs/' + str(time.time()), 'http://www.twitter.com')
        tree = tree + daily_item
        if len(old_list) > 2: old_list = old_list[0:2]
        for item in old_list:
            tree = tree + item
        old_list.insert(0, daily_item)

    tree = tree + xml_doc.bottom

    title_len = len(title_id)
    if title_len !=0:
        with open(path+'/favs.rss','w') as output:
            output.write(tree.encode('utf-8'))
        with open(path+'/old_list','w') as old_file:
            pickle.dump(old_list,old_file)

        with open(path+'/cache_list','wb') as cache_file:
            pickle.dump(cache_list,cache_file)
        with open(path+'/title_id','wb') as existed_id_file:
            pickle.dump(instant_id,existed_id_file)

    with open (path+'/log','rb') as log_file:
        logs=log_file.readlines()
    if len(logs)>10 : logs = logs[-9:]
    str_log = time.strftime("%b %d %H:%M  ")+str(title_len)+ \
    " items updated."+'\n'
    logs.append(str_log)
    with open (path+'/log','wb') as log_file:
        log_file.writelines(logs)


def main():
    SetTimeZone()
    GenerateXML()



if __name__ == '__main__':
    main()
