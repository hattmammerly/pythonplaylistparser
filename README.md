Original iteration of this project was messy, but I do still use it, so this rewrite gets a new branch until it matches or extends functionality.

Oh also the master branch only supports python 2.7 and some specific version of urwid.

Something to note for later: haskell's laziness may actually significantly speed up this program

So in this new version, the script uses plistlib over lxml which greatly speeds things up

#### openLibrary(loc):
feed it the location of your itunes library xml file and it will return a plistlib object

#### getTracks(library, trackIDs):
given a library from above and an array of ints, returns a list of dicts of track info

#### readPlaylist(library, playlistID):
feeds the list of tracks from the specified playlist through getTracks()

#### convertPlaylist(library, playlistID, form):
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


I wrote this script for myself on my dual-booting system. My Windows user and Linux users share the same name and path to the music library, so I run the following command to make this playlist usable on Linux.

sed -i 's/file:\/\/localhost\/C:\/Users\//\/home\//' sample.m3u && sed -i 's/%20/ /g' sample.m3u && sed -i 's/%5B/[/g' sample.m3u && sed -i 's/%5D/]/g' sample.m3u

Windows users could probably get by with the following (or another utility entirely).

sed -i 's/file:\/\/localhost\//' sample.m3u && sed -i 's/%20/ /g' sample.m3u && sed -i 's/%5B/[/g' sample.m3u && sed -i 's/%5D/]/g' sample.m3u
