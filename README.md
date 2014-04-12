# cli.py

#### openLibrary(loc):
calls underthehood.openLibrary(loc)

#### listPlaylists(library):
prints the name, ID and size of each playlist in the library on a line

#### getPlaylistID(library, name='Library'):
returns the ID value from a playlist with that given name.

#### convertPlaylist(library, form, playlistID):
playlists can be supplied by name or by ID and it'll still convert it (WOW!)

# underthehood.py

#### openLibrary(loc):
feed it the location of your itunes library xml file and it will return a plistlib dict of dicts and such. Defines global variable libID to be the ID of your library

#### getTracks(library, trackIDs):
given a library from above and an array of ints, returns a list of dicts of track info

#### readPlaylist(library, playlistID=libID):
feeds the list of tracks from the specified playlist through getTracks()

#### convertPlaylist(library, form, playlistID=libID):
converts specified playlist to the specified format from templates folder. There is an example m3u template included with the package.
Metadata available for use in the playlist:
- %trackName%
- %trackArtist%
- %trackAlbum Artist%
- %trackLocation%
- %trackAlbum%
- %trackGenre%
- %trackTotal Time%
- %trackYear%
- %trackBPM%
- %trackDate Added%
- %trackBit Rate%
- %trackPlay Count%
- %trackSkip Count%
- %trackPurchased%

#### getListofAttr(library,attr,playlistID=libID):
returns every value for a given attribute. e.g. returns a list of artists from the playlist

#### getTracksWithTrait(library, trait, value, playlistID=libID):
for instance, getTracksWithTrait(library,'Artist','Norah Jones') will get all Norah Jones songs in the library

#### getAttrUnderN(library, attr, n, playlistID=libID):
For instance, getAttrUnderN(library, 'Artist', 5) will return a list of artists with 5 or fewer songs in the library

#### unionPlaylist(library, playlists):
returns a list of tracks found in any of playlists with IDs in the playlists arg. Duplicate elements removed.

#### intersectPlaylist(library, playlists):
returns a list of tracks found in all of playlists with IDs in the playlists arg. Duplicate elements aren't removed yet.

#### correctPath(location)
NTFS is case-insensitive - a song with artist abc and another with artist AbC are put into the folder abc, but have case information preserved in the file uri recorded in iTunes's library plist.
If the case in the uri doesn't match the case of the real directory, windows doesn't really care, but linooks does. This takes a file uri, finds the case-insensitive match iTunes would use, and returns it.
