from lxml import etree
import time

start = time.time();

class Track:
    __slots__ = ('name','artist','album_artist','genre','length','year','bpm','date_added','bit_rate','play_count','skip_count','purchased','location');
    def tostring(self):
        return "{0} - {1}".format(self.artist, self.name);
    def __init__(self):
        self.year = '0000';
        self.purchased = False;
        self.location = '';

class Playlist:
    __slots__ = ('name','smart','tracks');
    def tostring(self):
        s = '{0}:'.format(self.name);
        for t in tracks:
            s = s + '\n\t{0}'.format(tracks[t].tostring());
        s = s + '\n';
        return s;
    def __init__(self):
        self.smart = False;
        self.tracks = {};

def printPlaylist(key):
    print playlists[key]['name'];
    t = playlists[key]['tracks'];
    for a in t:
        print tracks[a].tostring();

infos = ['name','artist','album_artist','genre','length','year','bpm','date_added','bit_rate','play_count','skip_count','purchased','location'];

try:
#    xml = open("iTunesMusicLibrary.xml");
    xml = open("testing.xml");
    tree = etree.parse(xml);
    print (time.time() - start);
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror);

tree = etree._ElementTree.getroot(tree);
#print etree.tostring(tree[0]);

tracksxml = tree[0][-3];  #there's probably a better way to parse
playlistsxml = tree[0][-1]; #but since it's always <key/><value/> this will always work

print time.time() - start;

#print '--------------';
#print etree.tostring(playlistsxml);
#print '--------------';
tracks = {};
for i in xrange(1,len(tracksxml), 2):
    trackno = tracksxml[i-1].text;
    tracks[trackno] = Track();
    for x in xrange(0,len(tracksxml[i]), 2):
        val = tracksxml[i][x+1].text;
        if tracksxml[i][x].text == "Name":
            tracks[trackno].name = val;
        elif tracksxml[i][x].text == "Artist":
            tracks[trackno].artist = val;
        elif tracksxml[i][x].text == "Album Artist":
            tracks[trackno].album_artist = val;
        elif tracksxml[i][x].text == "Genre":
            tracks[trackno].genre = val;
        elif tracksxml[i][x].text == "Total Time":
            tracks[trackno].length = int(val)/1000; # itunes library gives time in milliseconds
        elif tracksxml[i][x].text == "Year":
            tracks[trackno].year = val;
        elif tracksxml[i][x].text == "BPM":
            tracks[trackno].bpm = val;
        elif tracksxml[i][x].text == "Date Added":
            tracks[trackno].date_added = val;
        elif tracksxml[i][x].text == "Bit Rate":
            tracks[trackno].bit_rate = val;
        elif tracksxml[i][x].text == "Play Count":
            tracks[trackno].play_count = val;
        elif tracksxml[i][x].text == "Skip Count":
            tracks[trackno].skip_count = val;
        elif tracksxml[i][x].text == "Purchased":
            tracks[trackno].purchased = True;
        elif tracksxml[i][x].text == "Location":
            tracks[trackno].location = val;

#print len(playlistsxml);


playlists = {};
for i in xrange(0,len(playlistsxml)):
    playlist = playlistsxml[i];
    playlistno = playlist[3].text;
    playlists[playlistno] = Playlist();
    for x in xrange(0,len(playlistsxml[i]) - 1):
        val = playlistsxml[i][x+1].text;
        if playlistsxml[i][x].text == "Name":
            playlists[playlistno].name = val;
        elif playlistsxml[i][x].text == "Smart Info":
            playlists[playlistno].smart = True;
        elif playlistsxml[i][x].text == "Playlist Items":
            tracklist = [];
            for z in xrange(0,len(playlistsxml[i][x+1])):
                tracklist.append(playlistsxml[i][x+1][z][1].text);
            playlists[playlistno].tracks = tracklist;

#print playlists;
#print playlistsxml;
#print '------------------------------';
#printPlaylist('10001');

print playlists['10001'].tostring();

def convertPlaylist(key, form):
    f = open('playlists/{0}.{1}'.format(playlists[key].name, form),'w+')
    template = open("templates/{0}".format(form));
    tracktemplate = template.read();
    output = tracktemplate[:tracktemplate.index('<!--TRACK-->\n')];
    start = tracktemplate.index('<!--TRACK-->\n') + 13;
    tracktemplate = tracktemplate[start:tracktemplate.index('<!--END-->')];
    for track in playlists[key].tracks:
        t = tracks[track];
        tmp = tracktemplate
        for i in infos:
            try:
                tmp = tmp.replace('%track{0}'.format(i), str(getattr(t, i)));
            except AttributeError as e:
                pass;
        output = output + tmp;
    print output;
    f.write(output);
    #create new file(playlists[key].name.m3u)

convertPlaylist('10001','m3u');

