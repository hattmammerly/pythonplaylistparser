from lxml import etree

try:
#    xml = open("iTunesMusicLibrary.xml");
    xml = open("testing.xml");
    tree = etree.parse(xml);
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror);

tree = etree._ElementTree.getroot(tree);
print etree.tostring(tree[0]);

tracksxml = tree[0][-3];  #there's probably a better way to parse
playlistsxml = tree[0][-1]; #but since it's always <key/><value/> this will always work

print '--------------';
print etree.tostring(playlistsxml);
print '--------------';
tracks = {};
for i in xrange(1,len(tracksxml), 2):
    trackno = tracksxml[i-1].text;
    tracks[trackno] = {};
    for x in xrange(0,len(tracksxml[i]), 2):
        val = tracksxml[i][x+1].text;
        if tracksxml[i][x].text == "Name":
            tracks[trackno]['name'] = val;
        elif tracksxml[i][x].text == "Artist":
            tracks[trackno]['artist'] = val;
        elif tracksxml[i][x].text == "Album Artist":
            tracks[trackno]['album artist'] = val;
        elif tracksxml[i][x].text == "Genre":
            tracks[trackno]['genre'] = val;
        elif tracksxml[i][x].text == "Year":
            tracks[trackno]['year'] = val;
        elif tracksxml[i][x].text == "BPM":
            tracks[trackno]['bpm'] = val;
        elif tracksxml[i][x].text == "Date Added":
            tracks[trackno]['date added'] = val;
        elif tracksxml[i][x].text == "Bit Rate":
            tracks[trackno]['bit rate'] = val;
        elif tracksxml[i][x].text == "Play Count":
            tracks[trackno]['play count'] = val;
        elif tracksxml[i][x].text == "Skip Count":
            tracks[trackno]['skip count'] = val;
        elif tracksxml[i][x].text == "Purchased":
            tracks[trackno]['purchased'] = True;
        elif tracksxml[i][x].text == "Location":
            tracks[trackno]['location'] = val;

print len(playlistsxml);


playlists = {};
for i in playlistsxml:
    playlist = playlistsxml[i];
    playlistno = playlist[3];
    playlists[playlistno] = {};
    for x in playlistsxml[i]:
        val = playlistsxml[i][x+1];
        if playlistsxml[i][x].text == "Name":
            playlists[playlistno]['name'] = val;
        elif playlistsxml[i][x].text == "Smart Info":
            playlists[playlistno]['smart']=True;
        elif playlistsxml[i][x].text == "Playlist Items":
            tracklist = [];
            for z in playlistsxml:
                tracklist.append(playlistsxml[z][1]);
            playlists[playlistno]['tracks'] = tracklist;

print playlists;
print playlistsxml;
