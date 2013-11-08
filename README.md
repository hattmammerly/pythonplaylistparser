<<<<<<< HEAD
Original iteration of this project was messy, but I do still use it, so this rewrite gets a new branch until it matches or extends functionality.

Oh also the master branch only supports python 2.7 and some specific version of urwid.

So in this new version, the script uses plistlib over lxml which greatly speeds things up

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
=======
The rewrite branch at this point is faster, cleaner and simply better; use that instead if you can deal with rough edges.

This version depends on some particular urwid version and python 2.7, and even with those only works on one of my machines. The rewrite works with python 3 (3.3.2?), uses plistlib over lxml which greatly improves speed, and isn't too embarassing to link to on a resume.

this requires the latest urwid package. install it with pip since both gentoo and ubuntu have old versions in their repositories.

playlist template files can be read to convert an itunes playlist to that format
take a look at templates/m3u for what an example looks like
full list of things that can be added:
- %trackname : track name
- %trackartist : track artist
- %trackalbum\_artist : track album artist
- %trackalbum : track album
- %trackgenre : track genre
- %tracklength : track length
- %trackyear : track year
- %trackbpm : track beats per minute
- %trackdate\_added : date track was added to library
- %trackbit\_rate : bit rate of track in kbps (can it even be in anything else)
- %trackplay\_count : number of plays the track has
- %trackskip\_count : I guess itunes saves the number of times you skip it
- %trackpurchased : if the track was purchased in itunes
- %tracklocation : absolute location of file on the system

maybe I'll add something into the parser thing to let you put playlist metadata in there

you can interface with it via command line but my code got waaay too messy maybe I'll write out all the functions and what they do later. but basically you just use the file 'themeat.py' if you don't want urwid or whatever, man

v1.0?
>>>>>>> master
