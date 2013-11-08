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

I wrote this script for myself on my dual-booting system. My Windows user and Linux users share the same name and path to the music library, so I run the following command to make a playlist 'sample' usable on Linux.

```sed -i 's/file:\/\/localhost\/C:\/Users\//\/home\//' sample.m3u && sed -i 's/%20/ /g' sample.m3u && sed -i 's/%5B/[/g' sample.m3u && sed -i 's/%5D/]/g' sample.m3u```

Windows users could probably get by with the following (or another utility entirely).

```sed -i 's/file:\/\/localhost\//' sample.m3u && sed -i 's/%20/ /g' sample.m3u && sed -i 's/%5B/[/g' sample.m3u && sed -i 's/%5D/]/g' sample.m3ui```

# TODO:
Extend the CLI wrapper, and then work on an urwid cascading window system again
Something to note for later: haskell's laziness may actually significantly speed up this program
