import plistlib
import time

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
    # consider moving the '{0}'.format business here and just push an array of ints into this function
    ret = []
    for ID in trackIDs:
        ret.append(library['Tracks'][ID])
    return ret

def readPlaylist(library, playlistID): # playlistID must be int
    # getTracks(lib,[("{0}".format(track['Track ID'])) for track in lib['Playlists'][0]['Playlist Items']])
    return getTracks(lib,[('{0}'.format(track['Track ID'])) for track in [plist['Playlist Items'] for plist in lib['Playlists'] if plist['Playlist ID'] == playlistID][0]])
    # the comprehension does: [track number as string for every track in [the tracklist of the one playlist matching playlistID]]

def convertPlaylist(library,playlistID,form):
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
