Original iteration of this project was messy, but I do still use it, so this rewrite gets a new branch until it matches or extends functionality.

Oh also the master branch only supports python 2.7 and some specific version of urwid.

Something to note for later: haskell's laziness may actually significantly speed up this program

So in this new version, the script uses plistlib over lxml which greatly speeds things up

openLibrary(loc): feed it the location of your itunes library xml file and it will return a plistlib object

getTracks(library, trackIDs): given a library from above and an array of ints, returns a list of dicts of track info

readPlaylist(library, playlistID): feeds the list of tracks from the specified playlist through getTracks()
