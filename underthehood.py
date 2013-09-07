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
