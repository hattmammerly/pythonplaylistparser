import themeat
# originally this file would have been some urwid interface code
#didn't really feel like writing any of that though
#so you get a basic demo of how to use the main script isntead
xml = themeat.openlibrary('iTunesMusicLibrary.xml');
library = themeat.processlibrary(xml);

print library.gettrackswithattribute('artist','The Beatles');

print library.getattributeunderNinstances('artist',2);
