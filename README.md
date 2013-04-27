still haven't learned markdown

first off, this requires the latest urwid package. install it with pip since both gentoo and ubuntu have old versions in their repositories.

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
