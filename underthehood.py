import plistlib

libID = 5313
# perhaps instead of assigning a global variable, the default playlistID could
# be the ID of the 0th playlist of the library passed
# that way it defaults to the working library's Library, and allows more than one library to be used
# this may necessitate a rubbish default and a check in the function body though

# FORGET THIS LXML BUSINESS
# PLISTLIB IS WHERE IT'S AT
def openLibrary(loc):
    try:
        lib = plistlib.readPlist(loc)
    except IOError as e:
        print ("I/O error({}): {}".format(e.errno, e.strerror))
        return
    globals()['libID'] = lib['Playlists'][0]['Playlist ID'] # this is problematic with more than one library file...
    return lib

def getTracks(library,trackIDs):
    ret = []
    for ID in trackIDs:
        ret.append(library['Tracks'][ID])
    return ret

def readPlaylist(library, playlistID=libID): # playlistID must be int
    return getTracks(library,[('{0}'.format(track['Track ID'])) for track in [plist['Playlist Items'] for plist in library['Playlists'] if plist['Playlist ID'] == playlistID][0]])
    # the comprehension does: [track number as string for every track in [the tracklist of the one playlist matching playlistID]]

def convertPlaylist(library,form,playlistID=libID):
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

def getListofAttr(library,attr,playlistID=libID):
    return list(set([track[attr] for track in readPlaylist(library,playlistID) if attr in track]))
    # list(set([])) used to eliminate duplicates heh
        
def getTracksWithTrait(library,trait,value,playlistID=libID):
    ret = []
    for track in readPlaylist(library, playlistID):
        #print (track)
        try:
            if track[trait] == value:
                ret.append(track)
        except KeyError as e:
            pass
    return ret

def getAttrUnderN(library, attr, n,playlistID=libID):
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
