import plistlib
import itertools
import functools
import urllib.parse
import os

# FORGET THIS LXML BUSINESS
# PLISTLIB IS WHERE IT'S AT
def openLibrary(loc):
    try:
        lib = plistlib.readPlist(loc)
    except IOError as e:
        print ("I/O error({}): {}".format(e.errno, e.strerror))
        return
    return lib

def getTracks(library,trackIDs):
    ret = []
    for ID in trackIDs:
        ret.append(library['Tracks'][ID])
    return ret

def readPlaylist(library, playlistID=None): # playlistID must be int
    if playlistID == None:
        playlistID = library["Playlists"][0]["Playlist ID"]
    return getTracks(library,[('{0}'.format(track['Track ID'])) for track in [plist['Playlist Items'] for plist in library['Playlists'] if plist['Playlist ID'] == playlistID][0]])
    # the comprehension does: [track number as string for every track in [the tracklist of the one playlist matching playlistID]]

def convertPlaylist(library,form,playlistID=None):
    if playlistID == None:
        playlistID = library["Playlists"][0]["Playlist ID"]
    try:
        template = open('templates/{0}'.format(form))
    except IOError as e:
        print ('Could not open template file: templates/{0}.'.format(form))
        return
    try:
        fl = open('playlists/linux/{0}.{1}'.format([plist['Name'] for plist in library['Playlists'] if plist['Playlist ID'] == playlistID][0],form),'w+') # make new playlist in linux directory. consider putting in format-specific folders too?
        fw = open('playlists/windows/{0}.{1}'.format([plist['Name'] for plist in library['Playlists'] if plist['Playlist ID'] == playlistID][0],form),'w+') # make same playlist in windows directory
    except IOError as e:
        print ('Could not write playlist files')
        return
    tracktemplate = template.read()
    output = tracktemplate[:tracktemplate.index('<!--TRACK-->\n')]
    start = tracktemplate.index('<!--TRACK-->\n') + 13 # why was it +13?
    tracktemplate = tracktemplate[start:tracktemplate.index('<!--END-->')]
    trackinfos = ['Name','Artist','Album Artist','Location','Album','Genre','Total Time','Year','BPM','Date Added','Bit Rate','Play Count','Skip Count','Purchased']
    for track in readPlaylist(library,playlistID):
        entry = tracktemplate
        for trackinfo in trackinfos:
            try:
                if type(track[trackinfo]) == str:
                    if trackinfo == "Location":
                        entry = entry.replace('%track{0}%'.format(trackinfo), '{0}'.format(correctPath(urllib.parse.unquote(track[trackinfo].replace("localhost/C:/Users","/home")))))
                    else:
                        entry = entry.replace('%track{0}%'.format(trackinfo), '{0}'.format(urllib.parse.unquote(track[trackinfo])))
                else:
                    entry = entry.replace('%track{0}%'.format(trackinfo), '{0}'.format(track[trackinfo]))
            except KeyError as e:
                pass
        output = output + entry
    fl.write(output)
    fw.write(output)

def getListofAttr(library,attr,playlistID=None):
    if playlistID == None:
        playlistID = library["Playlists"][0]["Playlist ID"]
    return list(set([track[attr] for track in readPlaylist(library,playlistID) if attr in track]))
    # list(set([])) used to eliminate duplicates heh

def getTracksWithTrait(library,trait,value,playlistID=None): # this might be cleaned with a list comprehension | getTracks
    if playlistID == None:
        playlistID = library["Playlists"][0]["Playlist ID"]
    ret = []
    for track in readPlaylist(library, playlistID):
        #print (track)
        try:
            if track[trait] == value:
                ret.append(track)
        except KeyError as e:
            pass
    return ret

def getAttrUnderN(library, attr, n, playlistID=None):
    if playlistID == None:
        playlistID = library["Playlists"][0]["Playlist ID"]
    attrs = {}
    ret = []
    for track in readPlaylist(library, playlistID):
        try:
            if track[attr] in attrs:
                attrs[track[attr]] += 1
            else:
                attrs[track[attr]] = 1
        except KeyError as e:
            pass
    for key,value in attrs.items():
        if value <= n:
            ret.append(key)
    return ret

def unionPlaylist(library, playlists):
    return [dict(t) for t in set([tuple(d.items()) for d in list(itertools.chain.from_iterable([readPlaylist(library, id) for id in playlists]))])]

def intersectPlaylist(library, playlists):
    def intersectTwo(p1, p2):
        return [dict(t) for t in set([tuple(d.items()) for d in [track for track in p1 if track in p2]])]
    return functools.reduce(intersectTwo, [readPlaylist(library, playlist) for playlist in playlists] )

# takes library and list of playlist ids - subtracts from first playlist all following playlists
def differencePlaylist(library, playlists):
    if len(playlists) <= 1:
        return readPlaylist(library, playlists[0])

def correctPath(string):
    string = string.replace("file://","")
    loc, f = os.path.split(string)
    loc, album = os.path.split(loc)
    loc, artist = os.path.split(loc)
    target = ""
    good = False
    for d in [x for x in os.listdir(loc) if os.path.isdir(os.path.join(loc, target, x))]:
        if d.lower() == artist.lower():
            target += d + "/"
            good = True
            break
    if not good: # how do i want to deal with failure
        return "FAILURE"
    good = False
    for d in [x for x in os.listdir(os.path.join(loc, target)) if os.path.isdir(os.path.join(loc, target, x))]:
        if d.lower() == album.lower():
            target += d + "/"
            good = True
            break
    if not good: # how do i want to deal with failure
        return "FAILURE"
    good = False
    for d in [x for x in os.listdir(os.path.join(loc, target)) if os.path.isfile(os.path.join(loc, target, x))]:
        if d.lower() == f.lower():
            target += d
            good = True
            break
    if not good: # how do i want to deal with failure
        return "FAILURE"
    good = False
    return ("file://" + loc + "/" + target)
