import plistlib
import itertools

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
