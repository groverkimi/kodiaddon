import urlparse
import sys,urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urlresolver
import urllib2
import re
from bs4 import BeautifulSoup





base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

_addon = xbmcaddon.Addon()
_icon = _addon.getAddonInfo('icon')



def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def resolve_url(url):
    duration=7500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:        
        return stream_url    

def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_url = play_item.getfilename()
    stream_url = resolve_url(vid_url)
    if stream_url:
        play_item.setPath(stream_url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
##############
def parseHTML(url=''):
    #connect to a URL
    #website = urllib2.urlopen('http://m.perfectgirls.net/gal/497235/Astonishing_teacher_is_always_in_the_mood_to_fuck_her_students__if_no_one_is_watching_them')
    website = urllib2.urlopen(url)

    #read html code
    html = website.read()

    #use re.findall to get all the links
    #links = re.findall('"((http)s?://.*?)"', html)
    soup = BeautifulSoup(html)
    links = soup.select("a[href$=.mp4]")
    vdolist =[];
    for item in links:
        #print item
        #print item[0]
        vdolist.append(item.get('href'))

    return vdolist        
###########
def getLinks(url):
    website = urllib2.urlopen(url)
    #read html code
    html = website.read()
    soup = BeautifulSoup(html)
    links =[]
    for link in soup.select( '.list__item_link a'):
        #print(link.get('href'))
        #print(link.find('img').get('src'))
        links.append({'href': domainurl + link.get('href'), 'img':link.find('img').get('src')})
    #print(links)
    return links;


# addon kicks in

mode = args.get('mode', None)
domainurl = 'http://m.perfectgirls.net';
print 'mode='
print  mode
if mode is None or mode[0] == 'next':
    
    argsNext = args.get('nextval', None)
    print argsNext    
    if argsNext is not None:
       nextval = int(argsNext[0])+1
       url = 'http://m.perfectgirls.net/'+str(nextval)
    else:
       nextval = 1
       url = 'http://m.perfectgirls.net'
    print 'nextval', nextval 

    print 'url =', url
    vdoObjects = getLinks(url)
    #print(vdoObjects)
    for page in vdoObjects:
        #url = build_url({'mode' :'page', 'data' : page.get('href')})
        print('href=',page.get('href'))
        url = build_url({'mode' :'page', 'data' : page.get('href')})
        title = page.get('href').split('/')[-1]
        li = xbmcgui.ListItem(title, iconImage=page.get('img'))
        li.setInfo( type="Video", infoLabels={ "Title": title } )
        li.setProperty('isFolder','true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,isFolder=True)


    urlnext = build_url({'mode' :'next', 'nextval' : nextval})
    li = xbmcgui.ListItem('Next List', iconImage='DefaultVideo.png')
    li.setInfo( type="Video", infoLabels={ "Title": title } )
    li.setProperty('isFolder','true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlnext, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'page':
    print 'inside page'
    video_play_url = args['data'][0] #"http://m.perfectgirls.net/gal/497235/Astonishing_teacher_is_always_in_the_mood_to_fuck_her_students__if_no_one_is_watching_them"
    print('video_play_url=',video_play_url);
    vlist = parseHTML(video_play_url)
    print (vlist)
    for vdourl in vlist:
        url1 = build_url({'mode' :'play', 'playlink' : vdourl})
        fileName = vdourl.split('/')[-1]
        li1 = xbmcgui.ListItem(fileName, iconImage='DefaultVideo.png')
        li1.setProperty('IsPlayable' , 'true')
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url1, listitem=li1)

    


    xbmcplugin.endOfDirectory(int(sys.argv[1]))


elif mode[0] == 'play':
    final_link = args['playlink'][0]
    play_video(final_link)





