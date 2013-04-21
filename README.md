still haven't learned markdown

things are functions now.
- openlibrary(loc) opens the xml file at a specified location, returning the xml
- processlibrary(xml) returns a library object containing tracks and playlists
- convertplaylist(key,form) converts playlist with id 'key' to the format form from the templates folder

most operations are performed on a library objeict, with these methods:
- listplaylists() : lists all playlists in key: name form
- playlisttostring(key) : returns playlist as a string
- gettrackswithattribute(attr,val) : returns tracks with matching attr/val pair, eg, songs with artist:Norah Jones
- gettracksonalbum(val) : takes albums as 'Artist: Album' and returns tracklist in your library
- getattributeunderNinstances(attr, n) : returns, for example, all artists with five or fewer songs

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

maybe later I'll get some urwid action going on (but apparently latest versions haven't been pushed to any repositories so the tutorials don't really work)
