#! /usr/bin/python2.6

import twitter
import pickle
import os
import sys
import time
import string
from xml.etree import ElementTree
from xml.dom import minidom


def FormatString (raw_struc):
    raw_string = ElementTree.tostring(raw_struc)
    reparsed = minidom.parseString(raw_string)
    return reparsed.toprettyxml(indent=' ')

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
    #time.tzset()


def GenerateXML ():

    path = os.path.dirname(sys.argv[0])

    api = ImplementApi()
    if api.VerifyCredentials() == None:
        return

    xml_struc = ElementTree.Element('rss')
    xml_struc.set('version','2.0')
    xml_struc.set('xmlns:atom','http://www.w3.org/2005/Atom')
    xml_struc.set('xmlns:georss','http://www.georss.org/georss')


    channel = ElementTree.SubElement(xml_struc,'channel')
    ElementTree.SubElement(channel,'title').text = 'favs'
    ElementTree.SubElement(channel,'link').text = 'https://www.twitter.com'
    ElementTree.SubElement(channel,'description').text = 'favs of friends'
    ElementTree.SubElement(channel,'language').text = 'en-us'
    ElementTree.SubElement(channel,'ttl').text = '40'


    try:
        with open(path+'/title_id','rb') as title_store:
            id_existed = pickle.load(title_store)
    except IOError:
        id_existed = []
    title_id = []
    instant_id = []
    friends_list = api.GetFriends()
    for friend in friends_list[0:5]:
        title_list = api.GetFavorites(friend.screen_name)
        if len(title_list)>5: title_list=title_list[0:4]
        for fav_title in title_list:
            instant_id.append(fav_title.id)
            if fav_title.id not in id_existed:
                item = ElementTree.SubElement(channel,'item')
                ElementTree.SubElement(item,'title').text =fav_title.text + \
                '  [faved by ' + friend.screen_name + ']'
                ElementTree.SubElement(item,'description').text = fav_title.text
                ElementTree.SubElement(item,'link').text = 'none'
                title_id.append(fav_title.id)

    if title_id !=[]:
        with open(path+'/favs.rss','wb') as output:
            output.write(FormatString(xml_struc).encode('utf-8'))
        with open(path+'/title_id','wb') as existed_id_file:
            pickle.dump(instant_id,existed_id_file)
    with open (path+'/log','ab') as log_file:
        str_log = time.strftime("%b %d %H:%M  ")+str(len(title_id))+ \
        " items updated."+'\n'
        log_file.write(str_log)


def main():
    SetTimeZone()
    GenerateXML()



if __name__ == '__main__':
    main()
