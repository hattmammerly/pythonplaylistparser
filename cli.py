import underthehood

def openLibrary(loc):
    return underthehood.openLibrary(loc)

def listPlaylists(library):
    for plist in library['Playlists']:
        try:
            print ("Name: {0} | ID: {1} | {2} items".format(plist['Name'],plist['Playlist ID'], len(plist['Playlist Items'])))
        except KeyError as e:
            print ('Name: {0} | ID: {1}'.format(plist['Name'],plist['Playlist ID']))
            pass

def getPlaylistID(library, name='Library'):
        return [plist['Playlist ID'] for plist in library['Playlists'] if plist['Name'] == name][0]

def convertPlaylist(library, form, playlistID):
    if type(playlistID) is str:
        underthehood.convertPlaylist(library,form,getPlaylistID(library,playlistID))
    else:
        underthehood.convertPlaylist(library,form,playlistID)
